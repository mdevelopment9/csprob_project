"""
AudioData class module
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from file_data import FileData

class AudioData:
    """
    Class for storing the audio data
    """
    def __init__(self, file_data: FileData) -> None:
        self.spectrum = self.freqs = self.split_data = self.sliced_array = self.t = None
        self.samplerate, self.channels, self.length, self.data = file_data.get_file_data()


    def model_file(self) -> None:
        """
        Models the wav file and plots the signal amplitutde. 
        Then, for one channel only, plots the frequency.
        :return: none
        """
        try:
            self.split_data = self.data[:, 0]
        except IndexError:
            # in case of single channel audio
            self.split_data = self.data
        # model freq spectrum
        self.spectrum, self.freqs, self.t, _ = plt.specgram(self.split_data, Fs=self.samplerate, 
                                                        NFFT=1024, cmap=plt.get_cmap('autumn_r'))


    

    def find_resonance(self) -> int:
        """
        Gets the resonant frequency of the audio data
        """
        frequencies, power = welch(self.split_data, self.samplerate, nperseg=4096)
        dominant_frequency = frequencies[np.argmax(power)]
        return round(dominant_frequency)

    def find_nearest_freq(self, target_frequency:int):
        """
        Find nearest frequency to target frequency
        """
        idx = np.abs(self.freqs-target_frequency).argmin()
        return self.freqs[idx]


    def frequency_check(self, target_frequency: int) -> np.ndarray:
        """
        Returns the data to only include the target frequency
        """
        nearest_freq = self.find_nearest_freq(target_frequency)
        print(nearest_freq)
        index_of_target_frequency = np.where(self.freqs == nearest_freq)[0][0]
        data_for_frequency = self.spectrum[index_of_target_frequency]
        data_in_db_fun = 10 * np.log10(data_for_frequency)
        return data_in_db_fun

    def find_nearest_value(self, value) -> np.float64:
        """
        Finds the value closest to the input value
        """
        self.sliced_array = np.asarray(self.sliced_array)
        idx=(np.abs(self.sliced_array-value)).argmin()
        return self.sliced_array[idx]

    def find_reverb(self, target_frequency: int) -> dict:
        """
        Finds the reverb of the audio data
        """
        data_in_db = self.frequency_check(target_frequency)
        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        self.sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = self.find_nearest_value(value_of_max - 5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
        value_of_max_less_25 = self.find_nearest_value(value_of_max - 25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
        rt20 = (self.t[index_of_max_less_5] - self.t[index_of_max_less_25])[0]
        rt60 = np.abs(3 * rt20)
        if target_frequency < 750:
            color = "red"
            label = "Low Frequency"
        elif target_frequency < 4000 :
            color = "green"
            label = "Medium Frequency"
        else:
            color = "blue"
            label = "High Frequency"
        return {
            "data_in_db": data_in_db,
            "index_of_max": index_of_max,
            "index_of_max_less_5": index_of_max_less_5,
            "index_of_max_less_25": index_of_max_less_25,
            "rt60": rt60,
            "color": color,
            "label": label
        }
