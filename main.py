# File: main.py

from src.gui.main_window import App

if __name__ == "__main__":
    # This is the official entry point of our application.
    # It creates an instance of our main window class and starts the GUI event loop.
    app = App()
    app.mainloop()

 
                                    #### PySide6 version ####

# import sys
# from PySide6.QtWidgets import QApplication
# from src.gui.main_window_pyside import MainWindow

# if __name__ == "__main__":
#     # This is the standard entry point for a PySide6 application.
#     app = QApplication(sys.argv)
    
#     window = MainWindow()
#     window.show()
    
#     sys.exit(app.exec())