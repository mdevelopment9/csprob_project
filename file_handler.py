"""
FileHandler class module
"""
from pydub import AudioSegment
from scipy.io import wavfile
import os
import numpy as np
import matplotlib.pyplot as plt


class FileHandler:
    """
    A class that stores file data 
    """
    wavfile_loc = "tmp.wav"

    def __init__(self, input_file: str):
        split_input = input_file.split(".")
        file_end = split_input[len(split_input) - 1]
        sound_file = AudioSegment.from_file(input_file, format=file_end)
        sound_file.export(self.wavfile_loc, format="wav")
        self.samplerate, self.channels, self.length, self.audio_data = self.get_file_data()

    def get_file_data(self):
        """
        Internal class method to get file's data

        :return: File's sample rate, the number of audio channels, and length in seconds
        :rtype: tuple(float)
        """
        samplerate, data = wavfile.read(self.wavfile_loc)
        length = data.shape[0] / samplerate
        # returns the sample rate, the audio channels, and the length of the audio file
        return samplerate, data.shape[len(data.shape) - 1], length, data

    def model_file(self) -> None:
        """
        testing function to model the file in a plot.
        :return: none
        """
        time = np.linspace(0., self.length, self.audio_data.shape[0])
        plt.plot(time, self.audio_data[:, 0], label="Left channel")
        plt.plot(time, self.audio_data[:, 1], label="Right channel")
        plt.legend()
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()
        spectrum, freqs, t, im = plt.specgram(self.audio_data, Fs=self.samplerate,NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        cbar = plt.colorbar(im)
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        cbar.set_label('Intensity (dB)')
        plt.show()