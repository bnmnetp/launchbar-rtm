#!/usr/bin/env python

from rtm import *
import sys
import Growl

apiKey = "d1baafca31e05410b4d4563a6730707e"
secret = "9478ddbfa4d8cfb9"
token = "c42dc2bf01dbc4b442c6cab9fb7adc22dc9e69d8"

newTask = " ".join(sys.argv[1:])

rtm = createRTM(apiKey, secret, token)

tl = rtm.timelines.create()

rsp = rtm.tasks.add(timeline=tl.timeline,name=newTask,parse=1)

name = "RTM"
notifications = ["addedInbox", "notAdded", "completed"]
notifier = Growl.GrowlNotifier(name,notifications)
notifier.register()

if rsp.stat == 'ok':
    notifier.notify("addedInbox","Remember The Milk","Added: "+newTask)
else:
    notifier.notify("addedInbox","Remember The Milk","Error: "+rsp.stat)
