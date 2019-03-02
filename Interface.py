from tkinter import *
from tkinter import filedialog
import MIPS_X_interface
import asmtohex as assbly
import time


class Interface(Frame):
    
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""
    
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=700, height=700, **kwargs)
        fenetre.resizable(width=False,height=False)
        fenetre.title('Assembleur et ISS')
        self.pack(fill=BOTH)
        self.nb_clic = 0
        
        self.posAssembly = 2
        self.posISS = 5
        
        #initialisation de la vm
#        self.simulation = MIPS_X_interface.VM("")
    
        #creation des boutons
        self.bouton_quitter = Button(self, text="Quitter", bg = "green", command=self.quit)
        self.bouton_quitter.grid(row=0,column=2)
        
        self.bouton_startAssembly = Button(self, text="Assembly", command=self.startAssembly)
        self.bouton_startAssembly.grid(row=self.posAssembly,column=3)
        
        self.bouton_getfiles_ass = Button(self, text="Fichier à compiler", command=self.getfiles_ass)
        self.bouton_getfiles_ass.grid(row=self.posAssembly,column=0)
        
        self.bouton_getfiles_hex = Button(self, text="Load Fichier Hexadecimal", command=self.getFiles_hex)
        self.bouton_getfiles_hex.grid(row=self.posISS, column = 0)
        
        self.bouton_startISS = Button(self, text="Run",command=self.startISS)
        self.bouton_startISS.grid(row=self.posISS,column=4)
        
        
        self.bouton_pasapas = Button(self, text="Pas à Pas", command=self.pasapas)
        self.bouton_pasapas.grid(row=self.posISS,column=3)
        
        self.bouton_loadData = Button(self, text="LoadData", command=self.loadData)
        self.bouton_loadData.grid(row=self.posISS,column=2)
        
        self.registre = Label(self, text= 'Registres')
        self.registre.grid(row = self.posISS+2, column = 3)
        self.instr = Label(self, text= 'Instructions')
        self.instr.grid(row = self.posISS+2, column = 0)
        self.memoire = Label(self, text= 'Memoire')
        self.memoire.grid(row = self.posISS+2, column = 2)
        
        Label(self, text = '  ').grid(row = 0, column = 6)
        Label(self, text = '  ').grid(row = self.posAssembly+1, column = 6)
        Label(self, text = '  ').grid(row = self.posISS+1 , column = 6)
        Label(self, text = '  ').grid(row = 1 , column = 6)
        
    def affichageMemoire(self,message):
        self.affmemoire = Label(self, text= message)
        self.affmemoire.grid(row = self.posISS+5, column = 2)
    
    def affichageReg(self, message ):
        self.affReg = Label(self, text= str(message))
        self.affReg.grid(row = self.posISS + 5, column = 3)
        
    def affichageInstr(self,message):
        print(message)
        self.affInstr = Label(self, text = message)
        self.affInstr.grid(row = self.posISS + 5, column = 0)
        
    def getFiles_hex(self):
        filename = filedialog.askopenfilename()
        self.simulation = MIPS_X_interface.VM(filename)
        path = Label(self, text= filename)
        path.grid(row=self.posISS +1, column=0)
        print (filename)
        
    def getfiles_ass(self):
        self.filename_assembleur = filedialog.askopenfilename()
        path = Label(self, text= self.filename_assembleur)
        path.grid(row=self.posAssembly +1, column=0)
        
    def loadData(self):
        filename = filedialog.askopenfilename()
        self.simulation.getdata(filename)
        
        self.affichageMemoire(self.simulation.outTextMem())
        path = Label(self, text= filename)
        path.grid(row=self.posISS + 1, column=2)

    def startISS(self):     
        while(self.simulation.running != 0):
            self.bouton_pause = Button(self, text="Pause",command=self.pauseISS)
            self.bouton_pause.grid(row=self.posISS,column=5)
            self.simulation.unTour()
            time.sleep(0.1)
            

        self.affichageReg(self.simulation.outTextRegs())

    
    def pauseISS(self):
        self.simulation.running = 0
        
    def pasapas(self):
        
    
        self.simulation.unTour()
        self.affichageReg(self.simulation.outTextRegs())
        self.affichageInstr(self.simulation.instruction)
        self.affichageMemoire(self.simulation.outTextMem())
        
    def startAssembly(self):
        inputFileName = self.filename_assembleur
        outputFileName = self.filename_assembleur[0:len(self.filename_assembleur)-4]+"HEX.txt"
    
        asmInstructions = assbly.load_ASM(inputFileName)
        numInstructions = assbly.analyze_instructions(asmInstructions)
        hexInstructions = assbly.compute_hex_instructions(numInstructions)
    
        assbly.output_hex_instructions(hexInstructions, outputFileName)
        path = Label(self, text= outputFileName)
        path.grid(row=self.posAssembly + 1, column=3)
        
if __name__ == "__main__":
    fenetre = Tk()
    interface = Interface(fenetre)
    interface.mainloop()
    interface.destroy()
    fenetre.destroy()