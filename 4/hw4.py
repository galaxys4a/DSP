# -*- coding: utf-8 -*-

# fft(convolve(x, y)) = fft(x) * fft(y) | ifft()
# ifft(fft(convolve(x, y))) = ifft(fft(x) * fft(y))
# convolve(x, y) = ifft(fft(x) * fft(y))

import numpy as np
import datetime as dt


def get_signal_of_uniform_dist(low, high, size):
    return np.random.uniform(low, high, size)
    
def get_fourier_convolution(x_signal, y_signal):
    [x_signal_with_zeros, y_signal_with_zeros] = get_signals_with_added_zeros(x_signal, y_signal)
    x_fourier = np.fft.fft(x_signal_with_zeros)
    y_fourier = np.fft.fft(y_signal_with_zeros)
    h_fourier = x_fourier * y_fourier
    h_signal = np.fft.ifft(h_fourier)
    last_index = len(x_signal) + len(y_signal) - 1
    return h_signal[0 : last_index]
    
def get_signals_with_added_zeros(x_signal, y_signal):    
    number_pow2 = get_roundup_number_pow2(len(x_signal) + len(y_signal) - 1)
    x_signal_with_zeros = list(x_signal) + [0] * (number_pow2 - len(x_signal))
    y_signal_with_zeros = list(y_signal) + [0] * (number_pow2 - len(y_signal))    
    return x_signal_with_zeros, y_signal_with_zeros

def get_roundup_number_pow2(number):
    while number & (number - 1):
        number = (number | (number >> 1)) + 1
    return number  
 
 
low_for_x = 0
high_for_x = 10
size_of_x = 7

low_for_y = 0
high_for_y = 10
size_of_y = 9

number_of_iterations = 1000
epsilon = 10**(-9)

x = get_signal_of_uniform_dist(low_for_x, high_for_x, size_of_x)
y = get_signal_of_uniform_dist(low_for_y, high_for_y, size_of_y)

print 'signal x:', x
print 'signal y:', y

start_time = dt.datetime.now();
for i in xrange(number_of_iterations):
    h1 = np.convolve(x, y, 'full')
finish_time = dt.datetime.now()
time1 = (finish_time - start_time) / number_of_iterations

start_time = dt.datetime.now();
for i in xrange(number_of_iterations):
    h2 = get_fourier_convolution(x, y)
finish_time = dt.datetime.now()
time2 = (finish_time - start_time) / number_of_iterations


print ''
print 'Results:'
#3, 5, 10 - lengths of gaps
print 'num   directly     with fourier          delta'
delta_h = h1 - h2
index = 0 
while (index < len(delta_h)):
    print index + 1, ')', h1[index], ' ', abs(h2[index]),' ', abs(delta_h[index])
    index += 1
    
is_difference_very_small = True
for value in delta_h:
    if (abs(value) > epsilon):
        is_difference_very_small = False
print 'Are results equal? Answer:', is_difference_very_small 

print 'Directly calculated time:', time1
print 'Calculated with Fourier transform time:', time2