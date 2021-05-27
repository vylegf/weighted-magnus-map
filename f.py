maxlen = 10
names = list('~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

#я собираюсь хранить сумму 4*x2*x3-x1*x6+8*x4*x5*x6
#в списке наподобие
#[{}, {(2,3):4,(1,6):-1}, {(4,5,6)
:8},...]



def str_series(i):
	return [{(i,):1}]
def inv_series(i):
	return list({(i,)*j: (-1)**j} for j in range(1,maxlen))
	
def copy_series(s):
	return list(x for x in s)

def destroy_zeros(s):
	for i,x in enumerate(s):
		for t in x:
			if x[t] == 0:
				d.pop(t)

def add_dictionary(d1,d2):#прибавляет d2 к d1
	for it in d2:
		if it in d1:
			d1[it] += d2[it]
			if d1[it] == 0:
				d1.pop(it)
		else:
			d1[it] = d2[it]

def add_series(s, adds):
	l1 = len(s)
	l2 = len(adds)
	for i in range(l2):
		if i >= l1:
			s.append(adds[i])
		else:
			add_dictionary(s[i],adds[i])
			
def sum_of_series(s1,s2):
	ans = copy_series(s1)
	add_series(ans,s2)
	return ans
	
def mul_dict_from_right(tup, d):
	ans = {}
	for x in d:
		ans[tup+x] = d[x]
	return ans
	
def left_mul(s, tup,count):
	if count == 0:
		return []
	deg = len(tup)
	else:
		ans = [{}]*deg
		l = deg
		for d1 in s:
			ans.append(left_mul_dict(tup,d1))
			l += 1
			if l == maxlen:
				break
	return ans


def mul_series(ser1, ser2):
	for dic in ser1:
		for x in dic:
			add_series(ser2, le
			ans = add_series(ans, left_mul(ser2,x,dic[x]))
			
'''
def mul_series(ser1, ser2):
	ans = []
	len1 = len(ser1)
	len2 = len(ser2)
	end = min(len1+len2, maxlen+1)
	for j in range(1, end):
		ansj = []
		if len(ser1) > j-1:
			print('{}+0={}: multiplying {} and 1'.format(j,j,ser1[j-1]))
			ansj += ser1[j-1]
			
		if len(ser2) > j-1:
			print('0+{}={}: multiplying 1 and {}'.format(j,j,ser2[j-1]))
			ansj += ser2[j-1]		
		for k in range(1, j):
			l = j-k
			if l >= len2:
				continue
			if k >= len1:
				break
			ft = ser1[k]
			st = ser2[l]
			print('{}+{}={}: multiplying {} and {}'.format(k,l,j,ft,st))
			ansj += list((c1*c2,p1+p2) for c1,p1 in ft for c2,p2 in st if c1*c2 != 0)
		print('{}th component of product: {}'.format(j,ansj))
		ans.append(ansj)
	return ans

def str_series(i):
	return [[(1,[i])]]

def inv_series(i):
	return list([((-1)**j,[i]*j)] for j in range(1,maxlen))

def print_series(ser,name='-'):
	if name == '-':
		print('printing unknown series')
	else:
		print('printing ' + name)
	print('deg=0: 1')
	totals = '1'
	for i,x in enumerate(ser):
		s=''
		for c,p in x:
			if len(p) == 0 or c == 0:
				continue
			if c > 0 and s != '':
				s += '+'
			if c == -1:
				s += '-'
			elif c != 1 and c != 0:
				s += str(c)
			for l in p:
				s += names[l]		
		if len(s) > 0:
			print('deg={}: '.format(i+1) + s)
		if len(s) > 0 and s[0] != '-':
			totals += '+'
		totals += s
		if i == maxlen:
			break
	print('total: ' + totals)
		
ser = [
[],
[(-4,[2,3]),(5,[1,6])],
[(8,[4,5,6])]
]

s1 = [[(1,[1]),(-3,[2])],[(1,[1,1])]]
s2 = s1
print_series(s1,name='s1')
print_series(s2,name='s2')
print_series(mul_series(s1,s2),name='s1*s2')

