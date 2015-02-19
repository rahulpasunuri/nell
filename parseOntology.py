def parseOntology():
	f = open("ontology.csv", "r")
	lines = f.readlines()

	liRelations = []
	test=0
	for l in lines:
		l = l.strip()
	
		test += 1

		#if "skiarea" in l and "description" in l:
			#print l,"\t",test

		words = l.split("\t")
		d = '*'

		for i in range(len(words)):
			words[i] = words[i].strip()
			words[i] =words[i].replace("\"","")
			if d in words[i]:
				print "what??"
			if words[i]=="":
				print "what???"
			
		print words[0] + d + words[1] + d + words[2]
	
#parseOntology()



def parseBeliefs():
	f = open("beliefs.csv", "r")
	lines = f.readlines()

	liRelations = []
	test=0
	for l in lines:
		l = l.strip()
		test += 1
		words = l.split("\t")
		#d = '*'
		d='A' # as all characters are lower, we can safely use a capital letter as delimiter.
		isError = False
		problemIndex=0
		for i in range(len(words)):
			words[i] = words[i].strip()
			words[i] =words[i].replace("\"","")
			words[i] = words[i].lower()
			
			if d in words[i]:
				isError=True
			if words[i]=="" and i <6: #only worry about the first 6 columns..
				problemIndex = i
				isError=True

		temp = ""
		for j in range(len(words)):
			if j==0:
				temp = words[j]
			else:
				temp = temp+d+words[j]
				
		if isError:
			print "some thing is wrong: " , problemIndex,"\t",test
			for j in range(len(words)):
				print j,"\t",words[j]				
			return	
		
		print temp

parseBeliefs()
#for r in liRelations:
#	print r
