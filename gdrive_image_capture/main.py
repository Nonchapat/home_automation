#!/usr/bin/python

##################################
### Author : Somchai Somphadung ###
### Date : 2014-09-20                          ###
### N3A Media                                     ###
#################################

from ImageCapture import  ImageCapture
from RaspiGdata import RaspiGData
import time
import threading
import Queue
import RPi.GPIO as GPIO
import ConfigParser
import sys

conf_file="gdrive.conf"

#################################################
class Uploader(threading.Thread):
 def __init__(self,queue):
  threading.Thread.__init__(self)
  self.gdata = RaspiGData()
  self.queue=queue
  self.exitFlag=False

 def run(self):
  import os
  
  while not (self.exitFlag and self.queue.empty()) :
   fname = self.queue.get() 
   
   if fname :
    if not self.gdata.ready :
      self.gdata.create_client()
    else :
     success=self.gdata.upload_image(fname)
     if success :
      os.unlink(fname)
      pass
   
   

#################################################
class Snapper(threading.Thread):

 def __init__(self,queue,capture):
  threading.Thread.__init__(self)
  self.queue = queue
  self.imgcap = ImageCapture()
  self.exitFlag=False
  self.imgcap=capture

 def snap(self,pin):
  if self.imgcap and self.queue :
   fname = self.imgcap.capture()
   if fname :
    self.queue.put(fname,False)
 
 def run(self):
  while not self.exitFlag :
   pass

    
   
#################################################

def cleanup():
 global imgcap
 imgcap.quit()
 GPIO.cleanup()

def shutdown():
 import subprocess
 cmd = "/usr/bin/sudo /sbin/shutdown -h now"
 process = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE)
 output=process.communicate()[0]
 

#################################################
imgcap = ImageCapture()
imgqueue = Queue.Queue()

if __name__ == "__main__" :
 if len(sys.argv) < 2 :
  dur = 20
 else :
  dur = int(sys.argv[1])

 config  = ConfigParser.ConfigParser()
 config.read(conf_file)
 pir_pin=int(config.get('gpio','pin'))
 if config.get('gpio','mode') == "board" :
  GPIO.setmode(GPIO.BOARD)
 else :
  GPIO.setmode(GPIO.BCM)

 GPIO.setup(pir_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
 uploader = Uploader(imgqueue)
 snapper = Snapper(imgqueue,imgcap)

 try:
  GPIO.add_event_detect(pir_pin, GPIO.RISING)
  GPIO.add_event_callback(pir_pin, snapper.snap)
  uploader.start()
  snapper.start()
  s_time=time.time()
  e_time=s_time+dur
  while s_time < e_time :
   s_time=time.time()
   print str(e_time - s_time)
   time.sleep(1)

 except KeyboardInterrupt:
  print "Exit"

 GPIO.remove_event_detect(pir_pin)
 uploader.exitFlag=True 
 snapper.exitFlag=True      
 uploader.join()#wait until Thread job is done.
 cleanup() 
 shutdown()
