import networkx as nx
import matplotlib.pyplot as plt
import itertools as it
import sys

o0=ord('0')
oa=ord('a')
oA=ord('A')

#это для того, чтобы стильно модно молодёжно писать одну букву,
#когда образующих нужной длины (или вершин в графе) станет больше 10
def indtolet(x):
	if x < 10:
		return chr(o0+x)
	else:
		return chr(oa-10+x)

def lettoind(x):
	if x in '0123456789':
		return ord(x)-o0
	else:
		return 10+ord(x)-oa

#читает граф без призрачных вершин. В ответ передаётся m, чтобы учесть
#изолированные вершины.
#в файле должно быть написано: сначала кол-во вершин m, потом рёбра
#через пробел/перенос строки, наподобие "6 23 01 45". Вершины: {0,1,..,m-1}.
def str_to_graph(s):
	data = s.split()
	m = int(data[0])
	G = nx.Graph()
	G.add_edges_from(map(lambda x: (lettoind(x[0]), lettoind(x[1])), data[1:]))
	return (G,m)

#обратная операция
def graph_to_str(G, m):
	return str(m) + ' ' + ' '.join(indtolet(x[0])+indtolet(x[1]) for x in G.edges())

#полезные мелочи
def read_str(fin_name):
	fin = open(fin_name, 'r')
	s = ''.join(fin.readlines())
	fin.close()
	return s

def write_str(s, fout_name):
	fout = open(fout_name, 'w')
	print(s, file=fout)
	fout.close()

def read_graph(fin_name):
	return str_to_graph(read_str(fin_name))

def scan_graph():
	print('Enter graph in format similar to "5 01 12 23 34 04" (for pentagon):\n')
	return str_to_graph(input())

def write_graph(G, m, fout_name):
	write_str(graph_to_str(G,m), fout_name)

#краткая запись образующей
def simple_str_generator(g):
	return '(' + ',('.join(map(indtolet,         g[:-1]))+',' +indtolet(g[-1])+')'*(len(g)-1)

#запись на человеческом языке
def str_generator(g):
	return '(g'+'(g'.join(map(lambda x:str(x+1)+','+' '*(2-len(str(x+1))),g[:-1]))+' g'+str(g[-1]+1)+' '*(2-len(str(g[-1]+1)))+')'*(len(g)-1)

#распечатка списка образующих
def print_gens(gens, fout=sys.stdout):
	print('generators:')
	for i in range(len(gens)):
		let = chr(oa+i)
		for (j, gen) in enumerate(gens[i]):
			print('{}{}{}= {}'.format(
				let, str(j+1),
				' '*(3-len(str(j+1))),
				str_generator(gen)),
			file=fout)
	print('total: '+'+'.join(str(len(x)) for x in gens)+' generators')

def simple_print_gens(gens, fout=sys.stdout):
	print('generators:')
	for i in range(len(gens)):
		let = chr(oa+i)
		for (j, gen) in enumerate(gens[i]):
			print('{}{} = {}'.format(
				let, indtolet(j+1),
				simple_str_generator(gen)),
			file=fout)
#	print('total: '+'+'.join(str(len(x)) for x in gens)+' generators')
#------------------------------------------------------------------------------------------
#вычисляет список образующих по графу
def calculate_generators(G, m):
	rn = range(m)
	gens = []
	for r in range(2, m+1):
		r_gens = []
		for x in it.combinations(rn, r):#x - r-элементное подмножество
			Gx = G.subgraph(x)#Gx - полный подграф
			mx = max(x)
			if nx.number_connected_components(Gx) > 1:
				comps = nx.connected_components(Gx)
				x_gens = []
				for cp in comps:
					if mx in cp:
						continue
					v = min(cp)
					tx = list(x)
					tx.remove(v)
					x_gens.append(sorted(tx)+[v])
					#наим. вершина данной компоненты идёт последней в списке
				r_gens += x_gens
#		if len(r_gens):
		gens.append(r_gens)
	print_gens(gens)
	return gens

G, m = read_graph('torus_triang')
gens = calculate_generators(G, m)
print(graph_to_str(G,m))
#print(graph_to_str(G,m))
nx.draw(G)
plt.show()