#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 10:38:49 2019

@author: landaier
"""

import time
import signal
import numpy as np
import Cache as C

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
        self.n_mem = 32
        self.regs = [0 for k in range(self.n_reg)]
        self.Cach = C.Cache(self.n_mem)
        self.getdata(self.Cach)
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
        
        A noter que dans ce mode (performances maximales), ce choix est désactivé :
        le mode continu est choisi par défaut, et ne peut être modifié.
        
        Paramètres : 
        -------------
            Aucun
            
        Renvoie :
        ------------
            Rien.
        
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
    
    def getdata(self,Cach):
        """
        Récupère les données nécessaires à l'exécution du programme (contenues
        dans le fichier hexData.txt), les insère dans la mémoire de la machine
        virtuelle.
        
        Paramètres:
        ------------
            Cach : Objet Cache
            
        Renvoie : 
        ----------
            Rien.
        
        """
        ensData = self.load_hex("hexdata.txt")
        Ldata = [prog.split() for prog in ensData]

        for k in Ldata:
            Cach.Mem.write(int(k[0],16),int(k[1],16) )
        

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
                

        
        #print(self.instrNum,self.reg1, self.imm, self.o, self.reg2 )

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

        if self.instrNum == 14:
            self.store()

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
            #print('add r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1] + self.regs[self.o]
        elif self.imm == 1:
            #print('add r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
            #print(self.regs[self.reg1])
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
            #print('sub r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1] - self.regs[self.o]
        elif self.imm == 1:
            #print('sub r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
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
            #print('mult r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]*self.regs[self.o]
        elif self.imm == 1:
            #print('mult r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
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
            #print('div r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]/self.regs[self.o]
        elif self.imm == 1:
            #print('div r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
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
            #print('and r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]& self.regs[self.o]
        elif self.imm == 1:
            #print('and r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
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
            #print('or r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]|self.regs[self.o]
        elif self.imm == 1:
            #print('or r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
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
            #print('xor r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]^self.regs[self.o]
        elif self.imm == 1:
           # print('xor r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
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
          #  print('left r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            self.regs[self.reg2] = self.regs[self.reg1]<<self.regs[self.o]
        elif self.imm == 1:
            #print('left r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
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
            #print('right r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.regs[self.reg2] = self.regs[self.reg1]>>self.regs[self.o]
        elif self.imm == 1:
            #print('right r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
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
            #print('inf r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
            
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
            #print('inf/eg r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.regs[self.reg2] = int(self.regs[self.reg1]<=self.regs[self.o])
        elif self.imm == 1:
            #print('inf/eg r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
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
           # print('seq r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.regs[self.reg2] = int(self.regs[self.reg1]==self.regs[self.o])
        elif self.imm == 1:
           # print('seq r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
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
#             print('load r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
             self.regs[self.reg2],verif = self.get_data(self.regs[self.reg1] + self.regs[self.o])

            
        elif self.imm == 1:
#             print('load r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
#             print(self.regs[self.reg1]+self.o)
             self.regs[self.reg2],verif = self.get_data(self.regs[self.reg1]+self.o)
            
        self.c_cycle += 1 + verif*20
    
    def get_data(self,addr):
        """
        Récupère la donnée dans le cache, à l'adresse considérée.
        
        Paramètres : 
        --------------
            addr : adresse considérée.
            
        Renvoie :
        --------------
            Dta : la donnée à l'adresse considérée.
            
        """
        Dta = self.Cach.read(addr)
        return(Dta)

    
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
#             print('store r%s r%s r%s\n'%(self.reg1,self.o,self.reg2) )
             verif = self.Cach.write_through(self.regs[self.reg1] + self.regs[self.o], self.regs[self.reg2] )
        elif self.imm == 1:
#             print('store r%s #%s r%s\n'%(self.reg1,self.o,self.reg2) )
#             print(self.regs[self.reg1] + self.o )
             verif = self.Cach.write_through(self.regs[self.reg1] + self.o , self.regs[self.reg2] )
        self.c_cycle += 1 + verif*10
    
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
          #  print('jmp r%s r%s \n'%(self.reg2,self.o) )
             self.regs[self.reg2] = self.pc +1
             self.pc = self.regs[self.o] 
        elif self.imm == 1:
         #   print('jmp r%s #%s \n'%(self.reg2,self.o) )
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
        #print('braz r%s #%s \n'%(self.reg1,self.a) )
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
        #print('branz r%s #%s \n'%(self.reg1,self.a) )
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
        #print('scall #%s \n'%(self.n) )
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
        if self.running == 2:
            wait = input("Press any touch to continue; press C to go to continuous mode.")
            if wait == 'C' or wait == 'c':
                self.running =1

    
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
        return(self.t_dps_init)


def moy_perf(N):
    """
    Evalue la performance de l'ISS : le nombre moyen de cycles par seconde,
    et le nombre maximal de cycles par seconde.

        Paramètres : 
        -------------
            N : le nombre de tests voulant être effectué
            
        Renvoie : 
        ------------
            np.mean(L) : le nombre moyen de cycles par seconde
            np.max(L) : le nombre maximal de cycles par seconde
    """
    L  = []
    for k in range(N):
        Pg = VM('hexInstructions.txt')
        tps = Pg.run()
        Nc = Pg.c_cycle
        L.append(Nc/tps)
    print(Pg.regs)
    print(Pg.Cach.Mem.data[0:32])
    return(np.mean(L), np.max(L))
    

print(moy_perf(10000))
#
#Pg.run()
#print(Pg.regs[3])
#print(Pg.c_cycle)
#

