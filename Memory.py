# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:14:07 2019

@author: ehnla
"""

class Memory():
    def __init__(self,m):
        self.n_mem = m
        self.nbits_data = 4
        self.data = [None for k in range(self.n_mem)]
        #print(len(self.data))
        
    def write(self,addr,data):
        """
        Ecrit la donnée dans la mémoire
        """
        self.data[addr] = data
        
    def read(self,addr):
        """
        Lit la donnée à l'adresse considéré. Si cette donnée est un NoneType,
        ou si l'adresse est supérieure à la taille de la mémoire, renvoie un
        message d'erreur et aucune donnée.
        """
        if self.data[addr] == None :
            print("Error : Nonetype at address %s in data"%(addr))
            print("The program will continue without the loaded data\n")
        elif (self.data[addr]) >= self.n_mem:
            print("Error : out of memory boundaries")
            print("The program will continue without the loaded data\n")
        else :
            return(self.data[addr])

