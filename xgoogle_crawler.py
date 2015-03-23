import re
import urllib2
import urlparse
import time
import pprint
import json
from xgoogle.search import GoogleSearch, SearchError


dbFileName = "extractionPatterns.csv"
outFileName = "data.txt"
rels=["ceoof"]
cat=[]


#endMarkPattern = "[\.\<\>!;\"=]"
endMarkPattern = "[\.\<\>!=]"

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
    
    #limit the results to 5
    count=0

    try:
        gs = GoogleSearch(p) #input the pattern here..TODO choose between s or p ??
        gs.results_per_page = 25
        results = gs.get_results()

        if len(results)==0:
            print "No Results found for pattern: ",p
            continue
        
        for res in results:
            try:
                page=urllib2.urlopen(res.url.encode("utf8"))
                content = page.read()    	
                sentences = endMarkRegex.split(content)
                for s in sentences:				
                    if p in s:
                        data.append(s.strip())                        
				        
                if count>5:
                    break            
                count = count+1            
            except:
                print "Error reading the URL: ", res.url.encode("utf8")
            
            
    except SearchError, e:
        print "Search failed: %s" % e
        
    
	
outFile = open(outFileName, "w")
for s in data:
	outFile.write(s+"\n")	
outFile.close()	

