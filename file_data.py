"""
FileData class module
"""
from typing import Tuple
from pydub import AudioSegment
from scipy.io import wavfile


class FileData:
    """
    A model class that stores the file data 
    """
    wavfile_loc = "tmp.wav"

    def __init__(self, input_file: str):
        split_input = input_file.split(".")
        file_end = split_input[len(split_input) - 1]
        sound_file = AudioSegment.from_file(input_file, format=file_end)
        sound_file.export(self.wavfile_loc, format="wav")

    def get_file_data(self) -> Tuple[float]:
        """
        Class method to get file's data

        :return: File's sample rate, the number of audio channels, and length in seconds
        :rtype: tuple(float)
        """
        samplerate, data = wavfile.read(self.wavfile_loc)
        length = data.shape[0] / samplerate
        # returns the sample rate, the audio channels, and the length of the audio file
        return samplerate, data.shape[len(data.shape) - 1], length, data
