from series_class import *
a1 = Comm(3,1)
a1_inv = Comm(1,3)
b1 = InvSeries(4)*Comm(2,5)*StrSeries(4)*Comm(5,2)
b1_inv = Comm(2,5)*InvSeries(4)*Comm(5,2)*StrSeries(4)
print(a1_inv*b1_inv*a1*b1)
#print(a1)
#print(b1)