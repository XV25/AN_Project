from tkinter import *
from tkinter import filedialog
import tkinter.font as tkFont
import MIPS_X_Cache_interface
import asmtohex as assbly
import datawriter 
import time


class Interface(Frame):

    
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=700, height=700, **kwargs)
        fenetre.resizable(width=True,height=True)
        fenetre.title('Architecture Numérique')
        self.pack(fill=BOTH)
        self.nb_clic = 0
        
        self.posData = 1
        self.posAssembly = 3
        self.posISS = 5
        self.deb_ISS = 0
        self.fin_ISS = 0
        self.fichier_data_hex = ''
        self.fichier_programme_hex = ''
        
        #definition des polices et style d'ecriture
        self.BoutonFont = tkFont.Font( size=10, weight='bold')
        self.TitleFont = tkFont.Font( size=10,  weight='bold', underline = 1)
        self.italic = tkFont.Font( size=9, slant = 'italic')
        self.italic6 = tkFont.Font( size=6, slant = 'italic')
        
    
        #creation des boutons et des textes
        self.bouton_quitter = Button(self, text="Quitter", bg = "red", command=self.quit)
        self.bouton_quitter.grid(row=0,column=0)
        
        self.bouton_clear = Button(self, text="Réinitialiser",font = self.BoutonFont, bg = "red", command=self.clear)
        self.bouton_clear.grid(row=0,column=2)
        
        self.bouton_getfile_data_decimal = Button(self, text="Fichier Data Decimal",font = self.BoutonFont, command=self.getfiles_data)
        self.bouton_getfile_data_decimal.grid(row=self.posData,column=0)
        
        self.bouton_convert_data_dec2hex = Button(self, text="Convertir en Hexadecimal", font = self.BoutonFont, command=self.file_data_Dec2Hex)
        self.bouton_convert_data_dec2hex.grid(row=self.posData,column=3)
        
        self.bouton_startAssembly = Button(self, text="Assembly", font = self.BoutonFont, command=self.startAssembly)
        self.bouton_startAssembly.grid(row=self.posAssembly,column=3)
        
        self.bouton_getfiles_ass = Button(self, text="Fichier à compiler", font = self.BoutonFont, command=self.getfiles_ass)
        self.bouton_getfiles_ass.grid(row=self.posAssembly,column=0)
        
        self.bouton_getfiles_hex = Button(self, text=" 1 : Load Fichier Hexadecimal", font = self.BoutonFont, command=self.getFiles_hex)
        self.bouton_getfiles_hex.grid(row=self.posISS, column = 0)
        
        self.bouton_startISS = Button(self, text="Run", font = self.BoutonFont, command=self.startISS)
        self.bouton_startISS.grid(row=self.posISS,column=4)
        
        
        self.bouton_pasapas = Button(self, text="Pas à Pas", font = self.BoutonFont, command=self.pasapas)
        self.bouton_pasapas.grid(row=self.posISS,column=3)
        
        self.bouton_loadData = Button(self, text="2 : Load Fichier Data Hexadecimal", font = self.BoutonFont, command=self.loadData)
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
        
        
        #Pour reperer les lignes
        Label(self, text = '   0',font = self.italic6).grid(row = 0, column = 10)
        Label(self, text = '   1',font = self.italic6).grid(row = 1, column = 10)
        Label(self, text = '   2',font = self.italic6).grid(row = 2, column = 10)
        Label(self, text = '   3',font = self.italic6).grid(row = 3, column = 10)
        Label(self, text = '   4',font = self.italic6).grid(row = 4, column = 10)
        Label(self, text = '   5',font = self.italic6).grid(row = 5, column = 10)
        Label(self, text = '   6',font = self.italic6).grid(row = 6, column = 10)
        Label(self, text = '   7',font = self.italic6).grid(row = 7, column = 10)
        Label(self, text = '   8',font = self.italic6).grid(row = 8, column = 10)
        Label(self, text = '   9',font = self.italic6).grid(row = 9, column = 10)
        Label(self, text = '  10',font = self.italic6).grid(row = 10, column = 10) 
        Label(self, text = '  11',font = self.italic6).grid(row = 11, column = 10)
        Label(self, text = '  12',font = self.italic6).grid(row = 12, column = 10)
        Label(self, text = '  13',font = self.italic6).grid(row = 13, column = 10)
        Label(self, text = '  14',font = self.italic6).grid(row = 14, column = 10)
        
#        Label(self, text = '   ',font = self.italic6).grid(row = 0, column = 10)
#        Label(self, text = '   ',font = self.italic6).grid(row = 1, column = 10)
#        Label(self, text = '   ',font = self.italic6).grid(row = 2, column = 10)
#        Label(self, text = '   ',font = self.italic6).grid(row = 3, column = 10)
#        Label(self, text = '   ',font = self.italic6).grid(row = 4, column = 10)
#        Label(self, text = '   ',font = self.italic6).grid(row = 5, column = 10)
#        Label(self, text = '   ',font = self.italic6).grid(row = 6, column = 10)
#        Label(self, text = '   ',font = self.italic6).grid(row = 7, column = 10)
#        Label(self, text = '   ',font = self.italic6).grid(row = 8, column = 10)
#        Label(self, text = '   ',font = self.italic6).grid(row = 9, column = 10)
#        Label(self, text = '   ',font = self.italic6).grid(row = 10, column = 10) 
#        Label(self, text = '   ',font = self.italic6).grid(row = 11, column = 10)
#        Label(self, text = '   ',font = self.italic6).grid(row = 12, column = 10)
#        Label(self, text = '   ',font = self.italic6).grid(row = 13, column = 10)
#        Label(self, text = '   ',font = self.italic6).grid(row = 14, column = 10)

    def affichageMemoire(self,message):
        try : 
            self.affmemoire.destroy()
        except:
            pass
        self.affmemoire = Label(self, text= message)
        self.affmemoire.grid(row = self.posISS+3, column = 2)
    
    def affichageReg(self, message ):
        try:
            self.affReg.destroy()
        except:
            pass
        self.affReg = Label(self, text= str(message))
        self.affReg.grid(row = self.posISS + 3, column = 3)
        
    def affichageInstr(self,message):
        try:
            self.affInstr.destroy()
        except: 
            pass
        self.affInstr = Label(self, text = message)
        self.affInstr.grid(row = self.posISS + 3, column = 0)
        
    def affichageCache(self):
        posLigne  = 11
        posColonne = 2
        
        for i in range(4):
            txt = "                                                           "
            self.affCacheValid= Label(self, text= txt)
            self.affCacheValid.grid(row = posLigne, column = posColonne-1)
            self.affCacheTagbit = Label(self, text= txt)
            self.affCacheTagbit.grid(row = posLigne, column = posColonne)
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
        try :
            self.affPC.destroy()
        except : 
            pass
        self.affPC = Label(self, text = "pc = {}".format(self.simulation.pc))
        self.affPC.grid(row = self.posISS + 4, column = 3)
        
    def showStatus(self):
        try:
            self.affInstr.destroy()
        except: 
            pass
        self.simulation.get_information_temps()
        nombre_de_cycle = self.simulation.c_cycle
        temps_execution = self.simulation.t_dps_init
        txt = "Fin d'execution : \n Nombre de cycle : {} \n temps execution : {} s".format(nombre_de_cycle, temps_execution)
        self.affInstr = Label(self, text = txt)
        self.affInstr.grid(row = self.posISS + 3, column = 0)        
    
    def getfiles_data(self):
        try :
            self.path_getfiles_data.destroy()
        except :
            pass
        self.filename_data_decimal = filedialog.askopenfilename()
        self.path_getfiles_data = Label(self, text= self.filename_data_decimal, font = self.italic)
        self.path_getfiles_data.grid(row=self.posData +1, column=0)
        
   
    def getFiles_hex(self):
        try :
            self.path_getFiles_Hex.destroy()
        except :
            pass
        filename = filedialog.askopenfilename()
        self.fichier_programme_hex = filename
        self.path_getFiles_Hex = Label(self, text= filename, font = self.italic)
        self.path_getFiles_Hex.grid(row=self.posISS +1, column=0)
        self.fin_ISS = 0
        
    def getfiles_ass(self):
        try :
            self.path_getfiles_ass.destroy()
        except :
            pass
        self.filename_assembleur = filedialog.askopenfilename()
        self.path_getfiles_ass = Label(self, text= self.filename_assembleur, font = self.italic)
        self.path_getfiles_ass.grid(row=self.posAssembly +1, column=0)
        
    def loadData(self):
        try :
            self.path_loadData.destroy()
        except :
            pass
        filename = filedialog.askopenfilename()
        self.fichier_data_hex = filename
        
        self.path_loadData = Label(self, text= filename, font = self.italic)
        self.path_loadData.grid(row=self.posISS + 1, column=2)
        
    def file_data_Dec2Hex(self):
        try :
            self.path_file_data_Dec2Hex.destroy()
        except :
            pass
        try :
            self.path_loadData.destroy()
        except :
            pass
        inputFileName = self.filename_data_decimal
        outputFileName = self.filename_data_decimal[0:len(self.filename_data_decimal)-4]+"HEX.txt"
        self.fichier_data_hex = outputFileName
        
        strData = datawriter.load_dec(inputFileName)
        decData = datawriter.analyse_data(strData)
        datawriter.output_hex_data(decData,outputFileName,0x1)
        self.path_file_data_Dec2Hex = Label(self, text= outputFileName, font = self.italic)
        self.path_file_data_Dec2Hex.grid(row=self.posData + 1, column=3)
        self.path_loadData = Label(self, text= self.fichier_data_hex, font = self.italic)
        self.path_loadData.grid(row=self.posISS + 1, column=2)
        
        

    def startVM(self):
        self.simulation = MIPS_X_Cache_interface.VM(self.fichier_programme_hex)
        if self.fichier_data_hex != '':
            self.simulation.getdata(self.fichier_data_hex)


    def startAssembly(self):
        try :
            self.path_startAssembly.destroy()
        except : 
            pass
        try :
            self.path_getFiles_Hex.destroy()
        except : 
            pass
        
        inputFileName = self.filename_assembleur
        outputFileName = self.filename_assembleur[0:len(self.filename_assembleur)-4]+"HEX.txt"
    
        asmInstructions = assbly.load_ASM(inputFileName)
        numInstructions = assbly.analyze_instructions(asmInstructions)
        hexInstructions = assbly.compute_hex_instructions(numInstructions)
        assbly.output_hex_instructions(hexInstructions, outputFileName)
        
        self.fichier_programme_hex = outputFileName
        self.path_startAssembly = Label(self, text= outputFileName, font = self.italic)
        self.path_startAssembly.grid(row=self.posAssembly + 1, column=3)
                
        self.path_getFiles_Hex = Label(self, text= self.fichier_programme_hex, font = self.italic)
        self.path_getFiles_Hex.grid(row=self.posISS +1, column=0)
        self.fin_ISS = 0
        
    def pasapas(self):
        if self.fin_ISS == 0:
            if self.deb_ISS == 0:
                self.startVM()
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
                self.startVM()
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
            
    def clear(self):
        self.clearaffichage()
        self.clearExecution()
        self.clearCache()
        
        self.deb_ISS = 0
        self.fin_ISS = 0
        self.fichier_data_hex = ''
        self.fichier_programme_hex = ''
        try :
            self.simulation.RAZ()
        except :
            pass
        
        
    def clearaffichage(self):
        try :
            self.path_getfiles_data.destroy()
        except :
            pass
        try :
            self.path_file_data_Dec2Hex.destroy()
        except :
            pass
        try :
            self.path_loadData.destroy()
        except :
            pass
        try :
            self.path_getfiles_ass.destroy()
        except :
            pass
        try :
            self.path_getFiles_Hex.destroy()
        except :
            pass
        try :
            self.path_startAssembly.destroy()
        except : 
            pass
    
    def clearExecution(self):
        try:
            self.affInstr.destroy()
        except: 
            pass
        
        try :
            self.affPC.destroy()
        except : 
            pass
        
        try:
            self.affReg.destroy()
        except:
            pass
        
        try : 
            self.affmemoire.destroy()
        except:
            pass
    
    def clearCache(self):
        posLigne  = 11
        posColonne = 2
        
        for i in range(4):
            txt = "                                                           "
            self.affCacheValid= Label(self, text= txt)
            self.affCacheValid.grid(row = posLigne, column = posColonne-1)
            self.affCacheTagbit = Label(self, text= txt)
            self.affCacheTagbit.grid(row = posLigne, column = posColonne)
            self.affCacheBlock = Label(self, text= txt)
            self.affCacheBlock.grid(row = posLigne, column = posColonne+1)
            
            posLigne +=1
            
    
if __name__ == "__main__":
    fenetre = Tk()
    interface = Interface(fenetre)
    interface.mainloop()
    interface.destroy()
    fenetre.destroy()

