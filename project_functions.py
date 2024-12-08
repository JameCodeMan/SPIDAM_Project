from scipy.io import wavfile
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import tkinter

class WavObj:
    def __init__(self, SampRt, Data, Length, Time):
        self.SampRt=SampRt
        self.Data=Data
        self.Length=Length
        self.Time=Time
        self.spectrum, self.freqs, self.t, self.im = plt.specgram(self.Data, Fs=self.SampRt, NFFT=1024)
        self.TrgtFreq=0
        self.figcount=1
    
    #Plots 2-channel audio data very well
    #Will plot 4-channel data and single channel data, however the graph in both cases will be strange and seemingly worthless
    def WavPlt(self):
        plt.close()
        fig, ax = plt.subplots()
        Channels=self.Data.shape[len(self.Data.shape) - 1]
        try:
            for x in range(Channels):
                ax.plot(self.Time, self.Data[:,x], label=f"Channel {x+1}")
        except:
            ax.plot(self.Time, self.Data[:], label="Channel 1")
        ax.legend()
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")
        ax.grid()
        plt.show()

    #Used by other functions to determine frequency 
    def FreqGet(self, freq_range="low"):
        if freq_range == "low":
            freq_min = 20
            freq_max = 500
        elif freq_range == "mid":
            freq_min = 500
            freq_max = 2000
        elif freq_range == "high":
            freq_min = 2000
            freq_max = 20000
        else:
            raise ValueError("Unknown frequency range")
        return np.linspace(freq_min,freq_max, 1000)
    
    #Currently only works with single channel audio, plots intensity relative to frequency and time
    def FreqAmp(self):
        plt.close()
        no, noo, noooo, im=plt.specgram(self.Data, Fs=self.SampRt, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        cbar=plt.colorbar(im)
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (HZ)')
        cbar.set_label('Intensity (dB)')
        temp=plt
        return temp
    
    #Currently only works on single channel audio (probably), not sure exactly what it does but it seems to return some sort of measurement in decibels 
    def FreqChck(self,freq):
        plt.close()
        self.TrgtFreq=self.FreqGet(self.freqs)
        FreqIndx=np.where(self.freqs == self.TrgtFreq)[0][0]
        FreqData=self.spectrum[FreqIndx]
        DecData=10*np.log10(FreqData)
        return DecData
    
    #Currently only works on single channel audio (probably), plots decibel levels as a fucntion of time
    def FreqPlot(self):
        plt.close()
        DbData=self.FreqChck()
        plt.figure(self.figcount)
        self.figcount+=1
        plt.plot(self.t, DbData, linewidth=1, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')
        temp=plt
        plt.show()
     
    #Currently only works on single channel audio (probably), computes rt20 and rt60 values
    def RvrbMesr(self, ax=None, freq_range="low"):
        # Ensure a figure is created or use the provided axis
        if ax is None:
            fig, ax = plt.subplots(num=self.figcount)
            self.figcount += 1
        else:
            fig = ax.figure  # If an axis is provided, get its parent figure

        DbData = self.FreqGet(freq_range)
        MaxIndx = np.argmax(DbData)
        MaxVal = DbData[MaxIndx]

        # Plot the maximum point
        ax.plot(self.t[MaxIndx], DbData[MaxIndx], 'go', label="Max Value")

        ArrSlce = DbData[MaxIndx:]
        MaxMin5 = MaxVal - 5
        MaxMin5 = self.FindNearest(ArrSlce, MaxMin5)
        MaxMin5Indx = np.where(DbData == MaxMin5)[0][0]  # Get index
        plt.plot(self.t[MaxMin5Indx], DbData[MaxMin5Indx], 'yo', label="-5 dB")

        MaxMin25 = MaxVal - 25
        MaxMin25 = self.FindNearest(ArrSlce, MaxMin25)
        MaxMin25Indx = np.where(DbData == MaxMin25)[0][0]  # Get index
        plt.plot(self.t[MaxMin25Indx], DbData[MaxMin25Indx], 'ro', label="-25 dB")

        # Calculate RT20 and RT60
        rt20 = (self.t[MaxMin5Indx] - self.t[MaxMin25Indx])
        rt60 = 3 * rt20

        # Adjust axis and labels
        ax.set_xlim(0, ((round(abs(rt60), 2)) * 1.5))
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude [dB]")
        plt.grid()
        plt.legend()

        # Display RT60 information
        self.TrgtFreq = self.FreqGet(freq_range)
        fig.suptitle(f"RT60 at {int(self.TrgtFreq)}Hz: {round(abs(rt60), 2)} seconds")
        print(f"The RT60 reverb time at freq {int(self.TrgtFreq)}Hz is {round(abs(rt60), 2)} seconds")

        plt.show()
        return rt60
    
    def FindNearest(self, array, value):
        array=np.asarray(array)
        idx=(np.abs(array-value)).argmin()
        return array[idx]

def WavStat(WavName):
    SampRt, Data=wavfile.read(WavName)
    Length=Data.shape[0]/SampRt
    Time=np.linspace(0.,Length,Data.shape[0])
    return SampRt, Data, Length, Time


def main():
    """ wavfilepath=input("Input the absolute path of your .wav file: ")
    tempSamp, tempData, tempLength, tempTime=WavStat(wavfilepath)
    MyWavObj=WavObj(tempSamp, tempData, tempLength, tempTime)
    temp=MyWavObj.WavPlt() #Doesn't work with audio that isn't 2-channel, will be fixed soon
    temp.show()
    temp1=MyWavObj.FreqPlot()
    temp1.show()
    plot, rt60=MyWavObj.RvrbMesr()
    plot.show()
    print(f"The RT60 reverb time at freq {int(MyWavObj.TrgtFreq)}Hz is {round(abs(rt60), 2)} seconds")
    temp=MyWavObj.FreqAmp()
    temp.show() """

if __name__=="__main__":
    main()