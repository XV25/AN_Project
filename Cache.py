#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 11:25:33 2019

@author: landaier
"""

from math import *
import Memory as M

class Bloc():
    def __init__(self,valid,tag_bits,size=16):
        self.valid = valid
        self.tag_bits = tag_bits
        self.block = [None for k in range(size)]


class Cache():
    """
    S : nombre d'ensemble
    E : nombre de lignes par ensemble --> toujours égal à 1 car cache à 
    correspondance directe.
    B : nombre de blocs (pas la taille des blocs ici; grandeur non nécessaire
    sous Python.)
    m : nombre d'adresses physiques
        
    """
    def __init__(self,m):
        self.S = m//2
        self.E = 1
        self.B = 2
        self.m = m
        self.s = log2(self.S)
        self.b = log2(self.B)
        self.t = self.m - (self.s+self.b)
#        print(self.t)
        self.Mem = M.Memory(m)
        
        self.Cache = []
        for k in range(self.S):
            self.Cache += [Bloc(0,None,self.B)]

        
    def read(self,addr):
        """
        Lit la donnée indiquée par l'adresse dans le cache.
        Si cette donnée n'est pas présente (valid nul ou les tags ne
        correspondent pas), écrit cette donnée dans le cache.
        Sinon, renvoie directement la bonne donnée
        """
        t,s,b = self.ID(addr)
        C_ex = self.Cache[s]
        verif = 0
        if C_ex.valid == 0 or C_ex.tag_bits != t:
            verif = 1
            if b == 1:
                Dta2 = self.Mem.read(addr)
                Dta1 = self.Mem.read(addr-1)
                self.write(addr-1,Dta1)
                self.write(addr,Dta2)
            else:
                Dta1 = self.Mem.read(addr)
                Dta2 = self.Mem.read(addr+1)
                self.write(addr,Dta1)
                self.write(addr+1,Dta2)
        return(C_ex.block[b],verif)
            
    def write(self,addr,data):
        """
        Ecrit la donnée dans le cache, suivant l'adresse entrée.
        """
        t,s,b = self.ID(addr)
        C_ex = self.Cache[s]
        C_ex.valid = 1
        C_ex.tag_bits = t
        C_ex.block[b] = data
        
    def write_through(self,addr,data):
        """
        Ecrit la donnée dans la mémoire, suivant l'adresse entrée.
        Si la donnée remplacée est également présente dans le cache (et que
        l'ensemble considéré a bien déjà été utilisé une fois), modifie également
        le cache pour mettre la nouvelle donnée à la place de l'ancienne.
        """
        self.Mem.write(addr,data)
        t,s,b = self.ID(addr)
        C_ex = self.Cache[s]
        verif = 0
        if C_ex.valid != 0 and C_ex.tag_bits == t:
            verif = 1
            self.write(addr,data)
        return(verif)

        

    def ID(self,addr):
        """
        Renvoie le tag, l'ensemble, et le b offset associé à l'adresse entrée.        
        """
        S = self.S
        t = int( addr > 2**(S-1) )
        s = (addr//2)%S
        b = addr%2
        return(t,s,b)
        
