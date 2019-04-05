import Helper as hp 
import InitPopMethods as inPopMe
import GP
import Terminalset as ts
'''
a = inPopMe.rampinit(15,2,0,10,10,0.6)
for i in range(len(a)):
	a[i].polygon.plot()
	hp.drawtree(a[i].tree)'''

'''
[tree,lastnode] = GP.makeBlueTree(3,False,0,10,10)
tree = GP.genFullBlueTree(tree)
hp.drawtree(tree)


bluetree = GP.convertFullBluetree_to_oriBluetree(tree,True)
hp.drawtree(bluetree)
bluetree.valueofnode.plot()'''


'''
if tree.strname == 'Usubtree9':
    xxx = []
    for i in range(9):
        xxx.append(tree.childs[i].valueofnode)
else:
    xxx = []
    for i in range(7):
        xxx.append(tree.childs[i].valueofnode)'''

# test Lsubtree
'''
a = [-1,0.0739,-0.2973,0.3331,0.4497,0.3134,0.7034]
m = [-0.4,0.0739,-0.2973,0.3331,0.4497,0.3134,0.7034]
x = ts.Lsub_tree(10,10,2)
x.initchange(a)
x.polygon.plot()
print(x.strname)
x.change(m)
x.polygon.plot()
print(x.strname)'''
#test Usubtree.
xxx = [0.4, 0.5534, -0.6393, -0.7443, -0.0546, -0.1209, -0.5055, -0.2724, -0.2057]
m = [-0.4172, 0.5534,-0.6393, -0.7443, -0.0546, -0.1209, -1, -0.2724, -0.2057]
x = ts.Usub_tree(10,10,2)
x.initchange(xxx)
x.polygon.plot()
print(x.strname)
x.changeMaxXY([15,15])
x.polygon.plot()
print(x.strname)
#print(xxx)
'''
if len(xxx) == 9:
    #x = ts.Usub_tree(10,10,1)
    #x.initchange(xxx)
    #x.polygon.plot()
    bluetree = gfbt.convertFullBluetree_to_oriBluetree(tree,True)
    hp.drawtree(bluetree)
    #bluetree.valueofnode.plot()
else:
    #x = ts.Lsub_tree(10,10,1)
    #x.initchange(xxx)
    #x.polygon.plot()
    bluetree = gfbt.convertFullBluetree_to_oriBluetree(tree,True)
    hp.drawtree(bluetree)
    #bluetree.valueofnode.plot()'''
#x.change(m)
#x.polygon.plot()
#print(x.strname)

