#-*- coding:utf-8 -*-
from numpy import *

def loadDataSet(fileName , delim = '\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()] #这姿势真是太高大上了
    datArr = [map(float,line) for line in stringArr] #类型转换
    return mat(datArr)

def pca(dataMat , topNfeat = 9999999):
    meanVals = mean(dataMat,axis=0) #求矩阵的平均值
    meanRemoved = dataMat - meanVals
    covMat = cov(meanRemoved,rowvar=0) #求协方差矩阵
    eigVals , eigVects  = linalg.eig(mat(covMat)) #计算特征值和特征向量
    eigValInd = argsort(eigVals) #从小到大排序
    eigValInd = eigValInd[:-(topNfeat+1):-1] #选取最大的前topNfeat个，默认9999999,这里是反向选取
    redEigVect = eigVects[:,eigValInd]
    lowDDataMat = meanRemoved*redEigVect #转换空间
    reconMat = (lowDDataMat *redEigVect.T ) + meanVals
    return lowDDataMat , reconMat  #返回重构后的原始数据和降维后的数据

def replaceNanWithMean(): #处理NaN值，这里采取平均值法
    dataMat = loadDataSet('secom.data' , ' ')
    numFeat = shape(dataMat)[1] #计算出特征数目
    for i in range(numFeat): #对每个特征计算非NaN的均值
        meanVal = mean(dataMat[nonzero(~isnan(dataMat[:,i].A))[0],i]) #不是NAN的所有值的平均值
        dataMat[nonzero(isnan(dataMat[:,i].A))[0],i] = meanVal
    return dataMat
