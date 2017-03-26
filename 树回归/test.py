import regTrees
from numpy import *
MyDat = regTress.loadDataSet('ex00.text')
MyMat = mat(MyDat)
print regTrees.createTree(MyMat)