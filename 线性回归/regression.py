# -*- coding: utf-8 -*-
from numpy import *
def loadData(fileName):
    numFeat = len(open(fileName).readline().split('\t')) - 1 #通过这样的划分得到特征数
    #print "numFeat = " , numFeat
    dataMat = []  ; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t') #把一行划分为三个部分
        #print "curLine = " , curLine
        for i in range(numFeat):
            lineArr.append(float(curLine[i])) #把每行的前两个加入特征集里
        dataMat.append(lineArr)#加入特征集
        labelMat.append(float(curLine[-1])) #加入标签里
    return dataMat,labelMat

def standRegress(xArr,yArr):
    xMat = mat(xArr)
    yMat = mat(yArr).T
    xTx = xMat.T * xMat
    if linalg.det(xTx) == 0.0 :
        print  "this matrix is singular , cannot do inverse "
        return
    ws = xTx.I * (xMat.T * yMat) #结论：最小二乘法求最优解
    return ws

def lwlr(testPoint , xArr , yArr , k = 1.0):
    xMat = mat(xArr) ; yMat = mat(yArr).T
    m = shape(xMat)[0]
    weights = mat(eye((m)))
    for j in range(m):
        diffMat = testPoint  - xMat[j,:]
        weights[j,j] = exp(diffMat*diffMat.T / (-2.0*k**2))
    xTx = xMat.T * (weights*xMat)
    if linalg.det(xTx) == 0.0 :
        print "this matrix is singular , cannot do inverse "
        return
    ws = xTx.I * (xMat.T * (weights*yMat))
    return testPoint * ws

def lwlrTest(testArr,xArr , yArr , k= 1.0):
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i]  = lwlr(testArr[i],xArr,yArr,k)
    return yHat


def ridgeRegress(xMat,yMat ,lam = 0.2): #计算回归系数
    xTx = xMat.T * xMat #岭回归公式：w = (X.T * X + lambda*I)^-1 * X.T * y
    denom = xTx + eye(shape(xMat)[1])*lam
    if linalg.det(denom) == 0.0 : #判断行列式是否为0
        print "This matrix is singular , cannot do inverse "
        return
    ws = denom.T*(xMat.T*yMat)
    return ws

def ridgeTest(xArr,yArr):#测试数据集
    xMat = mat(xArr)
    yMat = mat(yArr).T
    yMean = mean(yMat,0)
    yMat = yMat - yMean
    xMeans = mean(xMat,0)
    xVar = var(xMat,0)
    xMat = (xMat - xMeans) / xVar #标准化操作：所有特征减去自己的均值并除以方差
    numTestPts = 30 #30个不同的lambda测试
    wMat = zeros((numTestPts,shape(xMat)[1]))
    for i in range(numTestPts):
        ws = ridgeRegress(xMat,yMat,exp(i-10)) #测试
        wMat[i,:] = ws.T#所有的回归系数加入矩阵返回结果
    return wMat

from time import sleep
import json
import urllib2
def searchForSet(retX,retY,setNum,yr,numPce,origPrc):
    sleep(10) #防止频繁访问
    myAPIstr = 'get from code.google.com'
    searchURL = 'https://www.googleapis,com/shopping/search/v1/public/products?\
                key=%s&country=US&q=lego+%d&alt=json' %(myAPIstr,setNum) #拼接URL，添加API信息和待查询的套装信息
    pg = urllib2.urlopen(searchURL) #访问url
    retDict = json.loads(pg.read()) #获取json数据
    for i in range(len(retDict['items'])):#按照item对物品进行搜索
        try:
            currItem = retDict['items'][i]
            if currItem['product']['condition'] == 'new':
                newFlag = 1
            else: newFlag = 0
            listOfInv = currItem['product']['inventories']
            for item in listOfInv:
                sellingPrice = item['price']
                if sellingPrice > origPrc * 0.5 :
                    print "%d\t%d\t%d\t%f\t%f\t" %(yr,numPce,newFlag,origPrc,sellingPrice)
                    retX.append([yr,numPce,newFlag,origPrc])
                    retY.append(sellingPrice)
        except:print 'problem with item %d' % i

def setDataCollect(retX,retY):
    searchForSet(retX, retY, 8288, 2006, 800, 49.99)
    searchForSet(retX, retY, 10030, 2002, 3096, 269.99)
    searchForSet(retX, retY, 10179, 2007, 5195, 499.99)
    searchForSet(retX, retY, 10181, 2007, 3428, 199.99)
    searchForSet(retX, retY, 10189, 2008, 5922, 299.99)
    searchForSet(retX, retY, 10196, 2009, 3263, 249.99)