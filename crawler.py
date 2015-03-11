import urllib2
import urlparse
import time
import pprint
import json
import BeautifulSoup # get html links

dbFileName = "extractionPatterns.csv"
outFileName = "data.txt"
rels=["ceoof"]
cat=[]

f = open(dbFileName, "r")
lines = f.readlines()

relPatterns=[]
catPatterns=[]

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
    data = json.loads(googlePage.read())
    for r in data["responseData"]["results"]:
        print r["url"]
    
