# -*- coding: utf-8 -*-

import numpy as np
import scipy.io.wavfile as sw
import pylab as plb


# [ 0 1 0 ... 0
#   0 0 1 ... 0
#   ....... 1 0
#   0 ......0 1
#   c[0] ... c[n-1]]
def generate_A_matrix(coefficients):
    shape = len(coefficients) - 1
    ones_vector = np.ones(shape)
    matrix = np.diag(ones_vector)
    
    shape = len(coefficients) - 1;
    zeros_vector = np.zeros((shape, 1))
    matrix = np.hstack((zeros_vector, matrix))
    
    matrix = np.vstack((matrix, coefficients))
    return matrix

# [ 0 0 0 ... 0 1] length = n    
def generate_s_vector(n): 
    s_vector = np.zeros(n)
    s_vector[n - 1] = 1
    return s_vector
    
def get_watermark(polynom):
    n = len(polynom)
    A = generate_A_matrix(polynom)
    s = generate_s_vector(n)
    d = polynom
    
    watermark = []    
    for i in xrange(2**n - 1):
        wk = np.dot(d, s) % 2
        wk = wk * 2 - 1 # {0, 1} -> {-1, 1}
        watermark.append(wk)
        s = np.dot(A, s) % 2
    return watermark
    
def find_watermark_position(filename, polynom):
    watermark = get_watermark(polynom)    
    
    soundfile = open(filename, 'rb')
    [freq, dti] = sw.read(soundfile) 
    soundfile.close() 
    
    correlation = np.correlate(dti, watermark)
    plb.figure()
    plb.plot(correlation)
    position = np.argmax(correlation)
    return position
    
    
polynom = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
filename = 'watermark.wav'
position = find_watermark_position(filename, polynom)
#699999
print position