import glob
import os
import sys
from bs4 import BeautifulSoup
import codecs

file = codecs.open("rawdata/SmalltalkMarionBot.html", "r", "utf-8")
RAWhtml=file.read()
html = BeautifulSoup(RAWhtml,features="html.parser")
lines=html.find_all('p')

conversacion=[]

for line in lines:
    #print (line)
    span=line.find("span")
    text=line.text
    if 'class="c2"'  in str(line):
        #locutor
        if len(text)>1:
            conversacion.append("")
            conversacion.append("LOCUTOR:")
            conversacion.append(line.text)

    if 'class="c1"' in str(line):
        #marion
        if len(text)>1:
            conversacion.append("")
            conversacion.append("MARION:")
            conversacion.append(line.text)

with open("smalltalk.txt", 'w') as out:
    for l in conversacion:
        out.write(l + '\n')
