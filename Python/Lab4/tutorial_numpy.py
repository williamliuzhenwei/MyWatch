#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 17:36:17 2020

@author: liuzhenwei
"""

import numpy as np

# Question 1
array1 = np.array([0,10,4,12])
#array1 = array1 - 20
# The output is a one dimensional array with elements [-20 -10 -16 -8]
# shape is (4,)


# Question 2
array2 = np.array([(0,10,4,12),(1,20,3,41)])
a = array2.reshape(4,2)
array2_new = np.zeros((2,2))
array2_new[0] = a[1]
array2_new[1] = a[2]
#print(array2_new)
# I reshaped array 2 to 4x2 and assign to a.
# Then I let array2_new first and second row to be the values of a's
# second and third row


# Question 3
array3 = []
array3 = np.hstack((np.vstack((array1, array1, array1, array1)), 
                        np.vstack((array1, array1, array1, array1))))
#print(array3)


# Question 4
array41 = np.arange(-3,16,6)
array42 = np.arange(-7, -20, -2)
#print(array42)


# Question 5
array5 = np.linspace(0, 100, 49, True)
#print(array5)
# I think the biggest difference is that using linspace we can 
# determine whether we want to include the stop value or not


# Question 6
array6 = np.zeros((3,4))
array6[0] = [12, 3, 1,2]
array6[:,1] = [3, 0, 2]
array6[2, :2] = [4, 2]
array6[2, 2:] = [3, 1]
array6[:,2] = [1, 1, 3]
array6[1,3] = 2
# print(array6[0])     
# print(array6[1,0])   
# print(array6[:,1])   
# print(array6[2, :2])
# print(array6[2, 2:]) 
# print(array6[:,2]) 
# print(array6[1,3]) 


# Question 7 
i = 0
c = []
string7 = "1,2,3,4"
b = np.fromstring(string7, dtype=int, sep=',')
c = b
array7 = np.zeros((100,4))
for i in range(99):
    #array7[i] = b
    i = i + 1
    array7 = np.vstack((c,b))
    c = array7
print(array7.size)
    


