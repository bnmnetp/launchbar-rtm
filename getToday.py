#!/usr/bin/env python

from rtm import *
import sys
import Growl
from rtmconfig import *   # load api key and token from rtmconfig

def sendNotify(ts):
    if type(ts.task) == list:
        for j in range(len(ts.task)):
            notifier.notify("today","Task Due: "+ts.task[j].due[:10],ts.name,sticky=True,icon=gIcon)
    else:
        notifier.notify("today","Task Due: "+ts.task.due[:10],ts.name,sticky=True,icon=gIcon)

if len(sys.argv) == 2:
    command = sys.argv[1]
else:
    command = "today"


name = "RTMDue"
notifications = ["today","tomorrow"]
notifier = Growl.GrowlNotifier(name,notifications)
notifier.register()
gIcon = Growl.Image.imageFromPath("/Users/bmiller/Projects/RTM/GrowlLogo.png")

if command[:3] == "tod" or command == '':
    cutoff = 'today'
elif command[:3] == "tom":
    cutoff = 'tomorrow'
else:
    cutoff = None 

rtm = createRTM(apiKey, secret, token)

if cutoff:
    filterString = 'status:incomplete and (due:%s or dueBefore:%s)'%(cutoff,cutoff)
else:
    filterString = 'status:incomplete'

theTasks = rtm.tasks.getList(filter=filterString)

if type(theTasks.tasks.list) == list:
    for i in range(len(theTasks.tasks.list)):
        if type(theTasks.tasks.list[i].taskseries) == list:
            for j in range(len(theTasks.tasks.list[i].taskseries)):
                ts = theTasks.tasks.list[i].taskseries[j]
                sendNotify(ts)
        else:
            ts = theTasks.tasks.list[i].taskseries
            sendNotify(ts)
else:
    if type(theTasks.tasks.list.taskseries) == list:
        for i in range(len(theTasks.tasks.list.taskseries)):
            ts = theTasks.tasks.list.taskseries[i]
            sendNotify(ts)
    else:
        ts = theTasks.tasks.list.taskseries
        sendNotify(ts)


