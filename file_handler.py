from pydub import AudioSegment
from scipy.io import wavfile
import scipy.io
"""convert file from supported format and convert to wav"""
class FileHandler:
    wavfile_loc = "tmp.wav"

    def __init__(self, input_file: str):

        split_input = input_file.split(".")
        file_end = split_input[len(split_input)-1]
        sound_file = AudioSegment.from_file(input_file,format=file_end)
        sound_file.export(self.wavfile_loc, format="wav")
        self.samplerate, self.channels, self.length = self.getFileData()

    def getFileData(self):
        samplerate,data = wavfile.read(self.wavfile_loc)
        length = data.shape[0] / samplerate
        #returns the sample rate, the audio channels, and the length of the audio file
        return samplerate,data.shape[len(data.shape) - 1],length
