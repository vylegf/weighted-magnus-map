maxlen = 12
names = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#weights = [1]+[2]*7+[3]*10+[4]*4
weights = [1]+[2]*8+[3]*12+[4]*40

#weights=[1]+[2]*6+[3]*10
#weights = [1]*50

#weights = [1,2,2,2,2,2,3,3,3,3,3]
#weights = [1,2,3,2,2,3,1,1,1,1,1]
#weights = [1,2,2,2,3,3,3,3,3,3,3,3]
#weights = [1,3,3,3,3,3,10,10,10,10,10]
#weights = [1,10,10,10,10,10,3,3,3,3,3]
def copy_dict(dic):
	ans = {}
	for x in dic:
		ans[x] = dic[x]
	return ans

#{[1,3,1]:-6} -> -6aca
class DictComponent:
	def __init__(self,something=''):
		if type(something) == type('') and something == '':
			self.dic={}
			return
		if type(something)==type({}):
			self.dic=copy_dict(something)
			return
		elif type(something) == type(DictComponent()):
			self.dic = copy_dict(something.dic)

		else:
			print("error: non-dict type in DictComponent's constructor!")
			return

	def add_elem(self, elem, count):
		if elem in self.dic:
			if count == -self.dic[elem]:
				self.dic.pop(elem)
			else:
				self.dic[elem] += count
		else:
			self.dic[elem] = count

	def mul_right(self, elem, count):
		if count == 0:
			self.dic = {}
			return
		newdic = {}
		for x in self.dic:
			newdic[x+elem] = dic[x]*count
		self.dic = newdic
	
	#DictComponent + DictComponent:
	#{[1,3,1]:-6} + {[2,3,1]:3} = {[1,3,1]:-6,[2,3,1]:3}
	
	#DictComponent + list:
	#{[1,3,1]:-6} + [1,3,1] = {[1,3,1]:-5}
	
	#DictComponent + tuple:
	#{[1,3,1]:-6} + ([1,3,1],5) = {[1,3,1]:-1}
	def __add__(self, other):
		ans = DictComponent(self)
	
		if type(other) == type(DictComponent()):
			for x in other.dic:
				ans.add_elem(x,other.dic[x])
		elif type(other) == type([]):
			ans.add_elem(other,1)
		elif type(other) == type((1,)):
			ans.add_elem(other[0],other[1])
		return ans

	def __sub__(self, other):
		ans = DictComponent(self.dic)
	
		if type(other) == type(DictComponent()):
			for x in other.dic:
				ans.add_elem(x,-other.dic[x])
		elif type(other) == type([]):
			ans.add_elem(other, -1)
		elif type(other) == type((1,)):
			ans.add_elem(other[0],-other[1])
		return ans


	#DictComponent * DictComponent:
	#{[1]:2} * {[2,3]:5} = {[1,2,3]:10}

	#DictComponent * list:
	#{[1,3,1]:-6} * [3] = {[1,3,1,3]:-6}


	#DictComponent * tuple:
	#{[1,3,1]:-6} * ([3],5) = {[1,3,1,3]:-30}
	def __mul__(self, other):
		ans = DictComponent(self.dic)
		if type(other) == type(DictComponent()):
			return component_product(self,other)
		elif type(other) == type([]):
			ans.mul_right(other,1)
		elif type(other) == type((1,)):
			ans.mul_right(other[0],other[1])
		return ans

	def __eq__(self, other):
		return (self.dic == other.dic)

	def __str__(self):
		ans = ''

		for x in self.dic:
			count = self.dic[x]
			if count == 0:
				continue
			if count > 0:
				ans += '+'
			if count == -1:
				ans += '-'
			elif count != 1:
				ans += str(count)
			for a in x:
				ans += names[a]

#		if len(ans) > 0 and ans[0] == '+':
#			ans = ' '+ans[1:]
		return ans

def component_product(comp1,comp2):
	ans = DictComponent()
	for x in comp1.dic:
		for y in comp2.dic:
			ans.add_elem(x+y, comp1.dic[x]*comp2.dic[y])
	return ans

class Series:
	def __init__(self):
		self.data = [DictComponent() for i in range(maxlen)]

	def __init(self, other):
		self.data = [DictComponent(x) for x in other.data]

	def __add__(self, other):
		ans = Series()
		for i in range(maxlen):
			ans.data[i] = self.data[i] + other.data[i]
		return ans

	def __sub__(self, other):
		ans = Series()
		for i in range(maxlen):
			ans.data[i] = self.data[i] - other.data[i]
		return ans

	def __mul__(self,other):
		if type(other) == type((0,)):
			self.mul_by_monom(other[0], other[1])
		elif type(other) == type([]):
			self.mul_by_monom(other,1)
		elif type(other) == type(Series()):
			ans = Series()
			ans = ans + self
	
			ans = ans + other
			for i in range(1,maxlen):
				for j in range(1, maxlen-i):
					comp1 = self.data[i]
					comp2 = other.data[j]
					ans.data[i+j] +=  comp1 * comp2
			return ans


	def __eq__(self,other):
		for i in range(1, maxlen):
			if self.data[i] != other.data[i]:
				return False
		return True
	def __ne__(self,other):
		return not (self == other)

	def __str__(self):
		ans = ' 1\n'
		for x in self.data:
			add = str(x)
			if add != '':
				ans += str(x)
				ans += '\n'
		return ans[:3000]
#		return ans[:-1]


def StrSeries(i):
	ans = Series()
	ans.data[weights[i]] = DictComponent({(i,):1})
	return ans

def InvSeries(i):
	ans = Series()
	w = weights[i]
	for j in range(1, maxlen//w):
		ans.data[j*w] = DictComponent({(i,)*j:(-1)**j})
	return ans

st=[StrSeries(i) for i in range(1,8)]
inv=[InvSeries(i) for i in range(1,8)]

def Comm(i,j):
	return inv[i]*inv[j]*st[i]*st[j]

#a_i^-1 * a_j * a_i
def Conj(i,j):
	return inv[i]*st[j]*st[i]