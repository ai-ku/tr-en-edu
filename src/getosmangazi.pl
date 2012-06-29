#!/usr/bin/python 
#-*-coding: utf-8-*-

import urllib
import os.path
import sys
import codecs
import unicodedata
from bs4 import BeautifulSoup

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

def getTable(main, fileName, option):
    pageFile = urllib.urlopen(main + fileName)
    pageHtml = pageFile.read()
    pageFile.close()

    if option == 0:
	langSpecifiedString = "Ders Kodu"
    elif option == 1:
	langSpecifiedString = "Course Code"

    soup = BeautifulSoup("".join(pageHtml), from_encoding='utf8')
    tables = soup.findAll("table")
    for table in tables:
    	itemsFromTable = table.findAll("td")
        firstItem = itemsFromTable[0].find("b")
	if firstItem:
    		if firstItem.contents[0] == langSpecifiedString:
                    return table

def getContent(table):
    content = []
    control = 0
    
    rows = table.findAll('tr')
    for tr in rows:
        cols = tr.findAll('td')
        for td in cols:
            text = ''.join(td.find(text = True))
            if text != None:
                try:
                    #print ''.join(text)
                    if control == 1:
                        control = 0
                        contentElement = td.find("font")
                        if contentElement:
                            content.append(''.join(contentElement.contents[0]))
                    elif control == 2 or control == 3 or control == 4:
                        if control == 2:
                            detail1 = td.find("span", id="DetailsView1_Label1")
                        elif control == 3:
                            detail1 = td.find("span", id="DetailsView1_Label2")
                        elif control == 4:
                            detail1 = td.find("span", id="DetailsView1_Label3")
                        control = 0
                        if detail1:
                            liList = detail1.findAll("li")
                            if len(liList) > 0:
                                for li in liList:
                                    if li:
                                        liTxt = ''.join(li.find(text = True))
                                        if liTxt:
                                            content.append(liTxt.strip())
                                            continue
                            else:
                                pList = detail1.findAll("p")
                                if len(pList) > 0:
                                    for p in pList:
                                        if p:
                                            pTxt = ''.join(p.find(text = True))
                                            if pTxt:
                                                content.append(pTxt.strip())
                                else:
                                    if detail1.find(text = True):
                                        content.append((''.join(detail1.find(text = True))).strip())
                                    else:
                                        content.append(" ")
                    else:
                        element = td.find("b")
                        if not element:
                            continue
                        if element.contents[0].strip() == "Course Code" or element.contents[0].strip() == u"Ders Kodu":
                            content.append(''.join(element.contents[0]).strip())
                        elif element.contents[0].strip() == "Course Title" or element.contents[0].strip() == u"Ders Adı":
                            content.append(''.join(element.contents[0]).strip())
                            control = 1
                        elif element.contents[0].strip() == "Academic Cycle" or element.contents[0].strip() == u"Öğretim Düzeyi":
                            content.append(''.join(element.contents[0]).strip())
                            control = 1
                        elif element.contents[0].strip() == "Year of Study" or element.contents[0].strip() == u"Sınıf":
                            content.append(''.join(element.contents[0]).strip())
                            control = 1
                        elif element.contents[0].strip() == "Instructor's Name" or element.contents[0].strip() == u"Öğretim Üyesi":
                            content.append(''.join(element.contents[0]).strip())
                            control = 0
                        elif element.contents[0].strip() == "Prerequisites" or element.contents[0].strip() == u"Ön Şart":
                            content.append(''.join(element.contents[0]).strip())
                            control = 0
                        elif element.contents[0].strip() == "Duration" or element.contents[0].strip() == u"Süre":
                            content.append(''.join(element.contents[0]).strip())
                            control = 1
                        elif element.contents[0].strip() == "Semester" or element.contents[0].strip() == u"Dönem":
                            content.append(''.join(element.contents[0]).strip())
                            control = 1
                        elif element.contents[0].strip() == "Examination" or element.contents[0].strip() == u"Sınav":
                            content.append(''.join(element.contents[0]).strip())
                            control = 1
                        elif element.contents[0].strip() == "Assessment" or element.contents[0].strip() == u"Değerlendirme":
                            content.append(''.join(element.contents[0]).strip())
                            control = 1
                        elif element.contents[0].strip() == "Description" or element.contents[0].strip() == u"Dersin Temel Amacı":
                            content.append(''.join(element.contents[0]).strip())
                            control = 2
                        elif element.contents[0].strip() == "Course Content" or element.contents[0].strip() == u"İçerik":
                            content.append(''.join(element.contents[0]).strip())
                            control = 3
                        elif element.contents[0].strip() == "Learning Objectives" or element.contents[0].strip() == u"Dersin Öğrenciye Kazandırdığı Beceriler":
                            content.append(''.join(element.contents[0]).strip())
                            control = 4
                        elif element.contents[0].strip() == "Read List" or element.contents[0].strip() == u"Kaynaklar":
                            content.append(''.join(element.contents[0]).strip())
                            control = 0
                except:
                    #print "Error:", sys.exc_info()[0]
                    pass
    return content
def editPunctuation(line):
    if not line.isspace():
        line = line.capitalize()
        out = []
        if line.endswith(","):
            out = line.rsplit(',', 1)[0] + "."
            line = out
        elif line.endswith(";"):
            out = line.rsplit(';', 1)[0] + "."
            line = out
        else:
            if not (line.endswith(":") or line.endswith("?") or line.endswith(".") or line.endswith("!")):
                line = line + "."
    return line
    
if len(sys.argv) != 2:
    print "Wrong call.\n"
    print "Usage: python extractContent.py mainFolder"
else:
    main = sys.argv[1]
    
    i = 0
    trLen = len(os.listdir(main + "html/"))
    for trEl in os.listdir(main + "html/"):
        i = i + 1
        print i, "/", trLen
        try:
            tmp = trEl.split(".html.tr")
            if len(tmp) == 1:
                continue
            
            course = tmp[0]
            tableTr = getTable(main + "html/", course + ".html.tr", 0)
            contentTr = getContent(tableTr)
            tableEn = getTable(main + "html/", course + ".html.en", 1)
            contentEn = getContent(tableEn)

            
            txtTr = codecs.open(main + "txt/" + course + ".txt.tr", "w", encoding="utf-8")
            txtEn = codecs.open(main + "txt/" + course + ".txt.en", "w", encoding="utf-8")
            
            for sTr in contentTr:
                if sTr in contentEn:
                    continue
                else:
                    txtTr.write(editPunctuation(sTr) + "\n")
            
            for sEn in contentEn:
                if sEn in contentTr:
                    continue
                else:
                    txtEn.write(editPunctuation(sEn) + "\n")

            txtTr.close()
            txtEn.close()
        except:
            #print "Error:", sys.exc_info()[0]
            pass
