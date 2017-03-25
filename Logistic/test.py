from numpy import *
import logRegres
dataArr , labelMat = logRegres.loadDataSet()
weights = logRegres.gradAscent0(array(dataArr),labelMat)
logRegres.plotBestFit(weights)
