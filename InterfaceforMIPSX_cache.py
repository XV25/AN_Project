from tkinter import *
from tkinter import filedialog
import tkinter.font as tkFont
import MIPS_X_Cache_interface
import asmtohex as assbly
import time


class Interface(Frame):

    
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=700, height=700, **kwargs)
        fenetre.resizable(width=False,height=False)
        fenetre.title('Architecture Numerique')
        self.pack(fill=BOTH)
        self.nb_clic = 0
        
        self.posAssembly = 2
        self.posISS = 5
        
        self.BoutonFont = tkFont.Font( size=10, weight='bold')
        self.TitleFont = tkFont.Font( size=10,  weight='bold', underline = 1)
        self.italic = tkFont.Font( size=9, slant = 'italic')
        self.italic6 = tkFont.Font( size=6, slant = 'italic')
        
        #initialisation de la vm
#        self.simulation = MIPS_X_Cache_interface.VM("")
    
        #creation des boutons
        self.bouton_quitter = Button(self, text="Quitter", bg = "red", command=self.quit)
        self.bouton_quitter.grid(row=0,column=2)
        
        self.bouton_startAssembly = Button(self, text="Assembly", font = self.BoutonFont, command=self.startAssembly)
        self.bouton_startAssembly.grid(row=self.posAssembly,column=3)
        
        self.bouton_getfiles_ass = Button(self, text="Fichier à compiler", font = self.BoutonFont, command=self.getfiles_ass)
        self.bouton_getfiles_ass.grid(row=self.posAssembly,column=0)
        
        self.bouton_getfiles_hex = Button(self, text="Load Fichier Hexadecimal", font = self.BoutonFont, command=self.getFiles_hex)
        self.bouton_getfiles_hex.grid(row=self.posISS, column = 0)
        
        self.bouton_startISS = Button(self, text="Run", font = self.BoutonFont, command=self.startISS)
        self.bouton_startISS.grid(row=self.posISS,column=4)
        
        
        self.bouton_pasapas = Button(self, text="Pas à Pas", font = self.BoutonFont, command=self.pasapas)
        self.bouton_pasapas.grid(row=self.posISS,column=3)
        
        self.bouton_loadData = Button(self, text="Load Fichier Data Hexadecimal", font = self.BoutonFont, command=self.loadData)
        self.bouton_loadData.grid(row=self.posISS,column=2)
        
        self.registre = Label(self, text= 'Registres', font = self.TitleFont)
        self.registre.grid(row = self.posISS+2, column = 3)
        self.instr = Label(self, text= 'Instructions',font = self.TitleFont)
        self.instr.grid(row = self.posISS+2, column = 0)
        self.memoire = Label(self, text= 'Memoire avant le cache',font = self.TitleFont)
        self.memoire.grid(row = self.posISS+2, column = 2)
        self.labelCache = Label(self, text= 'Cache :',font = self.TitleFont)
        self.labelCache.grid(row = 11, column = 0)
        self.labelCacheValid = Label(self, text= 'Valid',font = self.TitleFont)
        self.labelCacheValid.grid(row = 10, column = 1)
        self.labelCacheTagBit = Label(self, text= 'Tag bit',font = self.TitleFont)
        self.labelCacheTagBit.grid(row = 10, column = 2)
        self.labelCacheBlock = Label(self, text= 'Block',font = self.TitleFont)
        self.labelCacheBlock.grid(row = 10, column = 3)
        
        self.deb_ISS = 0
        self.fin_ISS = 0
        #Pour reperer les lignes
#        Label(self, text = '   0',font = self.italic6).grid(row = 0, column = 10)
#        Label(self, text = '   1',font = self.italic6).grid(row = 1, column = 10)
#        Label(self, text = '   2',font = self.italic6).grid(row = 2, column = 10)
#        Label(self, text = '   3',font = self.italic6).grid(row = 3, column = 10)
#        Label(self, text = '   4',font = self.italic6).grid(row = 4, column = 10)
#        Label(self, text = '   5',font = self.italic6).grid(row = 5, column = 10)
#        Label(self, text = '   6',font = self.italic6).grid(row = 6, column = 10)
#        Label(self, text = '   7',font = self.italic6).grid(row = 7, column = 10)
#        Label(self, text = '   8',font = self.italic6).grid(row = 8, column = 10)
#        Label(self, text = '   9',font = self.italic6).grid(row = 9, column = 10)
#        Label(self, text = '  10',font = self.italic6).grid(row = 10, column = 10) 
#        Label(self, text = '  11',font = self.italic6).grid(row = 11, column = 10)
#        Label(self, text = '  12',font = self.italic6).grid(row = 12, column = 10)
#        Label(self, text = '  13',font = self.italic6).grid(row = 13, column = 10)
#        Label(self, text = '  14',font = self.italic6).grid(row = 14, column = 10)

    def affichageMemoire(self,message):
        self.affmemoire = Label(self, text= message)
        self.affmemoire.grid(row = self.posISS+3, column = 2)
    
    def affichageReg(self, message ):
        self.affReg = Label(self, text= str(message))
        self.affReg.grid(row = self.posISS + 3, column = 3)
        
    def affichageInstr(self,message):
        self.affInstr = Label(self, text = message)
        self.affInstr.grid(row = self.posISS + 3, column = 0)
        
    def affichageCache(self):
        posLigne  = 11
        posColonne = 2
        
        for i in range(4):
            txt = "                                                           "
            self.affCache = Label(self, text= txt)
            self.affCache.grid(row = posLigne, column = posColonne)
            self.affCacheBlock = Label(self, text= txt)
            self.affCacheBlock.grid(row = posLigne, column = posColonne+1)
            
            posLigne +=1
        
        posLigne  = 11
        for i in self.simulation.Cach.Cache : #on a acces à la ligne de bloc
            txt = "{}".format(i.valid, i.tag_bits)
            self.affCacheValid = Label(self, text= txt)
            self.affCacheValid.grid(row = posLigne, column = posColonne-1)
            
            txt = "{}".format(i.tag_bits)
            self.affCacheTagbit = Label(self, text= txt)
            self.affCacheTagbit.grid(row = posLigne, column = posColonne)
            
            txt = '{}'.format(i.block)
            self.affCacheBlock = Label(self, text= txt)
            self.affCacheBlock.grid(row = posLigne, column = posColonne+1)
            posLigne +=1
          
            
    def affichageProgrammeCounter(self):
        self.affPC = Label(self, text = "pc = {}".format(self.simulation.pc))
        self.affPC.grid(row = self.posISS + 4, column = 3)
        
    def showStatus(self):
        self.simulation.get_information_temps()
        nombre_de_cycle = self.simulation.c_cycle
        temps_execution = self.simulation.t_dps_init
        txt = "Fin d'execution : \n Nombre de cycle : {} \n temps execution : {} s".format(nombre_de_cycle, temps_execution)
        self.status = Label(self, text = txt)
        self.status.grid(row = self.posISS + 3, column = 0)        
    
    def getFiles_hex(self):
        filename = filedialog.askopenfilename()
        self.simulation = MIPS_X_Cache_interface.VM(filename)
        self.path = Label(self, text= filename, font = self.italic)
        self.path.grid(row=self.posISS +1, column=0)
        print (filename)
        self.fin_ISS = 0
        
    def getfiles_ass(self):
        self.filename_assembleur = filedialog.askopenfilename()
        self.path = Label(self, text= self.filename_assembleur, font = self.italic)
        self.path.grid(row=self.posAssembly +1, column=0)
        
    def loadData(self):
        filename = filedialog.askopenfilename()
        self.simulation.getdata(filename)
        
        self.affichageMemoire(self.simulation.outTextMem())
        path = Label(self, text= filename, font = self.italic)
        path.grid(row=self.posISS + 1, column=2)

    def startAssembly(self):
        inputFileName = self.filename_assembleur
        outputFileName = self.filename_assembleur[0:len(self.filename_assembleur)-4]+"HEX.txt"
    
        asmInstructions = assbly.load_ASM(inputFileName)
        numInstructions = assbly.analyze_instructions(asmInstructions)
        hexInstructions = assbly.compute_hex_instructions(numInstructions)
    
        assbly.output_hex_instructions(hexInstructions, outputFileName)
        path = Label(self, text= outputFileName, font = self.italic)
        path.grid(row=self.posAssembly + 1, column=3)
        self.simulation = MIPS_X_Cache_interface.VM(outputFileName)
        path = Label(self, text= outputFileName, font = self.italic)
        path.grid(row=self.posISS +1, column=0)
        self.fin_ISS = 0
        
    def pasapas(self):
        if self.fin_ISS == 0:
            if self.deb_ISS == 0:
                self.simulation.deb_instr = time.time()
            self.deb_ISS = 1
            
            self.simulation.unTour()
            self.affichageReg(self.simulation.outTextRegs())
            self.affichageInstr(self.simulation.instruction)
            self.affichageMemoire(self.simulation.outTextMem())
            self.affichageProgrammeCounter()
            self.affichageCache()
            if self.simulation.running == 0:
                self.showStatus()
                self.fin_ISS = 1
    
    def startISS(self): 
        if self.fin_ISS == 0:
            if self.deb_ISS == 0:
                self.simulation.deb_instr = time.time()
            self.deb_ISS = 1
            
            while(self.simulation.running != 0):
                self.simulation.unTour()
            self.fin_ISS = 1
            self.affichageReg(self.simulation.outTextRegs())
            self.affichageInstr(self.simulation.instruction)
            self.affichageMemoire(self.simulation.outTextMem())
            self.affichageProgrammeCounter()
            self.affichageCache()
            self.showStatus()
            
        
        
    
        
if __name__ == "__main__":
    fenetre = Tk()
    interface = Interface(fenetre)
    interface.mainloop()
    interface.destroy()
    fenetre.destroy()# -*- coding: utf-8 -*-

