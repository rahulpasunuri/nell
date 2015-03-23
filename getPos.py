import sys

def pruneWord(word):
	index = word.rfind(':')
	return word[index+1:]

inpFileName = "NELL.08m.905.esv.csv"

posFileName = "pos.txt"
posFile = open(posFileName,"w")

f=open(inpFileName, "r")
lines=f.readlines()
f.close()

#liRel = ["person"]
#liCat = ["ceo"]


liRel = ["inverseofbankchiefexecutiveceo", "bankboughtbank", "bankchiefexecutiveceo", "economicsectorcompany", "acquiredby","inverseofbankboughtbank", "inverseofbankbankincountry","economicsectorhasperson","economicsectorusingacademicfield",
"bankbankincountry","academicfieldusedbyeconomicsector","personineconomicsector",
"agentholdssharesincompany","companyhasshareholder","companyeconomicsector","acquired"]


liCat = [ "personineconomicsector","companyeconomicsector","academicfieldusedbyeconomicsector"
,"companyhasshareholder","acquired","inverseofbankboughtbank","economicsectorusingacademicfield","bankboughtbank"
,"bankbankincountry","agentholdssharesincompany", "economicsectorhasperson","acquiredby","inverseofbankbankincountry"
,"bankchiefexecutiveceo","economicsectorcompany","inverseofbankchiefexecutiveceo"]


for i in range(len(liRel)):
    liRel[i] = "concept:"+liRel[i] 
    
for i in range(len(liCat)):
    liCat[i] = "concept:"+liCat[i] 

for l in lines:
    words = l.split('\t')
    if words[1] in liRel:
        prob = float("{0:.2f}".format(float(words[4])))
        posFile.write(str(prob)+"\t"+pruneWord(words[1])+"("+pruneWord(words[0])+","+pruneWord(words[2])+")"+"\n")
    
    elif words[1]=="generalizations" and words[2] in liCat:
        #this could be in the domain or range..
        prob = float("{0:.2f}".format(float(words[4])))
        posFile.write(str(prob)+"\t"+pruneWord(words[2])+"("+pruneWord(words[0])+")"+"\n")
        
        
posFile.close()
