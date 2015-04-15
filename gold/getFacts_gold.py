fileName = "NELL_gold.tsv"
f=open(fileName, "r")
lines = f.readlines()
f.close()

rels = ['personleadsorganization']

for l in lines:
	words = l.split('\t')
	if words[1] in rels:
		print words[1]+"("+words[0]+","+words[2]+")"
