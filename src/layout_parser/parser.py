# File: src/layout_parser/parser.py

def _parse_as_general_text(ocr_results: list) -> str:
    """
    Parses OCR results by sorting text top-to-bottom, then left-to-right.
    This is a robust method for general, unstructured, or rotated text.
    """
    if not ocr_results:
        return ""
    sorted_results = sorted(ocr_results, key=lambda item: (item[0][0][1], item[0][0][0]))
    extracted_texts = [item[1][0] for item in sorted_results]
    return "\n".join(extracted_texts)

def _parse_as_document(ocr_results: list) -> str:
    """
    Parses OCR results by grouping text into lines and respecting columns.
    This is best for structured documents like resumes.
    """
    if not ocr_results:
        return ""
    sorted_boxes = sorted(ocr_results, key=lambda item: item[0][0][1])
    
    try:
        avg_height = sum([box[0][2][1] - box[0][0][1] for box in sorted_boxes]) / len(sorted_boxes)
        y_threshold = avg_height * 0.5
        vertical_spacing_threshold = avg_height * 1.5
    except ZeroDivisionError:
        return ""

    lines = []
    current_line = []
    for box in sorted_boxes:
        if not current_line:
            current_line.append(box)
        else:
            previous_box_y = current_line[-1][0][0][1]
            current_box_y = box[0][0][1]
            if abs(current_box_y - previous_box_y) < y_threshold:
                current_line.append(box)
            else:
                lines.append(current_line)
                current_line = [box]
    if current_line:
        lines.append(current_line)
        
    for i in range(len(lines)):
        lines[i] = sorted(lines[i], key=lambda item: item[0][0][0])
        
    final_text = ""
    if not lines:
        return ""
    final_text += " ".join([item[1][0] for item in lines[0]])
    for i in range(1, len(lines)):
        current_line_y = lines[i][0][0][0][1]
        previous_line_y = lines[i-1][0][0][0][1]
        vertical_gap = current_line_y - previous_line_y
        if vertical_gap > vertical_spacing_threshold:
            final_text += "\n\n"
        else:
            final_text += "\n"
        final_text += " ".join([item[1][0] for item in lines[i]])
    return final_text

def parse_layout(ocr_results: list, mode: str = "general") -> str:
    """
    Master layout parser function. Invokes a specific parser based on the selected mode.

    Args:
        ocr_results (list): The raw list of results from the OCR engine.
        mode (str): The parsing mode ('general' or 'document').

    Returns:
        str: A formatted string with the parsed text.
    """
    if mode == "document":
        return _parse_as_document(ocr_results)
    else: # Default to general
        return _parse_as_general_text(ocr_results)