# -*- coding: utf-8 -*-
from math import log
import operator
def calcShannonEnt(dataset): #计算香农熵
    numEntries = len(dataset) #计算样本个数
    labelCounts = {} #创建一个字典储存类别
    for featVec in dataset:
        currentLabel = featVec[-1] #一般数据最后一列都是分类情况
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel]+=1
    shannonEnt = 0.0 #香农熵
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries #计算当前类别在总类别里的概率
        shannonEnt -= (prob*log(prob,2))  #log(x,y)代表以y为底x的对数
    return shannonEnt

def createDataSet():
    dataSet = [
        [1,1,'yes'],
        [1,1,'yes'],
        [1,0,'no'],
        [0,1,'no'],
        [0,1,'no']
    ]
    labels = ['no surfacing' , 'flippers']
    return dataSet,labels
def splitDataSet(dataSet,axis,value): #三个参数：待划分的参数集，划分数据集的特征，需要返回的特征的值
    #按照第axis列作为参考划分出值为value的列表
    retDataSet = []#新创建一个列表 将符合要求的假如
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis] #按照axis划分参数集，把axis拿出去
            reducedFeatVec.extend(featVec[axis+1:]) #extend方法：得到一个新的列表
            retDataSet.append(reducedFeatVec)#append方法：得到包含a~b的列表
    return retDataSet
def chooseBestFeatureToSplit(dataSet): #选择最好的数据划分方式
    numFeature = len(dataSet[0])-1 #算出数据个数
    baseEntropy = calcShannonEnt(dataSet) #计算香农熵
    bestInfoGain = 0.0 ; bestFeature = -1
    for i in range(numFeature):
        featList = [example[i] for example in dataSet] #创建分类标签
        uniqueVals = set(featList) #去重
        nuwEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value) #划分比较
            prob = len(subDataSet)/float(len(dataSet)) #Di/D
            nuwEntropy += prob*calcShannonEnt(subDataSet)
        infoGain = baseEntropy - nuwEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature
def majorityCnt(classLIst) : #多数表决
    classCount = {}
    for vote in classLIst:
        if vote not in classCount.keys() : classCount[vote] = 0
        classCount[vote]+=1
    sortedClassCount = sorted(classCount.iteritems(),key = operator.itemgetter(1),reversed=True)
    return sortedClassCount[0][0] # 返回最适合定义的叶子节点

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet] #创建包含数据集所有类标签的列表
    if classList.count(classList[0]) == len(classList): #类别如果完全相同则停止继续划分
        return classList[0]
    if len(dataSet[0])==1 :#如果所有特征都被使用完，则利用投票方法选举出类标签返回
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet) # 获取最好的数据集划分方式
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat]) #删除结点递归
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues) #得到列表包含的所有属性值
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree
#python的pickle模块实现了基本的数据序列和反序列化。
# 通过pickle模块的序列化操作我们能够将程序中运行的对象信息保存到文件中去，永久存储；
# 通过pickle模块的反序列化操作，我们能够从文件中创建上一次程序保存的对象。
def storeTree(inputTree , filename): #
    import pickle
    fw = open(filename , 'w')
    pickle.dump(inputTree,fw) #将inputtree保存到fw中
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(filename) #从file里读取一个字符串并且把它重构为原来的对象


