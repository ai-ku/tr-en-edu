#!/usr/bin/python 
#-*- coding: utf-8 -*-
# This code specifically written for anadolu.edu.tr web-site under the bologna project
# Author: myatbaz

import sys
import codecs
import re
import os.path
import lxml.html
from bs4 import BeautifulSoup as BB
from bs4 import Comment

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

inputFolder = sys.argv[1] #input dir
outputFolder = sys.argv[2] #input dir
parser = "lxml"
wheretoget = "sag"

### regexp
cariagereg = re.compile(ur'(\r|^\s+|\s+$)');
numreg = re.compile(ur'^[0-9.,\+!\?:;<\"&%\/\->\s\t\r\(\)* _\"\'…\]\[]+')
itemreg = re.compile(ur'^[\-\(]*[1-9a-z][\.\-\)][0-9\.\-\)]*')
isempty = re.compile(ur'/\S/')
def get_course_content(page):
    w2g1 = u"ctl00_ContentPlaceHolder_divDersAmaciIcerik"
    w2g2 = u"ctl00_ContentPlaceHolder_divOgrenmeCiktilariIcerik"
    w2g3 = u"ctl00_ContentPlaceHolder_divOgrenimTuruıcerik"
    w2g4 = u"ctl00_ContentPlaceHolder_divhaftalikAyrintilidersIcerigi"
    w2g = [w2g1,w2g2,w2g3,w2g4]
    soup = BB(open(inputFolder + filename), parser)
    middle = soup.find(id = wheretoget)    
#    print middle.prettify()
    if middle == None:
        print >> sys.stderr, "no div=" + wheretoget +  page
        return
    comments = middle.find(text=lambda text:isinstance(text, Comment))
    if comments != None:    map( lambda x: x.extract(), comments)    
    ###Output
    outname = re.sub(".html.",".txt.",filename)
    fout = codecs.open(outputFolder+outname,"w","utf-8")
    fs = []
    prev = ""
    for ww in w2g:
        cnt = middle.find(id = ww)
        if cnt == None:
#            return
            continue
#            print >> sys.stderr, filename,ww
        for s in cnt.stripped_strings:
            s = re.sub(cariagereg,"",s)
            fs += s.split("\n")
    for s in fs:
        s = re.sub(numreg,"",s)
        s = re.sub(itemreg,"",s)
        s = s.strip()
        if s and s != prev:
            prev = s
            if not re.search(ur'[\.!\?]$',s):
                s = s+ " ."
            fout.write( s + "\n")
    fout.close()

def  get_organization_content(page):
    w2g1 = "ctl00_ContentPlaceHolder_ltlGenelBilgiler"
    w2g2 = "ctl00_ContentPlaceHolder_ltlProgramCiktilari"
    w2g = [w2g1, w2g2]
    soup = BB(open(inputFolder + filename), parser)
    middle = soup.find(id = wheretoget)    
    if middle == None:
        print >> sys.stderr, "no div=" + w2g +  page
        return
    comments = middle.find(text=lambda text:isinstance(text, Comment))
    if comments != None and isinstance(comments, (list, tuple)):    map( lambda x: x.extract(), comments)    
     ###Output
    outname = re.sub(".html.",".txt.",filename)
    fout = codecs.open(outputFolder+outname,"w","utf-8")
    fs = []
    prev = ""
    for ww in w2g:
        cnt = middle.find(id = ww)
        if cnt == None:
            continue
        for s in cnt.stripped_strings:
            s = re.sub(cariagereg,"",s)
            fs += s.split("\n")

    for s in fs:
        s = re.sub(numreg,"",s)
        s = re.sub(itemreg,"",s)
        s = s.strip()
        if s and s != prev:
            prev = s
            if not re.search(ur'[\.!\?]$',s):
                s = s+ " ."
            fout.write( s  + "\n")
    fout.close()
    
for (i, filename) in enumerate(os.listdir(inputFolder),start=0):
    print >> sys.stderr,inputFolder+filename
    if re.search(ur'^cc',filename):
        get_course_content(filename)
    elif re.search(ur'^og',filename):
        get_organization_content(filename)
