
'''
import pickle


dom=[]
rang=[]
rels=[]
cString = "concept:"

with open( "domain.p", "rb" ) as handle:
  dom = pickle.load(handle)
  
  
with open( "range.p", "rb" ) as handle:
  rang = pickle.load(handle)
  
  
with open( "relations.p", "rb" ) as handle:
  rels = pickle.load(handle)

modRels = [cString+r for r in rels]

fileName = "NELL.08m.905.esv.csv"  
f = open(fileName, "r")

modRels = [cString+r1 for r1 in rels]
modDom = [cString+r1 for r1 in dom]
modRang = [cString+r1 for r1 in rang]

lines = f.readlines()

delim = "\t"

facts = []

for l in lines:
	words = l.split(delim)
	
	if words[1] in modRels:		
		#get domain...
		d1 = words[0][len(cString):]
		ix1 = d1.index(':')
		domain = d1[:ix1]
		print domain+"("+d1[ix1+1:]+")"
		
		#get range
		d2 = words[2][len(cString):]
		ix2 = d2.index(':')
		domain = d2[:ix2]
		print domain+"("+d2[ix2+1:]+")"
		
		print words[1][len(cString):]+"("+d1[ix1+1:]+", "+d2[ix2+1:]+")"
		
			
#for f in facts:
	#print f
'''

import sys


def pruneWord(word):
	index = word.rfind(':')
	return word[index+1:]

inpFileName = "NELL.08m.905.esv.csv"
ontFileName = "ontology.csv"

posFileName = "pos.txt"
negFileName = "neg.txt"

posFile = open(posFileName,"w")
negFile = open(negFileName, "w")


#get mutex predicates...
mutexPredicates = []
f=open(ontFileName, "r")
lines=f.readlines()
for l in lines:
	if "concept:" in l:
		continue
	words = l.split('\t')
	if words[1] == "mutexpredicates":
		if words[0]=="ceoof":
			mutexPredicates.append(words[2].strip())
		elif words[2]=="ceoof":
			mutexPredicates.append(words[0].strip())

print "Printin Mutex Predicates"
print mutexPredicates

#modify the strings a bit..
for i in range(len(mutexPredicates)):
	mutexPredicates[i] = "concept:"+mutexPredicates[i]

f.close()

f=open(inpFileName, "r")
lines=f.readlines()
f.close()
rel = "ceoof"
relation = "concept:"+rel

for l in lines:
	words = l.split('\t')
	if words[1] == relation:
		 posFile.write(pruneWord(words[0])+","+pruneWord(words[2])+"\n")
	elif words[1] in mutexPredicates:
		#ignore the facts which have "," in between them
		if ',' in words[0] or ',' in words[2]:
			continue
		negFile.write(pruneWord(words[0])+","+pruneWord(words[2])+"\n")

posFile.close()
negFile.close()	
