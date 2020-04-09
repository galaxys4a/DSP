# -*- coding: utf-8 -*-

'''
    Примечание: если крайняя правая точка равна 0, то она не учитывается в 
    этом интервале, а учитывается в следующем за этим интервалом (для последнего интервала 
    такая точка не учитывается). 
    Если такие точки необходимо учитывать в этих интервалах тоже, 
    то необходим код, который закомментирован.
'''

import scipy.io.wavfile as sw
import pylab as plb


def zero_crossing(dti, step):
    results = []
    
    start_index = 0
    finish_index = start_index + step
    number_of_iterations = 0 #additional variable for debugging

    while finish_index < len(dti):        
        count_of_zero_crossings = 0
          
        for index in xrange(start_index, finish_index - 1):
            if have_different_signs_or_equals_zero(dti[index], dti[index + 1]):
                count_of_zero_crossings += 1
        
        #if dti[finish_index] == 0:
        #    count_of_zero_crossings += 1 
        
        results.append(count_of_zero_crossings)
          
        start_index += step / 2
        finish_index = start_index + step
        number_of_iterations += 1

    if (finish_index > len(dti) - 1):
        finish_index = len(dti) - 1
        count_of_zero_crossings = 0

        for index in xrange(start_index, finish_index - 1):
            if have_different_signs_or_equals_zero(dti[index], dti[index + 1]):
                count_of_zero_crossings += 1
    
        #if dti[finish_index] == 0:
        #    count_of_zero_crossings += 1 
    
        results.append(count_of_zero_crossings)
        number_of_iterations += 1
    
    print 'number of iterations = ', number_of_iterations 
    return results      
          
def have_different_signs_or_equals_zero(first_number, second_number):    
    return (first_number < 0 and second_number > 0) or (first_number > 0 
        and second_number < 0) or first_number == 0


name_of_sound_file = 'voice.wav'
step = 256

sound_file = open(name_of_sound_file, 'rb')
[freq, dti] = sw.read(sound_file)
sound_file.close()

print 'frequency = ', freq
print 'length of dti = ', len(dti)
 
data = zero_crossing(dti, step)

plb.figure()

plb.plot(data)