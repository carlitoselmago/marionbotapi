import glob
import os
import sys
from bs4 import BeautifulSoup
import codecs

textos=[]

blacklisted=["chap","CHAPITRE",") ;"]
clean=["«","»","➥",";"]

filename="rawdata/epubs/Alain Bourdie - Decouvrir et comprendre l'art contemporain [FR]/index_split_000.html"
export="Decouvrir et comprendre l'art contemporain.txt"

f=codecs.open(filename, 'r')
RAWhtml=f.read()
html = BeautifulSoup(RAWhtml,features="html.parser")

lines=html.find_all('p', class_='calibre1')

for line in lines:

    texto=line.text
    texto=texto.strip()
    shouldpass=True

    if texto.isupper():
        shouldpass=False

    if texto.isnumeric():
        shouldpass=False

    for b in blacklisted:
        if b.upper() in texto.upper():
            shouldpass=False

    for c in clean:
        texto=texto.replace(c, "")

    if texto=="ANNEXES":
        break

    if shouldpass:
        if len(texto)>0:
            texto=texto.strip()
            textos.append(texto)
            textos.append("")



with open(export, 'w') as out:
    for texto in textos:
        print (texto)
        out.write(texto + '\n')
