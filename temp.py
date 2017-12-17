# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup as bsoup
import random

url = "http://www.thefreedictionary.com/4-letter-words.htm"
r = requests.get(url)
data = r.text
soup = bsoup(data)
ls = soup.findAll('a')
allwords = []
for l in ls:
    if len(l.text) == 4:
        if len(set(l.text)) == len(l.text):
            allwords.append(l.text)
print allwords

#r = random.choice(allwords)
r = "kset"
s = "test"
ref = set(r)
test = set(s)
intersect = ref & test

print r
print s

bulls = 0;
for i in range(0,4):
    if r[i] == s[i]:
        bulls = bulls + 1
cows = len(intersect)-bulls
print "bulls: " + str(bulls)
print "cows: " + str(cows)
#print soup.findAll("div", { "class" : "stylelistrow" })
