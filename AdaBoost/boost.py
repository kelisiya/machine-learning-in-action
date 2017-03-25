# -*- coding: utf-8 -*-
import adaboost
from numpy import *
dataArr , labelArr = adaboost.loadDataSet('horseColicTraining2.txt')
classfierArray = adaboost.adaBoostTrainDS(dataArr,labelArr,10)
testArr , testlabelArr = adaboost.loadDataSet('horseColicTest2.txt')
prediction10 = adaboost.adaClassify(testArr,testlabelArr)