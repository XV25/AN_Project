# -*- coding: utf-8 -*-
import Interface as fen
import MIPS_X 
import asmtohex as assembly
import Tkinter as tk

fenetre = tk.Tk()
interface = fen.Interface(fenetre)


interface.mainloop()
interface.destroy()
fenetre.destroy()
