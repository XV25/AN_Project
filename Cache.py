#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 11:25:33 2019

@author: landaier
"""

from math import *

class Cache():
    def __init__(self,m):
        self.S = 4
        self.E = 1
        self.B = 2
        self.m = m
        self.s = log(S)
        self.b = log(B)
        self.t = m - (s+b)
        
    def read(self,addr):
        ###