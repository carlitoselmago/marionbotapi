import glob
import os
import sys
from bs4 import BeautifulSoup
import codecs
import re
import pysrt

textos=[]

blacklisted=[""]
clean=["- ","<i>","</i>","...","*"]

gptmode=False

def srt_time_to_seconds(time):
    split_time=time.split(',')
    major, minor = (split_time[0].split(':'), split_time[1])
    return int(major[0])*1440 + int(major[1])*60 + int(major[2]) + float(minor)/1000

def srt_to_dict(srtText):
    subs=[]
    for s in re.sub('\r\n', '\n', srtText).split('\n\n'):
        st = s.split('\n')
        if len(st)>=3:
            split = st[1].split(' --> ')
            subs.append({'start': srt_time_to_seconds(split[0].strip()),
                         'end': srt_time_to_seconds(split[1].strip()),
                         'text': '<br />'.join(j for j in st[2:len(st)])
                        })
    return subs
count=0
for filename in sorted(glob.glob('rawdata/subtitles/*.srt')):
    print(filename)

    try:
        subs = pysrt.open(filename)
        print (len(subs))

        for s in subs:
            texto=s.text

            shouldpass=True
            """
            for b in blacklisted:
                if b.upper() in texto.upper():
                    shouldpass=False
            """
            if shouldpass:

                for c in clean:
                    texto=texto.replace(c, "")

                texto=texto.strip()

                if len(texto)>0:
                    if gptmode:
                        if (count % 2) == 0:
                            textos.append("")
                            textos.append("MARION:")
                        else:
                            textos.append("")
                            textos.append("LOCUTOR:")

                    textos.append(texto.replace('\n', ' ').replace('\r', ''))

                    count+=1
    except:
        pass



with open("subtitles.txt", 'w') as out:
    for texto in textos:
        out.write(texto + '\n')
