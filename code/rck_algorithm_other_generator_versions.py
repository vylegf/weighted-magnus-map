import networkx as nx
import matplotlib.pyplot as plt
import itertools as it
import sys
import time

finaldict={}
sorteddict={}
maxtopdict={}

#вложенный коммутатор вида (a,(b,(c,(d,e)))) (или обратный к нему)
#elems = [a,b,c,d,e]
class Comm:
	__slots__ = ['elems', 'invert']

	def __init__(self, *args):
		if len(args) == 0:
			print('error: zero arguments in Comm.__init__()')
			return

		if len(args) == 1:
			self.elems = args[0]
			self.invert = False
			return
#		if len(args) == 1:
#			self.elems  = args[0].elems[:]
#			self.invert = args[0].invert
#			return

		if len(args) == 2:
			elems, invert = args
			self.elems  = elems[:]
			self.invert = invert
			return

		print('error: too many args in Comm.__init__(*args)')

	def __hash__(self):
		return hash(tuple([self.invert]+self.elems))

	def __len__(self):
		return len(self.elems)

	def __neg__(self):
		return Comm(self.elems, not self.invert)

	def __eq__(self,other):
		return self.elems == other.elems and self.invert == other.invert

	#(a,K) -> K; (a,b) -> error
	def Inner(self):
		if len(self) > 2:
			return Comm(self.elems[1:], self.invert)
		else:
			print('something is wrong: called Comm.Inner(), but len(Comm) <= 2.')
			return

	def StringForm(self):
		if len(self) < 2:
			print('something is wrong: len(Comm)<2.')
			return
		let = chr(ord('a')+len(self)-2)
		return let + '_{' + ''.join(map(str,self.elems)) + '}'
#		if len(self) == 2:
#			return '({},{})'.format(self.elems[0], self.elems[1])
#		else:
#			return '({},{})'.format(self.elems[0], self.Inner().StringForm())

	def __str_(self):
#		ans = 'Comm'+self.StringForm()
		ans = self.StringForm()
		if self.invert:
			ans += '^{-1}'
		return ans

	def __repr__(self):
		ans = self.StringForm()
		if self.invert:
			ans += '^{-1}'
		return ans

#слово от вложенных коммутаторов (letters - список элементов типа Comm)
class Word:
	__slots__ = ['letters']

	def __init__(self, *args):
		if len(args) == 0:
			self.letters = []
			return

		if len(args) == 1:
			self.letters = args[0].letters[:]
			return

		if len(args) == 2:
			K, invert = args
			if not invert:
				self.letters = [K]
			else:
				self.letters = [-K]
			return

		print('error: too many args in Word.__init__(*args)')

	def __eq__(self, other):
		return (self.letters == other.letters)

	def __len__(self):
		return len(self.letters)

	def __add__(self,other):
		ans = Word()
		ans.letters = self.letters[:]
		for L in other.letters:
			if len(ans.letters) > 0 and ans.letters[-1] == -L:
				ans.letters = ans.letters[:-1]
			else:
				ans.letters += [L]
		return ans

	def __sub__(self,other):
		return self + (-other)

	def __neg__(self):
#		if not len(self):
#			return Word()
		return LTW([-let for let in reversed(self.letters)])

	def __repr__(self):
#		return 'Word['+''.join(str(K) for K in self.letters)+']'
		return ''.join(str(K) for K in self.letters)

	def __str__(self):
#		return 'Word['+''.join(str(K) for K in self.letters)+']'
		return ''.join(str(K) for K in self.letters)

#-------------------------------------------------------------------------------------
#                 простейшие операции
#-------------------------------------------------------------------------------------

#делает из коммутатора однобуквенное слово
def CTW(K):
	return Word(K,False)

def LTW(lets):
	ans = Word()
	ans.letters = lets
	return ans
#	ans = Word()
#	for lt in lets:
#		ans += CTW(lt)
#	return ans

#считает (g,K)
def Comm_CL(g,K):
	#tcomm=(g,|K|)
	tcomm = CTW(Comm([g]+K.elems))
	if not K.invert:
		return tcomm
	else:
		#Если K=L^{-1}, то (g,K)=K^{-1}(g,L)^{-1}K
		return -CTW(K)-tcomm +CTW(K)

#считает (g,W) по формуле вида (g,ABCD) = (g,D)D^{-1}(g,C)C^{-1}(g,B)B^{-1}(g,A)BCD
def Word_CL(g,W):
	if len(W) == 0:
		return Word()
	if len(W) == 1:
		return Comm_CL(g, W.letters[0])

	ans = Word()
	for K in W.letters[:0:-1]:
		ans += Comm_CL(g,K) - CTW(K)
	ans += Comm_CL(g, W.letters[0])
	for K in W.letters[1:]:
		ans += CTW(K) 
	return ans

def Comm_CR(K,g):
	return -Comm_CL(g,K)

#считает(W,g) как (g,W)^{-1}
def Word_CR(W,g):
	#БЕЗБОЖНЫЙ КОСТЫЛЬ ДЛЯ КОРРЕКТНОЙ РАБОТЫ Calc_WI:
	#благодаря ему можно вызывать Calc_WI(W,I) для W=число.
	#возможно, его аналоги надо поставить и в других местах
	if type(W) == type(1):
		return CTW(Comm([W,g]))
	return -Word_CL(g,W)

#[a,b,c,d] -> запись элемента (((a,b),c),d) через обычные коммутаторы
#def LeftNested(elems):
#	if len(elems) < 2:
#		print('something is wrong: LeftNested(elems) with len(elems)<2')
#		return
#	if len(elems) == 2:
#		return CTW(Comm(elems,False))
#	return Word_CR(LeftNested(elems[:-1]),elems[-1])

#(W, [5,2,1,3]) -> вычисляет (W,5213)=(W,3)(W,1)((W,1),3)(W,2)...((((W,5),2),1),3)
#как (W,213) + (W,5) + ((W,5),213)
def Calc_WI(W,I):
	if len(I) == 0:
		return Word()
	if len(I) == 1:
		return Word_CR(W, I[0])
	return Calc_WI(W, I[1:])+Word_CR(W,I[0])+Calc_WI(Word_CR(W,I[0]),I[1:])

#переставляет два внутренних элемента коммутатора:
#например, из (a,(b,(c,d))) делает слово, где на последних позициях везде (d,c)
#(везде ли? может, где-то другие буквы? надо обдумать)
def Comm_TTI(K):
	if len(K) == 2:
		a, b = K.elems
		return CTW(Comm([b,a], not K.invert))
	else:
		a, K0 = K.elems[0], K.Inner()
		TK0 = Comm_TTI(K0)
		return -TK0-Word_CL(a, -TK0)+TK0

#переставляет два внутренних элемента каждого из коммутаторов
def Word_TTI(W):
	return sum(map(Comm_TTI, W.letters), start=Word())

#просто переставляет эту позицию с той, которая чуть правее
def Comm_SimpleSwapRight(K, pos):
	if K.invert:
		return -Comm_SimpleSwapRight(-K,pos)
	n = len(K)
	if pos >= n-3:
		print('wrong swap in Comm_SimpleSwapRight')
	a = K.elems[pos]
	b = K.elems[pos+1]
	tail = K.elems[pos+2:]
	head = K.elems[:pos]

	#самую малость упрощает вычисления (наверно)
	if a > b:
		ab = Comm([a,b], False)
		ba = Comm([a,b], True)
	else:
		ab = Comm([b,a], True)
		ba = Comm([b,a], False)
	#(a,(b,K0))=(a,K0)K0^{-1}(a,b)K0(K0,b)(b,(a,K0))(K0,a)(b,a)(b,K0)
	wd = LTW([
		Comm([a]+tail,False),
		Comm(tail,True),
		ab,
		Comm(tail,False),
		Comm([b]+tail,True),
		Comm([b,a]+tail,False),
		Comm([a]+tail,True),
		ba,
		Comm([b]+tail,False)])

	for x in reversed(head):
		wd = Word_CL(x,wd)
	return wd
#--------------------------------------------------------------------------
#                     Панов-Верёвкин
#--------------------------------------------------------------------------
#добиваемся того, чтобы максимум стоял на предпоследнем месте
def Comm_MaxToItsPlace(K):
	global maxtopdict
	if K in maxtopdict:
		return maxtopdict[K]

	if K.invert:
		maxtopdict[K] = -Comm_MaxToItsPlace(-K)
		return maxtopdict[K]
#		return -Comm_MaxToItsPlace(-K)
	els = K.elems
	maxpos = els.index(max(els))
	n = len(els)
	if maxpos == n-2:
		maxtopdict[K] = CTW(K)
		return CTW(K)
	if maxpos == n-1:
		#ВОЗМОЖНО, НУЖНА ПОДСТРАХОВКА (она закомментирована)
		maxtopdict[K] = Comm_TTI(K)
		return maxtopdict[K]
#		return Comm_TTI(K)
#		return Word_MaxToItsPlace(Comm_TTI(K))
	if maxpos < n-3:
		wd = Comm_SimpleSwapRight(K, maxpos)
		maxtopdict[K] = Word_MaxToItsPlace(wd)
		return maxtopdict[K]
#		return Word_MaxToItsPlace(wd)
	if maxpos == n-3:
		m,a,b = els[-3:]
		if a > b:
			ab = Comm([a,b], False)
			ba = Comm([a,b], True)
		else:
			ab = Comm([b,a], True)
			ba = Comm([b,a], False)

		#(m,(a,b))=(m,b)(m,a)((m,a),b)(b,a)(a,(m,b))(b,m)(a,m)(a,b)
		wd = LTW([
			Comm([m,b],False),
			Comm([m,a],False),
			Comm([b,m,a],True),
			ba,
			Comm([a,m,b],False),
			Comm([m,b],True),
			Comm([m,a],True),
			ab])
		for el in els[-4::-1]:
			wd = Word_CL(el,wd)
		maxtopdict[K] = Word_MaxToItsPlace(wd)
		return maxtopdict[K]
#		return Word_MaxToItsPlace(wd)
	else:
		print('something is wrong in Comm_MaxToItsPlace')

def Word_MaxToItsPlace(W):
	return sum(map(Comm_MaxToItsPlace, W.letters), start=Word())

#выражаем через базис коммутанта свободной группы
#def Comm_ExpressInFree(K):
#	return Word_SortElems(Comm_MaxToItsPlace(K))
#def Word_ExpressInFree(W):
#	return sum(map(Comm_ExpressInFree,W.letters),start=Word())

#сортируем все элементы, кроме двух последних
def Comm_SortElems(K):
	global sorteddict
	if K in sorteddict:
		return sorteddict[K]
	if K.invert:
		sorteddict[K] = -Comm_SortElems(-K)
		return sorteddict[K]
	n = len(K)
	elems = K.elems
	for i in range(n-3):
		if elems[i] == elems[i+1]:
			print('error: equal elems!')
		if elems[i] > elems[i+1]:
			sorteddict[K] = Word_SortElems(Comm_SimpleSwapRight(K,i))
			return sorteddict[K]
	sorteddict[K] = CTW(K)
	return sorteddict[K]

def Word_SortElems(W):
	return sum(map(Comm_SortElems,W.letters),start=Word())

#----------------------------------
#ФУНКЦИИ С УЧАСТИЕМ ГРАФА (САМЫЕ ГЛАВНЫЕ)


def Comm_ExpressThroughBasis(K,graph):
	global finaldict
	if K in finaldict:
		return finaldict[K]

	if K.invert:
		finaldict[K] = -Comm_ExpressThroughBasis(-K, graph)
		return finaldict[K]
#		return -Comm_ExpressThroughBasis(-K,graph)

	els = K.elems
	n = len(els)

	if graph.has_edge(els[-1],els[-2]):
		finaldict[K]=Word()
		return Word()

	maxel = max(els)
	maxpos = els.index(maxel)

	if n == 2:

		if maxpos == 1:
#			return CTW(Comm(K.elems[::-1], True))
			a, b = K.elems
			finaldict[K]=CTW(Comm([b,a],True))
			return CTW(Comm([b,a], True))

		finaldict[K]=CTW(K)
		return CTW(K)

	if graph.has_edge(els[-1], els[-3]) and graph.has_edge(els[-2], els[-3]):
		finaldict[K]=Word()
		return Word()

	G = graph.subgraph(els)
	#добиваемся того, чтобы максимум стоял на своём месте
	if Comm_IsCanonical(K, G):
		finaldict[K]=CTW(K)
		return CTW(K)

	if maxpos != n-2:
		finaldict[K] = Word_ExpressThroughBasis(Comm_MaxToItsPlace(K), G)
		return finaldict[K] 
#		return Word_ExpressThroughBasis(Comm_MaxToItsPlace(K), G)

	last = els[-1]

	if AreInSameComponent(last, maxel, G):
		fst = FirstStep(last, maxel, G)
	else:
		mic = MinInComponent(last, G)
		if mic == last:
			#осталось отсортировать
			finaldict[K] = Word_ExpressThroughBasis(Comm_SortElems(K), G)
			return finaldict[K]
		micpos = els.index(mic)
		fst = FirstStep(last, mic, G)

	fstpos = els.index(fst)
	if fstpos < n-3:
		finaldict[K] = Word_ExpressThroughBasis(Comm_SimpleSwapRight(K,fstpos), G)
		return finaldict[K]
	elif fstpos == n-3:
		a,b,x=fst,maxel,last
		#пользуемся тем, что (a,x)=id; b - наибольший
		#поэтому (a,(b,x))=(x,(b,a))(a,b)(x,b)(b,a)(b,x)
		if a > b:
			ab = Comm([a,b], False)
			ba = Comm([a,b], True)
		else:
			ab = Comm([b,a], True)
			ba = Comm([b,a], False)
		wd = LTW([
			Comm([x,b,a], False),
			ab,
			Comm([x,b], False),
			ba,
			Comm([x,b], True)
			])
		for el in els[-4::-1]:
			wd = Word_CL(el,wd)
		#print('we are reduced to {}.\n'.format(wd))
		finaldict[K] = Word_ExpressThroughBasis(wd, G)
		return finaldict[K]
	else:
		print('something is wrong in Comm_ExpressThroughBasis: fstpos > n-3')

def Word_ExpressThroughBasis(W,graph):
	ans = Word()
	for K in W.letters:
		ans += Comm_ExpressThroughBasis(K,graph)
	return ans

#def Word_KillObvious(W,graph):
#	ans = Word()
#	for K in W.letters:
#		if not graph.has_edge(K.elems[-1],K.elems[-2]):
#			if len(K) == 2:
#				ans += CTW(K)
#			elif (not graph.has_edge(K.elems[-1], K.elems[-3])) or\
#				 (not graph.has_edge(K.elems[-2], K.elems[-3])):
#				if not Comm_IsCanonical(K,graph.subgraph(K.elems)):
#					print('{} is not canonical?! (in KillObvious)'.format(K))
#				ans += CTW(K)
#	return ans

#-----------------------------------------------------------
#         вспомогательное про графы
#------------------------------------------------------------

#в одной ли компоненте связности?
def AreInSameComponent(i,j, G):
	return (j in nx.node_connected_component(G,i))

#минимальный элемент компоненты связности, содержащей i
def MinInComponent(i, G):
	return min(nx.node_connected_component(G,i))

#первая вершина на пути от i к j в графе G
def FirstStep(i,j, G):
	return nx.shortest_path(G,source=i,target=j)[1]

def Comm_IsCanonical(K, graph):
	els = K.elems
	last = els[-1]
	n = len(els)
	maxel = max(els)
	if els.index(maxel) != n-2:
#		print(' {} not canonical since maxpos = {} != {}'.format(K, maxpos, n-2))
		return False
	if AreInSameComponent(maxel, last, graph):
#		print(' {} not canonical since {} and {} are in same component'.format(
#			K, maxel, last))
		return False
	if last != MinInComponent(last,graph):
		return False
	if n == 2:
		return True
	return all(els[i] < els[i+1] for i in range(n-2))

#--------------------------------------------------------------------------
#         ключевые вычисления для общего алгоритма
#--------------------------------------------------------------------------

#вычисляет T_I := (g_m, w_I)
def Final_ExpressTI(m,I,graph):
	return Word_ExpressThroughBasis(Calc_WI(m,I), graph)

#вычисляет K^{w_I} = K(K,w_I)
def Final_ConjComm(K,I,graph):
	return Word_ExpressThroughBasis(CTW(K)+Calc_WI(CTW(K),I),graph)

#--------------------------------------------------------------------------
# алгоритм для m-угольника!
#--------------------------------------------------------------------------

#из соотношения подграфа на первых (m-1) вершинах
#делаем новое соотношение сопряжением
#def OldRelation(m, R, graph):
#	return Final_ConjComm(R, [m], graph)

#если все вершины образующей J соединены с m в графе,
#и ни одна из вершин I не соединена,
#то алгоритм сопоставляет этому набору данных соотношение.
def NewRelation(m, I, J_generator, graph):
	print('(m={}) The relation concerning I={}, J_generator={}:'.format(m, I,J_generator))
	print('It has form ({},{}) {}^({}) = {}^({}{}) ({},{})'.format(
		m, ''.join(map(str,I)),
		J_generator, ''.join(map(str,I)),
		J_generator, ''.join(map(str,I)), m,
		m, ''.join(map(str,I))
		))

	I.sort(reverse=True)

	tstart_time = time.time()

	T = Final_ExpressTI(          m, I, graph)

	tend_time = time.time()
	print('T: {} seconds'.format(tend_time - tstart_time))
	astart_time = time.time()

	A = Final_ConjComm (J_generator, I, graph)

	aend_time = time.time()
	print('A: {} seconds'.format(aend_time - astart_time))
	bstart_time = time.time()

	#должно быть чуть быстрее, чем через Final_ConjComm
	B0 = Word()
	for K in A.letters:
		B0 += CTW(K) + Calc_WI(CTW(K), [m])
	B = Word_ExpressThroughBasis(B0, graph)

#	B = Word()
#	for K in A.letters:
#		B += Final_ConjComm(K, [m], graph)

	bend_time = time.time()
	print('B: {} seconds'.format(bend_time - bstart_time))

#	print('T=({},{})={}'.format  (          m,''.join(map(str,I)), T))
#	print('A={}^({})={}'.format  (J_generator,''.join(map(str,I)), A))
#	print('B={}^({}{})={}'.format(J_generator,''.join(map(str,I)), m, B))
	return (T,A,B)

def PolygonRelation(m):
	graph=nx.cycle_graph(range(1,m+1))
	T,A,B = NewRelation(m, list(range(2,m-1)), Comm([m-1,1],False), graph)
#	print('RELATION IN {}-gon: {}=id'.format(m,T+A-T-B))
	return T+A-T-B
#----------------------------------------------------------------------------
#                  запись через список образующих
#----------------------------------------------------------------------------

#СДЕЛАТЬ! это взаимодействие с write_generators.py, которую я не помню когда писал

#----------------------------------------------------------------------------
#            технологии проверки написанного
#----------------------------------------------------------------------------
def Comm_ToStr(K):
	if K.invert:
		return Comm_ToStr(-K)[::-1]
	if len(K)==2:
		return (chr(K.elems[0]+ord('0'))+chr(K.elems[1]+ord('0')))*2
#		return (str(K.elems[0])+str(K.elems[1]))*2
	s = Comm_ToStr(K.Inner())
	return chr(K.elems[0]+ord('0')) + s[::-1] + chr(K.elems[0]+ord('0')) + s
#	return str(K.elems[0]) + s[::-1] + str(K.elems[0]) + s

def Word_ToStr(W):
	return ''.join(map(Comm_ToStr,W.letters))

def SimplifyStr(s, m, graph):
	upd = True
	n = len(s)
	currshift = 0#сдвиг, с которого начинаем перебирать буквы
	while upd and n > 0:
		upd = False
		for ti in range(n):
			i = (ti+currshift) % n
			lt = s[i]#текущая буква
			if lt in s[i+1:]:
				nextpos = i+1+s[i+1:].index(lt)#следующая позиция её вхождения
				if all(graph.has_edge(ord(lt)-ord('0'),
									  ord(ot)-ord('0'))
						for ot in s[i+1:nextpos]):
#				if all(graph.has_edge(int(lt),int(ot)) for ot in s[i+1:nextpos]):
					n -= 2
					s = s[:i]+s[i+1:nextpos]+s[nextpos+1:]
					upd = True
					currshift = i-1#так быстрее всего убирать abcddcba
					break
	return s


#----------------------------------------------------------------
#       GENERATORS OF FORM (a,b)^{cdefgh}
#----------------------------------------------------------------
#rewritedict = {}
def Comm_RewriteAsConj(K):
	n = len(K)
	if n == 2:
		return CTW(K)
	if K.invert:
		return -Comm_RewriteAsConj(-K)
	a = K.elems[0]
	K0 = K.Inner()
	W0 = Comm_RewriteAsConj(K0)
	ans = Word()
	for L in W0.letters:
		ans += CTW(Comm([a]+L.elems, L.invert))
#	print('rewritten: {}->{}'.format(K,-ans+W0))
	return -ans + W0
	#смысл: (a,K) = (K^a)^{-1} K

def Word_RewriteAsConj(W):
	ans = Word()
	for K in W.letters:
		ans += Comm_RewriteAsConj(K)
	return ans
#------------------------------------------------------------------
#                      MAIN.CPP
#-----------------------------------------------------------------
for m in range(4,11):
	finaldict={}
	maxtopdict={}
	sorteddict={}
	print('m={}:'.format(m))
	start_time = time.time()
	rel = PolygonRelation(m)
	print('relation has len={} (expected 4x{}={})'.format(len(rel),1+(m-4)*2**(m-3),4+(m-4)*2**(m-1)))
#	print(rel)
#	print('rewritten:')
	newrel = Word_RewriteAsConj(rel)
#	print(newrel)
	print('new relation has len={}'.format(len(newrel)))
	calcrel_time = time.time()
	print('  calculated   in {} seconds;'.format(calcrel_time-start_time))
	for K in rel.letters:
		if not Comm_IsCanonical(K, nx.cycle_graph(range(1,m+1)).subgraph(K.elems)):
			print('{} is not canonical!!'.format(K))
	check_time = time.time()
	print('checked canon. in {} seconds;'.format(check_time-calcrel_time))
	wd = Word_ToStr(rel)
#	print(wd)
	wtolist_time = time.time()
	print('  put to list  in {} seconds;'.format(wtolist_time-check_time))
	swd = SimplifyStr(wd, m, nx.cycle_graph(range(1,m+1)))
	simplify_time = time.time()
	print('  simplified   in {} seconds;'.format(simplify_time-wtolist_time))
	print('simplification: "{}"'.format(swd))
#	print(finaldict)
	print('{}+{}+{}={} commutators in dictionaries'.format(
		len(maxtopdict),
		len(sorteddict),
		len(finaldict),
		len(maxtopdict)+len(sorteddict)+len(finaldict)))

#если f(m) - количество букв в соотношении для m-угольника, то
#f(4)=4, f(5)=34, f(6)=192, f(7)=916, f(8)=3976, f(9)=16268, f(10)=63940
#были бы соотношения минимальной длины - было бы
#g(4)=4, g(5)=20, g(6)= 68, g(7)=196, g(8)= 516, g(9)= 1284, g(10)= 3076