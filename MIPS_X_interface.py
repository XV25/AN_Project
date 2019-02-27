#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 10:38:49 2019

@author: landaier
"""

import time
import signal
import sys


"""Registres """

class VM():
    """
    Classe servant à simuler une machine virtuelle.
    """
    def __init__(self,inputFile):               
        """
        Constructeur de la classe VM (= Virtual Machine).
        
        Paramètres : 
        -------------
            inputFile : nom du fichier contenant les instructions du programme,
            sous forme héxadécimale.
            
        Variables : 
        ------------
            t_init : temps notant le début de l'initialisation de la machine
            virtuelle.
            deb_instr : temps notant le début de l'initialisation du programme.
            prog : liste de listes de nombres, contenant l'ensemble des instructions
            à exécuter.
            n_reg : nombres de registres disponibles.
            n_mem : taille de la mémoire disponible.
            regs : registres
            data : liste de nombres contenant l'ensemble des données disponibles.
            pc : variable contenant l'adresse de l'instruction à exécuter.
            running : variable indiquant le fonctionnement de la machine virtuelle.
        """
        self.t_init = time.time()
        self.n_reg = 32
        self.n_mem = 32 #1024
        self.regs = [0 for k in range(self.n_reg)]
        self.data = [None for k in range(self.n_mem)]
        self.prog = self.getprog(inputFile)
        self.pc = 0

        self.instrNum = 0
        self.reg1 = 0
        self.reg2 = 0

        self.imm = 0
        self.o = 0
        self.a = 0
        self.n = 0
        self.c_cycle = 0
        
        self.running = 1
        
        self.instruction = ''
#        self.step_choice()
        
#        self.deb_instr = time.time()

        
    def step_choice(self):
        """
        Permet de choisir si le programme doit fonctionner de façon continue ou 
        étape par étape. Si le choix continu est choisi, l'utilisateur peut
        choisir le temps entre l'exécution de chaque instruction.
        Il est possible de passer d'un mode étape par étape en un mode continu dans
        la suite du programme; ce choix est disponible à chaque affichage du registre.
        Il est aussi possible de passer d'un mode continu via un mode étape par
        étape en appuyant sur Ctrl+C.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie :
        ------------
            Rien.
        
        
        """
        self.chx = input("By step or continuous? [S for Step, anything else for Continuous]")
        if self.chx == 'S' or self.chx == 's':
            self.running = 2
        else: 
            print('\n')
            print('Continuous mode activated. Press Ctrl+C if you want to change the mode. \n')

            signal.signal(signal.SIGINT, self.signal_handler)
            self.time_chx = input("How many time do you want between instructions?")
            self.time_chx = int(self.time_chx)
            self.running = 1

    def signal_handler(self, signal, frame):
        """
        Réagit lorsque l'utilisateur appuye sur Ctrl+C. Permet :
            -soit de passer d'un mode continu à un mode pas à pas.
            -soit de modifier le temps entre l'exécution de chaque instruction 
            dans le mode continu.
            -soit d'arrêter l'exécution du programme.        
        
        Paramètres : 
        -------------
            signal : le signal permettant l'exécution de cette fonction
            frame : variable désignant la fonction en question
            
        Renvoie :
        ------------
            Rien.
        
        """
        
        
        chx = input("Would you want to go to step-by-step mode? [Y/N] \n")
        if chx == 'Y' or chx == 'y':
            self.running =2
        else:
            chx = input("Would you either modify the time between instructions? [Y/N] \n")
            if chx == 'Y' or chx == 'y':
                self.time_chx = input("How many time do you want between instructions? \n")
                self.time_chx = int(self.time_chx)
            else:
                chx = input("Do you want to quit? [Y/N] \n")
                if chx == 'Y' or chx == 'y':
                    sys.exit(0)


    def load_hex(self,fileName):
        """
    Permet de charger un fichier .txt, et de récupérer ses données sous forme
    de liste.
    
    Paramètres : 
    ------------
        fileName : le nom du fichier à récupérer
        
    Renvoie :
    ------------
        lines : list, contenant les lignes du fichier non vides
        """
        	# place lines from file in array and remove trailing whitespaces
        lines = [line.rstrip('\n') for line in open(fileName)]
        	# remove empty linesimport sys
        lines = [line for line in lines if line != '']
        return lines
    
    def getdata(self,filename):
        """
        Récupère les données nécessaires à l'exécution du programme (contenues
        dans le fichier hexData.txt), les insère dans la mémoire de la machine
        virtuelle.
        
        Paramètres:
        ------------
            data : liste contenant l'ensemble des emplacements mémoire de la
            machine virtuelle
            
        Renvoie : 
        ----------
            Rien.
        
        """
        ensData = self.load_hex(filename)
        Ldata = [prog.split() for prog in ensData]

        for k in Ldata:
            self.data[ int(k[0],16)] = int(k[1],16)
        #print(ensData)
        print(self.data)

        #return(data)

    def getprog(self,fileName):
        """
        Récupère les données nécessaires à l'exécution du programme, les insère
        dans la liste Lins.
        
        Paramètres:
        ------------
            filename : nom du fichier contenant l'ensemble des instructions 
            du programme à exécuter, sous forme héxadécimale.
            
        Renvoie : 
        ----------
            Lins : liste contenant l'ensemble des instructions sous forme d'entiers
            décimaux.
        
        """
        ensProg = self.load_hex(fileName)
        
        Lprog = [prog.split() for prog in ensProg]
        Lins = []
        #print(Lprog)
        for prog in Lprog:
            Lins.append( int(prog[1],16) )
        #print(Lins)
        return(Lins)

    def fetch(self):
        """
        Passe d'une instruction à une autre dans la liste des instructions.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie :
        -----------
            ret : l'instruction à exécuter.
        """
        ret = self.prog[self.pc]
        self.pc +=1
        return( ret)

    def decode(self,instr):
        """
        
        Décode l'instruction héxadécimale donnée en entrée; passe du format héxadécimal
        à un ensemble de nombres dans une liste, différent selon le premier terme
        de la liste (désignant le type d'opération à exécuter).
        Les termes de l'objet machine virtuelle correspondant à l'instruction 
        donnée sont modifiés.
        
        Paramètres : 
        -------------
            instr : l'instruction héxadécimale à décoder.
            
        Renvoie :
        ------------
            Rien.
        
        """
        self.instrNum = ( (instr & 0xF8000000) >> 27 )
        val = self.instrNum
        if val!=0:
            if val<= 14:
                """Cas dans lequel l'instruction est une opération """
                self.imm = ( (instr & 0x00200000) >> 21 )
                self.o = ( (instr & 0x001FFFE0) >> 5 ) #5
    
                self.reg1 = ( (instr & 0x07C00000) >> 22 )                 #0x7C0000
                self.reg2 = ( instr & 0x1F )
            elif val == 15:
                """Cas dans lequel l'instruction est un jmp """
                self.imm = ( (instr & 0x04000000) >> 26 )
                self.o = ( (instr & 0x03FFFFF0) >> 5 )    
                self.reg2 = ( instr & 0x1F )
            elif val == 16 or val == 17:
                """ Cas dans lequel l'opération est un braz ou un branz """
                self.reg1 = ( (instr & 0x07C00000) >> 22 ) 
                self.a = ( (instr & 0x003FFFFF) )
            elif val == 18:
                """ Cas dans lequel l'opération est un scall """
                self.n = ( (instr & 0x07FFFFFF) ) 
                

    def evalu(self):
        """
        
        Exécute l'instruction correspondante à celle donnée en entrée.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.
        
        
        """
        
        if self.instrNum == 0:
            print('Halt\n')
            self.running = 0
            
        if self.instrNum == 1:
            self.add()
            self.c_cycle +=1
        
        if self.instrNum == 2:
            self.sub()
            self.c_cycle +=1
            
        if self.instrNum == 3:
            self.mult()
            self.c_cycle +=2

        if self.instrNum == 4:
            self.div()
            self.c_cycle +=2
            
        if self.instrNum == 5:
            self.annd()
            self.c_cycle +=1
            
        if self.instrNum == 6:
            self.orr()
            self.c_cycle +=1
        
        if self.instrNum == 7:
            self.xor()
            self.c_cycle +=1
        
        if self.instrNum == 8:
            self.shl()
            self.c_cycle +=1
        
        if self.instrNum == 9:
            self.shr()
            self.c_cycle +=1
        
        if self.instrNum == 10:
            self.slt()
            self.c_cycle +=1
        
        if self.instrNum == 11:
            self.sle()
            self.c_cycle +=1
        
        if self.instrNum == 12:
            self.seq()
            self.c_cycle +=1
        
        if self.instrNum == 13:
            self.load()
            self.c_cycle +=1
        
        if self.instrNum == 14:
            self.store()
            self.c_cycle +=1
        
        if self.instrNum == 15:
            self.jmp()
            self.c_cycle +=2
        
        if self.instrNum == 16:
            self.braz()
            self.c_cycle +=2
        
        if self.instrNum == 17:
            self.branz()
            self.c_cycle +=2
        
        if self.instrNum == 18:
            self.scall()
            self.c_cycle +=2

        
    def add(self):
        """
        
        Exécute l'opération d'addition, selon les instructions donnés en entrée.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        
        """
        if self.imm == 0:
            print('add r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'add r%s r%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1] + self.regs[self.o]
        elif self.imm == 1:
            print('add r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'add r%s #%s r%s\n'%(self.reg1,self.o,self.reg2)
            print(self.regs[self.reg1])
            self.regs[self.reg2] = self.regs[self.reg1] + self.o
    
    def sub(self):
        """
        
        Exécute l'opération de soustraction, selon les instructions donnés en entrée.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        
        """
        if self.imm == 0:
            print('sub r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'sub r%s r%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1] - self.regs[self.o]
        elif self.imm == 1:
            print('sub r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'sub r%s #%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1] - self.o        
    

    def mult(self):
        """
        
        Exécute l'opération de multiplication, selon les instructions donnés en entrée.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        
        """
        if self.imm == 0:
            print('mult r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'mult r%s r%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1]*self.regs[self.o]
        elif self.imm == 1:
            print('mult r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'mult r%s #%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1]*self.o                    
    
    def div(self):
        """
        
        Exécute l'opération de division, selon les instructions donnés en entrée.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        
        """
        if self.imm == 0:
            print('div r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'div r%s r%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1]/self.regs[self.o]
        elif self.imm == 1:
            print('div r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'div r%s #%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1]/self.o                            

    def andd(self):
        """
        
        Exécute l'opération "et", selon les instructions donnés en entrée.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        
        """
        if self.imm == 0:
            print('and r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'and r%s r%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1]& self.regs[self.o]
        elif self.imm == 1:
            print('and r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'and r%s #%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1]& self.o               
    
    def orr(self):
        """
        
        Exécute l'opération "ou inclusif", selon les instructions donnés en entrée.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        
        """
        if self.imm == 0:
            print('or r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'or r%s r%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1]|self.regs[self.o]
        elif self.imm == 1:
            print('or r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'or r%s #%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1]| self.o           
    
    def xor(self):
        """
        
        Exécute l'opération "ou exclusif", selon les instructions donnés en entrée.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        
        """
        if self.imm == 0:
            print('xor r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'xor r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) 
            self.regs[self.reg2] = self.regs[self.reg1]^self.regs[self.o]
        elif self.imm == 1:
            print('xor r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'xor r%s #%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1]^self.o 
    
    def shl(self):
        """
        Opération dans laquelle r2 reçoit r1 décalé à gauche de o bits.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        
        """
        if self.imm == 0:
            print('left r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'left r%s r%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1]<<self.regs[self.o]
        elif self.imm == 1:
            print('left r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.instruction = 'left r%s #%s r%s\n'%(self.reg1,self.o,self.reg2)
            self.regs[self.reg2] = self.regs[self.reg1]<<self.o       
    
    def shr(self):
        """
        Opération dans laquelle r2 reçoit r1 décalé à droite de o bits.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        
        """
        if self.imm == 0:
             print('right r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.instruction = 'right r%s r%s r%s\n'%(self.reg1,self.o,self.reg2)
             self.regs[self.reg2] = self.regs[self.reg1]>>self.regs[self.o]
        elif self.imm == 1:
             print('right r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.instruction = 'right r%s #%s r%s\n'%(self.reg1,self.o,self.reg2)
             self.regs[self.reg2] = self.regs[self.reg1]>>self.o     

    def slt(self):
        """
        
        Exécute l'opération inférieur entre r1 et o, selon les instructions donnés 
        en entrée. Stocke le résultat dans r2.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        
        """
        if self.imm == 0:
             print('inf r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.instruction = 'inf r%s r%s r%s\n'%(self.reg1,self.o,self.reg2)
             self.regs[self.reg2] = int(self.regs[self.reg1]<self.regs[self.o])
        elif self.imm == 1:
            #print('inf r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.regs[self.reg2] = int(self.regs[self.reg1]<self.o)

    def sle(self):
        """
        
        Exécute l'opération inférieur ou égal entre r1 et o, selon les instructions 
        donnés en entrée. Stocke le résultat dans r2.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        """
        if self.imm == 0:
             print('inf/eg r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.instruction = 'inf/eg r%s r%s r%s\n'%(self.reg1,self.o,self.reg2)
             self.regs[self.reg2] = int(self.regs[self.reg1]<=self.regs[self.o])
        elif self.imm == 1:
             print('inf/eg r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.instruction = 'inf/eg r%s #%s r%s\n'%(self.reg1,self.o,self.reg2)
             self.regs[self.reg2] = int(self.regs[self.reg1]<=self.o)
    
    def seq(self):
        """
        
        Exécute l'opération égalité entre r1 et o, selon les instructions 
        donnés en entrée. Stocke le résultat dans r2.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        """
        if self.imm == 0:
             print('seq r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.instruction = 'seq r%s r%s r%s\n'%(self.reg1,self.o,self.reg2)
             self.regs[self.reg2] = int(self.regs[self.reg1]==self.regs[self.o])
        elif self.imm == 1:
             print('seq r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.instruction = 'seq r%s #%s r%s\n'%(self.reg1,self.o,self.reg2)
             self.regs[self.reg2] = int(self.regs[self.reg1]==self.o)
    
    def load(self):
        """
        
        Exécute l'opération chargement : r2 reçoit le contenu de la mémoire
        stockée à une certaine adresse. Cette adresse correspond au contenu de r1 
        + o (soit la valeur de o, soit la valeur du registre o).
        Contrôle si cette adresse est correcte; si ce n'est pas le cas, le
        programme continue.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        """

        if self.imm == 0:
             print('load r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.instruction = 'load r%s r%s r%s\n'%(self.reg1,self.o,self.reg2)
             if self.data[self.regs[self.reg1] + self.regs[self.o] ] == None :
                 print("Error : Nonetype at address %s in data"%(self.reg1 + self.regs[self.o] ))
                 print("The program will continue without the loaded data\n")
             elif (self.regs[self.reg1] + self.regs[self.o]) >= self.n_mem:
                 print("Error : out of memory boundaries")
                 print("The program will continue without the loaded data\n")
             else:
                 self.regs[self.reg2] = self.data[self.regs[self.reg1] + self.regs[self.o] ]

            
        elif self.imm == 1:
             print('load r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.instruction = 'load r%s #%s r%s\n'%(self.reg1,self.o,self.reg2)
             if self.data[self.regs[self.reg1] + self.o ] == None :
                 print("Error : Nonetype at address %s in data"%(self.reg1 + self.o ))
                 print("The program will continue without the loaded data\n")
             elif (self.regs[self.reg1] + self.o) >= self.n_mem:
                 print("Error : out of memory boundaries")
                 print("The program will continue without the loaded data\n")
             else : 
                 self.regs[self.reg2] = self.data[self.regs[self.reg1]+self.o]
    
    def store(self):
        """
        
        Exécute l'opération sauvegarde : le contenu de r2 est sotckée dans la mémoire,
        à une certaine adresse. Cette adresse correspond au contenu de r1 + o 
        (soit la valeur de o, soit la valeur du registre o).
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        """
        if self.imm == 0:
             print('store r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.instruction = 'store r%s r%s r%s\n'%(self.reg1,self.o,self.reg2)

             self.data[self.regs[self.reg1] + self.regs[self.o] ] = self.regs[self.reg2] 
        elif self.imm == 1:
             print('store r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.instruction = 'store r%s #%s r%s\n'%(self.reg1,self.o,self.reg2)
             print(self.regs[self.reg1] + self.o )
             self.data[self.regs[self.reg1] + self.o ] = self.regs[self.reg2] 

    
    def jmp(self):
        """
        
        Exécute l'opération jump. Saute à l'instruction correspondant à l'adresse
        stockée dans le registre o, note l'adresse de l'instruction suivant
        l'instruction du jump dans un registre.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        """
        if self.imm == 0:
             print('jmp r%s r%s \n'%(self.reg2,self.o) )
             self.instruction = 'jmp r%s r%s \n'%(self.reg2,self.o)
             self.regs[self.reg2] = self.pc +1
             self.pc = self.regs[self.o] 
        elif self.imm == 1:
             print('jmp r%s #%s \n'%(self.reg2,self.o) )
             self.instruction = 'jmp r%s #%s \n'%(self.reg2,self.o)
             self.regs[self.reg2] = self.pc +1
             self.pc = self.o
    
    def braz(self):
        """
        
        Exécute l'opération braz. Si le contenu du registre donné dans l'instruction
        est nul, passe à l'instruction correspondant à l'addresse a.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        """
        print('braz r%s #%s \n'%(self.reg1,self.a) )
        self.instruction = 'braz r%s #%s \n'%(self.reg1,self.a) 
        if self.regs[self.reg1] == 0:
            self.pc = self.a
            
    def branz(self):
        """
        
        Exécute l'opération branz. Si le contenu du registre donné dans l'instruction
        est non nul, passe à l'instruction correspondant à l'addresse a.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.        
        """
        print('branz r%s #%s \n'%(self.reg1,self.a) )
        self.instruction = 'branz r%s #%s \n'%(self.reg1,self.a)
        if self.regs[self.reg1] != 0:
            self.pc = self.a
            
    def scall(self):
        """
        
        Exécute l'opération scall. 
        Si la valeur correspondant à scall est nulle, cette opération correspond
        à une entrée de valeur; celle-ci est stockée dans le registre 1.
        Si la valeur correspondant à scall vaut 1, cette opération correspond
        à un affichage de la valeur dans le registre 1.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.  
        
        """
        print('scall #%s \n'%(self.n) )
        self.instruction = 'scall #%s \n'%(self.n)
        if self.n == 0:
            k = input("Enter a value")
            self.regs[1] = int(k)
        if self.n ==1:
            print("Content of R1 : ", self.regs[1])

    def showRegs(self):
        """
        
        Affiche le contenu de l'ensemble des registres. 
        Peut également passer en mode continu selon la commande de l'utilisateur.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.  
        
        """
        print('regs : ')
        print(self.regs)
        print('\n')
        self.IHM.affichageReg(self.outTextRegs)
        if self.running == 2:
            wait = input("Press any touch to continue; press C to go to continuous mode.")
            if wait == 'C' or wait == 'c':
                self.running =1
           

    def outTextRegs(self):
        txt = ''
        j = 0
        for i in self.regs:
            ligne = "r{} = {}\n".format(j,i)
            txt = txt + ligne
            j+=1
        return txt
    def outTextMem(self):
        txt = ''
        j = 0
        for i in self.data:
            ligne = "m{}. {}\n".format(j,i)
            txt = txt + ligne
            j+=1
        return txt
        
        
    def unTour(self):
        instr = self.fetch()
        self.decode(instr)
        self.evalu()
        self.regs[0] = 0
        
        
        
    def run(self):
        """
        
        Procède au déroulement de l'exécution de l'ensemble des instructions 
        données en entrée.
        Remet à 0 le registre 0 à chaque étape.
        
        Paramètres : 
        -------------
            Aucun.
            
        Renvoie : 
        ------------
            Rien.  
        
        """
        while(self.running != 0):
            self.showRegs()
            t0 = time.time()
            while time.time()-t0 < self.time_chx :
                pass
            instr = self.fetch()

            self.decode(instr)
            self.evalu()
            self.regs[0] = 0
        self.t_fin = time.time()
        self.t_dps_deb = self.t_fin - self.t_init
        self.t_dps_init = self.t_fin - self.deb_instr
        
        print("Durée depuis l'initialisation de l'ISS : %f \n"%self.t_dps_deb)
        print("Durée depuis l'exécution du programme mis en entrée : %f \n"%self.t_dps_init)
        
if __name__ == "__main__" :
    Pg = VM('hexInstructions.txt')
#    Pg.outTextRegs()
#    Pg.run()
    print(Pg.c_cycle)

