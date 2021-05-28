from weighted_series_class import *

str_names = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26}
inv_names = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12,'M':13,'N':14,'O':15,'P':16,'Q':17,'R':18,'S':19,'T':20,'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26}

#alg_interpretations = 
#{
#	'a':'+31-13','b':'+41-14','c':'+42-24','d':'+52-25','e':'+53-35',
#	'A':''
#}

def series_from_str(s):
	ans= Series()
	for ch in s:
		if ch in str_names:
			ans *= StrSeries(str_names[ch])
		elif ch in inv_names:
			ans *= InvSeries(inv_names[ch])
		else:
			print("error: unknown variable '{}'".format(ch))
	return ans

def inv_series_from_str(s):
	s = s[::-1]
	ans= Series()
	for ch in s:
		if ch in str_names:
			ans *= InvSeries(str_names[ch])
		elif ch in inv_names:
			ans *= StrSeries(inv_names[ch])
		else:
			print("error: unknown variable '{}'".format(ch))
	return ans	
#a  b  c  d  e  f  g  h  i  j
#a1 a2 a3 a4 a5 b1 b2 b3 b4 b5
conj_dict = {
'a':'eahE','b':'b','c':'dFcD','i':'eiBEb','j':'djBDb',
'A':'eHAE','B':'B','C':'dCfD','I':'BebIE','J':'BdbJD'
}
def conj_replacement(s):
	ans = ''
	for x in s:
		if x in conj_dict:
			ans += conj_dict[x]
		else:
			print("error: '{}' not in conj_dict".format(x))
	return ans

r1='hgQyTdJapHDtGefRxCfScFcLbkECsFgTdhPAjDtYqGHfSceKBlCfCsFcXrFE'
#r1='fNaCsVnFDtGfSceKBlCfCsFcXrFEgTedMfNvScAiCsVnFmDEtGefRxScLbkECsFgTdfNvSDceKBlCdMcIuLbnFGfBlCsCfScFcLbFghPfNwOBlUiCmDcLbkECdcIoWnFpH'
#r1='FhfOeKoFHfkE'
#r1='hPDedMpHmDEd'
#r1='dJaDecLbkECdAjDceKBlCE'

#r1='EqFdgNCoDGfQgePFdOcDfdMCpEcnGemD'
#r2='bAlBdgNCoDGbLgaKBdOcbHCkAcnGahBD'
#r3='bJiAlTjBEqFdgNCoDGfQebJtLEgePaIsKjBFdOcDfdMbHrJCkSiApEcnGeaIjRhBmD'

#t_rel = series_from_str('fMCecHmFhCEc')
#t_rel=series_from_str('ABab')
wr1=series_from_str(r1)
#wr2=series_from_str(r2)
#wr3=inv_series_from_str(r3)
print(wr1)
#print(series_from_str(r1))
#print(wr1*wr2*wr3)
'''
t_str = 'edG'
a_str = 'CbIaBcbJA'
b_str = conj_replacement(a_str)
#print(b_str)
T = series_from_str(t_str)
A = series_from_str(a_str)
#B = series_from_str(b_str)
T_inv = inv_series_from_str(t_str)
B_inv = inv_series_from_str(b_str)
#print(B_inv*B)
#print(T*A)
#print(B*T)
#print(B)
relation = T*A*T_inv*B_inv
#выдаёт [a,f]+[b,g]-[c,h]-[d,i]-[e,j]
#relation_fix = series_from_str('FAfaGBgbHChcDIdiEJej')
print(relation)
#print(relation*relation_fix)'''