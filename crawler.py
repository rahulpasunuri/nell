import re
import urllib2
import urlparse
import time
import pprint
import json

dbFileName = "extractionPatterns.csv"
outFileName = "data.txt"
rels=["ceoof"]
cat=[]


endMarkPattern = "[\.\<\>!;\"=]"
endMarkRegex = re.compile(endMarkPattern)

f = open(dbFileName, "r")
lines = f.readlines()

relPatterns=[]
catPatterns=[]

data=[]
totalMiss=0
#skip the first line..
lines=lines[1:]

for l in lines:
    words = l.split('\t')
    if words[0] in rels:
        p = words[2]
        p=p.replace("arg1", "")
        p=p.replace("arg2", "")
        p=p.strip()
        relPatterns.append(p)

#this header information is used to send requests..(avoids 403 forbidden error)
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}

#search google
for p in relPatterns:
	words=p.split()
	s="%20".join(words)
	s = "%22"+s+"%22"

	#create the search url
	#url="http://www.google.com/search?as_q=&as_epq="+s

	#can get more results with continuous calling as a client..
	url="http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&start=0&q="+s
	req = urllib2.Request(url, headers=hdr)   

	#get the search page//
	googlePage = urllib2.urlopen(req)
	googleJson = json.loads(googlePage.read())

	#fetch only the top 3 results of each query.
	count=0
	
	try:
		if googleJson is None or googleJson["responseData"] is None and googleJson["responseData"]["results"] is None:#error checking..
			print "some thing wrong with the pattern/google: "+p
			continue
	except:
		#wait for a minute for google to allow us to search again.
		print "some thing wrong with the pattern/google: "+p
		
		print "Waiting for 5 minutes."
		time.sleep(300)
		totalMiss=totalMiss+1
		
		continue
			
	for r in googleJson["responseData"]["results"]:
		if count>3:
			break
		count = count+1
		#print r["url"]
		print "Checking URL: "+r["url"]

		try:
			page=urllib2.urlopen(r["url"])
			content = page.read()    	
			sentences = endMarkRegex.split(content)
			for s in sentences:				
				if p in s:
					data.append(s.strip())					
					isPresent=True
			if isPresent == False:
				print "link didnot match with pattern- "+p+" ", r["url"]
		except:
			print "Error reading the link: ",r["url"]			
		
	#break #TODO
	
outFile = open(outFileName, "w")
for s in data:
	outFile.write(s+"\n")	
outFile.close()	
print "Total Miss Count is ", totalMiss
#break#TODO
