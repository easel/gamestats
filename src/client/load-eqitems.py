#!/usr/bin/env python
import time
import sys
import mx
import kinterbasdb
sys.path.append('site')
import eqlogdb
db = eqlogdb.EQLogDB()
f = file('items.txt')
headerline = f.readline()
headers = headerline.strip().split('|')
headers[headers.index('size')] = 'itemsize'
headers[headers.index('id')] = 'item_id'
headers.append('item_type_id')
print "%d columns" %(len(headers))
print headers
for line in f:
    vals = line.strip().split('|')
    #for i in range(0, len(vals)):
	#try:
	    #vals[i] = int(vals[i]) 
	#except:
	#    "do nothing"
    vals.append(None)
    if vals[headers.index('verified')] == '0':
	vals[headers.index('verified')] = None
    else:
	vals[headers.index('verified')] = mx.DateTime.mktime(time.strptime(
	    vals[headers.index('verified')], "%Y%m%d%H%M%S"))
    if len(headers) == len(vals):
	try:
	    db.rawInsert(headers, vals)
	except kinterbasdb.ProgrammingError,  e:
	    if e[0] == -803:
		"do nothing for unique constaint violations"
	    else:
		raise
db.commit()

