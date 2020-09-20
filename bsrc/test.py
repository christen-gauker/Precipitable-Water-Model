from numpy import *
import serial, time
from datetime import datetime, timedelta
import os

commit_message = "'Data dump for test location'"
fname = "../data/file.txt"


def github():
    add     = os.system("git add {}".format(fname))
    commit  = os.system("git commit -m {}".format(commit_message))
    push    = os.system("git push origin auto")
    add
    commit
    push
