# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 01:00:00 2018

@author: EREN
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from xlwt import Workbook

##deletes the 'index.html' part from the poet url
def formatPoetURL(poet_url):
    l = list(poet_url)
    del l[-10:]
    poet_url = ''.join(l)
    return poet_url

def get_encoding(soup):
    if soup.meta is not None:
        encod = soup.meta.get('charset')
        if encod == None:
            encod = soup.meta.get('content-type')
            if encod == None:
                content = soup.meta.get('content')
                match = re.search('charset=(.*)', content)
                if match:
                    encod = match.group(1)
                else:
                    encod = "-1"
        return encod

    else:
        return "-1"
    
def formatPoem(poemStr):    
    poem = list(poemStr)
    
    while poem[0] == "\n":
        del poem[0]
        
    poem2 = []
    
    for i in range(len(poem)):     
        if not (len(poem2) > 1 and poem2[-2]=="\n" and poem2[-1]=="\n" and poem[i]=="\n"):    
            if poem[i] != "\t":
                poem2.append(poem[i])
    
    poem2Str = ''.join(poem2)
    poem2Str = poem2Str.replace(u'\xa0', u' ')  
    poem2 = list(poem2Str)
    
    poem3 = []
    for i in range(len(poem2)-1):
        if not (poem2[i]==" " and (poem2[i+1]==" " or poem2[i+1]=="\n")):
            poem3.append(poem2[i])
            
    while poem3[-1] == "\n":
        del poem3[-1]
        
    while poem3[0] == "\n":
        del poem3[0]
        
    poem3Str = ''.join(poem3)
    return poem3Str
            
def getTitle(poemStr):   
    poem = list(poemStr)
    title = []
    
    for i in poem:
        if i == "\n":
            break
        
        else:
            title.append(i)
    
    return ''.join(title)


def getPoem(poemStr):
    poem = list(poemStr)
    siir = []
    
    for i in range((poem.index("\n")+2), (len(poem) - 1 - poem[::-1].index("\n")-1)):
        siir.append(poem[i])
        
    return ''.join(siir)
        
def getPoet(poemStr):
    poem = list(poemStr)
    poet = []
    
    for i in range(len(poem) - 1 - poem[::-1].index("\n")+1, len(poem)):
        if poem[i] != ",":
            poet.append(poem[i])
        
    return ''.join(poet)

def formatPoetTitle(str):
    l = list(str)
    i=0
    for j in l:
        if j=="-":
            i = l.index(j)
            break
    l = l[:i-1]
    
    return ''.join(l)
            
url = "http://www.siir.gen.tr/sairlerimiz.htm"
page = urlopen(url).read()
soup = BeautifulSoup(page)
site_url = "http://www.siir.gen.tr/"
poets = []

for link in soup.find_all('a'):
     poets.append(site_url + link.get('href'))

wb = Workbook()
sheet1 = wb.add_sheet("sheet_1")  
poemCount = 0  

for p in poets:
    
    if(poets.index(p)!=238 and poets.index(p)!=239):
        if p != "http://www.siir.gen.tr/siir/i/ismet_ozel/index.html" and p is not None:
            poet_page = urlopen(p).read()
            poet_soup = BeautifulSoup(poet_page)    
            poems_loc = poet_soup.find("b", text="ŞİİRLERİ")    
            
            if poems_loc is not None:      
                poems_loc= poems_loc.find_next("p")
                            
                if poems_loc is not None:
                    for poem in poems_loc.find_all("a", recursive=False):
                        if poem is not None:
                            if poem.get("href") is not None:
                                poemURL= formatPoetURL(p) + poem.get("href")
                                poemPage = urlopen(poemURL).read()
                                poemSoup = BeautifulSoup(poemPage)
                                
                                if poemSoup is not None:
                                   
                                    if get_encoding(poemSoup).lower() == "windows-1254" or get_encoding(poemSoup) == "-1":
                                        poemPage = poemPage.decode('cp1254', 'ignore').encode('utf-16','ignore')
                                        poemSoup = BeautifulSoup(poemPage)      
                                                                           
                                    elif get_encoding(soup) == "ISO-8859-9":
                                        page = page.decode('ISO-8859-9').encode('utf-16','ignore')
                                        soup = BeautifulSoup(page)                                                                              
                                    
                                    poemText = formatPoem(poemSoup.body.get_text())
                                    if(len(formatPoetTitle(poet_soup.title.get_text()))+len(poem.get_text())+len(getPoem(poemText)) < 32767):
                                        sheet1.write(poemCount,0,formatPoetTitle(poet_soup.title.get_text()))
                                        sheet1.write(poemCount,1,poem.get_text())
                                        sheet1.write(poemCount,2,getPoem(poemText))
                                        poemCount = poemCount + 1
                                        print(formatPoetTitle(poet_soup.title.get_text()) + " " + poem.get_text())
                                        
wb.save("allPoems_sonn.xls")  

        