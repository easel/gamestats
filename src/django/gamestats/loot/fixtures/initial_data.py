from django.contrib.auth.models import User
from gamestats.loot.models import LootType

def apply():
    apply_loottypes()
    apply_users()

def apply_loottypes():
    for name in ('Unknown', 'Raid Loot', 'Rare Quest', 'Spell'):
        LootType.objects.get_or_create(name=name)

def apply_users():
    for name in ('bardeil', 'zarax', 'archus', 'hador', 'vaynelle'):
        User.objects.get_or_create(username=name)
