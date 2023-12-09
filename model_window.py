"""
Module for the ModelWindow class
"""

import tkinter as tk
from tkinter import ttk
from audio_data import AudioData

class ModelWindow(tk.Toplevel):
    """
    View class for accessing the modeled data
    """
    def __init__(self, parent, audio_data: AudioData) -> None:
        super().__init__(parent)

        #Set window properties and assign the audio data to the window
        self.title("Model Information")
        self.geometry("200x300")
        self.maxsize(200, 300)
        self.minsize(200, 300)
        self.audio_data = audio_data
        self.controller = parent.controller
        self.add_widgets()

    def add_widgets(self) -> None:
        """
        Adds the labels, model data, and buttons to the window
        """
        top_frame = tk.Frame(self)
        bottom_frame = tk.Frame(self)
        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5, padx=5)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        separator.pack(side=tk.TOP, fill=tk.X, pady=10)

        length_label = tk.Label(
            top_frame, text="Audio Length: " + (str(self.audio_data.length) + " seconds")
        )
        length_label.grid(row=1,column=0, pady=5)

        bottom_frame.grid_columnconfigure(0,weight=1)
        bottom_frame.grid_columnconfigure(1,weight=1)
        bottom_frame.grid_columnconfigure(2,weight=1)

        plot_label = tk.Label(
            bottom_frame, text="Plot data:"
        )
        plot_label.grid(row=9, column=0, columnspan=3)


        waveform_button = tk.Button(
            bottom_frame, text="Waveform", command=lambda: self.controller.create_plot("Waveform")
        )
        waveform_button.grid(row=10, column=0, padx = 5, pady=(5,10))
        spectrum_button = tk.Button(
            bottom_frame, text="Spectrum", command=lambda: self.controller.create_plot("Spectrum")
        )
        spectrum_button.grid(row=10, column=1, padx=5, pady=(5,10))
        rt60_button = tk.Button( #future proofing
            bottom_frame, text="RT60"
        )
        rt60_button.grid(row=10, column=2, padx=5, pady=(5,10))
