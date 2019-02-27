# Translator: ASM instructions to hex


OP_CODES = {
	'stop': 0, 'add': 1, 'sub': 2, 'mult': 3, 'div': 4, 'and': 5, 'or': 6,
	'xor': 7, 'shl': 8, 'shr': 9, 'slt': 10, 'sle': 11, 'seq': 12, 'load': 13,
	'store': 14, 'jmp': 15, 'braz': 16, 'branz': 17, 'scall': 18
}


def load_ASM(fileName):
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
    #Supprime les lignes vides
    lines = [line for line in lines if line != '']
    return lines


def check_L(ListInstr):
    """
    Parcourt l'ensemble de la liste de données en entrée; chaque élément
    de cette liste correspond à une ligne du fichier d'instruction. 
    Dès qu'une de ces lignes contient une référence à une boucle (via la présence
    d'un L_...), cette boucle est enregistré dans un dictionnaire, et associée à 
    une adresse. 
    
    Paramètres : 
    ------------
        ListInstr : liste contenant l'ensemble des instructions assembleur.
    
    Renvoie :
    -----------
        ListInstr : liste contenant l'ensemble des instructions assembleur. Les 
        références aux L_... sont supprimés (elles ne sont plus nécessaires,
        puisqu'elles sont associées à une adresse dans le dictionnaire).
        D_Loop : dictionnaire associant chaque boucle à une adresse.
    """
    D_Loop = {}
    for k in range(len(ListInstr)):
        asmInstr = ListInstr[k]
        if asmInstr[0][0] == 'L':
            D_Loop[asmInstr[0][:-1]] = k
            #print(ListInstr[k])
            ListInstr[k] = ListInstr[k][1:]
    #print(ListInstr)
    return(ListInstr,D_Loop)


def find_L(D_L,L):
    """
    Renvoie l'adresse d'une boucle donnée en entrée.
    
    Paramètres : 
    ------------
        D_L : dictionnaire associant à chaque boucle du programme une adresse
        L : boucle dont on recherche l'adresse
    
    Renvoie :
    -----------
        D_L[c] : l'adresse associée à la boucle donnée en entrée
    
    """
    for c in D_L:
        if c == L:
            return(D_L[c])

    
def analyze_instructions(asmInstructions):
    """
    Transforme la suite d'instructions en code assembleur en liste de nombres.
    
    Paramètres : 
    ------------
        asmInstructions : la liste contenant toutes les instructions
        en code assembleur.
        
    Renvoie :
    -----------
        numInstructions : la liste contenant toutes les instructions sous forme 
        de suite de nombres.
    
    """
    asmInstructions = [instruction.split() for instruction in asmInstructions]
    numInstructions = []
    
    asmInstructions,D_L = check_L(asmInstructions)

    for i in range(len( asmInstructions)) :
        asmInstr = asmInstructions[i]
        numInstr = []

        """Associe un code à chaque instruction """
        numInstr.append(OP_CODES[asmInstr[0]])

        """Si l'instruction est de taille > 1, cela veut dire qu'elle ne correspond
        pas à une instruction stop : il faut donc la traiter."""
        if len(asmInstr) >1:
            lisInstr = asmInstr[1].split(',')
            
            """ Cas où l'instruction entrée est un jmp(o,r): 
                la suite de nombres codée sera alors : 
                code du jmp; valeur indiquant si o est une valeur ou un registre;
                adresse de saut o, r (registre d'enregistrement de l'adresse suivant le jmp)
                
                """
            if numInstr[0] ==15: 
                for k in range(len(lisInstr)):
                    if lisInstr[k][0] == 'L':
                        lisInstr[k] = find_L(D_L,lisInstr[k])
                        numInstr.append(1)
                        numInstr.append(lisInstr[k])
                    elif lisInstr[k][0] == 'r' :
                        numInstr.append(int(lisInstr[k][1:]))
                    else :
                        numInstr.append(0)
                        numInstr.append(lisInstr[k])
            elif (numInstr[0] ==16 or  numInstr[0] ==17):
                """ Cas où l'instruction entrée est un braz(r,a) (ou branz(r,a) ).
                    La suite de nombres codée sera alors : 
                    code de l'opération; registre dans lequel la vérification
                    du saut doit être fait; adresse à laquelle le saut doit être
                    fait. """
                for k in range(len(lisInstr)):
                    if lisInstr[k][0] == 'L':
                        lisInstr[k] = find_L(D_L,lisInstr[k])
                        numInstr.append(lisInstr[k])
                    elif lisInstr[k][0] == 'r' :
             #           print(lisInstr[k][0])
                        numInstr.append(int(lisInstr[k][1:]))
              #      print(numInstr)

            elif numInstr[0] == 18:
                """ 
                Cas où l'instruction entrée est un scall(n). La suite de nombres
                codée sera alors : code du scall; valeur de n.
                """
                numInstr.append(int(lisInstr[0]))
            else:
                """
                Cas où l'instruction entrée est une opération classique (ex : 
                add(r1,o,r2) ). 
                La suite de nombres codée sera alors : 
                code de l'opération, registre 1 (contenant le premier terme de
                l'opération), valeur indiquant si o désigne un registre ou une
                valeur, o (second terme de l'opération), registre 2 (devant 
                enregistrer le résultat de l'opération).
                
                """
                numInstr.append(int(lisInstr[0][1:]))
    #            print(numInstr)
    #            print(lisInstr)
    #            print(lisInstr[1][0])
                if lisInstr[1][0] == 'r':
                    numInstr.append(0)
                    numInstr.append(int(lisInstr[1][1:]))
                else:
                    numInstr.append(1)
                    numInstr.append(int(lisInstr[1][0:]))
    
                numInstr.append(int(lisInstr[2][1:]))
        
        numInstructions.append(numInstr)
            
    #print(numInstructions)
    
    return(numInstructions)


def compute_hex_instructions(numInstructions):
    """
    Transforme la liste de nombres données en entrée en instructions héxadécimales.
    (à noter que le codage de ces instructions diffèrent selon le type d'opération).
    
    Paramètres : 
    ------------
        numInstructions : liste contenant l'ensemble des instructions, sous forme
        de liste de liste de nombres.
        
    Renvoie : 
    -----------
        hexInstructions : liste contenant l'ensemble des instructions héxadécimales
    """
    hexInstructions = []
    
    for numInstr in numInstructions:
        decInstr = 0
        decInstr += (numInstr[0]<<27)
        
        if len(numInstr)>1:
            if numInstr[0] == 15:
                decInstr +=(numInstr[1]<<26)
                decInstr +=(numInstr[2]<<5)
                decInstr +=(numInstr[3])
                
            elif (numInstr[0] == 16) or (numInstr[0] == 17):
                decInstr += (numInstr[1]<<22)
                decInstr += numInstr[2]
            elif numInstr[0] == 18:
                decInstr += numInstr[1]
            
            else : 
                decInstr += (numInstr[1]<<22)
                decInstr += (numInstr[2]<<21)
                decInstr += (numInstr[3]<<5)
                decInstr+= (numInstr[4])
            
        hexInstructions.append(hex(decInstr))
    return(hexInstructions)


# receives a list of hex instructions and a file name and writes instructions into file
def output_hex_instructions(hexInstructions, fileName):
    """
    Crée le fichier hexadécimal à partir des données prises en entrée. Associe à
    chacune de ces données une adresse, qui est rajoutée dans le fichier hexadécimal :
    les adresses de ces données se suivent.
    
    Paramètres : 
    ------------
        hexInstructions : liste contenant les données du fichier, sous forme 
        héxadécimale.
        fileName : nom du fichier devant contenir les données hexadécimales
    
    Renvoie :
    ------------
        Rien.
    
    """
    adress = 0x0
    outputFile = open(fileName, 'w')
    for instr in hexInstructions :
        outputFile.write(hex(adress) + ' ')
        outputFile.write(instr + '\n')
        adress +=1


if __name__ == "__main__":
        
    inputFileName = 'asmInstructions.txt'
    outputFileName = 'hexInstructions.txt'
    
    asmInstructions = load_ASM(inputFileName)
    numInstructions = analyze_instructions(asmInstructions)
    hexInstructions = compute_hex_instructions(numInstructions)
    
    output_hex_instructions(hexInstructions, outputFileName)
