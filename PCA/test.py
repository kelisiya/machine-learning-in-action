#-*- coding:utf-8 -*-
from numpy import *
import pca
import matplotlib.pyplot as plt
dataMat = pca.replaceNanWithMean()
meanVal = mean(dataMat,axis=0) #均值
meanRemoved = dataMat  - meanVal #尽力归零化
covMat = cov(meanRemoved,rowvar=0) #协方差矩阵
eigVals , eigVects = linalg.eig(mat(covMat)) #特征值分析
print eigVals #检查特征值：发现大部分都是0，还有四舍五入造成的负数，只有前15个是大于10^5信息量很大

