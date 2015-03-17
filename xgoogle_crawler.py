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


#search google
for p in relPatterns:
    words=p.split()
    s="%20".join(words)
    s = "%22"+s+"%22"
    
    #limit the results to 3
    count=0

    try:
        gs = GoogleSearch(p) #input the pattern here..
        gs.results_per_page = 10
        results = gs.get_results()

        if len(results)==0:
            print "Error"
        
        for res in results:
            #print res.title.encode("utf8")
            #print res.desc.encode("utf8")
            #print res.url.encode("utf8")
            
            if count>3:
                break
            
            count = count+1
            
            print
    except SearchError, e:
        print "Search failed: %s" % e
	
outFile = open(outFileName, "w")
for s in data:
	outFile.write(s+"\n")	
outFile.close()	
print "Total Miss Count is ", totalMiss
#break#TODO





'''
from xgoogle.search import GoogleSearch
gs = GoogleSearch("catonmat")
gs.results_per_page = 10
results=[]
#results = gs.get_results()

while len(results)<30:

    tmp = gs.get_results()
    if not tmp: # no more results were found
      break
    results.extend(tmp)
    
    
print 'results', gs.num_results  # number of results

if len(results)==0:
    print "No Results"

for res in results:
    print res.url.encode('utf8')
    print "what??"

'''












'''
#!/usr/bin/python
from xgoogle.search import GoogleSearch, SearchError
try:
  gs = GoogleSearch("Batman\\ and\\ I")
  gs.results_per_page = 50
  results = gs.get_results()
  print 'results', gs.num_results  # number of results
  for res in results:
    print res.title.encode("utf8")
    print res.desc.encode("utf8")
    print res.url.encode("utf8")
    print
except SearchError, e:
  print "Search failed: %s" % e
'''
