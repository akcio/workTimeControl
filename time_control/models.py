# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timesince import timesince
# Create your models here.

class WorkTime(models.Model):
    id = models.AutoField(primary_key=True)
    startTime = models.DateTimeField('start', default=datetime.min)
    endTime = models.DateTimeField('end', default=datetime.min)
    user = models.ForeignKey(User)

    def __str__(self):
        return "User: " + str(self.user.username) + ". Timed: " +str(self.startTime) + "| - |" + str(self.endTime)

    def get_time_diff(self):
        return timesince(self.startTime, self.endTime)