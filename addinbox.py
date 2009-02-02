#!/usr/bin/env python

from rtm import *
import sys
import Growl
from rtmconfig import *

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
