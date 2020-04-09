# -*- coding: utf-8 -*-

from numpy import  pi, sin, cos, linspace, exp, arange, zeros, argmax
from numpy.fft import  fft

from pylab import figure, title, plot, show

from scipy.io.wavfile import read

    
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


def get_pitch_version1(signal, freq_sampl, window_size, offset, offset_number):
    pitch_list = []
    
    for i in xrange(0, len(signal), window_size / 2):
        average_spectrum = zeros(window_size / 2)
        count = 0        
        
        for j in xrange(0, offset * offset_number, offset_number):
            if (i + window_size + j < len(signal)):
                spectrum = fft(signal[i + j:i + window_size + j])
                spectrum = spectrum[0:len(spectrum) / 2]
                average_spectrum += spectrum
                count += 1
        
        if count != 0:
            average_spectrum /= count
            average_spectrum = abs(average_spectrum)
            k = argmax(average_spectrum)
            pitch_value = 1. * k * freq_sampl / window_size
            pitch_list.append(pitch_value)
    
    return pitch_list


filename = 'voice.wav'
[freq_sampl, dti] = read_sound_file(filename)

freq_linspace, spectrum = get_spectrum(dti, freq_sampl) 
draw(freq_linspace, spectrum, 'Spectrum', 'Spectrum')
       
pitch_list = get_pitch_version1(dti, freq_sampl, window_size = 512, offset = 1, offset_number = 10)
draw(xrange(len(pitch_list)), pitch_list, 'Pitch_ver1', 'Pitch_ver1')                   

show()  