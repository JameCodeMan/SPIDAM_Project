The SPIDAM project makes use of the NumPy, PyDub and SciPy libraries to analyze .wav audio files. It can be used to determine the duration, maximum frequency, and three points of frequency (Low, middle and high) of a selected .wav audio file. This allows for examining the resonance of a certain sound using data surrounding it's duration and frequency.

Upon opening the module, you should see a button labeled "Load File". This allows you to upload the audio file you would like to analyze. If the file is not a .wav file already (i.e. if it's a .mp3 or .aan file), it will be converted to .wav automatically.

The "Analyze" button tells the program to scan the audio file. It will then return the duration of the sound in seconds, the highest frequency the sound reaches, and the three points of frequency - low, middle and high.

On the right, there is an option to create one of five graphs - a waveform graph, an RT60 high graph, an RT60 mid graph, an RT60 low graph, and a combined graph of all three RT60 types. 
