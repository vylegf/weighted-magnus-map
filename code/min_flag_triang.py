import random

two_sphere=[[1],[2],[3],[4],
[1,2],[1,3],[1,4],[2,3],[2,4],[3,4],
[1,2,3],[1,2,4],[1,3,4],[2,3,4]]

def set_to_num(s):
	return sum(2**(x+1) for x in s)

def edges_to_graph(set_of_edges):
	set_of_vertices = set()
	for edge in set_of_edges:
		set_of_vertices.add(edge[0])
		set_of_vertices.add(edge[1])
	list_of_vertices = list(set_of_vertices)
	list_of_vertices.sort()
	d={}
	for (i,x) in enumerate(list_of_vertices):
		d[x]=i
	n = len(list_of_vertices)

	graph = [[] for i in range(n)]
	for edge in set_of_edges:
		a,b=edge
		graph[d[a]].append(d[b])
		graph[d[b]].append(d[a])

	for i in range(n):
		graph[i] = list(set(graph[i]))
	return graph

def b_subdivision(comp):
	set_of_edges = set()
	for s1 in comp:
		for s2 in comp:
			if set(s1) & set(s2) == set(s1) and set(s1) != set(s2):
				tup = tuple([set_to_num(s1), set_to_num(s2)])
				set_of_edges.add(tup)
#		l = len(simp)
#		for i in range(l):
#			print(simp)
#			ts = simp[:i] + simp[i+1:]
#			print(ts)
#			print(set_to_num(ts))
#			print(set_to_num(simp))
#			tup = tuple([set_to_num(ts), set_to_num(simp)])
#			set_of_edges.add(tup)
	return edges_to_graph(set_of_edges)

#входит ли ребро (i,j) в какой-то 4-цикл
#def is_admissible(graph, i, j):
#	if j not in graph[i]:
#		print('not admissible: no edge (i,j)')
#		return False
#	for x in graph[i]:
#		if x == j:
#			continue
#		for y in graph[x]:
#			if y == i or y == j:
#				continue
#			if j in graph[y]:
#				print('found 4-cycle ({},{},{},{})'.format(i,j,y,x))
#				return False
#	return True

#def contract_everything(graph):
#	ok = True
#	changed = False
#	while ok:
#		ok = False
#		adm_edges = []
#		n = len(graph)
#		for i in range(n):
#			for j in graph[i]:
#				if is_admissible(graph,i,j):
#					adm_edges.append([i,j])
#		N = len(adm_edges)
#		ok = (N>0)
#		if ok:
#			changed = True
#			i,j = random.choice(adm_edges)
#			graph = contract_edge(graph,i,j)
#	if changed:
#		print('contractions! now {} vertices'.format(len(graph)))
#	return graph

#def contract_edge(graph, i, j):
#	if j not in graph[i]:
#		print('cannot contract nonexistent edge ({},{})'.format(i,j))
#		return graph
#	print('contraction of ({},{}); n={}->{}'.format(i,j,n,n-1))
#	n = len(graph)
#	new_graph = [[] for t in range(n-1)]
#	d = {}
#	for t in range(j):
#		d[t] = t
#	d[j] = i
#	for t in range(j+1,n):
#		d[t] = t-1
#
#	for k in range(n):
#		for s in graph[k]:
#			if d[k] != d[s]:
#				new_graph[d[k]].append(d[s])
#	return new_graph

def contract_everything(graph):
	ok = True
#	changed = False
	while ok:
		ok = False

		adm_triples = []
		n = len(graph)
		for j in range(n):
			for i in graph[j]:
				for k in graph[j]:
					if i == k or i in graph[k]:
						continue
					if admissible_triple(graph,i,j,k):
						adm_triples.append([i,j,k])
		N = len(adm_triples)
		if N>0:
			ok = True
#			changed = True
			i,j,k = random.choice(adm_triples)
			graph = inverse_to_subdivision(graph,i,j,k)

#	if changed:
#		print('contractions! now {} vertices'.format(len(graph)))
	return graph

#подразумевается, что рёбра (i,j) и (j,k) уже есть, а (i,k) нету
def admissible_triple(graph, i, j, k):
#	if i in graph[k]:
#		return False
	return set(graph[j])|set([j]) == (set(graph[i]) & set(graph[k])) | set([i,k])
#	return set(graph[j]) = set(graph)

def inverse_to_subdivision(graph, i, j, k):
	n = len(graph)
	new_graph = [[] for t in range(n-1)]
	d = {}

	for t in range(j):
		d[t] = t
#	d[j] = i
	for t in range(j+1,n):
		d[t] = t-1

	for t in range(n):
		if t == j:
			continue
		for s in graph[t]:
			if s != j:
				new_graph[d[t]].append(d[s])
	new_graph[d[i]].append(d[k])
	new_graph[d[k]].append(d[i])
	return new_graph

def subdivide_edge(graph, i, j):
	if j not in graph[i]:
		print('cannot subdivide nonexistent edge ({},{})'.format(i,j))
		return graph
	n = len(graph)
#	print('subdivision of ({},{}); n={}->{}'.format(i,j,n,n+1))
	mutuals = list(set(graph[i]) & set(graph[j]))
	graph.append(mutuals)
	for v in mutuals:
		graph[v].append(n)
	graph[i].append(n)
	graph[i].remove(j)
	graph[j].append(n)
	graph[j].remove(i)
	graph[n].append(i)
	graph[n].append(j)
	return graph

def randomly_subdivide(graph, max_n):
	n = len(graph)
	while n < max_n:
		all_edges = []
		for i in range(n):
			for j in graph[i]:
				all_edges.append([i,j])
		i,j = random.choice(all_edges)
		subdivide_edge(graph,i,j)
#		contract_everything(graph)
#		n = len(graph)
		n += 1

#------------------------------------------------------------------------------
comp1=[[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12], [1, 2], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [2, 6], [2, 7], [2, 8], [2, 9], [3, 4], [3, 10], [3, 11], [3, 12], [4, 3], [4, 10], [4, 11], [4, 12], [5, 6], [5, 9], [6, 7], [6, 8], [6, 9], [7, 8], [8, 9], [10, 11], [10, 12], [11, 12], [0, 1, 5], [0, 1, 7], [0, 1, 8], [0, 2, 6], [0, 2, 8], [0, 2, 9], [0, 3, 10], [0, 3, 12], [0, 4, 10], [0, 4, 11], [0, 5, 9], [0, 6, 7], [0, 11, 12], [1, 2, 6], [1, 2, 7], [1, 2, 9], [1, 5, 6], [1, 8, 9], [2, 7, 8], [3, 4, 11], [3, 4, 12], [3, 10, 11], [4, 10, 12], [5, 6, 9], [6, 7, 8], [6, 8, 9], [10, 11, 12]]
comp2=[[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [1, 2], [1, 5], [1, 6], [1, 9], [1, 10], [2, 5], [2, 9], [3, 4], [3, 6], [3, 7], [3, 8], [3, 9], [4, 6], [4, 7], [4, 8], [5, 6], [5, 10], [6, 7], [6, 10], [7, 8], [7, 10], [8, 9], [8, 10], [9, 10], [0, 1, 6], [0, 1, 10], [0, 2, 5], [0, 2, 9], [0, 3, 7], [0, 3, 8], [0, 3, 9], [0, 4, 6], [0, 4, 7], [0, 4, 8], [0, 5, 10], [1, 2, 5], [1, 2, 9], [1, 5, 6], [1, 9, 10], [3, 4, 6], [3, 4, 7], [3, 4, 8], [3, 6, 7], [3, 7, 8], [3, 8, 9], [5, 6, 10], [6, 7, 10], [7, 8, 10], [8, 9, 10]]
comp3=[[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [1, 2], [1, 6], [1, 7], [1, 9], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9], [2, 10], [3, 4], [3, 5], [3, 7], [3, 8], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [4, 10], [5, 6], [5, 7], [5, 9], [5, 10], [6, 7], [7, 8], [7, 9], [8, 9], [9, 10], [0, 1, 6], [0, 1, 7], [0, 1, 9], [0, 2, 5], [0, 2, 8], [0, 2, 10], [0, 3, 5], [0, 3, 7], [0, 3, 8], [0, 4, 6], [0, 4, 9], [0, 4, 10], [1, 2, 6], [1, 2, 7], [1, 2, 9], [2, 5, 6], [2, 7, 8], [2, 9, 10], [3, 4, 5], [3, 4, 7], [3, 4, 8], [4, 5, 10], [4, 6, 7], [4, 8, 9], [5, 6, 7], [5, 7, 9], [5, 9, 10], [7, 8, 9]]
#------------------------------------------------------------------------------
REPEATS = 10000
N = 100

def try_complex(comp, N):
	g = b_subdivision(comp)
	randomly_subdivide(g, N)
	con = contract_everything(g)
	print(len(con))
	print(con)

def work_with_complex(comp):
	g = b_subdivision(comp)
	N = 100
	min_n = 1000
#	for rep in range(REPEATS):
	while True:
		gc=[x[:] for x in g]
		randomly_subdivide(gc, N)
#			randomly_subdivide(g, N)
#			g = contract_everything(g)
		contr = contract_everything(gc)
		curr_n = len(contr)
#			curr_n = len(g)
		if curr_n < min_n:
			min_n = curr_n
			print('new record: {}'.format(min_n))
			print(contr)
#				print(g)
#			else:
#				print('try: {}'.format(curr_n))


work_with_complex(comp1)
#print('--------------------------------------------')
#work_with_complex(comp2)
#print('--------------------------------------------')
#for i in range(100):
#	try_complex(comp2, 200)
#work_with_complex(comp3)
#print('--------------------------------------------')