# -*- coding: utf-8 -*-
from numpy import *
def loadDataSet():
    dataMat = [] ; labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split() #划分数据
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX)) #返回sigmod的值

def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn) #转换数据类型为numpy的矩阵数据类型
    labelMat = mat(classLabels).transpose() #同理 并且为了下一步要转置
    m,n = shape(dataMatrix) #获取行列
    alpha = 0.001
    maxCycles = 500 #迭代次数
    weights = ones((n,1)) #这里先把回归系数初始化为1
    for k in range(maxCycles):
        h = sigmoid(dataMatrix*weights) # 预测函数 : h = g(Z) = 分类器输入数据 * 回归系数
        error = (labelMat - h) #这里是梯度上升的写法,每一步的迭代计算而不是列综合式
        weights = weights  + alpha*dataMatrix.transpose()*error
    return weights #返回最优系数

def gradAscent0(dataMatrix,classLabels):#随机梯度上升
    m,n = shape(dataMatrix)#求出行，列
    alpha = 0.01 #步长为0.01
    weights = ones(n) #最优化系数初始化为1，后面的根据样本数据调整
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i]*weights))
        #当前样本的预测值，一次只有一个样本更新
        #dataMartrix[i]*weights也为当前样本行乘以weights
        error = classLabels[i] - h #此处误差为一个值，而不是向量
        weights = weights + alpha*error*dataMatrix[i] #只对当前样本的最优系数更新
    return weights
#随机梯度上升是建立在‘在线算法’上的‘批处理’算法，一次仅用一个样本点，
def plotBestFit(weights):#接受最优系数画出决策边界
    import matplotlib.pyplot as plt
    dataMat , labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0] #提取行数
    xcord1 = [] ; ycord1 = [] #储存第一列坐标信息
    xcord2 = [] ; ycord2 = [] #储存第二列坐标信息
    for i in range(n):
        if int(labelMat[i]==1) : #如果特征为1
            xcord1.append(dataArr[i,1]) ; ycord1.append(dataArr[i,2]) #把第i行两个特征存起来
        else:
            xcord2.append(dataArr[i,1]) ; ycord2.append(dataArr[i,2]) #同理
    fig = plt.figure() #创建图
    ax = fig.add_subplot(111) #add_subplot(x,y,z) 代表把一块图分为x行y列从左到右从上到下第z块
    ax.scatter(xcord1,ycord1, s= 30 , c = 'red' , marker = 's') #形状
    ax.scatter(xcord2,ycord2, s= 30 , c = 'green')
    x = arange(-3.0,3.0,0.1) #代表从线从-3到+3，单位为0.1
    y = (-weights[0]-weights[1]*x)/weights[2] #这里设定 0 = w0*x0+w1*x1+w2*x2，即sigmod = 0 ，x0=1，解出分割线方程
    ax.plot(x,y) #线段为x，斜率为y
    plt.xlabel('X1'); plt.ylabel('X2')
    plt.show()






