from multiprocessing import freeze_support
from gui.app import App

if __name__ == "__main__":
    freeze_support()
    app = App()
    app.mainloop()