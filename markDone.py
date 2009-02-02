#!/usr/bin/env python

from rtm import *
import sys
import Growl

def markComplete(ts,ms,timeline,listid):
    foundOne = False
    if type(ts.task) == list:
        for j in range(len(ts.task)):
            if ts.name.find(ms) >= 0:
                foundOne = True
                stat = rtm.tasks.complete(timeline,listid,ts.id,ts[j].id,ts[j].task.id)
                if stat.stat == 'ok':
                    notifier.notify("completed","Completed: ",ts.name,sticky=False,icon=gIcon)
                else:
                    notifier.notify("completed","Not Completed",stat.stat,sticky=False,icon=gIcon)
    else:
        if ts.name.find(ms) >= 0:
            foundOne = True
            stat = rtm.tasks.complete(timeline=timeline,list_id=listid,taskseries_id=ts.id,task_id=ts.task.id)            
            if stat.stat == 'ok':
                notifier.notify("completed","Completed: ",ts.name,sticky=False,icon=gIcon)
            else:
                notifier.notify("completed","Not Completed",stat.stat,sticky=False,icon=gIcon)
    return foundOne

if len(sys.argv) == 2:
    description = " ".join(sys.argv[1:])
else:
    description = "xyz"

apiKey = "d1baafca31e05410b4d4563a6730707e"
secret = "9478ddbfa4d8cfb9"
token = "c42dc2bf01dbc4b442c6cab9fb7adc22dc9e69d8"

name = "RTM"
notifications = ["addedInbox", "notAdded", "completed"]
notifier = Growl.GrowlNotifier(name,notifications)
notifier.register()
gIcon = Growl.Image.imageFromPath("/Users/bmiller/Projects/RTM/GrowlLogo.png")

cutoff = None 

rtm = createRTM(apiKey, secret, token)

if cutoff:
    filterString = 'status:incomplete and (due:%s or dueBefore:%s)'%(cutoff,cutoff)
else:
    filterString = 'status:incomplete'

theTasks = rtm.tasks.getList(filter=filterString)
timeline = rtm.timelines.create()

found = False
if type(theTasks.tasks.list) == list:
    for i in range(len(theTasks.tasks.list)):
        if type(theTasks.tasks.list[i].taskseries) == list:
            for j in range(len(theTasks.tasks.list[i].taskseries)):
                ts = theTasks.tasks.list[i].taskseries[j]
                ns = markComplete(ts,description,timeline.timeline,theTasks.tasks.list[i].id)
                if not found:
                    found = ns
        else:
            ts = theTasks.tasks.list[i].taskseries
            ns = markComplete(ts,description,timeline.timeline,theTasks.tasks.list[i].id)
            if not found:
                found = ns
else:
    if type(theTasks.tasks.list.taskseries) == list:
        for i in range(len(theTasks.tasks.list.taskseries)):
            ts = theTasks.tasks.list.taskseries[i]
            ns = markComplete(ts,description,timeline.timeline,theTasks.tasks.list.id)
            if not found:
                found = ns
    else:
        ts = theTasks.tasks.list.taskseries
        ns = markComplete(ts,description,timeline.timeline,theTasks.tasks.list.id)
        if not found:
            found = ns

if not found:
    notifier.notify("completed","No matching Tasks found!","searched for: "+description,sticky=False,icon=gIcon)


