###################################
###  Author : Somchai Somphadung ###
###  Date : 2014-09-20           ###
### N3A Media                    ###
##################################

import pygame
import pygame.camera
import pygame.image
import time
import ConfigParser

conf_file="gdrive_conf.conf"

class ImageCapture:

 def __init__(self,imgsize=(320,240),pic_format="RGB",loc="/home/pi/"):
  # pic_format could be RGB, YUV, HSV
  config  = ConfigParser.ConfigParser()
  config.read(conf_file)
  pygame.init()
  pygame.camera.init()
  cameras = pygame.camera.list_cameras()
  if not cameras :
    raise ValueError("There is not camera attached")
    self.camera=None
  
  w=config.get('captured_image','width')
  h=config.get('captured_image','height')
  picsize=(int(w),int(h))
  picformat=str(config.get('captured_image','format'))
  self.camera=pygame.camera.Camera(cameras[0],picsize,picformat)
  self.is_end=False
  self.img_loc=config.get('captured_image','folder')

 def create_img_name(self):
  exp="%Y_%m_%d-%H_%M_%S"
  return "snap_"+time.strftime(exp)+".jpeg"

 def capture(self):
  if self.camera is not None :
   self.camera.start()
   snapshot = self.camera.get_image()
   fname = self.img_loc+"/"+self.create_img_name()
   pygame.image.save(snapshot,fname)
   self.camera.stop()
   return fname
  else :
   return None

 def quit(self):
  pygame.quit()
