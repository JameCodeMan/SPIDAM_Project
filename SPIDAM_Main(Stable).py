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
        try:
            self.spectrum, self.freqs, self.t, self.im = plt.specgram(self.Data, Fs=self.SampRt, NFFT=1024)
        except:
            print("Multi-Channel data detected, only the WavPlt function will work.")
            
        self.TrgtFreq=0
        self.figcount=1
    
    #Plots 2-channel audio data very well
    #Will plot 4-channel data and single channel data, however the graph in both cases will be strange and seemingly worthless
    def WavPlt(self):
        plt.close()
        Channels=self.Data.shape[len(self.Data.shape) - 1]
        try:
            for x in range(Channels):
                plt.plot(self.Time, self.Data[:,x], label=f"Channel {x+1}")
        except:
            plt.plot(self.Time, self.Data[:], label="Channel 1")
        plt.legend()
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        temp=plt
        return temp
        #plt.show()

    #Used by other functions to determine frequency 
    def FreqGet(self, freqs):
        targfreq=input("Input your target frequency: ")
        for x in freqs:
            if x>int(targfreq):
                break
        return x
    
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
    def FreqChck(self):
        plt.close()
        self.TrgtFreq=self.FreqGet(self.freqs)
        FreqIndx=np.where(self.freqs == self.TrgtFreq)[0][0]
        FreqData=self.spectrum[FreqIndx]
        DecData=10*np.log10(FreqData)
        return DecData
     
    #Currently only works on single channel audio (probably), computes rt20 and rt60 values
    def RvrbMesr(self):
        plt.close()
        plt.figure(self.figcount)
        self.figcount+=1
        DbData=self.FreqChck()
        DbData=self.FreqChck()
        plt.figure(self.figcount)
        self.figcount+=1
        plt.plot(self.t, DbData, linewidth=1, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')
        MaxIndx=np.argmax(DbData)
        MaxVal=DbData[MaxIndx]
        plt.plot(self.t[MaxIndx], DbData[MaxIndx], 'go')
        ArrSlce=DbData[MaxIndx:]
        MaxMin5=MaxVal-5
        MaxMin5=self.FindNearest(ArrSlce, MaxMin5)
        MaxMin5Indx=np.where(DbData==MaxMin5)
        plt.plot(self.t[MaxMin5Indx], DbData[MaxMin5Indx], 'yo')
        MaxMin25=MaxVal-25
        MaxMin25=self.FindNearest(ArrSlce, MaxMin25)
        MaxMin25Indx=np.where(DbData==MaxMin25)
        plt.plot(self.t[MaxMin25Indx], DbData[MaxMin25Indx], 'ro')
        rt20=(self.t[MaxMin5Indx]-self.t[MaxMin25Indx])[0]
        rt60=3*rt20
        #plt.xlim(0, ((round(abs(rt60), 2))*1.5))
        plt.grid()
        temp=plt
        self.TrgtFreq=self.FreqGet(self.freqs)
        #plt.show()
        #print(f"The RT60 reverb time at freq {int(self.TrgtFreq)}Hz is {round(abs(rt60), 2)} seconds")
        return temp, rt60
    
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
    wavfilepath=input("Input the absolute path of your .wav file: ")
    tempSamp, tempData, tempLength, tempTime=WavStat(wavfilepath)
    MyWavObj=WavObj(tempSamp, tempData, tempLength, tempTime)
    temp=MyWavObj.WavPlt() #Doesn't work with audio that isn't 2-channel, will be fixed soon
    temp.show()
    plot, rt60=MyWavObj.RvrbMesr()
    plot.show()
    print(f"The RT60 reverb time at freq {int(MyWavObj.TrgtFreq)}Hz is {round(abs(rt60), 2)} seconds")
    temp=MyWavObj.FreqAmp()
    temp.show()
    
if __name__=="__main__":
    main()
