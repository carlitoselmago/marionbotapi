import glob
import os
import sys
from bs4 import BeautifulSoup
import codecs
# Python program to
# demonstrate merging
# of two files

combined=""

for filename in sorted(glob.glob('ready/*.txt')):

    # Reading data from file
    with open(filename) as fp:
        data = fp.read()
        combined+=data



with open ('COMBINED/ALL.txt', 'w') as fp:
    fp.write(combined)
