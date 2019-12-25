from NodeAsicWorld import NodeAsicWorld
from Com import *

def main():
    rootnode = NodeAsicWorld("http://www.asic-world.com/verilog/veritut.html")
    parsenode(rootnode)
    NodeAsicWorld.genpdf("main")

def parsenode(currentnode):
    if currentnode.parentnode == None:
        NodeAsicWorld.cathtml(currentnode.content, "./data/main.html")
    if currentnode.content == None and currentnode.depth == MaxDepth:
        return
    NodeAsicWorld.cathtml(currentnode.content, "./data/main.html")
    for i in currentnode.childnodes:
        if i.content != None:
            NodeAsicWorld.cathtml(i.content, "./data/main.html")
        parsenode(i)
    
if __name__ == "__main__":
    main()