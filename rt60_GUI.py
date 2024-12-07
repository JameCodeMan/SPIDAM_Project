import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import numpy as np
from pydub import AudioSegment
import soundfile as sf
import mutagen
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram
import scipy.io

class AudioAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("Reverberation Time Analyzer")

        # GUI Elements
        self.label = tk.Label(master, text="RT60 Analyzer", font=("Arial", 16))
        self.label.grid(row=0, column=0, pady=10)

        self.load_button = tk.Button(master, text="Load File", command=self.load_file)
        self.load_button.grid(row=1, column=0, pady=5)

        self.analyze_button = tk.Button(master, text="Analyze", command=self.analyze_audio)
        self.analyze_button.grid(row=2, column=0, pady=5)

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.grid(row=3, column=0, pady=5)

        # Frame for displaying the audio file chosen
        _img_frame = ttk.LabelFrame(master, text='Content', padding='9 0 0 0')
        _img_frame.grid(row=4, column=0, sticky="NSEW", padx=10, pady=5)

    
        self.audio_file_label = tk.Label(_img_frame, text="No file selected", width=50, anchor="w")
        self.audio_file_label.grid(row=0, column=0, padx=5, pady=5)

        self.file_path = None

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.aac")])
            
        if self.file_path.endswith(".wav"):
            pass
        else:
           return self.convert_audio(self.file_path)

        if not self.file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        # Update label with the file name
        file_name = self.file_path.split("/")[-1]
        self.audio_file_label.config(text=f"Selected File: {file_name}")
        messagebox.showinfo("File Loaded", f"Loaded file: {self.file_path}")

        #checks for metadata and removes it
        meta = mutagen.File(self.file_path)
        if meta:
            meta.clear()
            meta.save()
        else:
            pass
        

    def monochannel(self):
        wav_fname = AudioSegment.from_file(self.file_path)
        mono_audio = wav_fname.set_channels(1)
        mono_audio.export(self.file_path, format = "wav")


    def convert_audio(self,file_path):
           if file_path:
              audio = AudioSegment.from_file(file_path)
              self.output = file_path.rsplit('.',1)[0] + ".wav"
              audio.export(self.output, format="wav")
              self.file_path = self.output
              self.file_name = self.output.split("/")[-1]
              self.audio_file_label.config(text=f"Selected File: {self.file_name}")
              messagebox.showinfo("File Loaded", f"Loaded file: {self.output}")

    def analyze_audio(self):

        samplerate, data = wavfile.read(self.file_path) #Scans audio file
        duration = len(data) / samplerate #Finds duration in seconds

        freqs, times, Sxx = spectrogram(data, samplerate) #Sets up spectogram graph

        freq_min, freq_max = freqs[0], freqs[-1]

        freq_lower = freq_min + (freq_max - freq_min) / 3
        freq_upper = freq_min + 2 * (freq_max - freq_min) / 3

        rt60_low = np.mean(Sxx[freqs <= freq_lower])  # Low frequency
        rt60_mid = np.mean(Sxx[(freqs > freq_lower) & (freqs <= freq_upper)])  # Mid frequency
        rt60_high = np.mean(Sxx[freqs > freq_upper])  # High frequency

        max_freq = freqs[np.argmax(Sxx.sum(axis=1))] #Finds maximum frequency

        low = np.mean(Sxx[freqs < 5000]) #Low frequency, below 5000
        mid = np.mean(Sxx[(freqs >= 5000) & (freqs < 15000)]) #Mid frequency, between 5000 and 15000
        high = np.mean(Sxx[freqs >= 15000]) #High frequency, above 15000

        if not self.file_path:
            messagebox.showerror("Error", "Please load an audio file first.")
            return

        # Continue with your audio analysis code here
        messagebox.showinfo("Analyze", f"Analyzing: {self.file_path}")

        result = (f"Duration: {duration:.1f} seconds\n" 
        f"Highest frequency: {max_freq:.1f} Hz\n"
        f"Low: {low:.1f}\n"
        f"Mid: {mid:.1f}\n"
        f"High: {high:.1f}")
        messagebox.showinfo("Results", result) #Prints results


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioAnalyzerApp(root)
    root.mainloop()
