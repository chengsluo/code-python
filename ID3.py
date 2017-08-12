#ID3决策树算法
#决策树的构造

from math import log
import operator


'计算给定数据集的 信息熵——度量无序程度'
def calcEnt(dataSet):
    numEntries = len(dataSet)    #实例中的总数
    labelCounts ={}              #创建一个字典
    '为所有可能分类创建字典，key:标签 value:次数'
    for featVec in dataSet:
        currentLabel = featVec[-1]   #保存特征（label 翻译成标签或标记都可)
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] +=1
    '以2为底求对数，计算信息熵'
    Entropy = 0.0   #信息熵
    for key in labelCounts:   #计算信息熵
        prob = float(labelCounts[key])/numEntries #每种类别的概率
        Entropy -= prob * log(prob,2)
    return Entropy


'按照特定特征划分数据集'
def splitDataSet (dataSet,axis,value):
    #dataSet:待划分的数据集    axis:划分数据集的特性   value:特征的返回值
    retDataSet = []    #创建新的list对象
    for featVec in dataSet:
        if featVec[axis] == value: #发现符合要求的值
            #'抽取',删除dataSet中的第axis列
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

'对每个特征划分数据集的结果计算一次信息熵，'
'然后判断按照哪个特征（或称属性）划分数据集是最好的划分方式——计算信息增益，信息增益越大，"纯度提升"越大'

'选择最好的数据集划分方式'
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1   #记录有几个特征值
    baseEntropy = calcEnt(dataSet)      #初始信息熵
    bestInfoGain = 0.0                  #保存最好的信息增益
    bestFeature = -1                    #索引值
    for i in range(numFeatures):  #遍历数据集中的所有特征(0~numFeatures-1)
        '创建唯一的分类标签列表'
        featList = [example[i] for example in dataSet]
        #数据集中所有第i个特征值或所有可能存在的值写入featList
        uniqueVals = set(featList)      #变为set,删去重复的值
        newEntropy = 0.0
        '计算每种划分方式的信息熵'
        for value in uniqueVals:        #遍历当前特征中的所有唯一属性值
            subDataSet = splitDataSet(dataSet,i,value) #每个特征划分一次数据集
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcEnt(subDataSet)   #计算新的熵,并求和
        infoGain = baseEntropy - newEntropy #信息增益    这部分的计算公式详见西瓜树p74
        '计算最好的信息增益(信息增益越大，纯度提升越大)'
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature  #返回最好特征划分的索引值

'类标签仍不唯一时，多数表决算法决定叶子节点的分类'
def majorityCnt(classlist):
    classcount={}
    for vote in classcount:
        if vote not in classcount.keys():
            classcount[vote] = 0
        classcount[vote] += 1
    sortedClassCount = sorted(classcount.__iter__(),
    key = operator.itemgetter(1),reversed=True)
    return sortedClassCount[0][0]

'创建决策树'
def createTree(dataSet,labels):  #数据集 和 特征列表（包含数据集中所有特征的标签）
    classList = [example[-1] for example in dataSet] #保存数据集每个样例的标签
    '类别完全相同停止划分'
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    '遍历完所有特征时返回出现次数最多的'
    if len(dataSet[0]) == 1:      #所有的特征都用完了，仍不能将数据集划分成仅包含唯一类别的分组
        return majorityCnt(classList)
    '创建树'
    bestFeat = chooseBestFeatureToSplit(dataSet)    #获得最好的划分的索引值
    bestFeatLabel = labels[bestFeat]                #信息增益最大的特征
    print(labels)                                     # 演示 特征列表 被挑选过程
    print(bestFeatLabel)
    myTree = {bestFeatLabel:{}}                     #字典变量myTree
    del(labels[bestFeat])                          #特征列表中删除已经划分好的某个特征
    featValues = [example[bestFeat] for example in dataSet] #列表中存每个样例中该特征的值
    uniqueVals = set(featValues)                    #变为集合，删去重复的值
    '遍历当前选择特征的所有属性值，在每个数据集划分上 递归调用createTree'
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

'建立一个数据'
def createDataSet():
    dataSet = [
        ['重要', '高', '大', '低', '高', 'A'],
        ['中等', '高', '中', '低', '中', 'A'],
        ['一般', '中', '大', '低', '高', 'A'],
        ['一般', '高', '小', '高', '低', 'B'],
        ['一般', '中', '中', '低', '中', 'C'],
        ['一般', '高', '中', '低', '中', 'B'],
        ['重要', '中', '大', '中', '高', 'A'],
        ['一般', '高', '大', '高', '高', 'A'],
        ['一般', '中', '大', '高', '高', 'A'],
        ['一般', '中', '大', '低', '高', 'A'],
        ['中等', '高', '大', '低', '高', 'A'],
        ['中等', '中', '中', '低', '高', 'B'],
        ['一般', '高', '大', '低', '低', 'B'],
        ['一般', '高', '小', '低', '高', 'C'],
        ['中等', '中', '中', '低', '低', 'C'],
        ['重要', '高', '大', '中', '低', 'A'],
        ['一般', '低', '中', '高', '高', 'C'],
        ['一般', '低', '中', '低', '高', 'C'],
        ['一般', '中', '小', '中', '高', 'B'],
        ['低', '高', '大', '低', '中', 'C'],
    ]
    labels = ['社会重要性','用电可靠性','用电量','电价高低','客户信用','客户分类']    #这里的labels 指 特征列表
    return dataSet,labels

if __name__ == '__main__':
     myDat,labels = createDataSet()
     print(createTree(myDat,labels))
