# -*- coding: utf-8 -*-


from numpy import  pi, linspace, sin, cos, real, imag, sqrt, arctan, diff, unwrap
from numpy.fft import  fft

from pylab import figure, title, plot, show

from scipy.signal import hilbert


# M - AM-modulation coefficient
# w - carrier frequency
# A - amplitude
# phi - phase shift
def get_AM_signal(signal, t, M, w, A = 1, phi = 0):
    am_signal = A * (1 + M * signal) * cos(2 * pi * w * t + phi)
    return am_signal
    
    
def get_spectrum(signal, freq_sampl):
    spectrum = abs(fft(signal))
    spectrum = spectrum[0:len(spectrum) / 2]
    freq_linspace = linspace(0, freq_sampl / 2, len(spectrum))
    return freq_linspace, spectrum
    

def draw(x_axis, y_axis, figure_name, title_name):
    figure(figure_name)
    title(title_name)
    plot(x_axis, y_axis)
    

def get_data_from_analytic_signal(z):
    s = real(z)
    s_ort = imag(z)

    a = sqrt(s**2 + s_ort**2)
    
    phi = arctan(s / s_ort)
    phi_unwrap = arctan(unwrap(s / s_ort))
    
    w = (diff(s)/diff(t) * s_ort[:-1] - diff(s_ort)/diff(t) * s[:-1]) / (s[:-1]**2 + s_ort[:-1]**2)
    w_unwrap = unwrap(w)    
    
    return [a, phi, w, phi_unwrap, w_unwrap]
    
        
freq_sampl = 1000
t = linspace(0, 1, freq_sampl)
w0 = 5
information_signal = sin(2 * pi * w0 * t)

M = 1
carrier_freq = 100
am_signal = get_AM_signal(information_signal, t, M, carrier_freq)


draw(t, information_signal, 'Information signal', 'Information signal')
freq_linspace, spectrum = get_spectrum(information_signal, freq_sampl)
draw(freq_linspace, spectrum, 'Information signal spectrum', 'Spectrum of information signal')

draw(t, am_signal, 'AM signal', 'AM signal')
freq_linspace, spectrum = get_spectrum(am_signal, freq_sampl)
draw(freq_linspace, spectrum, 'AM signal spectrum', 'Spectrum of AM signal')

z = hilbert(am_signal)
[a, phi, w, phi_unwrap, w_unwrap] = get_data_from_analytic_signal(z)

draw(range(len(a)), a, 'Envelope', 'Envelope')
draw(range(len(phi)), phi, 'Phase', 'Phase')
draw(range(len(w)), w, 'Frequency', 'Frequency')

draw(range(len(phi_unwrap)), phi_unwrap, 'Phase(unwrap)', 'Phase(unwrap)')
draw(range(len(w_unwrap)), w_unwrap, 'Frequency(unwrap)', 'Frequency(unwrap)')

show() 