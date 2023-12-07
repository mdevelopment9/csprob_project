import tkinter as tk
from view import View
from controller import Controller


class Window(tk.Tk):
    """
    Main window of the program
    """

    def __init__(self):
        super().__init__()
        # init window params
        self.title('Acoustic Modeling')
        self.maxsize(350, 100)
        self.minsize(350, 100)

        # add view frame
        view = View(self)
        view.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10, padx=10)

        # create controller and add it to view
        controller = Controller(view)
        view.set_controller(controller)

        # add the widgets to the window
        view.add_widgets()


if __name__ == '__main__':
    window = Window()
    window.mainloop()
