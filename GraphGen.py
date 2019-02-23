# -*- coding:utf-8 -*-
import snap
import pandas as pd
import csv
from collections import defaultdict

ID = 0
name2idDict = {}
id2nameDict = {}
userEdgeCount = {}
userLink = defaultdict(int)

data = pd.DataFrame(pd.read_csv("fans.csv"))
userLinkData = pd.DataFrame(pd.read_csv("links.csv"))
upList = data["A"].unique().tolist()
fansList = data["B"].unique().tolist()

for row in userLinkData.iterrows():
    userLink[row[1].user] = str(row[1].Link)

for item in upList:
    if item not in name2idDict:
        name2idDict[item]=ID
        id2nameDict[ID] = item
        ID += 1

for item in fansList:
    if item not in name2idDict:
        name2idDict[item]=ID
        id2nameDict[ID] = item
        ID += 1


dataLength = data.shape[0]
G = snap.TUNGraph.New()
for index in range(dataLength):
    rowData = data.loc[index]
    upID = int(name2idDict[rowData[0]])
    fanID = int(name2idDict[rowData[1]])
    if G.IsNode(upID) == False:
        G.AddNode(upID)
    if G.IsNode(fanID) == False:
        G.AddNode(fanID)
    if G.IsEdge(upID,fanID) == False:
        G.AddEdge(upID,fanID)

nodeSet = snap.TIntSet()
for index in range(len(name2idDict)):
    nodeSet.AddKey(index)


delNodeList = []
limit = 1
#for nodeID in name2idDict.values():
'''
nodeList = sorted(name2idDict.values(),reverse=True)#.reverse()
flag = True
while flag:
    flag = False
    for nodeID in nodeList:
        #print nodeID
        EdgeCount = snap.CntEdgesToSet(G, nodeID, nodeSet)
        if EdgeCount < limit and G.IsNode(nodeID):
            G.DelNode(nodeID)
            flag = True
'''
nodeList = sorted(name2idDict.values(),reverse=True)#.reverse()
NIdColorH = snap.TIntStrH()
for nodeID in nodeList:
    #print nodeID
    EdgeCount = snap.CntEdgesToSet(G, nodeID, nodeSet)
    userEdgeCount[nodeID] = EdgeCount

    if EdgeCount < 2:
        NIdColorH[nodeID]="yellow"
        delNodeList.append(nodeID)
    elif 2<= EdgeCount < 5:
        NIdColorH[nodeID]="green"
    elif 5<= EdgeCount < 60:
        NIdColorH[nodeID]="blue"
    else:
        NIdColorH[nodeID] = "red"
for node in delNodeList:
    G.DelNode(node)
G.DelNode(38)

userEdgeCount = sorted(userEdgeCount.items(), lambda x, y: cmp(x[1], y[1]),reverse=True)

#for node in delNodeList:
#    G.DelNode(node)
#EdgeCount = snap.CntEdgesToSet(G, nodeID, nodeSet)
#print "Number of edges from %d to NodeSet in PNGraph = %d" % (nodeID, EdgeCount)

with open("fansTop100.csv","w") as outer:
    writer = csv.writer(outer,lineterminator='\n')
    writer.writerow(["id","user","count","link"])
    for i in range(100):
        item = userEdgeCount[i]
        id = item[0]
        user = id2nameDict[item[0]]
        ccount = item[1]
        link = userLink[user]
        #writer.writerow([item[0],id2nameDict[item[0]],item[1]])
        writer.writerow([id, user, ccount,link])
print("[+]Top users saved!")

print("[+]Drawing graph...")
#snap.DrawGViz(G, snap.gvlSfdp, "network---"+str(limit)+".png", "graph 3", True,NIdColorH)
snap.DrawGViz(G, snap.gvlSfdp, "network-fan.png", "follow", True,NIdColorH)
print("[+]Done!")


'''
G1 = snap.TUNGraph.New()
G1.AddNode(1)
G1.AddNode(2)
G1.AddNode(5)
G1.AddEdge(2, 5)
G1.AddEdge(1,5)
snap.DrawGViz(G1, snap.gvlSfdp, "network.png", "graph 3", True)
'''