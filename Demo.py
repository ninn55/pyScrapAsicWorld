from NodeAsicWorld import NodeAsicWorld
from Com import *
import _pickle as pickle

global nodedef
nodedef = ["digraph G{", "remincross=true;rankdir=\"TB\";"]

global nodeconnec
nodeconnec = []

def main():
    #rootnode = readtree():
    rootnode = NodeAsicWorld("http://www.asic-world.com/verilog/veritut.html")
    savetree(rootnode)
    #gendot(rootnode)
    #parsenode(rootnode)
    #NodeAsicWorld.genpdf("main")

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

def gendot(currentnode):
    drawgraph(currentnode)
    with open("./data/graph.dot", "w") as f:
        f.write('\n'.join(nodedef) + '\n')
    with open("./data/graph.dot", "a") as f:
        f.write('\n'.join(nodeconnec) + '\n')
    with open("./data/graph.dot", "a") as f:
        f.write('\n' + "}")

def savetree(currentnode):
    with open("./data/tree", "wb") as f:
        f.write(pickle.dumps(currentnode))

def readtree():
    with open("./data/tree", "rb") as f:
        return pickle.loads(f.read())

def drawgraph(currentnode):
    tempdef = "n%(id)s [shape=record, label = \"{<url> %(url)s|<id> %(id)s}\"];" % {
            "id": currentnode._id,
            "url": currentnode.url.split("/")[-1].split(".")[0]
    }
    nodedef.append(tempdef)

    for i in currentnode.childnodes:
        tempconnec = "n%(id_parent)s -> n%(id_child)s" % {
            "id_parent": currentnode._id,
            "id_child": i._id
        }
        nodeconnec.append(tempconnec)
        drawgraph(i)

if __name__ == "__main__":
    main()