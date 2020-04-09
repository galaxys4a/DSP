# -*- coding: utf-8 -*-

from numpy import arange, zeros, linspace
from numpy.fft import fft

from pylab import figure, title, plot, show

from scipy.io.wavfile import read
import wave
import struct


def downsampling(dti, freq_sampl, M):
    down_dti = dti[arange(0, len(dti), M)]
    return down_dti
    

def upsampling(dti, freq_sampl, M):
    up_dti = zeros(len(dti) * M)
    up_dti[arange(0, len(dti) * M, M)] = dti
    return up_dti


def get_spectrum(signal, freq_sampl):
    spectrum = abs(fft(signal))
    spectrum = spectrum[0:len(spectrum) / 2]
    freq_linspace = linspace(0, freq_sampl / 2, len(spectrum))
    return freq_linspace, spectrum
    

def draw(x_axis, y_axis, figure_name, title_name):
    figure(figure_name)
    title(title_name)
    plot(x_axis, y_axis)
    
    
def read_sound_file(filename):
    sound_file = open(filename, 'rb')
    [freq_sampl, dti] = read(sound_file)
    sound_file.close()
    return [freq_sampl, dti]
    
    
def write_sound_file(dti, freq_sampl, filename):
    sound_file = wave.open(filename, 'wb')
    
    pck = []
    for dti_value in dti:
        pck.append(struct.pack('h', dti_value))

    str_out = ''.join(pck)
    
    sound_file.setparams((1, 2, freq_sampl, 0, 'NONE', 'not compressed'))
    sound_file.writeframes(str_out)
    sound_file.close()
    

filename = 'voice.wav'
[freq_sampl, dti] = read_sound_file(filename)

[freq_linspace, spectrum] = get_spectrum(dti, freq_sampl) 
draw(freq_linspace, spectrum, 'Original signal', 'Spectrum of original signal')       

M = 2

down_dti = downsampling(dti, freq_sampl, M)
[freq_linspace, spectrum] = get_spectrum(down_dti, freq_sampl)
draw(freq_linspace, spectrum, 'Downsampled signal', 'Spectrum of downsampled signal')   
write_sound_file(down_dti, freq_sampl, 'downsampling.wav') 

up_dti = upsampling(dti, freq_sampl, M)
[freq_linspace, spectrum] = get_spectrum(up_dti, freq_sampl) 
draw(freq_linspace, spectrum, 'Upsampled signal', 'Spectrum of upsampled signal')   
write_sound_file(up_dti, freq_sampl, 'upsampling.wav') 

show()