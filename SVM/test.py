import SVM
dataArr , labelArr = SVM.loadDataSet('testSet.txt')
b,alphas = SVM.smoSimple(dataArr,labelArr,0.6,0.001,40)
print b
print alphas[alphas>0] #这里是因为0元太多只观察大于0的