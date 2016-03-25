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

exons = {} #hash of exons

#per ogni riga
for riga in in_file.readlines():
    #controllo che sia un esone 
    matchObj = re.match( r'chr([A-Za-z1-9]*)\s+[A-Za-z.]*\s*exon\s*([0-9]*)\s*([0-9]*)\s*.\s*(.)\s*.\s*gene_id\s*([a-zA-z1-9-]*).*', riga, re.M|re.I)
    
    exon = {}
    #Inizio per calcolare sequenza nucleotidica
    if matchObj:
       support_server = server
       exon['chromosome'] = matchObj.group(1)
       exon['start'] = matchObj.group(2)
       exon['end'] = matchObj.group(3)
       id = exon['start'] + ':' + exon['end']
       if id not in exons:
           exons['id'] = exon
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

for elem in lista:
        t = True
        for elem_supp in lista_supporto:
            if(elem_supp == elem[0]):
                t = False
        if (t == True):
            j = 0
            lista_stampa = []
            lista_supporto.append(elem[0])
            elemento = elem[0]
            f.write("\"Gene_id\" : \""+elemento+"\"")
            #print("\"Gene_id\" : \""+elemento+"\"")
            while (j < len(lista)):
                if( lista[j][0] == elemento):
                    lista_stampa.append(lista[j][0:6])
                    #print(lista[j][1:6],"\n")
                j += 1

        #print(lista_stampa[:][0:5])
            #print(len(lista_stampa))
            for elem in lista_stampa:
                f.write(json.dumps({'Inizio' : elem[1],
                                    'Fine' : elem[2],
                                    'Strand' : elem[3],
                                    'Sequenza' : elem[4],
                                    'Cromosoma' : elem[5],
                                   },sort_keys=True,indent=16, separators=(',',':')) + "\n")

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
