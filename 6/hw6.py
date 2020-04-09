# -*- coding: utf-8 -*-

import numpy as np
import pylab as plb
import scipy.signal as sgn


def get_complex_sin_signal(freqs, freq_sampl):
    signal = 0
    t = np.linspace(0, 1, freq_sampl)
    for freq in freqs:
        signal += np.sin(2 * np.pi * freq * t)
    return signal

def get_fir_bandpass_filter(order, f1, f2, f_sampl):
    f1 = 1.0 * f1 / f_sampl
    f2 = 1.0 * f2 / f_sampl
    left_f1 = f1 - 0.05
    right_f2 = f2 + 0.05
    freq = [0, left_f1, f1, f2, right_f2, 1]
    gain = [0, 0, 1, 1, 0, 0]
    filt = sgn.firwin2(order, freq, gain)
    return filt

# input data
sin_freqs = [15, 40, 60, 90]
f_sampl = 200
order = 100
f1 = 40
f2 = 60

f_max = max(sin_freqs)
filt = get_fir_bandpass_filter(order, f1, f2, f_sampl / 2)
w, h = sgn.freqz(filt)

plb.figure('Filter')
plb.title('Transfer function of FIR filter')
plb.plot(w / np.pi, abs(h))
plb.legend()

plb.figure('Filter_custom')
plb.title('Transfer function of FIR filter')
plb.plot(w / np.pi * f_max, abs(h))
plb.legend()

signal = get_complex_sin_signal(sin_freqs, f_sampl)
spectr = np.fft.fft(signal)
spectr_of_s = abs(spectr)[0 : len(spectr) / 2]

filtered_signal = sgn.lfilter(filt, 1, signal)
spectr = np.fft.fft(filtered_signal)
spectr_of_filt_s = abs(spectr)[0 : len(spectr) / 2]

plb.figure('Before')
plb.title('Spectrum of signal')
plb.plot(spectr_of_s)

plb.figure('After')
plb.title('Spectrum of signal')
plb.plot(spectr_of_filt_s)

plb.figure('Spectrum')
plb.title('Spectrum of signal')
plb.plot(spectr_of_s, label = 'Before filtering')
plb.plot(spectr_of_filt_s, label = 'After filtering', color = 'red')
plb.legend()
plb.show()