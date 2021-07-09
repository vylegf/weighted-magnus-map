import networkx as nx
import matplotlib.pyplot as plt
import itertools as it
import sys
import time

#вложенный коммутатор вида (a,(b,(c,(d,e)))) (или обратный к нему)
#elems = [a,b,c,d,e]
class Comm:
	elems = []
	invert = False

	def __init__(self, *args):
		if len(args) == 0:
			print('error: zero arguments in Comm.__init__()')
			return

		if len(args) == 1:
			self.elems  = args[0].elems[:]
			self.invert = args[0].invert
			return

		if len(args) == 2:
			elems, invert = args
			self.elems  = elems[:]
			self.invert = invert
			return

		print('error: too many args in Comm.__init__(*args)')

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
		if len(self) == 2:
			return '({},{})'.format(self.elems[0], self.elems[1])
		else:
			return '({},{})'.format(self.elems[0], self.Inner().StringForm())

	def __str_(self):
		ans = 'Comm'+self.StringForm()
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
	letters = []
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
		if not len(self):
			return Word()
		return LTW([-self.letters[i] for i in reversed(range(len(self)))])

	def __repr__(self):
		return 'Word['+''.join(str(K) for K in self.letters)+']'
#		return ''.join(str(K) for K in self.letters)

	def __str__(self):
		return 'Word['+''.join(str(K) for K in self.letters)+']'
#		return ''.join(str(K) for K in self.letters)

#-------------------------------------------------------------------------------------
#                 простейшие операции
#-------------------------------------------------------------------------------------

#делает из коммутатора однобуквенное слово
def CTW(K):
	return Word(K, False)

def LTW(lets):
	ans = Word()
	ans.letters = lets
	return ans

#считает (g,K)
def Comm_CL(g,K):
	#tcomm=(g,|K|)
	tcomm = CTW(Comm([g]+K.elems, False))
	if K.invert == False:
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
		return CTW(Comm([W,g],False))
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
	if K.invert == True:
		return -Comm_SimpleSwapRight(-K,pos)
	n = len(K)
	if pos >= n-3:
		print('something is wrong in Comm_SimpleSwapRight')
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
#          Панов-Верёвкин
#--------------------------------------------------------------------------
#добиваемся того, чтобы максимум стоял на предпоследнем месте
def Comm_MaxToItsPlace(K):
	if K.invert:
		return -Comm_MaxToItsPlace(-K)
	els = K.elems
	maxpos = els.index(max(els))
	n = len(els)
	if maxpos == n-2:
		return CTW(K)
	if maxpos == n-1:
		#ПОДСТРАХОВКА: кажется, верхнюю функцию не надо навешивать, но не проверял.
#		return Comm_TTI(K)
		return Word_MaxToItsPlace(Comm_TTI(K))
	if maxpos < n-3:
		wd = Comm_SimpleSwapRight(K, maxpos)
		return Word_MaxToItsPlace(wd)
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
		return Word_MaxToItsPlace(wd)
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


def Word_SortElems(W):
	return sum(map(Comm_SortElems,W.letters),start=Word())

#----------------------------------
#ФУНКЦИИ С УЧАСТИЕМ ГРАФА (САМЫЕ ГЛАВНЫЕ)

def Comm_IsCanonical(K, graph):
	els = K.elems
	last = els[-1]
	n = len(els)
	maxel = max(els)
	maxpos = els.index(maxel)
	if maxpos != n-2:
		return False
	if AreInSameComponent(maxel, last, graph):
		return False
	if last != MinInComponent(last,graph):
		return False
	if n == 2:
		return True
	return all(els[i] < els[i+1] for i in range(n-2))

#улучшает ситуацию с неканоническим коммутатором
def Comm_Updated(K, graph):
	if K.invert:
		return -Comm_Updated(-K,graph)
	els = K.elems
	last = els[-1]
	n = len(els)
	maxel = max(els)
	maxpos = els.index(maxel)
	if AreAdjacent(els[-1], els[-2], graph):
		return Word()
	if maxpos != n-2:
		return Comm_MaxToItsPlace(K)
	if AreInSameComponent(maxel, last, graph):
		if n == 2:
			return Word()
		fst = FirstStep(last, maxel, graph)
		if els.index(fst) == n-3 and AreAdjacent(fst, maxel, graph):
			return Word()
		else:
			fstpos = els.index(fst)
			if fstpos < n-3:
				return Comm_SimpleSwapRight(K,fstpos)
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
				return wd
	if last != MinInComponent(last, graph):
		mic = MinInComponent(last, graph)
		micpos = els.index(mic)
#		if micpos == n-1:
#			return Comm_SortElems(K)
		fst = FirstStep(last, mic, graph)
		fstpos = els.index(fst)
		if fstpos < n-3:
			return Comm_SimpleSwapRight(K,fstpos)
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
			return wd
	for i in range(n-3):
		if els[i] > els[i+1]:
			return Comm_SimpleSwapRight(K,i)
#	return Comm_SortElems(K)

def Comm_SortElems(K):
	if K.invert == True:
		return -Comm_SortElems(-K)
	n = len(K)
	elems = K.elems
	for i in range(n-3):
		if elems[i] == elems[i+1]:
			print('error: equal elems!')
		if elems[i] > elems[i+1]:
			return Word_SortElems(Comm_SimpleSwapRight(K,i))
	return CTW(K)
#	else:
#		mic = MinInComponent(last, G)
#		micpos = els.index(mic)
#		if micpos == n-1:
#			return Comm_SortElems(K)
#			#нужное достигнуто, осталось отсортировать и убить двухэлементные
#			return Word_KillObvious(Comm_SortElems(K),graph)
#		fst = FirstStep(last, mic, G)

def Word_ExpressThroughBasis(W, graph):
	expressed = False
	while not expressed:
		expressed = True
		temp_W = Word()
		for K in W.letters:
			if not Comm_IsCanonical(K, graph.subgraph(K.elems)):
#				print('{} is not canonical'.format(K))
				expressed = False
				temp_W += Comm_Updated(K, graph.subgraph(K.elems))
#				print('{} -> {}'.format(K, Comm_Updated(K, graph.subgraph(K.elems))))
			else:
				temp_W += CTW(K)
		W = temp_W
#		print(W)
	return W
#		expressed = all(Comm_IsCanonical(K, graph) for K in W.letters)


#-----------------------------------------------------------
#         вспомогательное про графы
#------------------------------------------------------------

#в одной ли компоненте связности?
def AreInSameComponent(i,j, G):
	return (j in nx.node_connected_component(G,i))

#минимальный элемент компоненты связности, содержащей i
def MinInComponent(i, G):
	return min(nx.node_connected_component(G,i))

#соединены ли ребром
def AreAdjacent(i,j, G):
	return G.has_edge(i,j)

#первая вершина на пути от i к j в графе G
def FirstStep(i,j, G):
	return nx.shortest_path(G,source=i,target=j)[1]

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
def OldRelation(m, R, graph):
	return Final_ConjComm(R, [m], graph)

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
	T = Final_ExpressTI(          m, I, graph)
	A = Final_ConjComm (J_generator, I, graph)

	B = Word()
	for K in A.letters:
		B += Final_ConjComm(K, [m], graph)

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
#		return [    K.elems[0],     K.elems[1] ]*2
		return (str(K.elems[0])+str(K.elems[1]))*2
	s = Comm_ToStr(K.Inner())
	return str(K.elems[0]) + s[::-1] + str(K.elems[0]) + s
#	return    [K.elems[0]] + s[::-1] +    [K.elems[0]] + s

def Word_ToStr(W):
	return ''.join(map(Comm_ToStr,W.letters))
#	return sum(map(Comm_ToList,W.letters),start=[])

def SimplifyStr(s, m, graph):
	upd = True
	n = len(s)
	currshift = 0#сдвиг, с которого начинаем перебирать буквы
	while upd and n > 0:
		upd = False
		for ti in range(n):
			i = (ti+currshift) % n
			lt = s[i]#текущая буква
#			print('lt={}, i={}, L[i+1:]={}'.format(lt,i,L[i+1:]))
			if lt in s[i+1:]:
				nextpos = i+1+s[i+1:].index(lt)#следующая позиция её вхождения
#				if all(AreAdjacent(lt,ot,graph) for ot in L[i+1:nextpos]):
				if all(AreAdjacent(int(lt),int(ot),graph) for ot in s[i+1:nextpos]):
#					print('found: {}'.format(L[i:nextpos+1]))
					n -= 2
					s = s[:i]+s[i+1:nextpos]+s[nextpos+1:]
					upd = True
					currshift = i-1#так быстрее всего убирать abcddcba
					break
#				else:
#					print('not found: {}'.format(L[i:nextpos+1]))

#			if not upd:
#				print('nothing good at {}/{}'.format(i, n))
	return s

for m in range(4,9):
	print('m={}:'.format(m))
	start_time = time.time()
	rel = PolygonRelation(m)
	calcrel_time = time.time()
	print(len(rel))
	print('  calculated  in {} seconds;'.format(calcrel_time-start_time))
	wd = Word_ToStr(rel)
	wtolist_time = time.time()
	print('  put to list in {} seconds;'.format(wtolist_time-calcrel_time))
	swd = SimplifyStr(wd, m, nx.cycle_graph(range(1,m+1)))
	simplify_time = time.time()
	print('  simplified  in {} seconds;'.format(simplify_time-wtolist_time))
	print('simplification: "{}"'.format(swd))
#	swd = SimplifyList(wd, m, nx.cycle_graph(range(1,m+1)))

#m=5
#rel = PolygonRelation(m)
#wd= Word_ToList(rel)
#swd = SimplifyList(wd, m, nx.cycle_graph(range(1,m+1)))

#если f(m) - количество букв в соотношении для m-угольника, то
#f(4)=4, f(5)=34, f(6)=192, f(7)=944, f(8)=5780, f(9)=101510

#for i in range(4,10):
#	start_time =
#print(rel)
#print('"'+''.join(map(str,wd))+'"')
#print('simplified to "'+''.join(map(str,swd))+'"')


#fout = open('9-gon relation', 'w')
#print(rel, file=fout)
#print('"'+''.join(map(str,wd))+'"', file=fout)
#print('simplified to "'+''.join(map(str,swd))+'"', file=fout)
#fout.close()