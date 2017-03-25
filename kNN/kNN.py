# -*- coding: utf-8 -*-
from numpy import *
import operator
def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels

def classify0(inX , dataSet , labels, k): #4个输入参数分别为：用于分类的输入向量inX，输入的训练样本集dataSet，标签向量labels，选择最近邻居的数目k
    dataSetSize = dataSet.shape[0]#把行数求出来
    diffMat = tile(inX , (dataSetSize,1) ) - dataSet #tile是将inx数组重复n次,把相对距离的x y 求出来
    sqDiffMat = diffMat**2 #表示乘方，diffMar^2
    sqDistance = sqDiffMat.sum(axis=1) #axis = 1代表行向量相加， 0就是普通的求和
    distance = sqDistance**0.5#距离
    sortedDisIndicies = distance.argsort() #np排序，代表的是返回从小到大排序的下标
    classCount = {}
    for i in range(k):#选择距离最近的k个点
        voteIlabel = labels[sortedDisIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1 #get返回指定键的值，否则返回默认值
    sortedClasscount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True) #排序
    return sortedClasscount[0][0]

def file2matrix(filename):#讲文本记录解析为Numpy的解析程序
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines,3)) #填充0，另一纬度设置为固定的3
    classLabelVector = [] #把分类labels存为列表
    index = 0
    for line in arrayOLines:
        line = line.strip() #去除最右端回车
        listFromLine = line.split('\t') #用空格把字符串分成列表
        returnMat[index,:] = listFromLine[0:3] #选取前三个特征存到特征矩阵里，然后index自加
        classLabelVector.append(int(listFromLine[-1])) #将每行样本数据的最后一个数据加入类标签向量中
        index+=1
    return returnMat,classLabelVector #返回训练样本矩阵和类标签向量

def autoNorm(dataSet):#输入为数据集数据
    minVals = dataSet.min(0)#获得数据每列的最小值,minval是个列表
    maxVals = dataSet.max(0)#获得数据每列的最大值,maxval是个列表
    ranges = maxVals - minVals#获得取值范围
    normDataSet = zeros(shape(dataSet)) #初始化归一化数据集
    m = dataSet.shape[0]#得到行
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet = normDataSet/tile(ranges,(m,1)) #特征值相除
    return normDataSet,ranges , minVals#返回归一化矩阵，取值范围， 最小值

def datingClassTest():
    hoRatio = 0.10 #测试数据占总样本的10%
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt') #样本集，样本标签
    normMat , ranges , minVals = autoNorm(datingDataMat) #归一化处理样本集，然后得到取值范围和最小值
    m = normMat.shape[0]#样本集行数
    numTestVecs = int(m*hoRatio) #测试样本集的数量
    errorCount = 0.0#初始化错误率
    for i in range(numTestVecs):#对样本集进行错误收集
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m], 3)#kNN
        print("The classifier came back with : %d , the real answer is : %d" % (classifierResult,datingLabels[i]))
        if(classifierResult!=datingLabels[i]):
            errorCount+=1.0
    print("the total error rate if :%f" % (errorCount/float(numTestVecs)))#计算错误率并输出
#自定义分类器：输入信息并得出结果
def classfyPerson():
    resultList = ['not at all' , 'in small doese ' , 'in large dose'] #分类器
    precentTats = float(raw_input("precentage of time spent playint video games?")) #输入数据
    ffMiles = float(raw_input("frequent flier miles earned per year"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat , datingLabels = file2matrix('datingTestSet2.txt') #训练集
    normMat , ranges , minVals =  autoNorm(datingDataMat) #进行训练
    inArr =array([ffMiles,precentTats,iceCream]) #把特征加入矩阵
    #4个输入参数分别为：用于分类的输入向量inX，输入的训练样本集dataSet，标签向量labels，选择最近邻居的数目k
    classfierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3) #归一化处理矩阵，并且结果就是序列号-1就是对应
    print "You will probably like this person : " , resultList[classfierResult - 1 ]