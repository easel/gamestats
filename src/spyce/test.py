import eqlogdb
import mx

db = eqlogdb.EQLogDB()
con = db.getConnection()
cur = con.cursor()
characterid = db.findCharacterID('Bardeil')
itemid = db.findItemID('Blue Diamond')
print 'itemid is %d' %(itemid)
t = '2006-01-14 03:56:05.00'
cur.execute("""select count(*)
from tbl_loot inner join tbl_item
on tbl_loot.item_id = tbl_item.item_id where tbl_loot.item_id = ?
and tbl_loot.character_id = ? 
and tbl_loot.submitter_user_id != ?
and (tbl_item.loregroup != 0 
or (tbl_loot.event_timestamp + 0.005 > ? and tbl_loot.event_timestamp -0.005 < ?))
""" , [itemid, characterid, 1, t, t])
#, [itemid, characterid])
if cur.fetchone()[0] > 0:
    print 'already logged'
else:
    print 'not logged'

#start_time = mx.DateTime.strptime( '2006-03-23 19:00:00', '%Y-%m-%d %H:%M:%S')
start_time = mx.DateTime.strptime( '2006-03-24 01:00:00', '%Y-%m-%d %H:%M:%S')
end_time = mx.DateTime.strptime( '2006-03-24 03:00:00', '%Y-%m-%d %H:%M:%S')
print start_time.gmtime(), end_time.gmtime()
cur.execute(""" 
    select attendance_id, start_time, end_time from tbl_attendance
    where character_id = ?
    and ((start_time < ? and start_time > ?)
    or (end_time < ? and end_time > ?)
    or (end_time > ? and start_time < ?))
""" , [characterid, end_time, start_time, end_time, start_time, end_time, start_time])
vals = cur.fetchone()
print vals
if vals and vals[1] > start_time:
    print "Updating ", vals[1], ' to ', start_time
if vals and vals[2] < end_time:
    print "Updating ", vals[2], ' to ', end_time

