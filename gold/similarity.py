import math

ascii_min=97
ascii_max=122

def filterNonAlpha(s):
	ret=""
	for c in s:
		ascii= ord(c)
		if ascii <= ascii_max and ascii >= ascii_min:
			ret+=c
			
	return ret

def getMagnitude(f):
	mag=0
	for val in f:
		mag = mag + val*val
	
	return math.sqrt(mag)

def getFeature(st, feature):
	ret = []
	for c in feature:
		count=0
		for s in st:
			if s==c:
				count=count+1
		ret.append(count)
	return ret 

def cosineSimilarity(s1, s2):
	#convert both the strings to lower case...
	s1=s1.lower()
	s2=s2.lower()
	
	s1=filterNonAlpha(s1)
	s2=filterNonAlpha(s2)
	
	#get unique characters..
	s=s1+s2
	
	unique=""
	
	for c in s:
		if c not in unique:
			unique=unique+c
	
	#create the feature vectors..
	f1=getFeature(s1, unique)
	f2=getFeature(s2, unique)
	
	#get corresponding magnitudes..
	mag1= getMagnitude(f1)
	mag2= getMagnitude(f2)
	 	
	cos=0;
	for i in range(len(unique)):
		cos=cos+f1[i]*f2[i]
	
	return float(cos)/(mag1*mag2)


	
print cosineSimilarity("james bond", "dnob")
