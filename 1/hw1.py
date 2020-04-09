# -*- coding: utf-8 -*-

def sum_cubes(N):
    result = 0
    for i in range(N + 1):
        result += i**3 
    return result
        
def calculate_avr_and_median(list_of_numbers):
    count = len(list_of_numbers)
    summ = 0.0
    for number in list_of_numbers:
        summ += number
    average = summ / count
        
    tmp_list = list_of_numbers
    sort_list(tmp_list)
    median = 0.0
    if count % 2 == 1:
        median = tmp_list[count / 2]
    else:
        median = (tmp_list[count / 2 - 1] + tmp_list[count / 2]) / 2.0
        
    return average, median

def sort_list(a):
    for i in range(len(a) - 1):
        for j in range(len(a) - i - 1):            
            if a[j] > a[j + 1]:
                tmp = a[j]
                a[j] = a[j + 1]
                a[j + 1] = tmp
                
                
N = 3
print "Sum of cubes of first 3 integers = ", sum_cubes(N)
N = 5
print "Sum of cubes of first 5 integers = ", sum_cubes(N)

lst = [1, 2, 3, 4]
print lst, "average and median are", calculate_avr_and_median(lst)
lst = [11, 9, 7, 5, 3]
print lst, "average and median are", calculate_avr_and_median(lst)