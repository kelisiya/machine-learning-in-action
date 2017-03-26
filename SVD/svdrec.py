#-*- coding:utf-8 -*--
def loadExData():
    return[[0, 0, 0, 2, 2],
           [0, 0, 0, 3, 3],
           [0, 0, 0, 1, 1],
           [1, 1, 1, 0, 0],
           [2, 2, 2, 0, 0],
           [5, 5, 5, 0, 0],
           [1, 1, 1, 0, 0]]
def loadExData2():
    return[[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]

from numpy import *
from numpy import linalg as la
#三种相似度计算方法，这里假设inA和inB都是列向量
def eulidASim(inA,inB):
        return 1.0/(1.0+la.norm(inA-inB)) #这里运用了欧氏距离，方便相似度值再0~1之间变化

def pearsSim(inA,inB):
        if len(inA) < 3 : return 1.0
        return 0.5+0.5*corrcoef(inA,inB,rowvar=0)[0][1] #皮尔逊相关系数：取值范围归一化到0~1之间，以向量计算

def cosSim(inA,inB):
        num = float(inA.T*inB)
        denom = la.norm(inA)*la.norm(inB) #这里是默认为2范数
        return 0.5+0.5*(num/denom) #余弦相似度

def standEst(dataMat,user,simMeas,item): #给定相似度计算方法后，用户对物品的估计评分值
        #物品矩阵，用户编号，相似度计算方法，物品编号
        n = shape(dataMat)[1]#找出物品个数
        simTotal = 0.0 ; ratSimTotal = 0.0 #初始化估计评分值的两个变量
        for j in  range(n):
                userRating = dataMat[user,j]
                if userRating ==0 : continue #如果该物品评分为0，那么认为用户没有对物品评分
                overLap  = nonzero(logical_and(dataMat[:,item].A>0,
                                               dataMat[:,j].A>0))[0] #寻找两个物品已经被评分的那个
                if len(overLap) ==0 : similarity = 0
                else : similarity = simMeas(dataMat[overLap,item],dataMat[overLap,j])
                simTotal+=similarity
                ratSimTotal+=similarity*userRating #相似度和用户的成绩
        if simTotal ==0 : return 0 #相似度为0终止这次循环
        else : return ratSimTotal/simTotal#利用归一化

def recommend(dataMat,user,N=3,simMeans=cosSim,estMethod=standEst):
        #矩阵，用户，默认推荐前三个，默认采用余弦相似度，默认采用standEst估计方法
        unratedItems = nonzero(dataMat[user,:].A==0)[1]  #建立一个没有评分的表
        if len(unratedItems)==0 : return 'you rated everything' #不存在没有评分的物品就退出函数
        itemScores = []
        for item in unratedItems: #对每个没有评分的物品进行评分
                estimatedScore = estMethod(dataMat,user,simMeans,item)
                itemScores.append((item,estimatedScore)) #得出物品和物品的分数
        return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:N]

def svdEst(dataMat, user, simMeas, item):
    n = shape(dataMat)[1] #求出个数
    simTotal = 0.0; ratSimTotal = 0.0
    U,Sigma,VT = la.svd(dataMat) #svd分解
    Sig4 = mat(eye(4)*Sigma[:4]) #建立对角矩阵
    xformedItems = dataMat.T * U[:,:4] * Sig4.I  #构建转换后的物品
    for j in range(n):
        userRating = dataMat[user,j]
        if userRating == 0 or j==item: continue
        similarity = simMeas(xformedItems[item,:].T,xformedItems[j,:].T)  #构建评分系统,这里把计算方法嵌套了进去
        print 'the %d and %d similarity is: %f' % (item, j, similarity)
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0: return 0
    else: return ratSimTotal/simTotal