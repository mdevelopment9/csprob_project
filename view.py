"""
Main view class module
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from controller import Controller
from audio_data import AudioData
from model_window import ModelWindow



class View(ttk.Frame):
    """
    Main view class
    """

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        # Setting parameters to None if they need to be defined later
        self.controller: Controller = None
        self.run_button: tk.Button = None

    def set_controller(self, controller: Controller) -> None:
        """
        Sets the controller parameter.

        :param controller: Controller instance
        """
        self.controller = controller

    def add_widgets(self) -> None:
        """
        Adds the widgets to the window.

        Adds a file picker, and a run button
        """
        # Create base frames
        top_frame = tk.Frame(self)
        bottom_frame = tk.Frame(self)
        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        separator.pack(side=tk.TOP, fill=tk.X, pady=10)
        # Create file selction box and the button which opens the file selection dialog
        file_box = tk.Text(
            top_frame,
            height=1,
            width=30,
            state=tk.DISABLED
        )
        file_box.grid(row=0, column=0, padx=5)
        select_button = tk.Button(
            top_frame, text="Select file", command=lambda: self.controller.select_file(file_box)
        )
        select_button.grid(row=0, column=1, padx=5)

        # Create the actual button that starts the modelling process
        self.run_button = tk.Button(
            bottom_frame, text="Start modeling",
            command=lambda: self.controller.start_model(file_box.get("1.0", tk.END).strip())
        )
        self.run_button.pack(side=tk.BOTTOM, anchor=tk.S)

    def show_message_box(self, fnfe: FileNotFoundError) -> None:
        """
        Method to show the FileNotFoundError
        """
        tk.messagebox.showerror("ERROR", f"Please choose an audio file before running the program\n\n Error:{fnfe}")