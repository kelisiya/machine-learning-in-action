#-*- coding:utf-8 -*-
class treeNode:
    def __init__(self,nameValue,numOccur,parentNode): #存放节点名字的变量和计数值
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None #类似于链表指针
        self.parent = parentNode #指向当前父节点
        self.children = {} #存放节点的子节点

    def inc(self,numOccur):
        self.count += numOccur

    def disp(self,ind=1): #将节点以文本的形式显示
        print " "*ind , self.name , ' ' , self.count
        for child in self.children.values():
            child.disp(ind+1)

    def createTree(dataSet,minSup = 1):
        headerTabel = {}
        for trans in dataSet:
            for item in trans:
                headerTabel[item] = headerTabel.get(item,0) + dataSet[trans]
        for k in headerTabel.keys():
            if headerTabel[k] < minSup:
                del (headerTabel[k]) #如果不满足最小支持度，删除
        freqItemSet = set(headerTabel.keys()) #去重
        if len(freqItemSet)==0 : return None,None
        for k in headerTabel:
            headerTabel[k] = [headerTabel[k],None]
        retTree = treeNode('Null Set',1,None)
        for tranSet , count in dataSet.items():  #根据全局频率对每个事物中的元素进行排序
            localID = {}
            for item in tranSet:
                if item in freqItemSet:
                    localID[item] = headerTabel[item][0]
            if len(localID) > 0 :
                orderedItem[ v[0] for v in sorted(localID.items(),key=lambda p:p[1],reversed=True)]
                updateTree(orderedItem,retTree,headerTabel,count) #使用排序后的频繁项集填充
        return retTree,headerTabel

    def updateTree(items,inTree,headerTable,count):
        if items[0] in inTree.children:
            inTree.children[items[0]].inc(count)
        else:
            inTree.children[items[0]] = treeNode(items[0],count,inTree)
            if headerTable[items[0]][1] == None:
                headerTable[items[0]][1] = inTree.children[items[0]]
            else:
                updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
        if len(items) > 1:
            updateTree(items[1::],inTree.children[items[0]],headerTable ,count)

    def updateHeader(nodeToTest,targetNode):
        while(nodeToTest.nodeLink != None ):
            nodeToTest = nodeToTest.nodeLink
        nodeToTest.nodeLink = targetNode

    def mineTree(inTree,headerTable,minSup,preFix,freqItemList):
        bigL = [v[0] for v in sorted(headerTable.items() , key= lambda p:p[1])]

        for basePat in bigL:
            newFreqSet = preFix.copy()
            newFreqSet.add(basePat)

