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
        self.spectrum = None
        self.freqs = None
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
        Models the wav file and plots the signal amplitutde. Then, for one channel only, plots the frequency.
        :return: none
        """
        time = np.linspace(0., self.length, self.audio_data.shape[0])
        try:
            split_data = self.audio_data[:, 0]
        except IndexError as e:
            # in case of single channel audio
            split_data = self.audio_data
        plt.plot(time, split_data, label="Left channel")
        plt.legend()
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()
        # model freq spectrum
        self.spectrum, self.freqs, t, im = plt.specgram(split_data, Fs=self.samplerate, NFFT=1024,
                                                        cmap=plt.get_cmap('autumn_r'))
        cbar = plt.colorbar(im)
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        cbar.set_label('Intensity (dB)')
        plt.show()
        self.find_file_reverb(self.spectrum,self.freqs,t,im)

    def find_target_frequency(self,freqs):
        for x in freqs:
            if x > 1000:
                break
            return x

    def frequency_check(self):
        global target_frequency
        target_frequency = self.find_target_frequency(self.freqs)
        index_of_target_frequency = np.where(self.freqs == target_frequency)[0][0]
        data_for_frequency = self.spectrum[index_of_target_frequency]
        data_in_db_fun = 10 * np.log10(data_for_frequency)
        return data_in_db_fun
    def find_file_reverb(self,spectrum,freqs,t,im):
        data_in_db = self.frequency_check()
        plt.figure(2)
        plt.plot(t, data_in_db, linewidth=1, alpha=0.7)
        plt.xlabel("Time [s]")
        plt.ylabel("Power (dB)")
        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
        sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5
        #unfinished