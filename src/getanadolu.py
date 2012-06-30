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

def mycapitalize(s):
    s = s[0].capitalize() + s[1:]
    return s

def lecture_content(inputFolder, filename):
    soup = BB(open(inputFolder + filename), "lxml")
    strings = []
    if not re.search(ur'^dt',filename):
        middle = soup.find(id = "content")
        if middle == None:
            print >> sys.stderr, "No content",filename
            return
        comments = middle.findAll(text=lambda text:isinstance(text, Comment))
        map( lambda x: x.extract(), comments)
        strings =  middle.stripped_strings
    else:
        ## This section clears the unwanted tables if more than 5
        ## tables are found then there is an error        
        middle = soup.find("div","content-center")
        comments = middle.findAll(text=lambda text:isinstance(text, Comment))
        map( lambda x: x.extract(), comments)
        tables = middle.find_all("table","mytable",recursive=False)
#        for tt in tables:
#            print "###",tt.prettify() 
        if len(tables) != 5:
            print >> sys.stderr, "Something wrong with the lecture page:tables:",filename,len(tables)
            sys.exit(1)
        define = tables[1]
        program = tables[2]
        trtr = define.find_all("tr",recursive=False)
        if len(trtr) != 8:
            print >> sys.stderr, "Something wrong with the lecture page trtr:",filename,len(trtr)
            sys.exit(1)
        for t in trtr[4].find("td").stripped_strings:
            strings.append(mycapitalize(t))
        for t in trtr[5].find("td").stripped_strings:
            strings.append(mycapitalize(t))
        for t in trtr[6].find("td").stripped_strings:
            strings.append(mycapitalize(t))
        prev = ""
        for t in program.find_all("tr"):
            td = t.find_all("td")
            if td == None:
                continue
            elif len(td) == 2:
                for s in td[0].stripped_strings:
                    strings.append(mycapitalize(s))
                for s in td[1].stripped_strings:
                    if prev != s:
                        strings.append(mycapitalize(s))
                        prev = s
#        for s in strings:
#            print s
#        sys.exit(1)
    return strings

def split_stars(s):#split star should be last splitting job
    star = re.compile(ur'\*')
    sp = star.split(s)
    fsp = []
    if len(sp) == 1:#if splitted do the require preprocess
        fsp.append(s)
        return fsp
    for ss in sp:
        ss = ss.strip("\s\r\n\t\- ")    
        if len(ss) == 0: continue
        ss = mycapitalize(ss)
        if re.search(ur'[\.!\?]$',ss):
            fsp.append(ss)
        else:
            ss = re.sub(ur'[:,;]$',"",ss)
            fsp.append(ss + " .")
    return fsp


inputFolder = sys.argv[1] #input dir
outputFolder = sys.argv[2] #input dir
parser = "lxml"
extreg = re.compile(r'\.html\.')
numreg = re.compile(r'^[0-9\.,\+!\?:;<\"&%\/\->\s\t\r\(\)\* _\"\'…\]\[]+$')
startreg = re.compile(r'^\$')
cariagereg = re.compile(r'\r')
# Lecture related
lecturereg = re.compile(ur'^(NAME OF LECTURER|ÖĞRETİM ELEMAN)')
outcomereg = re.compile(ur'^(LEARNING OUTCOMES OF|DERSİN ÖĞRENME ÇIKTILARI)')
deliveryreg = re.compile(ur'^(MODE OF DELIVERY|DERSİN VERİLİŞ BİÇİMİ)')
readingreg = re.compile(ur'^(RECOMMENDED OR REQUIRED READING|ZORUNLU YA DA)')
planreg = re.compile(ur'^(PLANNED LEARNING ACTIVITIES|ÖĞRETİM YÖNTEM VE TEKNİKLERİ)')
itemreg = re.compile(ur'([ \-\(]*[1-9][\.\-\)][0-9\.\-\)]{0,1}[0-9\.\-\)]{0,1}|[\( \n\t][a-z][\)])')
stritemreg = re.compile(ur'^[\-\(]*[1-9a-z][\.\-\)][0-9\.\-\)]*')
for (i, filename) in enumerate(os.listdir(inputFolder),start=0):
    if not re.search(ur'html\.(tr|en)$',filename): 
        continue
    if i % 100 == 0: print >>sys.stderr, ".",
    print inputFolder+filename
    middle = lecture_content(inputFolder, filename)
    ###Output
    outname = re.sub(extreg,".txt.",filename)
    fout = codecs.open(outputFolder+outname,"w","utf-8")
    (lecturerFlag, outcomeFlag, readingFlag) = (False, False,False)    
    for s in middle:
        s = re.sub(ur'[\r •]',"",s); # remove windows cariage
        if re.search(ur'^(<!--.*?-->|\/p>|-->|\">|<|\$)$',s): continue #remove uncatched comments
        s = re.sub(ur'^(çevirileri görmek için tıklayın|görmek için tıklayın|için tıklayın|tıklayın)\\\">',"",s)
        if len(s)==0: continue
#        print >> sys.stderr, "["+s+"]\n"
        t = lxml.html.fromstring(s) # remove html tags if the pages
        s = t.text_content()        # are bad coded
        s = s.strip()               # strip whitespace
        if re.search(ur'^@', s): continue
#        fout.write(s + "\n")
#        continue
        sp = []
        if lecturerFlag:#splits the things that are lecture
            lecturerFlag = False
            continue        
        elif re.search(planreg,s):#removes the reading metarial
            readingFlag = False
            continue
        elif readingFlag:#continue over reading flags
            continue
        elif re.search(deliveryreg,s):
            outcomeFlag = False
        elif re.search(readingreg,s):
            readingFlag = True
#        elif outcomeFlag:
#            sp = itemreg.split(s)
        elif re.search(lecturereg,s):
            lecturerFlag = True
        elif re.search(outcomereg,s):
            outcomeFlag = True
        elif re.search(numreg,s) or re.search(startreg,s): 
            continue

        #item or enumarate split of text
        sp = itemreg.split(s)
#        fout.write("BEFORE SPLIT print[["+s+"]]"+str(len(sp))+"\n")
#        for si in sp:
#            fout.write("sppart[["+si+"]]\n")
        fsp= []
        if len(sp) > 1: # if we perform split
#            fout.write("SPLIT print\n")
            for ss in sp:
                if len(ss) == 0: continue
                fsp += split_stars(ss)                
            sp = fsp
            fsp = []
            for ss in sp:
                ss = ss.strip(" \t\n\r\f\v\-")
                ss = re.sub(numreg,'',ss)
                if len(ss) == 0: continue
                ss = mycapitalize(ss)
                if re.search(ur'[\.!\?]$',ss):
                    fsp.append(ss)
                else:
                    ss = re.sub(ur'[:,;]$',"",ss)
                    fsp.append(ss + " .")
#            for ss in fsp:
#                fout.write(ss + "\n")
        else:
#            fout.write("ELSE print0["+s+"]\n")            
            if len(sp) == 0:
                sp.append(s)            
            for ss in sp:
                ss = ss.strip(" \t\n\r\f\v\-")
                ss = re.sub(stritemreg,"",ss)
                ss = re.sub(numreg,"",ss)
                fsp += split_stars(ss)
        for ss in fsp:
            if not re.search(ur'[\.!\?]$',ss):
                ss = re.sub(ur'[,;:]$',"",ss)
                ss = ss + " ."
            if ss.strip(): fout.write(ss.strip() + "\n")
    fout.close()
        
