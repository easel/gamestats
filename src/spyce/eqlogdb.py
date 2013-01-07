import kinterbasdb
import time
import mx
from elementtree import ElementTree

class Callable:
    def __init__(self, anycallable):
            self.__call__ = anycallable

class EQLogDB:
    def __init__(self):
        # Connect to the DB
        self.con = EQLogDB.getConnection()

    def getConnection():
        return kinterbasdb.connect(
            host=None, database='/var/firebird/gamestats.eqlog.fdb',
            user='SYSDBA', password='vsinTI65'
        )
        #return kinterbasdb.connect(
        #    host='firebird.server.realm.ilsw.com', 
	#    database='/filesrv/firebird0/gamestats.eqlog.fdb',
        #    user='SYSDBA', password='NTSUCKS'
        #k)
    getConnection = Callable(getConnection)

    def resultToXml(cursor, writer, roottag ='recordset', attributes = None, recordtag = 'record'):
	if attributes:
	    for key in attributes.keys():
		attributes[key] = EQLogDB.prep_data(attributes[key])

        root = writer.start(roottag, attributes)
        for record in cursor.itermap():
            data = dict()
            for key in record.keys():
                data[key] = EQLogDB.prep_data(record[key])
            writer.start(recordtag, data)
            writer.end()
        writer.end(roottag)
    resultToXml = Callable(resultToXml)

    def prep_data(data):
	"""Stringifies all data for export to XML.  Formats any dates for XSLT."""
	if(type(data) == kinterbasdb.DATETIME):
	    # Convert to EST, and add the timezone to the date string in 
	    # case exslt ever gets smart and learns about timezones
	    return (data + mx.DateTime.TimeDelta(-5.0)).strftime('%Y-%m-%dT%H:%M:%S-05:00')
	elif(data is None or data == 'None'):
	    return ''
	else:
	    return str(data)
    prep_data = Callable(prep_data)


    def listToXml(data, writer, roottag = 'recordset', attributes = None, recordtag = 'record'):
        root = writer.start(roottag, attributes)
        for rec in data:
            writer.start(recordtag, rec)
            writer.end()
        writer.end(roottag)
    listToXml = Callable(listToXml)

    def dictToXml(data, writer, recordtag = 'record'):
        writer.start(recordtag, data)
        writer.end()
    dictToXml = Callable(dictToXml)

    def getLookup(table):
        con = EQLogDB.getConnection()
        cur = con.cursor()
        cur.execute('select * from %s' %(table))
        return cur.fetchall()
        con.commit()
        con.close()
    getLookup = Callable(getLookup)

    def findUserID(self, name, addNew=True):
        cur = self.con.cursor()
        param = list()
        param.append(name)
        cur.execute('select USER_ID from TBL_USER where NAME = ?', param)
        row = cur.fetchone()
        if row:
            return row[0]
        elif addNew:
            cur.execute('select gen_id(GEN_USER_ID, 1) from RDB$DATABASE')
            id = cur.fetchone()[0]
            cur.execute('insert into TBL_USER (USER_ID, NAME) VALUES (?, ?)', (id, name))
            return id
	else:
	    return None

    def findCharacterID(self, name, addNew=True):
        cur = self.con.cursor()
        param = list()
        param.append(name)
        cur.execute('select CHARACTER_ID from TBL_CHARACTER where NAME = ?', param)
        row = cur.fetchone()
        if row:
            return row[0]
        elif addNew:
            cur.execute('select gen_id(GEN_CHARACTER_ID, 1) from RDB$DATABASE')
            id = cur.fetchone()[0]
            cur.execute('insert into TBL_CHARACTER (CHARACTER_ID, NAME) VALUES (?, ?)', (id, name))
            return id
	else:
	    return None

    def findItemID(self, name, addNew=True):
        cur = self.con.cursor()
        param = list()
        param.append(name)
        cur.execute('select ITEM_ID from TBL_ITEM where NAME = ?', param)
        row = cur.fetchone()
        if row:
            return row[0]
        elif addNew:
            cur.execute('select gen_id(GEN_ITEM_ID, 1) from RDB$DATABASE')
            id = cur.fetchone()[0]
            cur.execute('insert into TBL_ITEM (ITEM_ID, NAME) VALUES (?, ?)', (id, name))
	    self.commit()
            return id
	else:
	    return None

    def rawInsert(self, cols, vals):
        cur = self.con.cursor()
        if len(cols) != len(vals):
            raise Exception('Number of columns does not match number of values')
        #colstring = '"' + '","'.join(cols) + '"'
        colstring = ','.join(cols) 
        vall = list()
        for val in vals:
            vall.append('?')
        valstring = ",".join(vall)
        sql = "insert into TBL_ITEM (%s) VALUES (%s);" %(colstring, valstring)
        cur.execute(sql, vals)

    def setItemType(self, item_id, item_type_id):
        cur = self.con.cursor()
        cur.execute("update TBL_ITEM set ITEM_TYPE_ID = ? where ITEM_ID = ?",
             [item_type_id, item_id ])


    def addLoot(self, userid, timestamp, characterid, itemid):
        cur = self.con.cursor()
        try:
            # Query if we've ever seen this character gamestats.loot this lore item, OR if somebody
            # else submitted the same item within +- 7 minutes or so
	    # ignore lore flags for bazu and last blood
	    sql = """
                select count(*)
                from tbl_loot inner join tbl_item
                on tbl_loot.item_id = tbl_item.item_id 
                where 
		tbl_loot.item_id = ? 
		and tbl_loot.character_id = ?
                and extract(hour from tbl_loot.event_timestamp) = extract(hour from cast(? as TIMESTAMP))
                and extract(day from tbl_loot.event_timestamp) = extract(day from cast(? as TIMESTAMP))
                and extract(month from tbl_loot.event_timestamp) = extract(month from cast(? as TIMESTAMP))
                and extract(year from tbl_loot.event_timestamp) = extract(year from cast(? as TIMESTAMP))
"""
	    #raise Exception(sql)
            cur.execute(sql , (itemid, characterid, timestamp, timestamp,timestamp,timestamp))
            if cur.fetchone()[0] == 0: 
                cur.execute("""
                    insert into TBL_LOOT (SUBMITTER_USER_ID, 
                    EVENT_TIMESTAMP, CHARACTER_ID, ITEM_ID) values (?, ?, ?, ?);
                """, (userid, timestamp, characterid, itemid))
		cur.execute("""
		    update TBL_CHARACTER set CHARACTER_TYPE_ID = ? where CHARACTER_ID = ?
		""", (1, characterid))
        except kinterbasdb.ProgrammingError, e:
	    if e[0] == -803:
		"""do nothing for uniqueness violations"""
	    else:
		raise

    def addAttendee(self, userid, characterid, start_time, end_time):
        cur = self.con.cursor()
        try:
            # check if theres already an attendance record for this person
            # which overlaps the provided start and end times. if so, extend it
            # rather than creating a new one
            start_time = mx.DateTime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_time = mx.DateTime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            cur.execute("""
                select attendance_id, start_time, end_time from tbl_attendance
                where character_id = ?
                and ((start_time < ? and start_time > ?)
                or (end_time < ? and end_time > ?)
                or (end_time > ? and start_time < ?))
            """, [characterid, end_time, start_time, end_time, start_time, end_time, start_time])
            vals = cur.fetchone()
            if vals and vals[1] > start_time:
                print "Updating start time ", vals[1], ' to ', start_time
                cur.execute('update TBL_ATTENDANCE set START_TIME = ? where attendance_id = ?', 
                    [start_time, vals[0]])
            elif vals and vals[2] < end_time:
                print "Updating end time ", vals[2], ' to ', end_time
                cur.execute('update TBL_ATTENDANCE set END_TIME   = ? where attendance_id = ?', 
                    [end_time, vals[0]])
            else:
                cur.execute('insert into TBL_ATTENDANCE (SUBMITTER_USER_ID, CHARACTER_ID, '
                + ' START_TIME, END_TIME) values (?, ?, ?, ?) ', (userid, characterid, start_time, end_time))
        except kinterbasdb.ProgrammingError, e:
	    if e[0] == -803:
		"""do nothing for uniqueness violations"""
	    else:
		raise
	self.reCompute()

    def addKill(self, userid, killerid, killeeid, timestamp):
        cur = self.con.cursor()
        try:
            # seee if somebody else already submitted the same kill within 7 minutes or so,
            # if not, store it
            cur.execute("""
                select count(*) from TBL_KILL where SUBMITTER_USER_ID != ? AND KILLER = ?
                and KILLEE = ? and EVENT_TIMESTAMP + 0.005 > ? and EVENT_TIMESTAMP - 0.005 < ?
            """, [userid, killerid, killeeid, timestamp, timestamp])
            if cur.fetchone()[0] == 0:
                cur.execute('insert into TBL_KILL (SUBMITTER_USER_ID, KILLER, KILLEE, EVENT_TIMESTAMP) values (?, ?, ?, ?)', 
                    (userid, killerid, killeeid, timestamp))
        except kinterbasdb.ProgrammingError, e:
	    if e[0] == -803:
		"""do nothing for uniqueness violations"""
	    else:
		raise

    def reCompute(self):
	cur = self.con.cursor()
	cur.execute("""
update tbl_attendance set raid_flag = 1 where
raid_flag IS NULL and
exists (
select tbl_loot.loot_id from tbl_loot inner join
tbl_item on tbl_loot.item_id = tbl_item.item_id
where (tbl_item.item_type_id = 5
or tbl_item.item_type_id = 6
or tbl_item.item_type_id = 7)
and event_timestamp > tbl_attendance.start_time
and event_timestamp < tbl_attendance.end_time )
	""")
	cur.execute("""update tbl_attendance set raid_flag = 0 where raid_flag IS NULL""")
	self.commit()

    def deDuplicate(self):
	cur = self.con.cursor()
	cur.execute("""
	    select tbl_loot.loot_id, tbl_loot.character_id, 
	    tbl_item.item_id, tbl_item.name, tbl_loot.submitter_user_id
	    from tbl_loot 
	    left join tbl_item on tbl_loot.item_id = tbl_item.item_id 
	    where (tbl_item.item_type_id = 5 
	    or tbl_item.item_type_id = 6
	    or tbl_item.item_type_id = 7 )
	    and tbl_item.item_id != 33315 
	    and tbl_item.item_id != 33316 
	    order by tbl_loot.character_id, tbl_loot.item_id
	""")
	last = tuple((None, None, None, None, None))
	cur2=self.con.cursor()
	for row in cur:
	    if row[1] == last[1] and row[2] == last[2] and row[4] != last[4]:
		print 'Deleting ', last, row
		cur2.execute('delete from tbl_loot where loot_id = ?', [row[0]])
	    last = tuple((row[0], row[1], row[2], row[3], row[4]))
	self.commit()
	

    def commit(self):
        self.con.commit()

    def main(self):
	self.deDuplicate()

if __name__ == "__main__":
    e = EQLogDB()
    e.main()
