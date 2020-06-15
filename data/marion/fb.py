import glob
import os
import sys
from bs4 import BeautifulSoup
import codecs

textos=[]

for filename in sorted(glob.glob('fb/*.html')):
    print(filename)

    # do your stuff
    f=codecs.open(filename, 'r')
    RAWhtml=f.read()
    html = BeautifulSoup(RAWhtml,features="html.parser")
    lines=html.find_all('div', attrs={'class':'_3-96 _2let'})
    for line in lines:
        texto=line.text
        if "http" not in texto:
            if len(texto)>0:
                print (texto)
                print("....")
                textos.append(texto)

with open("fb.txt", 'w') as out:
    for texto in textos:
        out.write(texto + '\n')
