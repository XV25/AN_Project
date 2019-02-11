#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 10:38:49 2019

@author: landaier
"""

"""Registres """

class VM():
    def __init__(self):       

        self.n_reg = 4
        self.regs = ['0' for k in range(self.n_reg)]

        """ Programme à exécuter """

        self.prog = [0x1064,0x11C8,0x2201,0x0000]

        """ Variables """

        self.pc = 0

        self.instrNum = 0
        self.reg1 = 0
        self.reg2 = 0
        self.reg3 = 0
        self.imm = 0

        self.running = 1
        """ Fonctions """

    def fetch(self):
        ret = self.prog[self.pc]
        self.pc +=1
        return( ret)

    def decode(self,instr):
        """Fonctionnement : 
            Ex : pr 0x1064
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
            """
        self.instrNum = hex((instr & 0xF000) >> 12 )
        self.reg1 = hex( (instr & 0xF00) >> 8 )
        self.reg2 = hex( (instr & 0xF0) >> 4 )
        self.reg3 = hex( instr & 0xF )
        self.imm = hex( instr & 0xFF )

#        self.instrNum = (instr & 0xF000) >> 12 
#        self.reg1 =  (instr & 0xF00) >> 8 
#        self.reg2 = (instr & 0xF0) >> 4 
#        self.reg3 =  instr & 0xF 
#        self.imm =  instr & 0xFF 
#        
        #print(self.instrNum,self.reg1, self.reg2, self.reg3, self.imm )

    def evalu(self):
        I_instrNum = int(self.instrNum,16)
        I_reg1= int(self.reg1,16)
        I_reg2 = int(self.reg2,16)
        I_reg3 = int(self.reg3,16)
        I_imm = int(self.imm,16)
        
        if I_instrNum == 0:
            print('Halt\n')
            self.running = 0
            
        if I_instrNum == 1:
            print('loadi r%s #%s\n'%(I_reg1,self.imm) )
            self.regs[I_reg1] = self.imm
    
        if I_instrNum == 2:
            print('add r%s r%s r%s\n'%(I_reg1,I_reg2,I_reg3) )
            self.regs[I_reg1] = hex( int(self.regs[I_reg2],16) + int(self.regs[I_reg3],16) )
    
    def showRegs(self):
        print('regs : ')
        for i in range(self.n_reg):
            print(self.regs[i])
        print('\n')
           

    
    def run(self):
        while(self.running == 1):
            self.showRegs()
            instr = self.fetch()

            self.decode(instr)
            self.evalu()
        
Pg = VM()
Pg.run()

