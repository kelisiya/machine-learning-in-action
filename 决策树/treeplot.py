# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
#定义文本框和箭头格式
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

#绘制带箭头的注解
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)
#def createPlot():
 #   fig = plt.figure(1, facecolor='white')
  #  fig.clf()#绘制并且清空图
   # createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
   # plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode) #绘制两个不同的节点
    #plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
    #plt.show()

def getNumLeafs(myTree): #获取叶节点个数：利用字典存树信息
    numLeafs = 0
    firstStr = myTree.keys()[0] #从父节点开始可以遍历整棵树
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict': #判断数据类型是不是字典类型
            numLeafs += getNumLeafs(secondDict[key]) #递归调用累计叶子节点个数，返回值
        else:
            numLeafs+=1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = myTree.keys()[0]#获取父节点
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key]) #遍历到达叶子节点，递归返回，深度加一
        else:
            thisDepth = 1
        if thisDepth > maxDepth : maxDepth = thisDepth #三目运算符：比较当前最深，求出最大深度
    return maxDepth

def retrieveTree(i):
    listOfTrees =[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                  ]
    return listOfTrees[i]

def plotMidText(cntrpt , parentpt , txtString): #在节点之间填充信息
    xMid = (parentpt[0]-cntrpt[0]) / 2.0 + cntrpt[0] #父子节点x轴的平均
    yMid = (parentpt[1]-cntrpt[1])/2.0 + cntrpt[1]  #父子节点y轴的平均
    createPlot.ax1.text(xMid,yMid,txtString)

def plotTree(myTree, parentPt, nodeTxt):#画图主函数：
    numLeafs = getNumLeafs(myTree)  #求出节点个数
    depth = getTreeDepth(myTree)#求出节点深度
    firstStr = myTree.keys()[0]     #
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#判断子节点是不是字典类型决定是否继续划分
            plotTree(secondDict[key],cntrPt,str(key))
        else:   #画出节点
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(inTree, (0.5,1.0), '')
    plt.show()