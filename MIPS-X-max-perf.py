#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 10:38:49 2019

@author: landaier
"""

import time
import signal


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
        self.n_mem = 1024
        self.regs = [0 for k in range(self.n_reg)]
        self.data = [None for k in range(self.n_mem)]
        self.getdata(self.data)

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
        
        #self.step_choice()
        self.running = 1
        self.deb_instr = time.time()
        
    def step_choice(self):
        """
        Permet de choisir si le programme doit fonctionner de façon continue ou 
        étape par étape.
        Il est possible de passer d'un mode étape par étape en un mode continu dans
        la suite du programme; 
        """
        chx = input("By step or continuous? [S for Step, anything else for Continuous]")
        if chx == 'S' or chx == 's':
            self.running = 2
        else: 
            self.running = 1

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
        lines = [line.rstrip('\n') for line in open(fileName)]

        lines = [line for line in lines if line != '']
        return lines
    
    def getdata(self,data):
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
        ensData = self.load_hex("hexdata.txt")
        Ldata = [prog.split() for prog in ensData]

        for k in Ldata:
            data[ int(k[0],16)] = int(k[1],16)


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
        ret = self.prog[self.pc]
        self.pc +=1
        return( ret)

    def decode(self,instr):
        """Fonctionnement : 
            Ex : pr 0x1064 (sur 16 bits)
            instrNum : prend à partir du 12e bit (en comptant de droite à gauche),
            décale de 12 à gauche.(je crois)
            reg1 : prend à partir du 8e bit (en comptant de droite à gauche),
            décale de 8 à gauche.(je crois)
            reg2 : Idem avec 4
            reg3 : Prend dernier
            imm : Prend les deux premiers octets en comptant de droite à gauche.
            
            Ex : si instr = 2210 : 
                instrNum = 2
                reg1 = 2
                reg2 = 1
                reg3 = 0
                imm = 10
                
                o : sur 16 bits 
                
            imm : indique si le o est un registre ou une valeur.
            1 => immediate, 0=> register
            """
        self.instrNum = ( (instr & 0xF8000000) >> 27 )
        val = self.instrNum
        if val!=0:
            if val<= 14:
              
                self.imm = ( (instr & 0x00200000) >> 21 )
                self.o = ( (instr & 0x001FFFE0) >> 5 ) #5
    
                self.reg1 = ( (instr & 0x07C00000) >> 22 )                 #0x7C0000
                self.reg2 = ( instr & 0x1F )
            elif val == 15:
                
                self.imm = ( (instr & 0x04000000) >> 26 )
                self.o = ( (instr & 0x03FFFFF0) >> 5 )    
                self.reg2 = ( instr & 0x1F )
            elif val == 16 or val == 17:
                self.reg1 = ( (instr & 0x07C00000) >> 22 ) 
                self.a = ( (instr & 0x003FFFFF) )
            elif val == 18:
                self.n = ( (instr & 0x07FFFFFF) ) 
                

#        self.instrNum = (instr & 0xF000) >> 12 
#        self.reg1 =  (instr & 0xF00) >> 8 
#        self.reg2 = (instr & 0xF0) >> 4 
#        self.reg3 =  instr & 0xF 
#        self.imm =  instr & 0xFF 
#        
        #print(self.instrNum,self.reg1, self.imm, self.o, self.reg2 )

    def evalu(self):
        
        if self.instrNum == 0:
            #print('Halt\n')
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
            self.slt()Tag,Index,Offset = 
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
        # 1 --> immediate; 0--> register
        if self.imm == 0:
            #print('add r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1] + self.regs[self.o]
        elif self.imm == 1:
            #print('add r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            #print(self.regs[self.reg1])
            self.regs[self.reg2] = self.regs[self.reg1] + self.o
    
    def sub(self):
        if self.imm == 0:
            #print('sub r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1] - self.regs[self.o]
        elif self.imm == 1:
            #print('sub r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1] - self.o        
    

    def mult(self):
        if self.imm == 0:
            #print('mult r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]*self.regs[self.o]
        elif self.imm == 1:
            #print('mult r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]*self.o                    
    
    def div(self):
        if self.imm == 0:
            #print('div r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]/self.regs[self.o]
        elif self.imm == 1:
            #print('div r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]/self.o                            

    def andd(self):
        if self.imm == 0:
            #print('and r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]& self.regs[self.o]
        elif self.imm == 1:
            #print('and r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]& self.o               
    
    def orr(self):
        if self.imm == 0:
            #print('or r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]|self.regs[self.o]
        elif self.imm == 1:
            #print('or r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]| self.o           
    
    def xor(self):
        if self.imm == 0:
            #print('xor r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]^self.regs[self.o]
        elif self.imm == 1:
           # print('xor r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]^self.o 
    
    def shl(self):
        if self.imm == 0:
          #  print('left r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]<<self.regs[self.o]
        elif self.imm == 1:
            #print('left r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]<<self.o       
    
    def shr(self):
       if self.imm == 0:
            #print('right r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]>>self.regs[self.o]
       elif self.imm == 1:
            #print('right r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]>>self.o     

    def slt(self):
       if self.imm == 0:
            #print('inf r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            
            self.regs[self.reg2] = int(self.regs[self.reg1]<self.regs[self.o])
       elif self.imm == 1:
            #print('inf r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = int(self.regs[self.reg1]<self.o)

    def sle(self):
       if self.imm == 0:
            #print('inf/eg r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = int(self.regs[self.reg1]<=self.regs[self.o])
       elif self.imm == 1:
            #print('inf/eg r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = int(self.regs[self.reg1]<=self.o)
    
    def seq(self):
       if self.imm == 0:
           # print('seq r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = int(self.regs[self.reg1]==self.regs[self.o])
       elif self.imm == 1:
           # print('seq r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = int(self.regs[self.reg1]==self.o)
    
    def load(self):
        # vérif si dépasse pas de mémoire.
       if self.imm == 0:
            #print('load r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            if self.data[self.regs[self.reg1] + self.regs[self.o] ] == None :
                print("Error : Nonetype at address %s in data"%(self.reg1 + self.regs[self.o] ))
                print("The program will continue without the loaded data\n")
            elif (self.regs[self.reg1] + self.regs[self.o]) >= self.n_mem:
                print("Error : out of memory boundaries")
                print("The program will continue without the loaded data\n")
            else:
                self.regs[self.reg2] = self.data[self.regs[self.reg1] + self.regs[self.o] ]
            #self.regs[self.reg2] = self.data[self.regs[self.reg1] + self.regs[self.o] ]
            
       elif self.imm == 1:
            #print('load r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            if self.data[self.regs[self.reg1] + self.o ] == None :
                print("Error : Nonetype at address %s in data"%(self.reg1 + self.o ))
                print("The program will continue without the loaded data\n")
            elif (self.regs[self.reg1] + self.o) >= self.n_mem:
                print("Error : out of memory boundaries")
                print("The program will continue without the loaded data\n")
            else : 
                self.regs[self.reg2] = self.data[self.regs[self.reg1]+self.o]
    
    def store(self):
       if self.imm == 0:
           # print('store r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            #self.data[self.reg1 + self.regs[self.o] ] = self.regs[self.reg2] 
            self.data[self.regs[self.reg1] + self.regs[self.o] ] = self.regs[self.reg2] 
       elif self.imm == 1:
            #print('store r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            #print(self.regs[self.reg1] + self.o )
            self.data[self.regs[self.reg1] + self.o ] = self.regs[self.reg2] 
            #self.showRegs()
            #time.sleep(1)
        #poss de storer données à fin de programme, dans autre fichier texte.
    
    def jmp(self):
       if self.imm == 0:
          #  print('jmp r%s r%s \n'%(self.reg2,self.o) )
            self.regs[self.reg2] = self.pc +1
            self.pc = self.regs[self.o] 
       elif self.imm == 1:
         #   print('jmp r%s #%s \n'%(self.reg2,self.o) )
            self.regs[self.reg2] = self.pc +1
            self.pc = self.o
    
    def braz(self):
        #print('braz r%s #%s \n'%(self.reg1,self.a) )
        if self.regs[self.reg1] == 0:
            self.pc = self.a
            
    def branz(self):
        #print('branz r%s #%s \n'%(self.reg1,self.a) )
        if self.regs[self.reg1] != 0:
            self.pc = self.a
            
    def scall(self):
        #print('scall #%s \n'%(self.n) )
        if self.n == 0:
            k = input("Enter a value")
            self.regs[1] = int(k)
        if self.n ==1:
            print("Content of R1 : ", self.regs[1])

    def showRegs(self):
        print('regs : ')

        print(self.regs)
        print('\n')
        if self.running == 2:
            wait = input("Press any touch to continue; press C to go to continuous mode.")
            if wait == 'C' or wait == 'c':
                self.running =1

    
    def run(self):
        while(self.running != 0):
            #self.showRegs()
            instr = self.fetch()

            self.decode(instr)
            self.evalu()
            self.regs[0] = 0
        self.t_fin = time.time()
        self.t_dps_deb = self.t_fin - self.t_init
        self.t_dps_init = self.t_fin - self.deb_instr
        
        print("Durée depuis l'initialisation de l'ISS : %f \n"%self.t_dps_deb)
        print("Durée depuis l'exécution du programme mis en entrée : %f \n"%self.t_dps_init)
        
Pg = VM('hexInstructions.txt')

#Pg.decode(0x8800022)
Pg.run()
print(Pg.regs[3])
print(Pg.c_cycle)

