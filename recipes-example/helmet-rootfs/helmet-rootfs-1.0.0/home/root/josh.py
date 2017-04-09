#!/usr/bin/python

import subprocess
import os
import time
import sys
import threading
import signal

from upload import ftp_open, upload
import gpio
from gpio import setup,mode,read,set,cleanup

led_red=91
led_amber=90
led_green=65
button_switch=95

def updateIndicators(stop_event):
  blinker=0
  while not stop_event.wait(0.1):
    v=read(button_switch)
    #print "button-switch", v
    if v: ##disabled the blinker## and blinker<15:
      set(led_red,0)
    else:
      set(led_red,1)
    blinker=blinker+1
    if blinker >= 20:
      blinker=0
  print 'updateIndicators thread has terminated.'

csi1_video='/dev/' + str(sys.argv[1])
print 'ipu0_csi1 @', csi1_video

# count the restarts due to errors, this value affect the filename see sinkfile definition for details
restarts = 0

# index numbers in filename
idx_nums = 3

def touch(fname):
  try:
    os.utime(fname, None)
  except OSError:
    open(fname, 'a').close()

def delold():
  try:
    index_fossil = os.path.getmtime("trilobite")
  except: ## there was an error reading/accessing file trilobite, for now we just return
    pass
    return

  for root, dirs, files in os.walk("."):
    for name in files:
      try:
        ## delete file if older than X seconds compared to trilobite
        if index_fossil > (os.path.getmtime(name)+1000):
          #print "del", os.path.join(root,name), ", T:", os.path.getmtime(name)
          os.remove( os.path.join(root,name) )
      except:
        pass

def button_status():
  changed=True
  old_v=-1
  while True: # this will never exit (unless there is an error, maybe?)
    v=read(95)
    changed=(old_v!=v)
    yield (changed,v)
    old_v=v

b = button_status()
# v = next(b) 
def button():
  v = next(b)
  #print 'button', v 
  return v

os.chdir("/media/")


def getGstCmd():
  myfile = "usbcam{0}.mkv"
  sinkfile = myfile.format( "{1}%0{0}d".format(idx_nums, chr(ord('A')+(restarts%26)) ) )
  print "This is my file format:", sinkfile
  maxsize=4*1024*1024

  gstcmd_csi = (
  "gst-launch-1.0 -v -e "
  "imxv4l2videosrc capture-mode=1 device={2} ! "
  "imxvpuenc_h264 quant-param=20 ! "
  "h264parse ! matroskamux ! "
  "multifilesink location={0} next-file=4 "
  "max-file-size={1}".format(sinkfile,maxsize,csi1_video)
  )
  
  gstcmd = (
  "gst-launch-1.0 -v -e "
  "v4l2src device={2} num-buffers=-1 ! "
  "videoconvert ! "
  "video/x-raw,format=I420,width=640,height=360,framerate=10/1 ! "
  "imxvpuenc_h264 quant-param=20 ! "
  "multifilesink post-messages=1 location={0} next-file=4 "
  "max-file-size={1}".format(sinkfile,maxsize,"/dev/video1")
  )
  print "cmd:", gstcmd_csi
  return gstcmd_csi

def main():
   try:
     retval = subprocess.call(getGstCmd(), shell=True)
     if retval < 0:
       print >>sys.stderr, "Child was terminated by signal", -retval
     else:
       print >>sys.stderr, "Child returned", retval
   except ValueError as e:
     print "execution failed:", e
   except OSError as e:
     print "OS error:", e
   except subprocess.CalledProcessError as e:
     print "Called process error:", e   
   except KeyboardInterrupt:
     print "user interrupted with ctrl-C"
   except:
     print "error."   
   finally:
     print "adios!"

def josh():
   event_counter=0
   while button() != (False,1):
     time.sleep(0.5)
     touch("trilobite")

   try:                                                                   
     gstproc = subprocess.Popen(getGstCmd(), shell=True)                         
   except ValueError as e:  
     print "value error:", e
   except OSError as e:                                                   
     print "OS error:", e                                                 
   except subprocess.CalledProcessError as e:        
     print "called process error:", e
   finally:
     print "Popen finished."

   while gstproc.poll() is None:
     time.sleep(1)
     if button()==(True,0):
       break
     #print ".",
     event_counter = event_counter + 1
     if event_counter > 10:
       event_counter=0
       delold()
       touch("trilobite")
       #print "T"

   time.sleep(2)
   #gstproc.wait(5)

   ### when gstproc fails with returncode == 255, it has indicated the video source
   ### may be incorrect; instead of /dev/video0 (default) it could be /dev/video1, etc.

   print "gst process finished, rc=", gstproc.returncode
   #gstproc.kill() #terminate()
   os.kill(gstproc.pid, signal.SIGINT)
   print 'signal.SIGINT:', signal.SIGINT


if __name__ == "__main__":
  print "starting josh.py..."
  pill2kill = threading.Event()
  ioThread = threading.Thread(target=updateIndicators, args=(pill2kill,))
  ioThread.start()
  while True:
    try:
      josh()
    except KeyboardInterrupt:
      pass
      break
    restarts = restarts + 1
    print "...restarting({0}) gst recorder...".format( restarts )
  pill2kill.set()
  cleanup(led_red)
  cleanup(button_switch)
  print "Gst Recording script has terminated."
