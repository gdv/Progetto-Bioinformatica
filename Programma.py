import sys          #serve per il messagio di mancato file
import re           #server per le regualar expression
import requests     #serve per la sequenza nucleotidica
import json         #serve per stampare in formato json

#controllo esistenza file di input ed sua apertura
try:
    in_file = open("input.gtf", "r")    
except OSError:
    print("File non trovato")
    
#apertura/creazione del file di output             
f = open ("output.json", "w")


#servono per la sequenza nucleotidica
server = "http://grch37.rest.ensembl.org"
ext = "/sequence/region/human/"

lista_supporto = [] #mi serve per tenere conto dei geni presenti
lista_stampa = []   #mi serve per raggruppare gli esoni rispetto al gene
t = True


lista = [] #lista che conterrà tutti gli esoni del file di input

#per ogni riga
for riga in in_file.readlines():
    #controllo che sia un esone 
    matchObj = re.match( r'chr([A-Za-z1-9]*)\s+[A-Za-z.]*\s*exon\s*([0-9]*)\s*([0-9]*)\s*.\s*(.)\s*.\s*gene_id\s*([a-zA-z1-9-]*).*', riga, re.M|re.I)
    
    #Inizio per calcolare sequenza nucleotidica
    if matchObj:
       support_server = server
       support_ext = ext + matchObj.group(1)
       support_ext += ":"
       support_ext += matchObj.group(2)
       support_ext += ".."
       support_ext += matchObj.group(3)
       support_ext += ":" 
       """if(matchObj.group(4) == '-'):
           support_ext += "-1?"
       if(matchObj.group(4) == '+'):
           support_ext += "1?"
           """
       support_ext += "1?"

       r = requests.get(support_server+support_ext, headers = {"Content-Type" : "text/plain"})

       #fine sequenza nucleotidica
       lista.append([matchObj.group(5), matchObj.group(2), matchObj.group(3), matchObj.group(4), r.text,matchObj.group(1)])       
       if not r.ok:
           r.raise_for_status()
           sys.exit()
           print (r.text)

i = 0

while ( i < len(lista)):
        t = True
        z = 0
        while(z < len (lista_supporto)):
            if(lista_supporto[z] == lista[i][0]):
                t = False
            z += 1
        if (t == True):
            j = 0
            lista_stampa = []
            lista_supporto.append(lista[i][0])
            elemento = lista[i][0]
            f.write("\"Gene_id\" : \""+elemento+"\"")
            #print("\"Gene_id\" : \""+elemento+"\"")
            while (j < len(lista)):
                if( lista[j][0] == elemento):
                    lista_stampa.append(lista[j][0:6])
                    #print(lista[j][1:6],"\n")
                j += 1

        #print(lista_stampa[:][0:5])
            m = 0
            #print(len(lista_stampa))
            while (m < len(lista_stampa)):
                f.write(json.dumps({'Inizio' : lista_stampa[m][1],
                                    'Fine' : lista_stampa[m][2],
                                    'Strand' : lista_stampa[m][3],
                                    'Sequenza' : lista_stampa[m][4],
                                    'Cromosoma' : lista_stampa[m][5],
                                   },sort_keys=True,indent=16, separators=(',',':')))
                f.write("\n")
                m+=1
            """
            print("          " + lista[m][1])
            print("          " + lista[m][2])
            print("          " + lista[m][3])
            print("          " + lista[m][4])
            print("          " + lista[m][5])
            """
        i += 1
        
#chiusura dei file di input/output
f.close()
in_file.close()






"""      
i = 0
while (i < len(lista)):
    print("\n",lista[i],"\n")
    i+=1
"""









"""

in_file = open("a.gtf", "r")

import re
import requests, sys

server = "http://grch37.rest.ensembl.org"
ext = "/sequence/region/human/"
cont = 1;


lista = []
#per ogni riga
for riga in in_file.readlines():

    matchObj = re.match( r'chr([A-Za-z1-9]*)\s+[A-Za-z.]*\s*exon\s*([0-9]*)\s*([0-9]*)\s*.\s*(.)\s*.\s*gene_id\s*([a-zA-z1-9-]*).*', riga, re.M|re.I)
   #sequenza nucleotidica
    if matchObj:
       support_server = server
       support_ext = ext+matchObj.group(1)
       support_ext += ":"
       support_ext += matchObj.group(2)
       support_ext += ".."
       support_ext += matchObj.group(3)
       support_ext += ":" 
       if(matchObj.group(4) == '-'):
           support_ext += "-1?"
       if(matchObj.group(4) == '+'):
           support_ext += "1?"

       r = requests.get(support_server+support_ext, headers = {"Content-Type" : "text/plain"})
       #fine sequenza nucleotidica
       lista.append([matchObj.group(5),matchObj.group(2),matchObj.group(3),matchObj.group(4),r.text,matchObj.group(1)])       
       if not r.ok:
           r.raise_for_status()
           sys.exit()
           print (r.text)
i = 0
while (i < len(lista)):
    print("\n",lista[i],"\n")
    i+=1

"""













"""
#Apro un file GTF
in_file = open("a.gtf", "r")

import re
import requests, sys

server = "http://grch37.rest.ensembl.org"
ext = "/sequence/region/human/"
cont = 1;
errori = 0
erroreCont = 0
#per ogni riga
for riga in in_file.readlines():

    matchObj = re.match( r'chr([A-Za-z1-9]*)\s+[A-Za-z.]*\s*exon\s*([0-9]*)\s*([0-9]*)\s*.\s*(.)\s*.\s*gene_id\s*([a-zA-z1-9-]*).*', riga, re.M|re.I)
    print(str(cont))
    if matchObj:
       support_server = server
       support_ext = ext+matchObj.group(1)
       support_ext += ":"
       support_ext += matchObj.group(2)
       support_ext += ".."
       support_ext += matchObj.group(3)
       support_ext += ":" 
       if(matchObj.group(4) == '-'):
           support_ext += "-1?"
       if(matchObj.group(4) == '+'):
           support_ext += "1?"

       r = requests.get(support_server+support_ext, headers = {"Content-Type" : "text/plain"})

       if not r.ok:
          # r.raise_for_status()
           errori+=1
           erroreCont= cont
          # sys.exit()
           print (r.text)
       
   # else:
      # print ("Non va bene "+ str(cont))

    cont = cont+1
print("Ci sono stati : ", str(errori), " errori")
print("l'ultimo errore e' ", erroreCont)

#chiusura del file di lettura
in_file.close()

#/^[A-Za-z1-9]*\s*[A-Za-z.]*\s*[A-Za-z]*\s*([0-9]*)\s*([0-9]*).*$/
#/^[A-Za-z1-9]*\s+[A-Za-z.]*\s*[A-Za-z]*\s*([0-9]*)\s*([0-9]*).*
#[A-Za-z1-9]*\s+[A-Za-z.]*\s*[A-Za-z]*\s*([0-9]*)\s*([0-9]*)\s*.\s*.\s*.\s*gene_id\s*([a-zA-z1-9-]*).*
#[A-Za-z1-9]*\s+[A-Za-z.]*\s*exon\s*([0-9]*)\s*([0-9]*)\s*.\s*(.)\s*.\s*gene_id\s*([a-zA-z1-9-]*).*

#[A-Za-z1-9]*\s+[A-Za-z.]*\s*exon\s*([0-9]*)\s*([0-9]*)\s*.\s*(.)\s*.\s*gene_id\s*([a-zA-z1-9-]*).*
"""
