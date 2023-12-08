"""
Main controller class module
"""
import tkinter as tk
from tkinter import filedialog as fd
from file_data import FileData
from audio_data import AudioData


class Controller:
    """
    Main controller class
    """

    def __init__(self, view):
        self.view = view

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
        audio_data = AudioData(file_data)
        self.view.plot_data(audio_data)
