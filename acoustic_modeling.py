import tkinter as tk
from view import View
from controller import Controller


class Window(tk.Tk):
    """
    Main window of the program
    """
    def __init__(self):
        super().__init__()
        self.title('Acoustic Modeling')

        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        controller = Controller(view)
        view.set_controller(controller)



if __name__ == '__main__':
    window = Window()
    window.mainloop()
