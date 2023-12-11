"""
Module for the ModelWindow class
"""

import os
import tkinter as tk
from tkinter import ttk
import numpy as np
from audio_data import AudioData
from file_data import WAVEFILE_LOC

class ModelWindow(tk.Toplevel):
    """
    View class for accessing the modeled data
    """
    def __init__(self, parent, audio_data: AudioData) -> None:
        super().__init__(parent)
        self.parent = parent
        #Set window properties and assign the audio data to the window
        self.title("Model Information")
        self.geometry("250x300")
        self.maxsize(250, 300)
        self.minsize(250, 300)
        self.audio_data = audio_data
        self.controller = parent.controller
        self.add_widgets()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

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
            top_frame,
            anchor=tk.W,
            justify=tk.LEFT,
            text=f"Audio Length: {round(self.audio_data.length,3)} seconds"
        )
        length_label.grid(sticky = tk.W, row=1,column=0, pady=3)

        resonance_label = tk.Label(
            top_frame,
            anchor=tk.W,
            justify=tk.LEFT,
            text=f"Resonance Frequency: {self.audio_data.find_resonance()} Hz"
        )
        resonance_label.grid(sticky=tk.W, row=2,column=0, pady=3)

        low = self.audio_data.find_reverb(250)["rt60"]
        medium = self.audio_data.find_reverb(1000)["rt60"]
        high = self.audio_data.find_reverb(5000)["rt60"]
        rt60_difference = np.average([low,medium,high]) - 0.5

        low_reverb_label = tk.Label(
            top_frame,
            anchor=tk.W,
            justify=tk.LEFT,
            text=f"Low RT60 value: {round(low,3)} seconds"
        )
        low_reverb_label.grid(sticky=tk.W, row=3,column=0, pady=3)

        mid_reverb_label = tk.Label(
            top_frame,
            anchor=tk.W,
            justify=tk.LEFT,
            text=f"Mid RT60 value: {round(medium,3)} seconds"
        )
        mid_reverb_label.grid(sticky=tk.W, row=4,column=0, pady=3)

        high_reverb_label = tk.Label(
            top_frame,
            anchor=tk.W,
            justify=tk.LEFT,
            text=f"High RT60 value: {round(high,3)} seconds"
        )
        high_reverb_label.grid(sticky=tk.W, row=5,column=0, pady=3)

        difference_label = tk.Label(
            top_frame,
            anchor=tk.W,
            justify=tk.LEFT,
            text=f"RT60 difference: {round(rt60_difference,3)} seconds"
        )
        difference_label.grid(sticky=tk.W, row=6, column=0, pady=3)


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
            bottom_frame, text="RT60", command=lambda: self.controller.create_plot("RT60")
        )
        rt60_button.grid(row=10, column=2, padx=5, pady=(5,10))

    def on_close(self):
        """
        Method to reenable run button and delete the temporary .wav file before closing the program.
        """
        self.parent.run_button['state'] = tk.NORMAL
        os.remove(WAVEFILE_LOC)
        self.destroy()
