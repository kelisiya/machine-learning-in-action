# -*- coding:utf-8 -*-
from numpy import *
def loadDataSet():#测试集
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1] #1代表侮辱性文字，0代表正常语言；并且之所以有6个是因为6组测试并且分别为正常言论和带有侮辱性的
    return postingList,classVec #返回第一个是切分好的文档集合，第二个是分类标签
#这些文本的类别由人工标注，标注信息用于训练程序以便自动检测侮辱留言

def creatVocabList(dataSet): #对数据集切换为向量集
    vocabSet = set([]) #创建一个空集
    for document in dataSet:
        vocabSet = vocabSet | set(document) #并集操作
    return list(vocabSet) #得到的是一个去重过的单词集

def setOfWords2Vec(vocabList , inputSet): #函数输入文档，输出文档向量（1 or 0）表示该词在输入文档是否出现
    returnVec = [0]*len(vocabList) #创建一个其中所含元素都为0的向量（初始化）
    for word in inputSet:#遍历，如果出现了词汇表中的单词，变为1.这样就不用在检查单词是否在vocablist中了
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word : %s is not in my vocabulary!" % word
    return returnVec

def trainNB0(trainMatrix,trainCategory):#文档矩阵，类别标签构成的向量
    numTrainDocs = len(trainMatrix) #先得到测试矩阵的长度
    numWords = len(trainMatrix[0]) #单词个数
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords) ; p1Num = ones(numWords) #初始化概率
    p0Denom = 2.0 ; p1Denom = 2.0 #防止概率为0的时候让累乘概率为0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1 :
            p1Num += trainMatrix[i] #向量相加
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)#为了避免python下溢出，ln(a*b) = ln(a) + ln(b)
    p0Vect = log(p0Num/p0Denom)
    return p0Vect,p1Vect,pAbusive #出现负值是正确的，不影响最终结果
#f(x) 和 ln(f(x)) 会一块增大，这表明想求函数的最大值的时候，可以使用该函数的自然对数替换原函数求解
#拉普拉斯平滑：当某个条件概率为0，这样在贝叶斯定理中分子分母都为0，为了避免这种情况，使用该定理
#分子+1，分母加X^i , 可能出现的种类数，这里仅仅让词出现次数为1，分母初始化为2，又名+1平滑

def classifyNB(vec2Classify , p0Vec, p1Vec , pClass1) :#贝叶斯分类函数：要分类的向量和三个概率
    p1 = sum(vec2Classify*p1Vec) + log(pClass1) #元素相乘 , 是求两个向量中的第1,2,3...个元素对应相乘，再相加，
    p0 = sum(vec2Classify*p0Vec) + log(1.0-pClass1) #在加上类别的对数函数，返回大概率对应的
    if p1>p0: #选择(x,y)点的概率偏向于哪一方
        return 1
    else:
        return 0

def testingNB(): #封装操作
    listOPosts , listClasses = loadDataSet()
    myVocabList = creatVocabList(listOPosts)#构建自己的单词表
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
    p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses))

    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as : ', classifyNB(thisDoc, p0V, p1V, pAb)

    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as : ', classifyNB(thisDoc, p0V, p1V, pAb)


