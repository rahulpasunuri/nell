
def printList(l):
	print "\n*****Printing List*****\n"
	for r in l:
		print r
	print "\n*****End of List*****\n"

#list of constants..
delimiter = "*"
fileName =  "modOntology.csv"
domain = "sports"
descString = delimiter+"description"+delimiter	

#read file
rows = []
rels = []
dom = {}
rang = {}

matches = ["sport", "team", "play", "trophy"]
notMatches = ["instrument", "transport"] #instrument played by...

printNegated = False


#get the predicates relevant to our domain..
f = open(fileName, "r")
lines = f.readlines()
for i in range(len(lines)):
	lines[i] = lines[i].strip()
	
for l in lines:	
	words = l.split(delimiter)
	if 'concept:' in l:
		continue
	if words[1] == "memberofsets" and words[2] == "rtwrelation":		
		for m in matches:
			if m in words[0]:
				add = True
				for m2 in notMatches:
					if m2 in words[0]:
						add=False
						break
				
				if add==True:
					rels.append(words[0]) #get relevant relations..
				break			

invAdded = []
genAdded = []
isGlobalAdded = True

while isGlobalAdded==True:
	isGlobalAdded = False
	#add the inverses as well to the relevant category
	for l in lines:	
		if 'concept:' in l:
			continue
		words = l.split(delimiter)
		if words[1] == "inverse" and (words[0], words[2]) not in invAdded:		
			isAdded = False
			if words[0] in rels and words[2] not in rels:
				rels.append(words[2])
				isAdded=True		
	
			elif words[2] in rels and words[0] not in rels:
				rels.append(words[0])		

			if isAdded == True:
				isGlobalAdded = True
				invAdded.append((words[0], words[2]))
				if printNegated == True:
					print words[0]+"(X, Y) => " + words[2]+"(Y, X)"	
					print
				
				
				
		if words[1] == "generalizations" and (words[0], words[2]) not in genAdded:
			isRelation = False
		
			#ignore the below case for now....TODO
			#if words[0] in rels and words[2] not in rels:
			#	rels.append(words[2])
			#	isRelation = True			
		
			if words[2] in rels and words[0] not in rels:
				rels.append(words[0])
				isRelation = True
			
			elif words[0] in rels and words[2] in rels:
				isRelation = True
	
			if isRelation: #not handling generalizations of categories. TODO
				#handle cats and rels here.. so first have to get domain and range..
				if words[0] in rels: # this is a relation
						isGlobalAdded = True
						genAdded.append((words[0], words[2]))							
						print words[0]+"(X, Y) => " + words[2]+"(X, Y)"
						print				
				
			
	
for l in lines:
	if "concept:" in l:
		continue
	words = l.split(delimiter)
	if words[1] == "domain" and words[0] in rels: #get the domain of the relevant predicates...
		dom[words[0]] = words[2]
		print words[0]+"(X, Y) => "+words[2]+"(X)"
		print
		
	elif  words[1] == "range" and words[0] in rels: #get the domain of the relevant predicates...
		rang[words[0]] = words[2]
		print words[0]+"(X, Y) => "+words[2]+"(Y)"
		print
		
	elif words[1] == "antireflexive" and words[2] == "true" and words[0] in rels:
		if printNegated == True:
			print "!"+words[0]+"(X, X)"	
			print
		
	elif words[1] == "antisymmetric" and words[2]=="true" and words[0] in rels: #handle anti symmetric relations...
		if printNegated == True:
			print words[0]+"(X, Y), [X!=Y] => !"+words[0]+"(Y, X)"	#this is a simplified constraint compared to anti symmetric one.
			print

for l in lines:
	if "concept:" in l:
		continue
	words = l.split(delimiter)
	if words[1] == "mutexpredicates" and words[0] in rels and words[2] in rels :
		if printNegated==True:
			print words[0]+"(X, Y) => !"+words[2]+"(X, Y)"
			print
			

for l in lines:
	if "concept:" in l:
		continue
	words = l.split(delimiter)
	if words[0] in rels and words[1] == 'nrofvalues' and words[2] != 'any':
		n = int(words[2])
		s=''
		for j in range(n):
			s = s+words[0]+"(X, Y"+str(j)+") , [Y!=Y"+str(j)+"]"
			if j!=n-1:
				s=s+","
		s = s+" =>!"+words[0]+"(X, Y)"
					
		print s+"\n"		



print "\n//______Printing Relations:______\n"
for r in rels:
	print r+"(X, Y)\n"
	
cats = []
for d in dom:
	if d not in cats:
		cats.append(d)

for d in rang:
	if d not in cats:
		cats.append(d)

print "\n//______Printing Categories:______\n"

for c in cats:
	print c+"(X)\n"

print "\n//______Printing description of relations:______\n"

for l in lines:
	if "concept:" in l:
		continue
	words = l.split(delimiter)
	if words[1] == "description" and words[0] in rels:
		print "//",words[0],":\t", words[2]
	
