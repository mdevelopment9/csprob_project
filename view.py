"""
Main view class module
"""
import tkinter as tk
from tkinter import ttk
from controller import Controller


class View(ttk.Frame):
    """
    Main view class
    """

    def __init__(self, parent: tk.Tk):
        super().__init__(parent, width=200, height=100)
        # Need to set controller later, as it depends on the View class.
        self.controller: Controller = None

    def set_controller(self, controller: Controller) -> None:
        """
        Sets the controller parameter.

        :param controller:
        :return:
        """
        self.controller = controller
