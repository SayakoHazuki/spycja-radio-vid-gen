from os import path
from pydub import AudioSegment
from scipy.io import wavfile
import numpy as np
import cv2
from scipy import signal
from PIL import Image

def image_array_to_png(image_array, mode="L"):
    """
    Convert a numpy array to a PNG image.
    """
    image = Image.fromarray(image_array, mode)
    return image

def export_image_array(image_array, filename, mode=None):
    """
    Export a numpy array as a PNG image.
    """
    image = image_array_to_png(image_array, mode)
    image.save(filename)

class WaveformGenerator:
    """
    WaveformGenerator class
    """
    def __init__(self, audio_file, **kw):
        self.audio_input_file_path = audio_file
        
        audio = AudioSegment.from_mp3(audio_file)
        audio.export("../output/temp/tmpwav.wav", format="wav")
        self.audio_wav_file_path = "../output/temp/tmpwav.wav"
        
        self.samplerate, self.show_data = wavfile.read(self.audio_wav_file_path)
        self.samples = self.show_data.shape[0]
        self.channels, self.is_stereo = 1, False
        if self.show_data.ndim > 1:
            self.channels = self.show_data.shape[1]
            self.is_stereo = True
            
        self.audio_info = {
            "samplerate": self.samplerate,
            "samples": self.samples,
            "channels": self.channels,
            "is_stereo": self.is_stereo
        }
        
    def generate_spectral_waves(self, shape, threshold, nps=None):
        _, _, spg = signal.spectrogram(self.show_data[:, 0], self.samplerate, nperseg=nps)
        spg /= spg.max()    # Normalize spectrogram
        # Remove empty spaces
        _, th_bin = cv2.threshold(spg, threshold, 1.0, cv2.THRESH_BINARY)
        nzrs = np.nonzero(th_bin.sum(axis=1))
        _, th_trc = cv2.threshold(spg[np.min(nzrs):np.max(nzrs), :], threshold, 1.0, cv2.THRESH_TRUNC)
        # Reshape spectrogram
        resized = cv2.resize(th_trc, shape, interpolation=cv2.INTER_AREA)
        resized /= resized.max()
        self.spectral_waves = resized.transpose()
        return resized
    
    def generate_wave_frames(self, spectral_waves):
        height, width = (1080, 200)
        num_frames, num_bits = spectral_waves.shape
        area = ( 10, width-10, 80, 120)
        x_line = np.linspace(area[0], area[1], num_bits, dtype='int')
        self.frames = []
        for i in range(len(spectral_waves)):
            for bit in range(num_bits):
                p1 = (x_line[bit], 100 - int(100*spectral_waves[i][bit]))
                p2 = (x_line[bit], 100 + int(100*spectral_waves[i][bit]))
                empty_frame = np.zeros((1080, 1920, 3), dtype='uint8')
                cv2.line(empty_frame, p1, p2, (255, 255, 255), thickness=5, lineType=cv2.LINE_AA)
            self.frames.append(empty_frame)
        return self.frames
        
    
if __name__ == "__main__":
    audio_file = "C:\\Code\\spycja-radio-vid-gen\\assets\\20231209\\untitled.mp3"
    wg = WaveformGenerator(audio_file)
    wg.generate_spectral_waves((1080, 200), 1e-3)
    wg.generate_wave_frames(wg.spectral_waves)
    breakpoint()
    pass