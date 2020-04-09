# -*- coding: utf-8 -*-

from numpy import pi, linspace, sin, var, sqrt, correlate, argmax
from numpy.fft import fft

from scipy.io.wavfile import read
from scipy.signal import firwin, filtfilt

from matplotlib.pylab import figure, plot, show


def open_and_read_file(path, is_stereo=False):
    f = open(path, 'rb')
    [freq_sampl, dti] = read(f)
    f.close()
    if is_stereo:
        dti = dti[:, 0]
    return freq_sampl, dti


def get_spectrum(signal):
    spectrum = abs(fft(signal))
    spectrum = spectrum[0:len(spectrum) / 2]
    return spectrum


def draw(name_of_figure, x_axis, y_axis):
    figure(name_of_figure)
    plot(x_axis, y_axis)


def get_watermark(freq_list, freq_sampl, coeff=1.):
    watermark = 0
    t = linspace(0, 1, freq_sampl)
    for freq in freq_list:
        watermark += sin(2 * pi * freq * t)
    watermark /= len(freq_list)
    watermark *= coeff
    return watermark


def insert_watermark(signal, watermark, start_signal=0, start_watermark=0, finish_watermark=0):
    finish_signal = start_signal + (finish_watermark - start_watermark)

    dispersion = sqrt(var(signal[start_signal : finish_signal]))
    watermark *= dispersion

    for i in xrange(start_watermark, finish_watermark):
        signal[start_signal + i] += watermark[i]
    return signal


def get_correlation(signal, watermark):
    correlation = correlate(signal, watermark)
    position = argmax(correlation)
    return correlation, position


file_name = 'voice.wav'
[freq_sampl, dti] = open_and_read_file(file_name, is_stereo=True)

spectrum = get_spectrum(dti)
freq_linspace = linspace(0, freq_sampl / 2, len(spectrum))
draw('Original signal spectrum', freq_linspace, spectrum)

freq_list = [20100, 21000]
watermark = get_watermark(freq_list, freq_sampl, 0.2)

spectrum = get_spectrum(watermark)
freq_linspace = linspace(0, freq_sampl / 2, len(spectrum))
draw('Watermark spectrum', freq_linspace, spectrum)

start_signal = 60000
start_watermark = 0
finish_watermark = 2047
dti = insert_watermark(dti, watermark, start_signal, start_watermark, finish_watermark)
c, position = get_correlation(dti, watermark[start_watermark:finish_watermark])

figure('Correlation')
plot(c)
print 'Watermark position is', position

spectrum = get_spectrum(dti)
freq_linspace = linspace(0, freq_sampl / 2, len(spectrum))
draw('Spectrum of signal with inserted watermark', freq_linspace, spectrum)

order = 55
cut_freq = 30000
b = firwin(order, cut_freq, pass_zero=False, nyq=freq_sampl)

filt_signal = filtfilt(b, 1, dti)
spectrum = get_spectrum(filt_signal)
freq_linspace = linspace(0, freq_sampl / 2, len(spectrum))
draw('Signal with watermark after filtering', freq_linspace, spectrum)

show()