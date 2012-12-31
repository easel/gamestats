import logging

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from gamestats.loot.managers import LootManager, AttendanceManager

class ItemType(models.Model):
    name = models.CharField(max_length=100)

class Item(models.Model):
    name = models.CharField(max_length=200, unique=True)

class CharacterType(models.Model):
    name = models.CharField(max_length=100)

class Character(models.Model):
    name = models.CharField(max_length=100)
    characterType = models.ForeignKey(CharacterType, null=True)

class LootType(models.Model):
    name = models.CharField(max_length=100)

class Loot(models.Model):
    submitter = models.ForeignKey(User)
    timestamp = models.DateTimeField()
    character = models.ForeignKey(Character)
    item = models.ForeignKey(Item)
    lootType = models.ForeignKey(LootType)

    objects = LootManager()

class Drop(models.Model):
    item = models.ForeignKey(Item)
    character = models.ForeignKey(Character)

class Attendance(models.Model):
    submitter = models.ForeignKey(User)
    character = models.ForeignKey(Character)
    start = models.DateTimeField()
    end = models.DateTimeField()

    objects = AttendanceManager()

class Kill(models.Model):
    submitter = models.ForeignKey(User)
    timestamp = models.DateTimeField()
    killer = models.ForeignKey(Character, related_name='kills')
    killee = models.ForeignKey(Character, related_name='deaths')

    objects = KillManager()
        
class Import:
    @staticmethod
    def load():
        conn = EQLogDB.getConnection()
        cur = conn.cursor()
        if False:
            cur.execute("select * from TLKP_ITEM_TYPE")
            for item in cur.itermap():
                v = ItemType(pk=item['ITEM_TYPE_ID'],name=item['ITEM_TYPE'])
                v.save()

            cur.execute('select * from TLKP_CHARACTER_TYPE')
            for i in cur.itermap():
                v = CharacterType(pk=i['CHARACTER_TYPE_ID'],
                                  name=i['CHARACTER_TYPE'])
                v.save()

            cur.execute('select * from TLKP_LOOT_TYPE')
            for i in cur.itermap():
                v = LootType( pk=i['LOOT_TYPE_ID'], name=i['LOOT_TYPE'] )
                v.save()

            cur.execute('select * from TBL_CHARACTER')
            for i in cur.itermap():
                v = Character( pk=i['CHARACTER_ID'], name=i['NAME'])
                if i['CHARACTER_TYPE_ID']:
                    v.characterType=CharacterType.objects.get(pk=i['CHARACTER_TYPE_ID'])
                v.save()

            cur.execute("select * from TBL_ITEM")
            for i in cur.itermap():
                v = Item(pk=i['ITEM_ID'], name=i['name'])
                v.save()

            cur.execute('select * from TBL_USER')
            for i in cur.itermap():
                v = User(pk=i['USER_ID'], username=i['NAME'])
                v.save()

        cur.execute('select * from TBL_LOOT')
        for i in cur.itermap():
            v = Loot( pk=i['LOOT_ID'] )
            v.character = Character.objects.get(pk=i['CHARACTER_ID'])
            v.item = Item.objects.get(pk=i['ITEM_ID'])
            v.timestamp = i['EVENT_TIMESTAMP']
            v.submitter = User.objects.get(pk=i['SUBMITTER_USER_ID'])
            v.lootType = LootType.objects.get(pk=2)
            v.save()

