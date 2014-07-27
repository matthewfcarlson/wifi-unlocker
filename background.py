import subprocess, thread, time
import ConfigParser
from settings import *

def run():
    global can_break

    args = "sudo tcpdump -i mon1 -elnq 'type mgt subtype auth and (wlan host "
    args += mac_address
    args += ")' "
    shell = True
    print args
    count = 0
    popen = subprocess.Popen(args, shell=shell, stdout=subprocess.PIPE)
    while True:
        line = popen.stdout.readline()
        if line == "": continue
        do_something_with(line)
        break

    print "We got our authentication! Unlock the door!"
    popen.terminate()
    print "Done."
    can_break = True

def do_something_with(line):
    print '>>> This is it:', line

while True:
 
 thread.start_new_thread(run, tuple())
 can_break = False
 while not can_break:
    time.sleep(1)
 print 'check to see if someone is standing there!'
 print 'actuate servo!'
