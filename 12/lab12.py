# -*- coding: utf-8 -*-

from numpy import  pi, sin, cos, linspace, exp
from numpy.fft import  fft

from pylab import figure, title, plot, show

from scipy.signal import firwin2
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


freq_sampl = 1000
t = linspace(0, 1, freq_sampl)
w = 200
x = sin(2 * pi * w * t)

freq_linspace, spectr = get_spectrum(x, freq_sampl)
draw(freq_linspace, spectr, 'x', 'x')

w0 = 100

y_exp = x * exp(2 * pi * 1j * w0 * t)
freq_linspace, spectr = get_spectrum(y_exp, freq_sampl)
draw(freq_linspace, spectr, 'y_exp', 'y_exp')

y_cos = x * cos(2 * pi * w0 * t)
freq_linspace, spectr = get_spectrum(y_cos, freq_sampl)
draw(freq_linspace, spectr, 'y_cos', 'y_cos')


[freq_sampl, dti] = read_sound_file('voice.wav')

freq_linspace, spectr = get_spectrum(dti, freq_sampl)
draw(freq_linspace, spectr, 'dti', 'dti')


w0 = 5000

dti_exp = []
for i in xrange(len(dti)):
    dti_exp.append(dti[i] * exp(2 * pi * 1j * w0 * i / freq_sampl))

freq_linspace, spectr = get_spectrum(dti_exp, freq_sampl)
draw(freq_linspace, spectr, 'dti_exp', 'dti_exp')

dti_cos = []
for i in xrange(len(dti)):
    dti_cos.append(dti[i] * cos(2* pi * w0 * i / freq_sampl))

freq_linspace, spectr = get_spectrum(dti_cos, freq_sampl)
draw(freq_linspace, spectr, 'dti_cos', 'dti_cos')

filters = []
delta = 100
order = 100

for i in xrange(1, freq_sampl - delta, delta):
    freqs = [0, 0.9995 * i, 0.9999 * i, i, i + delta, 1.0001 * (i + delta), 1.0005 * (i + delta), freq_sampl]
    gain_levels = [0, 0, 1, 1, 1, 1, 0, 0] 
    fir_filter = firwin2(order, freqs, gain_levels, nyq = freq_sampl)
    filters.append(fir_filter)
   
show()