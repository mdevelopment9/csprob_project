"""
Module for the PlotWindow class
"""
import tkinter as tk
from audio_data import AudioData
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from rt60_toolbar import RT60Toolbar
from matplotlib.figure import Figure



class PlotWindow(tk.Toplevel):
    """
    View class for viewing matplotlib plots
    """
    def __init__(self, parent, audio_data:AudioData, plot_type:str) -> None:
        super().__init__(parent)

        self.title(plot_type+" Plot")
        self.geometry("750x500")
        self.audio_data = audio_data
        self.controller = parent.controller

        self.fig = Figure(figsize = (5,5),
                     dpi = 100)
        time = np.linspace(0., audio_data.length, audio_data.data.shape[0])
        try:
            split_data = audio_data.data[:, 0]
        except IndexError:
            # in case of single channel audio
            split_data = audio_data.data

        self.plot = self.fig.add_subplot(111)
        match plot_type:
            case "Waveform":
                self.plot.plot(time, split_data, label="Waveform")
                self.plot.legend()
                self.plot.set_xlabel("Time [s]")
                self.plot.set_ylabel("Amplitude")
                self.plot.set_title("Waveform amplitude graph")
                self.canvas = FigureCanvasTkAgg(self.fig, master=self)
                self.canvas.draw()
                toolbar = NavigationToolbar2Tk(self.canvas, self)
                toolbar.update()
                self.canvas.get_tk_widget().pack(fill='both',expand=True)
            case "Spectrum":
                spectrogram_data = self.plot.specgram(
                    split_data,
                    Fs=audio_data.samplerate,
                    NFFT=1024,
                    cmap=plt.get_cmap('autumn_r')
                )
                cbar = self.fig.colorbar(spectrogram_data[3])
                self.plot.set_xlabel('Time (s)')
                self.plot.set_ylabel('Frequency (Hz)')
                cbar.set_label('Intensity (dB)')
                self.plot.set_title("Frequency Spectrogram")
                self.canvas = FigureCanvasTkAgg(self.fig, master=self)
                self.canvas.draw()
                toolbar = NavigationToolbar2Tk(self.canvas, self)
                toolbar.update()
                self.canvas.get_tk_widget().pack(fill='both',expand=True)
            case "RT60":
                self.low = audio_data.find_reverb(250)
                self.medium = audio_data.find_reverb(1000)
                self.high = audio_data.find_reverb(5000)

                self.rt60_index = 0
                self.plot_rt60([self.low])
                self.plot.set_title("Low Frequency RT60 graph")
                self.canvas = FigureCanvasTkAgg(self.fig, master=self)
                self.canvas.draw()
                toolbar = RT60Toolbar(self.canvas, self)
                toolbar.update()
                self.canvas.get_tk_widget().pack(fill='both',expand=True)


            case _:
                raise NameError("Invalid type of plot")


    def plot_rt60(self,  data_list: list) -> None:
        """
        Method which plots an RT60 graph given a list of data dictionaries.
        Data dictionary contains all RT60 data returned from audio_data.find_reverb
        """
        self.plot.set_xlabel("Time [s]")
        self.plot.set_ylabel("Power (dB)")
        for data in data_list:
            data_in_db = data["data_in_db"]
            index_of_max = data["index_of_max"]
            index_of_max_less_5 = data["index_of_max_less_5"]
            index_of_max_less_25 = data["index_of_max_less_25"]
            color = data["color"]
            label = data["label"]
            self.plot.plot(self.audio_data.t, data_in_db, linewidth=1, alpha=0.7, color=color, label=label)
            self.plot.plot(self.audio_data.t[index_of_max], data_in_db[index_of_max], 'go')
            self.plot.plot(self.audio_data.t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')
            self.plot.plot(self.audio_data.t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

        if len(data_list) > 1:
            self.plot.legend()

        self.plot.grid()

    def next_rt60(self) -> None:
        """
        Plots next rt60 graph
        """
        array=[[self.low],[self.medium],[self.high],[self.low,self.medium,self.high]]
        title_array = ["Low frequency RT60 graph", "Medium frequency RT60 graph", "High frequency RT60 graph", "All RT60 graphs"]
        self.rt60_index += 1
        self.rt60_index %= len(array)
        self.plot.clear()
        self.plot_rt60(array[self.rt60_index])
        self.plot.set_title(title_array[self.rt60_index])
        self.canvas.draw()
    def prev_rt60(self) -> None:
        """
        Plots previous rt60 graph
        """
        array=[[self.low],[self.medium],[self.high],[self.low,self.medium,self.high]]
        title_array = ["Low frequency RT60 graph", "Medium frequency RT60 graph", "High frequency RT60 graph", "All RT60 graphs"]
        self.rt60_index -= 1
        if self.rt60_index == -1:
            self.rt60_index = len(array) - 1
        self.plot.clear()
        self.plot_rt60(array[self.rt60_index])
        self.plot.set_title(title_array[self.rt60_index])
        self.canvas.draw()
