#!/usr/bin/python

import subprocess
import os
import time
import socket

import traceback, sys
import fnmatch 

import threading

from upload import ftp_open, upload

import gpio
from gpio import set,cleanup

def uploadIndicator(stop_event):
  while not stop_event.wait(0.05):
    set(90,0) ## amber on
    time.sleep(0.05)
    set(90,1) ## amber off


# index numbers in filename
idx_nums = 3

def touch(fname):
  try:
    os.utime(fname, None)
  except OSError:
    open(fname, 'a').close()

def led_thread():                                                               
  pill2kill=threading.Event()
  t = threading.Thread(target=uploadIndicator, args=(pill2kill,))
  t.start()
  return t,pill2kill
            
def myupload(ftp,name):
  tid,p2k = led_thread()
  upload(ftp,name)
  p2k.set()
  tid.join()

def oldestfilesfirst(mypath):
  matches = []
  for root, dirs, files in os.walk(mypath):
    for file in fnmatch.filter(files, "*.mkv"):
      matches.append( os.path.join( root, file ) )
  return sorted( matches, key=os.path.getmtime )

def delold(ftp):
  try:
    index_fossil = os.path.getmtime("trilobite")
  except:
    pass
    return

  ## this can be optimized: use the following list and iterate until 'trilobite' is found
  ## once its found we have uploaded all the 'old' aka 'complete' files
  files = oldestfilesfirst(".")
  for name in files:
   ## delete file if older than X seconds compared to trilobite
   try:
    if index_fossil > (os.path.getmtime(name)+30):
      myupload( ftp, name )
      #print "del", name, ", T:", os.path.getmtime(name)
      os.remove( name )
   except OSError as e:
    print "OSError:", e

os.chdir("/media/")
myfile = "usbcam{0}.mvk"
sinkfile = myfile.format("%0{0}d".format(idx_nums))
print "This is my file format:", sinkfile
maxsize=1024*1024

def josh():
   try_again = True
   event_counter=0
   while try_again:
     try_again = False
     try:
       ftp=ftp_open("joshs-mbp", ("joshwest", "endorphine6"))
       ftp.cwd("hummingboard/")
     except ValueError as e:  
       print "value error:", e
     except OSError as e:                                                   
       print "OS error:", e                                                 
     except KeyboardInterrupt:
       print "user interrupted with ctrl-C"
     except socket.gaierror as e:
       print "probably not connected to internet"
       try_again = True
       time.sleep(10)
     finally:
       print "ftp_open done"

   try:
     while True:
       time.sleep(5)
       #print ".",
       delold(ftp)
       touch("ammonite")
       #print "T"
   except:
     print "uploading error"
     type, value, tb = sys.exc_info()
     traceback.print_exc()

   print "upload process finished"
   try:
     ftp.quit()
   except:
     print "ftp may not have closed properly"


if __name__ == "__main__":
  print "starting uploader.py..."
  try:
    josh()
  except KeyboardInterrupt:
    pass
  
