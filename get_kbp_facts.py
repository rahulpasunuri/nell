def pruneWord(word):
	index = word.rfind(':')
	return word[index+1:].strip()

fileName="kbp.txt"
nell_file="NELL.08m.905.esv.csv"

outfile=open("kbp_relations.txt","w")

f=open(fileName, "r")
lines=f.readlines()
f.close()

mapping={}

for l in lines:
	l=l.strip()
	#'=' in line => a mapping is defined between nell and kbp relations..
	if l[0:2]!="//" and l!="" and '=' in l:
		if (" and " not in l) and (" or " not in l): #TODO
			i = l.find('=')
			kbp_pred=l[:i].strip()
			nell_pred=l[i+1:].strip()[6:]
			mapping[nell_pred]=kbp_pred
			
		
f=open(nell_file, "r")
lines=f.readlines()
f.close()
lines=lines[1:] #ignore the header line.



for pred in mapping:
	outfile.write("\n//Printing Facts for relation: "+pred+"\n")
	mod = "concept:"+pred
	for l in lines:
		words= l.split('\t')
		if words[1]==mod:
			prob = float("{0:.2f}".format(float(words[4])))
			t=str(prob)+"\t"+mapping[pred]+"("+pruneWord(words[0])+","+pruneWord(words[2])+")"+"\n"
			outfile.write(t)
			
			
outfile.close()


