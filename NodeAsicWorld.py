from Node import Node
from urllib.parse import urljoin
import subprocess
import uuid
import os
from bs4 import BeautifulSoup
from Com import *

class NodeAsicWorld(Node):
    def __init__(self, usrurl, prntnode=None):
        super(NodeAsicWorld, self).__init__(usrurl, prntnode=prntnode)
        self.filename = "%(depth)s_%(url)s"%{
                    "depth":self.depth,
                    "url": self._id,
        }
        self.driver = chromedriver.getdriver()
        
        self.parseurl()
        #self.genhtml()
        #self.genpdf()
        self.parsechild()

    @Node.depthcheck
    def parsechild(self):
        if self.isneutered == True:
            return
        urllst = []
        for i in self.content.find_all('a'):
            if i.b == None or i["href"] == None:
                continue
            tempurl = urljoin(self.url, i["href"])
            urllst.append(tempurl) 
        
        for i in urllst:
            temp = NodeAsicWorld(i, self)
            self.appendnode(temp)

    def parseurl(self):
        if self.isparsed == True:
            pass
        else:
            self.driver.get(self.url)
            tempcntnt = self.driver.find_elements_by_tag_name('table')[3].get_attribute('innerHTML')
            self.content = BeautifulSoup(tempcntnt, 'html.parser')
            self.removegoogleads()
            self.removegooglelogo()
            self.removeblanks()
            self.parseimgyrl()
            self.isparsed = True


    def removegoogleads(self):
        while 1:
            try:
                self.content.script.decompose()
            except AttributeError:
                break
    
    def removegooglelogo(self):
        for i in self.content.find_all('img'):
            try :
                _ = i['src']
            except KeyError :
                continue
            if  "google.com" in i['src']:
                i.decompose()

    def removeblanks(self):
        for i in self.content.find_all('img'):
            try :
                _ = i['alt']
            except KeyError :
                continue
            if i["alt"] == 'space.gif':
                i.decompose()
    
    def parseimgyrl(self):
        for i in self.content.find_all('img'):
            i['src'] = urljoin(self.url, i["src"])
    
    def genhtml(self):
        if self.isparsed == True:
            with open("./%(name)s.html"%{"name": self.filename}, 'wb') as f:
                f.write(self.content.encode('utf-8'))
        else:
            raise RuntimeError("File is not parsed yet")

    @staticmethod
    def genpdf(fname:str):
        fnmaehtml = os.path.join(DataDir, "%(name)s.html")%{"name": fname}
        fnmaepdf = os.path.join(DataDir, "%(name)s.pdf")%{"name": fname}
        pandoccommand = "pandoc %(namehtml)s -t %(engine)s -o %(namepdf)s"%{"namehtml": fnmaehtml, "namepdf": fnmaepdf, "engine": "html5"}
        werror = subprocess.call(pandoccommand, shell = True)
        if werror != 0:
            pandoccommand = "pandoc %(namehtml)s -t %(engine)s -o %(namepdf)s"%{"namehtml": fnmaehtml, "namepdf": fnmaepdf, "engine": "latex"}
            werror = subprocess.call(pandoccommand, shell = True)
            if werror != 0:
                print("Gen file %(name)s.pdf failed"%{"name": fname})

    @staticmethod
    def cathtml(strcntnt, fname:str):
        with open(fname, "ab") as f:
            f.write("\n".encode('utf-8'))
            f.write(strcntnt.encode('utf-8'))
            f.write("\n".encode('utf-8'))

if __name__ == "__main__":
    raise RuntimeError("Not suppose to be runned")