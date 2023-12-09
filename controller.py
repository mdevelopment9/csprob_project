"""
Main controller class module
"""
import tkinter as tk
from tkinter import filedialog as fd
from file_data import FileData
from audio_data import AudioData
from model_window import ModelWindow
from plot_window import PlotWindow


class Controller:
    """
    Main controller class
    """

    def __init__(self, view):
        self.view = view
        self.audio_data = None

    def select_file(self, file_box: tk.Text) -> None:
        """
        Selects an audio file to be used in the program

        :param file_box: tkinter text box for the audio file's location
        """
        file_types = [('Audio Files', '.wav .mp3 .m4a .flac')]
        file_name = fd.askopenfilename(title='Choose the audio file', filetypes=file_types)
        file_box['state'] = tk.NORMAL
        file_box.insert('end', file_name)
        file_box['state'] = tk.DISABLED

    def start_model(self, file_name: str) -> None:
        """
        Starts the audio modelling process

        :param file_box: File name for the audio file
        """
        file_data = FileData(file_name)
        self.audio_data = AudioData(file_data)
        self.audio_data.model_file()
        ModelWindow(self.view, self.audio_data)

    def create_plot(self, plot_type:str) -> None:
        """
        Creates a plot window
        """
        PlotWindow(self.view, self.audio_data, plot_type)