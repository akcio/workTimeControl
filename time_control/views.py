# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from datetime import datetime
from math import ceil

# Create your views here.

from django.http import HttpResponse, Http404
from .models import WorkTime
from django.contrib.auth.models import User

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def indexUser(request, userName):
    time_started = False
    try:
        user = User.objects.get_by_natural_key(userName)
        wti = WorkTime.objects.all().filter(user=user, startTime__lte = datetime.now(), endTime=datetime.min)
        time_started = (wti.count() > 0)
    except User.DoesNotExist:
        raise Http404("No user")
    return render(request, 'index.html', {'userName': userName, 'started' : time_started})


def startWork(request, userName):
    try:
        user = User.objects.get_by_natural_key(userName)
    except User.DoesNotExist:
        raise Http404("No user!")
    startedTime = datetime.now()
    if(WorkTime.objects.all().filter(user=user, startTime__lte = datetime.now(), endTime=datetime.min)):
        return HttpResponse("Already started")
    #if (WorkTime.objects.all().filter(user=user, startTime))
    wti = WorkTime(startTime=startedTime, user=user)
    wti.save()
    return HttpResponse("Hello! Workstart in: %s" %startedTime)

def endWork(request, userName):
    try:
        user = User.objects.get_by_natural_key(userName)
    except:
        raise Http404("No user!")
    wti = WorkTime.objects.filter(user = user, endTime = datetime.min).first()
    if wti == None:
        return HttpResponse('Not started yet')
    wti.endTime = datetime.now()
    wti.save()
    return HttpResponse('ended')

def getStatisticByUser(user, reportStart = datetime.min, reportEnd = datetime.max):
    allDateTime = 0.0
    for item in WorkTime.objects.all().filter(user=user, startTime__gte = reportStart, endTime__lte = reportEnd):
        if (item.endTime < item.startTime):
            continue
        delta = item.endTime - item.startTime
        allDateTime = allDateTime + delta.seconds
    if (allDateTime > 0):
        allDateTime = ceil(allDateTime / 3600.0)
    return allDateTime

def getStatistic(request, userName, reportStart = datetime.min, reportEnd = datetime.max):
    try:
        user = User.objects.get_by_natural_key(userName)
        reportStart = datetime.strptime(request.GET.get('start', '1900-01-01-00-00'), '%Y-%m-%d-%H-%M')
        reportEnd = datetime.strptime(request.GET.get('end', '2050-12-31-23-59'), '%Y-%m-%d-%H-%M')
    except:
        raise Http404("No user")
    allDateTime = getStatisticByUser(user, reportStart, reportEnd)
    if allDateTime > 0:
        return render(request, 'userWorktime.html', {'startDate' : reportStart.strftime("%Y-%m-%d-00-00"), 'endDate' : reportEnd.strftime("%Y-%m-%d-23-59"), 'total' : allDateTime, 'times': WorkTime.objects.all().filter(user=user, startTime__gte = reportStart, endTime__lte = reportEnd)})
        #return HttpResponse("All: %5.f" % allDateTime)
    return render(request, 'userWorktime.html', {'total' : 0, 'times': {}, 'startDate' : reportStart.strftime("%Y-%m-%d-00-00"), 'endDate' : reportEnd.strftime("%Y-%m-%d-23-59")})

def getAllInfo(request, startWith=1):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    userStataList = []
    userPerPage = 20
    paginator = Paginator(User.objects.all(), userPerPage)
    try:
        users = paginator.page(startWith)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    for user in users:#User.objects.all().order_by('username')[startWith:userPerPage]:
        userStataList.append({'userName' : user.username, 'all' : getStatisticByUser(user) })
    return render(request, 'stataList.html', {'stataList': userStataList, 'paginator' : users})