import glob
import os
import sys
from bs4 import BeautifulSoup
import codecs

textos=[]

blacklisted=["sent an attachment","http","@","+34","+33","0034","0033","Click for","roger de","lluria",".pdf",".doc"]

for filename in sorted(glob.glob('fb/*.html')):
    print(filename)
    blockcount=0
    # do your stuff
    f=codecs.open(filename, 'r')
    RAWhtml=f.read()
    html = BeautifulSoup(RAWhtml,features="html.parser")
    lines=html.find_all('div', class_='pam _3-95 _2pi0 _2lej uiBoxWhite noborder')
    #lines=html.find_all('div', attrs={'class':'_3-96 _2let'})


    for line in lines:
        newCom=[]
        if "Participants:" not in line.text:
            autor=line.find('div', class_='_3-96 _2pio _2lek _2lel')
            if not autor:
                autor=line.find('div', class_='_3-96 _2pio _2lek _2lel')

            autor=autor.text.strip()
            texto=line.find('div',class_='_3-96 _2let').text.strip()

            if autor=="Marion Balac":
                newCom.append("")
                newCom.append("MARION:")
            else:
                newCom.append("")
                newCom.append("LOCUTOR:")


            if len(texto)>0:
                shouldpass=True
                for b in blacklisted:
                    if b.upper() in texto.upper():
                        shouldpass=False
                #print (texto)
                #print("....")
                if shouldpass:
                    newCom.append(texto)
                    textos[:0]=newCom
                    blockcount+=1


    print("total blocks:",blockcount)


with open("fb.txt", 'w') as out:
    for texto in textos:
        out.write(texto + '\n')
