import fpGrowth
rootNode = fpGrowth.treeNode('pyramid' , 9 , None)
rootNode.children['eye'] = fpGrowth.treeNode('eye',13,None)
print rootNode.disp()