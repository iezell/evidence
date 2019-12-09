from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.core.signals import request_finished
from django.dispatch import receiver

from simple_history.models import HistoricalRecords

import datetime, pymongo

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    history = HistoricalRecords()

class Organization(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True, db_index=True)
    history = HistoricalRecords()

@receiver(post_save, sender=User)
@receiver(post_save, sender=Organization)
def upsertReport(sender, instance, **kwargs):
    #MongoDB Connection to objectreport db and report collection
    client = pymongo.MongoClient('localhost', 27017)
    db = client.objectreport
    collection = db.report

    responseDict = {}
    changed = []
    data = {}
    senderHistory = {}
    skip = ['_state','id']

    #Determines Updated or Created based of history
    try:
        senderHistory = sender.history.first().prev_record.__dict__
        operation = 'updated'
    except AttributeError:
        operation = 'created'

    for i in instance.__dict__:
        #Cleans a couple extra fields
        if i in skip:
            continue

        #Checks for Updates to Fields
        if i in senderHistory.keys() and instance.__dict__[i] != '':
            if instance.__dict__[i] != senderHistory[i]:
                changed.append(i)
                data.update({i: instance.__dict__[i]})

        #Adds Fields in Not Present in Object History
        elif i not in senderHistory.keys() and instance.__dict__[i] != '':
            changed.append(i)
            data.update({i: instance.__dict__[i]})

    responseDict.update({"operation": operation,
                         "changed": changed,
                         "data": data,
                         "pk": instance.id,
                         "class": instance.__class__.__name__,
                         "time":datetime.datetime.now().isoformat()})

    # print(responseDict)
    collection.insert_one(responseDict)

@receiver(post_delete, sender=User)
@receiver(post_delete, sender=Organization)
def deleteReport(sender, instance, **kwargs):
    #MongoDB Connection to objectreport db and report collection
    client = pymongo.MongoClient('localhost', 27017)
    db = client.objectreport
    collection = db.report

    #Fills In Deleted Fields
    responseDict = {}
    responseDict.update({"operation": "deleted",
                         "changed": 'null',
                         "data": 'null',
                         "pk": instance.id,
                         "class": instance.__class__.__name__,
                         "time": datetime.datetime.now().isoformat()})

    # print(responseDict)
    collection.insert_one(responseDict)
