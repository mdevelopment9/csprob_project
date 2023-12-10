"""
Module for the PlotWindow class
"""
import tkinter as tk
from audio_data import AudioData
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
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

        fig = Figure(figsize = (5,5),
                     dpi = 100)
        time = np.linspace(0., audio_data.length, audio_data.data.shape[0])
        try:
            split_data = audio_data.data[:, 0]
        except IndexError:
            # in case of single channel audio
            split_data = audio_data.data

        plot = fig.add_subplot(111)
        match plot_type:
            case "Waveform":
                plot.plot(time, split_data, label="Left channel")
                plot.legend()
                plot.set_xlabel("Time [s]")
                plot.set_ylabel("Amplitude")
                canvas = FigureCanvasTkAgg(fig, master=self)
                canvas.draw()
                toolbar = NavigationToolbar2Tk(canvas, self)
                toolbar.update()
                canvas.get_tk_widget().pack(fill='both',expand=True)
            case "Spectrum":
                spectrogram_data = plot.specgram(
                    split_data,
                    Fs=audio_data.samplerate,
                    NFFT=1024,
                    cmap=plt.get_cmap('autumn_r')
                )
                cbar = fig.colorbar(spectrogram_data[3])
                plot.set_xlabel('Time (s)')
                plot.set_ylabel('Frequency (Hz)')
                cbar.set_label('Intensity (dB)')
                canvas = FigureCanvasTkAgg(fig, master=self)
                canvas.draw()
                toolbar = NavigationToolbar2Tk(canvas, self)
                toolbar.update()
                canvas.get_tk_widget().pack(fill='both',expand=True)
            case "RT60":
                low = audio_data.find_reverb(250)
                medium = audio_data.find_reverb(1000)
                high = audio_data.find_reverb(5000)
            case _:
                raise NameError("Invalid type of plot")
