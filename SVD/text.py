#-*- coding:utf-8 -*-
from numpy import *
import svdrec
myMat = mat(svdrec.loadExData2())
print svdrec.recommend(myMat,1,estMethod=svdrec.svdEst)
