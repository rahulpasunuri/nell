fileName="kbp.txt"

f=open(fileName, "r")
lines=f.readlines()
f.close()

for l in lines:
	l=l.strip()
	#'=' in line => a mapping is defined between nell and kbp relations..
	if l[0:2]!="//" and l!="" and '=' in l:
		if (" and " not in l) and (" or " not in l): #TODO
			i = l.find('=')
			kbp_pred=l[:i].strip()
			nell_pred=l[i+1:].strip()[6:]
			
