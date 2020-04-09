# -*- coding: utf-8 -*-

import numpy as np


def get_signal_to_noise_ratio(signal, number_of_bits):
    coefficient = 2**(number_of_bits - 1)
    quantification = np.round(signal * coefficient) / coefficient
    error = signal - quantification
    dispersion_of_signal = np.var(signal) 
    dispersion_of_error = np.var(error)
    signal_to_noise_ratio = 10 * np.log10(dispersion_of_signal / dispersion_of_error)
    return signal_to_noise_ratio

def get_theor_signal_to_noise_ratio(number_of_bits):
    return 20 * number_of_bits * np.log10(2)    
    
    
# w - frequency of signal 
w = 10
# Fd - sampling frequency
Fd = 1000
# t - time
t = np.linspace(0, 1, Fd)
# B - number of bits
B = 16
x = np.sin(2 * np.pi * w * t)
print 'For sin signal:'
print 'Practical value of SNR = ', get_signal_to_noise_ratio(x, B)
print 'Theoretical value of SNR = ', get_theor_signal_to_noise_ratio(B)

x = np.random.uniform(-1.0, 1.0, Fd)
print 'For random signal (uniform distribution):'
print 'Practical value of SNR = ', get_signal_to_noise_ratio(x, B)
print 'Theoretical value of SNR = ', get_theor_signal_to_noise_ratio(B)