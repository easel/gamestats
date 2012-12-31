from xml.etree import ElementTree
from gamestats.loot.models import Character, Item, Loot, Attendance, Kill

def parse_xml(xml):
    """
    Parse an XML submission
    """

    tree = ElementTree.parse(xml)
    elem = tree.getroot()
    submitter = Character.objects.get(name=elem.get('submitter'))

    elem = tree.getroot().find('gamestats.loot')
    for child in elem.getchildren():
        character = Character.objects.get_or_create(name=child.get('looter'))
        item = Item.objects.get_or_create(name=child.get('item'))
        timestamp = child.get('timestamp').replace('T', ' ')
        Loot.objects.get_or_create(
            submitter=submitter,
            timestamp=timestamp,
            looter=character,
            item=item
        )

#    elem = tree.getroot().find('attendance')
#    for child in elem.getchildren():
#        character = Character.objects.get(name=child.get('name'))
#        start_time = child.get('start_time').replace('T', ' ')
#        end_time = child.get('end_time').replace('T', ' ')
#        Attendance.objects.get_or_create(
#            submitter = submitter,
#            attendee = character,
#            start_time = start_time,
#            end_time = end_time
#        )
#        db.addAttendee(userid, characterid, start_time, end_time)

    elem = tree.getroot().find('kills')
    for child in elem.getchildren():
        killer = Character.objects.get_or_create(name=child.get('killer'))
        killee = Character.objects.get_or_create(name=child.get('killee'))
        timestamp = child.get('timestamp').replace('T', ' ')
        Kill.objects.add_if_new(
            submitter = submitter,
            killer = killer,
            killee = killee,
            timestamp = timestamp
        )
