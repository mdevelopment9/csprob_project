"""
AudioData class module
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from file_data import FileData

class AudioData:
    """
    Class for storing the audio data
    """
    def __init__(self, file_data: FileData) -> None:
        self.spectrum = self.freqs = None
        self.samplerate, self.channels, self.length, self.audio_data = file_data.get_file_data()


    def model_file(self) -> None:
        """
        Models the wav file and plots the signal amplitutde. Then, for one channel only, plots the frequency.
        :return: none
        """
        

    def find_target_frequency(self,freqs):
        for x in freqs:
            if x > 1000:
                break
            return x

    def frequency_check(self):
        target_frequency = self.find_target_frequency(self.freqs)
        index_of_target_frequency = np.where(self.freqs == target_frequency)[0][0]
        data_for_frequency = self.spectrum[index_of_target_frequency]
        data_in_db_fun = 10 * np.log10(data_for_frequency)
        return data_in_db_fun
    
    def find_reverb(self,spectrum,freqs,t,im):
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
