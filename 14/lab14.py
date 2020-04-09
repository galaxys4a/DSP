# -*- coding: utf-8 -*-

from numpy import linspace, zeros
from numpy.fft import fft, ifft
from numpy.linalg import solve

from pylab import figure, title, plot, legend, show
from scipy.io.wavfile import read
from scipy.signal import lfilter


def get_spectrum(signal, freq_sampl):
    spectrum = abs(fft(signal))
    spectrum = spectrum[0:len(spectrum) / 2]
    freq_linspace = linspace(0, freq_sampl / 2, len(spectrum))
    return freq_linspace, spectrum


def draw(x_axis, y_axis, figure_name, title_name):
    figure(figure_name)
    title(title_name)
    plot(x_axis, y_axis)


def draw(y_values, figure_name, title_name):
    figure(figure_name)
    title(title_name)
    plot(xrange(len(y_values)), y_values)


def read_sound_file(filename):
    sound_file = open(filename, 'rb')
    [freq_sampl, dti] = read(sound_file)
    sound_file.close()
    return [freq_sampl, dti]


def get_r(dti, count):
    double_count = 2 * count
    extended_dti = zeros(double_count)
    extended_dti[0:count] = dti[0:count]
    r = abs(ifft(fft(extended_dti[0:double_count]) ** 2))
    return r


def get_A_k_matrix(r, k):
    A_k = zeros((k, k))
    for i in xrange(k):
        for j in xrange(k):
            if i == j:
                A_k[i, j] = r[0]
            else:
                A_k[i, j] = A_k[j, i] = r[i]
    return A_k


def get_f_k_vector(r, k):
    f_k = zeros((k, 1))
    for i in xrange(k):
        f_k[i] = r[i + 1]
    return f_k


def get_a_k(dti, count, k):
    r = get_r(dti, count)
    A_k = get_A_k_matrix(r, k)
    f_k = get_f_k_vector(r, k)
    a_k = solve(A_k, f_k)
    return a_k


filename = 'voice.wav'
[freq_sampl , dti] = read_sound_file(filename)

count = 512
k = 14
a_k = get_a_k(dti, count, k)


dti = dti[0:2 * count]
filtered_signal = lfilter(a_k.flatten(), 1, dti)

draw(dti, 'Original signal', 'Original signal')
draw(filtered_signal, 'Predicted signal', 'Predicted signal')

figure("Both signals")
title("Both signals")
plot(dti, label = 'Original signal')
plot(filtered_signal, label = 'Predicted signal')
legend()

show()
