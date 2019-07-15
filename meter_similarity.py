# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 09:26:19 2018
@author: EREN
"""
hece_matrix = [[0 for i in range(2827)] for j in range(2827)]
aruz_matrix = [[0 for i in range(2827)] for j in range(2827)]
sim_matrix = [[0 for i in range(2827)] for j in range(2827)]

file1 = open("olcu_sim_son.txt","r")
lines = file1.readlines()
for i in range(2827):
    words = lines[i].split()
    for j in range(2827):
        hece_matrix[i][j] = words[j]
        
file2 = open("aruz_sim_son.txt","r")
lines = file2.readlines()
for i in range(2827):
    words = lines[i].split()
    for j in range(2827):
        aruz_matrix[i][j] = words[j]
        
        
for i in range(2827):
    for j in range(2827):
        if (1-(1-float(hece_matrix[i][j]) + (1-float(aruz_matrix[i][j]))))>0:
            sim_matrix[i][j] =  (1-(1-float(hece_matrix[i][j]) + (1-float(aruz_matrix[i][j]))))
        else:
            sim_matrix[i][j] = 0
                      
file = open("olcu_sim_final.txt","w")  
for i in range(0,2827):
    print(i,"matrix")
    for j in range(0,2827):
        file.write(str(sim_matrix[i][j]) + " ")        
    file.write("\n")
file.close()                 
