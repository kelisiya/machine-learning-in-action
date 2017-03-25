#-*- coding:utf-8 -*-
import kMeans
from numpy import *
datamat = mat(kMeans.loadDataSet('testSet.txt'))
centList , myNewAssments = kMeans.biKmeans(datamat,3) #每次给出四个质心，三次迭代后收敛
print centList