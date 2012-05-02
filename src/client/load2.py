#!/usr/bin/env python
import time
import sys
import mx
import csv
sys.path.append('site')
import eqlogdb

db = eqlogdb.EQLogDB()
#r = csv.reader(file('UF-Old-DB.txt'), dialect='excel')
r = csv.reader(file('errors.txt'), dialect='excel')
#print r.next()

errs = csv.writer(file('olderrors.txt', 'w'))

for rec in r:
    try:
	event_timestamp = mx.DateTime.strptime(rec[0], '%m/%d/%Y')
	itemid = db.findItemID(rec[3], addNew=False)
	characterid = db.findCharacterID(rec[2], addNew=False)
	if None == itemid or None == characterid:
	    errs.writerow(rec)
	else:
	    db.setItemType(itemid, 6)
	    db.addLoot(0, event_timestamp, characterid, itemid)
    except:
	""" do nothing """
	#raise
db.commit()


