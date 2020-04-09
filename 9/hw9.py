# -*- coding: utf-8 -*-

from numpy import pi, linspace, angle, diff, unwrap
from numpy.fft import fft
from scipy.signal import iirfilter, chirp, freqz, filtfilt

from pylab import figure, title, plot, show


def get_spectrum(signal, freq_sampl):
    spectrum = abs(fft(signal))
    spectrum = spectrum[0:len(spectrum) / 2]
    freq_linspace = linspace(0, freq_sampl / 2, len(spectrum))
    return freq_linspace, spectrum
    
    
def draw(x_axis, y_axis, figure_name, title_name):
    figure(figure_name)
    title(title_name)
    plot(x_axis, y_axis)

#f(t) = f0 + (f1 - f0) * t / t1
def generate_and_filter_chirp_signal(b, a, t, f0, t1, f1, index, method='linear', phi=0):
    s = chirp(t, f0, t1, f1, method, phi)
    draw(t, s, 'Original signal' + str(index), 'Original signal' + str(index))

    freq_linspace, spectr = get_spectrum(s, freq_sampl)
    draw(freq_linspace, spectr, 'Original signal spectrum' + str(index), 'Spectrum of original signal'+ str(index))

    filt_signal = filtfilt(b, a, s)
    draw(t, filt_signal, 'Filtered signal' + str(index), 'Filtered signal' + str(index))

    freq_linspace, spectr = get_spectrum(filt_signal, freq_sampl)
    draw(freq_linspace, spectr, 'Filtered signal spectrum' + str(index), 'Spectrum of filtered signal' + str(index))


order = 13
cutoff_freq = 0.8
b, a = iirfilter(order, cutoff_freq, btype='lowpass')

w, h = freqz(b, a)
draw(w / pi, abs(h), 'Filter', 'Transfer function of IIR filter')

argument_teta = angle(h / abs(h))
phase_delay = unwrap(argument_teta) / w
group_delay = unwrap(diff(argument_teta) / diff(w))

draw(w, phase_delay, 'Phase delay', 'Phase delay')
draw(w[:-1], group_delay,'Group delay', 'Group delay')

figure('Phase delay 2')
title('Phase delay 2')
plot(w, phase_delay)
plot(w, unwrap(argument_teta))

freq_sampl = 1000
t = linspace(0, 1, freq_sampl)

f0 = 500
t1 = 0.9
f1 = 900
index = 1
generate_and_filter_chirp_signal(b, a, t, f0, t1, f1, index)

f0 = 30
t1 = 0.9
f1 = 10
index += 1
generate_and_filter_chirp_signal(b, a, t, f0, t1, f1, index)

show()