import optparse
import email.Utils
import time
import re
import types
import os
import httplib
import cStringIO
from elementtree.SimpleXMLWriter import XMLWriter

MAX_FIGHT_PAUSE = 10
MAX_CACHED_ENTRIES = 20
XML_TIMESTAMP_FMT = '%Y-%m-%dT%H:%M:%S'
MAX_ATTENDEE_SILENCE = 30*60 # max amount of time without
MIN_ATTENDEE_TIME = 5*60     # minimum number of seconds to count as attended

class Fight:
    """ class for fight data """
    def __init__(self, attacker, defender, starttime):
        self.attacker = attacker
        self.defender = defender
        self.starttime = starttime
        self.lasttime = starttime
        self.attacks = dict()
        self.complete = False
        self.damage = 0

    def __getAttack(self, timestamp, atktype):
        if not self.attacks.has_key(atktype):
            self.attacks[atktype] = dict()
        self.lasttime = timestamp
        return self.attacks[atktype]

    def addAttack(self, timestamp, atktype, amount):
        attack = self.__getAttack(timestamp, atktype)
        if not attack.has_key(amount):
            attack[amount] = 1
        else:
            attack[amount] = self.attacks[atktype][amount] + 1
        if type(amount) is types.IntType:
            self.damage = self.damage + amount
            

    def endFight(self, timestamp):
        """ end the fight """
        self.lasttime = timestamp
        self.complete = True
        
    def __repr__(self):
        result = "%s vs %s for %d sec\n" % (self.attacker, self.defender, self.lasttime - self.starttime)
        
        for atktype in self.attacks.keys():
            result = result + "\t%s\n" %(atktype)
            if type(self.attacks[atktype]) is types.DictType:
                vals = list(self.attacks[atktype].keys())
                vals.sort()
                i = 0
                for val in vals:
                    if type(val) is types.IntType:
                        i = i+1
                        result = result + "\t\t%d\t%d\t%d\n" % ( i, val, self.attacks[atktype][val])
                    else:
                        result = result + "\t\t%s\t%d\n" % ( val, self.attacks[atktype][val])


        result = result + 'Total Damage: %8d (%4.0f DPS)\n' %(self.damage, float(self.damage) / self.elapsedTime())
        return result

    def elapsedTime(self):        
        etime = self.lasttime - self.starttime
        if etime == 0:
            etime = 1
        return etime

    def asXml(self, writer):
        fmt="%Y-%m-%dT%H:%M:%S"
        writer.start('fight', attacker=self.attacker, defender=self.defender,
                       starttime=time.strftime(fmt, time.gmtime(self.starttime)),
                       endtime=time.strftime(fmt, time.gmtime(self.lasttime)))
        for atktype in self.attacks.keys():
            if type(self.attacks[atktype]) is types.DictType:
                vals = list(self.attacks[atktype].keys())
                vals.sort()
                i = 0
                for val in vals:
                    if type(val) is types.IntType:
                        writer.element('attack', type=atktype, amount=str(val), count=str(self.attacks[atktype][val]))
                    else:
                        writer.element('evade', type=val, count=str(self.attacks[atktype][val]))
        writer.element('summary', damage=str(self.damage), elapsed_time=str(self.elapsedTime()),
                       dps=str(float(self.damage)/self.elapsedTime()))
        writer.end('fight')

class FightTracker:
    """ keep track of fight data """
    def __init__(self, debug=False):
        self.lasttime = 0
        self.fights = dict()
        self.complete_fights = list()

    def __endFight(self, timestamp, key):
        self.fights[key].endFight(timestamp)
        self.complete_fights.append(self.fights[key])
        #print self.fights[key]
        del self.fights[key]
        

    def getFight(self, timestamp, attacker, defender):
        """
        return the ongoing fight for attacker and defender
        if there is no active fight, create a new one and return the handle to it
        """
        fightkey = '%s vs %s' %(attacker, defender)
        if self.fights.has_key(fightkey):
            fight = self.fights[fightkey]
            if timestamp - fight.lasttime > MAX_FIGHT_PAUSE:
                self.__endFight(timestamp, fightkey)
        if not self.fights.has_key(fightkey):
            fight = Fight(attacker, defender, timestamp)
            self.fights[fightkey] = fight
        return self.fights[fightkey]

    def addDeath(self, timestamp, attacker, defender):
        """
        since somebody died, clear out all his fights
        """
        for key in self.fights.keys():
            if self.fights[key].defender == defender or self.fights[key].attacker == defender:
                self.__endFight(timestamp, key)

        
    def __repr__(self):
        result = ''
        for fight in self.complete_fights:
            result = result + repr(fight) + "\n"
        return result

    def asXml(self, writer):
        writer.start("fights")
        for fight in self.complete_fights:
            fight.asXml(writer)
        writer.end()

class AttendanceTracker:
    def __init__(self, debug=False):
        self.FIRST = 0
        self.LAST = 1
        self.current = dict()
        self.log = list()
        self.lastprune = 0 
        self.debug = debug

    def __repr__(self):
        return repr(self.log)

    def __len__(self):
        return len(self.log)

    def clear(self):
        self.log = list()

    def mark(self, timestamp, attendee):
        if not attendee:
            return
        self.prune(timestamp)
        if self.current.has_key(attendee):
            rec = self.current[attendee]
            if rec[1] - timestamp < MAX_ATTENDEE_SILENCE:
                self.current[attendee][1] = timestamp
        else:
            self.current[attendee] = [timestamp, timestamp]
            if self.debug:
                print "%10s %s joined the raid" %(time.strftime("%c", 
                        time.localtime(timestamp)), attendee)

    def unmark(self, attendee):
        rec = self.current[attendee]
        elapsed_time = rec[1] - rec[0]
        if elapsed_time > MIN_ATTENDEE_TIME:
            self.log.append((attendee, rec[0], rec[1]))
            if self.debug:
                print "%10s %s was last seen, was active for %.1f min" %(time.strftime("%c", 
                        time.localtime(rec[1])), attendee, float(rec[1] - rec[0])/60.0)
        del self.current[attendee]

    def prune(self, timestamp):
        if timestamp - self.lastprune > MAX_ATTENDEE_SILENCE:
            self.lastprune = timestamp
            for attendee in self.current.keys():
                rec = self.current[attendee]
                if timestamp - rec[1] > MAX_ATTENDEE_SILENCE:
                    self.unmark(attendee)

    def asXml(self, writer):
        writer.start('attendance')
        for rec in self.log:
            writer.element('attendee',
                    name = rec[0],
                    start_time = time.strftime(XML_TIMESTAMP_FMT, time.gmtime(rec[1])),
                    end_time = time.strftime(XML_TIMESTAMP_FMT, time.gmtime(rec[2]))
                    )
        writer.end()

class LootTracker:
    def __init__(self, debug=False):
        self.loot = list()
        self.debug = debug

    def __len__(self):
        return len(self.loot)

    def __repr__(self):
        return repr(self.loot)

    def clear(self):
        self.loot = list()

    def addLoot(self, timestamp, looter, item):
        self.loot.append((timestamp, looter, item))
        if self.debug:
            print "%10s %s looted %s" %(time.strftime("%c", 
                    time.localtime(timestamp)), looter, item)

    def asXml(self, writer):
        writer.start('loot')
        for lootevent in self.loot:
            writer.element('event', 
                    timestamp=time.strftime(XML_TIMESTAMP_FMT, time.gmtime(lootevent[0])),
                    looter=lootevent[1],
                    item=lootevent[2]
                    )
        writer.end()

class KillTracker:
    def __init__(self, debug=False):
        self.clear()
        self.debug=debug

    def __len__(self):
        return len(self.kills)

    def __repr__(self):
        return repr(self.kills)

    def clear(self):
        self.kills = list()

    def addKill(self, timestamp, mob):
        self.kills.append((timestamp, mob))
        if self.debug:
            print "%10s kill of %s" %(time.strftime("%c", 
                    time.localtime(timestamp)), mob)

    def asXml(self, writer):
        writer.start('kills')
        for kill in self.kills:
            writer.element('kill',
                timestamp = time.strftime(XML_TIMESTAMP_FMT, time.gmtime(kill[0])),
                mob = kill[1]
                )
        writer.end()

class Parser:
    """ parser class. parses lines via addLine into tables """
    def __init__(self, extract=None, debug=False, myname=None):
        self.extract = extract
        self.re_damage = re.compile('^(.*) (punche?s?|kicks?|bashe?s?|claws?|bites?|hits?|slashe?s?|crushe?s?|pierces?) (.*) for (\d+) points of (non-melee)? ?damage')
        self.re_death = re.compile('(.*) (has been slain by|have slain) (.*)!')
        self.re_miss = re.compile('^(.*) tries to (claw|bite|hit|slash|crush|pierce) (.*) but misses')
        self.re_defensive = re.compile('^(.*) tr\w+ to (claw|bite|hit|slash|crush|pierce) .*, but (.*) (dodges?|parry?i?es?|blocks?|ripostes?)!')
        self.re_loot = re.compile('--(\w*) ha[vs]e? looted a (.*).--')
        self.re_attendance = re.compile('^(\w*) (tells? |says?,|begins? to cast)')
        self.re_myname = re.compile('[Yy]our? ')
        self.myname = myname
    
        self.fights = FightTracker(debug=debug)
        self.loot = LootTracker(debug=debug)
        self.kills = KillTracker(debug=debug)
        self.attendance = AttendanceTracker(debug=debug)

    def parseLine(self, line):
        """ parse a line of eq logfile """

        # Bail out on lines with a malformed timestamp
        try:
            timestamp = time.mktime(time.strptime(line[1:25], "%a %b %d %H:%M:%S %Y"))
        except:
            return
        
        text = line[27:]
        
        if self.myname:      
            self.attendance.mark(timestamp, self.myname)
            text = self.re_myname.sub(self.myname + ' ', text)  
            
        damage = self.re_damage.search(text)
        #damage = False
        death = self.re_death.search(text)
        #death = False
        miss = self.re_miss.search(text)
        #miss = False
        #defensive = self.re_defensive.search(text)
        defensive = False
        loot = self.re_loot.search(text)
        attendance = self.re_attendance.search(text)
        if damage:
            (attacker, atktype, defender, amount,  nonmelee) = damage.groups()
            if nonmelee:
                atktype = 'non-melee'
            if self.extract and (self.extract == attacker or self.extract == defender):
                self.fights.getFight(timestamp, attacker, defender).addAttack(timestamp, atktype, int(amount))
                if attacker.count(' ') == 0:
                    self.attendance.mark(timestamp, attacker)
                if defender.count(' ') == 0:
                    self.defender.mark(timestamp, defender)
        elif miss:
            (attacker, atktype, defender) = miss.groups()
            if self.extract and (self.extract == attacker or self.extract == defender):
                self.fights.getFight(timestamp, attacker, defender).addAttack(timestamp, atktype, 'miss')
                if attacker.count(' ') == 0:
                    self.attendance.mark(timestamp, attacker)
                if defender.count(' ') == 0:
                    self.defender.mark(timestamp, defender)
        elif defensive:
            (attacker, atktype, defender, defensetype) = defensive.groups()
            if self.extract and (self.extract == attacker or self.extract == defender):
                self.fights.getFight(timestamp, attacker, defender).addAttack(timestamp, atktype, defensetype)
                if attacker.count(' ') == 0:
                    self.attendance.mark(timestamp, attacker)
                if defender.count(' ') == 0:
                    self.defender.mark(timestamp, defender)
        elif death:
            (defender, junk, attacker) = death.groups()
            if junk.count('have slain'):
                (defender, attacker) = (attacker, defender)
            # Use PC deaths to track their attendance
            if defender.count(' ') == 0:
                self.attendance.mark(timestamp, defender)
            elif attacker.count(' ') == 0:
                self.kills.addKill(timestamp, defender)
            if self.extract and (self.extract == attacker or self.extract == defender):
                self.fights.addDeath(timestamp, attacker, defender)
                if attacker.count(' ') == 0:
                    self.attendance.mark(timestamp, attacker)
        elif loot:
            (looter, item) = loot.groups()
            self.loot.addLoot(timestamp, looter, item)
            self.attendance.mark(timestamp, looter)
        elif attendance:
            attendee = attendance.group(1)
            self.attendance.mark(timestamp, attendee)

    def __repr__(self):
        return str(self.fights)


    def asXml(self):
        outs = cStringIO.StringIO()
        w = XMLWriter(outs)
        root = w.start("parsedlog")
        self.fights.asXml(w)
        self.loot.asXml(w)
        self.attendance.asXml(w)
        self.kills.asXml(w)
        w.close(root)
        return str(outs.getvalue())

    def persist(self):
        # Stuff the xml into an http post
        headers = {"Content-type": "application/xml",
                   "Accept": "text/plain"}

        conn = httplib.HTTPConnection('beauty.quonic.net')
        conn.request("POST", "/~erik/eqlogdb/submit.psp", self.asXml)
        response = conn.getresponse()
        if response.status == 200:
                self.loot.clear()
                self.attendance.clear()
                self.kills.clear()
        print response.read()
        conn.close()

    def persistIfNeeded(self):
        if len(self.loot) > MAX_CACHED_ENTRIES \
                    or len(self.attendance) > MAX_CACHED_ENTRIES \
                    or len(self.kills) > MAX_CACHED_ENTRIES:
            self.persist()

    def parse(self, filename):
        """ parse 'filename' for new lines into memory """
        infile = file(filename)
        for line in infile:
            self.parseLine(line)

class Main:
    def main(self):
        usage = "usage: %prog [-mpo]"
        parser = optparse.OptionParser(usage)
        parser.add_option("-m", "--monitor",
            help="file to monitor",
            dest="monitorfile", default=None)
        parser.add_option("-p", "--parse",
            help="file to parse",
            dest="parsefile", default=None)
        parser.add_option("-l", "--loot", 
            help="print loot listing", dest="loot", 
            action="store_true", default=False)
        parser.add_option("-e", "--extract",
            help="fighter to extract",
            dest="extract", default=None)
        parser.add_option("-n", "--myname",
            help="log owners name", 
            dest="myname", default=None)
        parser.add_option("-o", "--output",
            help="output file", dest="outputfile", default=None)
        parser.add_option("-t", "--output-type", help="output type",
            dest="output_type", default='Text')
        parser.add_option("-d", "--debug", help="debug",
            dest="debug", default=False)
        

        (options, args) = parser.parse_args()

        self.parser = Parser(extract=options.extract, debug=options.debug, 
                myname = options.myname)              
        self.output_type = options.output_type
        self.loot = options.loot
        if options.monitorfile:
            print "Monitoring %s" % (options.monitorfile)
            self.monitor(options.monitorfile)
        elif options.parsefile:
            self.parse(options.parsefile)
            self.parser.persist()
        else:
            parser.error('You must specify at least one action')
        
    def monitor(self, filename):
        """ monitor 'filename' for new lines, outputting fights as they are completed """
        self.do_tail(filename, 0)

    # Simple 'tail' implementation
    # Contributed to Python Cookbook by Ed Pascoe (2003)
    def tail_lines(self, fd, linesback = 0):
        avgcharsperline = 75

        while 1:
            try:
                fd.seek(-1 * avgcharsperline * linesback, 2)
            except IOError:
                fd.seek(0)

            if fd.tell() == 0:
                atstart = 1
            else:
                atstart = 0

            lines = fd.read().split("\n")
            if (len(lines) > (linesback+1)) or atstart:
                break

            avgcharsperline=avgcharsperline * 1.3

        if len(lines) > linesback:
            start = len(lines) - linesback - 1
        else:
            start = 0

        return lines[start:len(lines)-1]

    def do_tail(self, filename, lines):
        print "File is " + filename
        fd = file(filename)
        fd.seek(0,2)

        for line in self.tail_lines(fd, lines):
            func(line + "\n")

        while 1:
            where = fd.tell()
            line = fd.readline()
            if not line:
                fd_results = os.fstat(fd.fileno())
                try:
                    st_results = os.stat(filename)
                except OSError:
                    st_results = fd_results

                if st_results[1] == fd_results[1]:
                    time.sleep(1)
                    fd.seek(where)
                else:
                    print "%s changed inode numbers from %d to %d" % (filename, fd_results[1], st_results[1])
                    fd = file(filename)
            else:
            # Do the work
                self.parser.parseLine(line)

def main():
    m = Main()
    m.main()
