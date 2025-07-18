# File: main.py

from src.gui.main_window import App

if __name__ == "__main__":
    # This is the official entry point of our application.
    # It creates an instance of our main window class and starts the GUI event loop.
    app = App()
    app.mainloop()