# Node in the tree
import urllib
from bs4 import BeautifulSoup
from functools import wraps 
from Com import *
import uuid

#Parent class
class Node(object): 
    """
    A node in the web scrapper parse tree.
    """
    def __init__(self, usrurl:str, prntnode = None):
        self._url = ""
        self._content = None

        self._isparsed = False
        self._isneutered = False

        self._childnodes = []
        self._parentnode = None #None for root node
        self._depth = 0
        self._id = str(uuid.uuid1()).split("-")[0]

        self.url = usrurl
        self.parentnode = prntnode

        self._setdepth()

    def _setdepth(self):
        if self.parentnode == None:
            self.depth = 0
        else:
            self.depth = self.parentnode.depth + 1

    @property
    def depth(self):
        return self._depth
    
    @depth.setter
    def depth(self, value):
        if value > MaxDepth or type(value) != int:
            raise RuntimeError("Depth error")
        self._depth = value
    
    def getsiblings(self):
        """
        Not Tested
        """
        if self.parentnode == None:
            raise RuntimeError("Node is root node. Has no parent.")
        templst = []
        for i in self.parentnode.childnodes:
            if self != i:
                templst.append(i)
        return templst
    
    def __eq__(self, another):
        if type(self) == type(another) and self.url == another.url and self.parentnode == another.parentnode:
            return True
        else:
            return False

    def __ne__(self, another):
        if type(self) == type(another) and self.url == another.url and self.parentnode == another.parentnode:
            return False
        else:
            return True
    
    def __hash__(self):
        return hash((self.url, self.parentnode))

    #for child to overwrite
    #set self.content
    def parseurl(self):
        pass

    @property
    def parentnode(self):
        return self._parentnode
    
    @parentnode.setter
    def parentnode(self, value):
        #if type(value) != Node and value != None:
        if value != None and value.__class__.__bases__[0] != self.__class__ and value.__class__ != self.__class__:
            raise TypeError("Must be a node")
        self._parentnode = value

    #for child to overwrite
    #set self.childnode
    def parsechild(self):
        pass

    @property
    def isparsed(self):
        return self._isparsed

    @isparsed.setter
    def isparsed(self, value):
        if type(value) != bool:
            raise TypeError("Not a bool value")
        self._isparsed = value

    @property
    def childnodes(self):
        return self._childnodes
    
    def appendnode(self, value):
        if value.__class__.__bases__[0] != self.__class__ and value.__class__ != self.__class__:
            raise TypeError("not a node")
        self.childnodes.append(value)
        return self.childnodes

    #getter
    @property
    def content(self):
        return self._content
    
    #setter
    #check type
    @content.setter
    def content(self, value:BeautifulSoup):
        if type(value) is BeautifulSoup:
            self._content = value
        else:
            raise TypeError("content must be beatifulsoup.")

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, value:str):
        if not Node.checkurl(value):
            raise TypeError("Url not valid")
        self._url = value

    @property
    def isneutered(self):
        return self._isneutered

    @isneutered.setter
    def isneutered(self, value):
        if type(value) != bool:
            raise TypeError("Not a bool value")
        self._isneutered = value

    @staticmethod
    def checkurl(usrurl: str)-> bool:
        if type(usrurl) != str:
            return False
        if urllib.parse.urlparse(usrurl).netloc == "":
            return False
        return True

    @staticmethod
    def depthcheck(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.depth > MaxDepth:
                raise RuntimeError
            else:
                if self.depth == MaxDepth:
                    self.isneutered = True
                ret =  func(self, *args, **kwargs)
                return ret
        return wrapper
    
    #deleter
    def __del__(self):
        del self._url
        del self._content

        del self._isparsed
        del self._isneutered

        del self._childnodes
        del self._parentnode
        del self._depth

if __name__ == "__main__":
    raise RuntimeError("Not suppose to be called.")