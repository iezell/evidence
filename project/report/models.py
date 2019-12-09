from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.core.signals import request_finished
from django.dispatch import receiver

from simple_history.models import HistoricalRecords

import datetime

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
    responseDict = {}
    changed = []
    data = {}
    senderHistory = {}
    skip = ['_state','id']

    try:
        senderHistory = sender.history.first().prev_record.__dict__
        operation = 'updated'
    except AttributeError:
        operation = 'created'

    for i in instance.__dict__:
        if i in skip:
            continue

        if i in senderHistory.keys() and instance.__dict__[i] != '':
            if instance.__dict__[i] != senderHistory[i]:
                changed.append(i)
                data.update({i: instance.__dict__[i]})

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
    mongoCol.insert_one(responseDict)

@receiver(post_delete, sender=User)
@receiver(post_delete, sender=Organization)
def deleteReport(sender, instance, **kwargs):
    responseDict = {}
    responseDict.update({"operation": "deleted",
                         "changed": 'null',
                         "data": 'null',
                         "pk": instance.id,
                         "class": instance.__class__.__name__,
                         "time": datetime.datetime.now().isoformat()})

    # print(responseDict)
    mongoCol.insert_one(responseDict)