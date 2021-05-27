from series_class import *

a1_dic = {(3,1):1,(1,3):-1}
a2_dic = {(4,1):1,(1,4):-1}
a3_dic = {(4,2):1,(2,4):-1}
a4_dic = {(5,2):1,(2,5):-1}
a5_dic = {(5,3):1,(3,5):-1}
b1_dic = {(4,5,2):1,(4,2,5):-1,(5,2,4):-1,(2,5,4):1}
b2_dic = {(3,5,2):1,(3,2,5):-1,(5,2,3):-1,(2,5,3):1}
b3_dic = {(1,5,3):1,(1,3,5):-1,(5,3,1):-1,(3,5,1):1}
b4_dic = {(3,4,1):1,(3,1,4):-1,(4,1,3):-1,(1,4,3):1}
b5_dic = {(2,4,1):1,(2,1,4):-1,(4,1,2):-1,(1,4,2):1}

def dcomm(d1,d2):
	return d1*d2-d2*d1

def tcomm(d1,d2):
	return d1*d2+d2*d1

a1 = DictComponent(a1_dic)
a2 = DictComponent(a2_dic)
a3 = DictComponent(a3_dic)
a4 = DictComponent(a4_dic)
a5 = DictComponent(a5_dic)
b1 = DictComponent(b1_dic)
b2 = DictComponent(b2_dic)
b3 = DictComponent(b3_dic)
b4 = DictComponent(b4_dic)
b5 = DictComponent(b5_dic)
x1 =  dcomm(a1,b1)
x2 =  dcomm(a2,b2)
x3 =  dcomm(a3,b3)
x4 =  dcomm(a4,b4)
x5 =  dcomm(a5,b5)
#print(a1)
#print(b1)
#print(x1)
#print(x2)
#print(x3)
#print(x4)
#print(x5)
print(x1+x2+x3-x4-x5)
print('')
y1 =  dcomm(b1,b3)
y2 =  dcomm(b2,b4)
y3 =  dcomm(b3,b5)
y4 =  dcomm(b4,b1)
y5 =  dcomm(b5,b2)
#print(y2-y1+y3-y4-y5)
print('')
z1 =  dcomm(dcomm(a2,a4),a5)
z2 =  dcomm(dcomm(a3,a5),a1)
z3 =  dcomm(dcomm(a1,a4),a3)
z4 =  dcomm(dcomm(a2,a4),a1)
z5 =  dcomm(dcomm(a2,a5),a3)
#print(z1+z2-z3-z4+z5)
print(y2-y1+y3-y4-y5+z1+z2-z3-z4+z5)

#print('[a1,b1]='+str(x1))
#print('[a2,b2]='+str(x2))
#print('[a3,b3]='+str(x3))
#print('[a4,b4]='+str(x4))
#print('[a5,b5]='+str(x5))'''