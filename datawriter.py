# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 14:01:25 2019

@author: ehnla
"""

inputFileName = 'decdata.txt'
outputFileName = 'hexdata.txt'

def load_dec(fileName):
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
	# remove empty lines
    lines = [line for line in lines if line != '']
    return lines


def analyse_data(decData):
    """
    Supprime les commentaires présents sur les lignes du fichier, renvoie
    les données présents dans ce fichier sous forme d'une liste.
    
    Paramètres : 
    ------------
        decData : la liste contenant les lignes du fichier, sans traitement.
            
    Renvoie :
    ------------
        Ldata : list, contenant les données du fichier.
    """  
    decData = [instruction.split() for instruction in decData]
    Ldata = []
    #print(decData)
    for i in range(len(decData)) :
        j = 0
        L_vu = decData[i]
        while j< len(L_vu) and L_vu[j][0]!= '#':
            #print(L_vu[j])
            Ldata.append(int(L_vu[j]) )
            j +=1
            
    return(Ldata)

def output_hex_data(hexData, fileName,deb_add):
    """
    Crée le fichier hexadécimal à partir des données prises en entrée. Associe à
    chacune de ces données une adresse, qui est rajoutée dans le fichier hexadécimal :
    les adresses de ces données se suivent.
    
    Paramètres : 
    ------------
        hexData : liste contenant les données du fichier
        fileName : nom du fichier devant contenir les données hexadécimales
        deb_add : adresse de la 1e donnée. 
    
    Renvoie :
    ------------
        Rien.
    
    """
    adress = deb_add
    outputFile = open(fileName, 'w')
    for instr in hexData :
        outputFile.write(hex(adress) + ' ')
        outputFile.write(hex(instr) + '\n')
        adress +=1
    return(None)


strData = load_dec(inputFileName)
decData = analyse_data(strData)
output_hex_data(decData,outputFileName,0x1)
