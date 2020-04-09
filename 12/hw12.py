# -*- coding: utf-8 -*-


from numpy import pi, linspace, exp, real
from numpy.fft import fft

from pylab import figure, title, plot, show

from scipy.io.wavfile import read
from scipy.signal import hilbert

import wave
import struct


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


def move_spectrum_right(signal, freq_sampl, w):
    c = hilbert(signal)
    
    z = []
    for i in xrange(len(c)):
        z.append(c[i] * exp(2 * pi * 1j * w * i / freq_sampl))

    xs = real(z)
    return xs


[freq_sampl, dti] = read_sound_file('voice.wav')

freq_linspace, spectr = get_spectrum(dti, freq_sampl)
draw(freq_linspace, spectr, 'Original signal spectrum', 'Spectrum of original signal')

w = 2000
xs = move_spectrum_right(dti, freq_sampl, w)

freq_linspace, spectr = get_spectrum(xs, freq_sampl)
draw(freq_linspace, spectr, 'Modified signal spectrum', 'Spectrum of modified signal')    

write_sound_file(xs, freq_sampl, 'new_voice.wav')
    
show()  