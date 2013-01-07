from xml.etree import ElementTree
from django.contrib.auth.models import User
from gamestats.loot.models import Character, Item, Loot, Attendance, Kill, LootType

def parse_xml(xml):
    """
    Parse an XML submission
    """

    root = ElementTree.fromstring(xml)
    submitter = User.objects.get(username__iexact=root.get('submitter'))

    elem = root.find('loot')
    for child in elem.getchildren():
        character, _ = Character.objects.get_or_create(name=child.get('looter'))
        item, _ = Item.objects.get_or_create(name=child.get('item'))
        timestamp = child.get('timestamp').replace('T', ' ')
        Loot.objects.get_or_create(
            submitter=submitter,
            timestamp=timestamp,
            character=character,
            item=item,
            defaults = {
                'lootType': LootType.objects.get(name='Unknown')
            }
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

    root.find('kills')
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
