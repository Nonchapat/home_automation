####################################
###  Author : Somchai Somphadung ###
###  Date : 2014-09-13           ###
### N3A Media                    ###
####################################

import pygame
import pygame.camera
import pygame.image
import time

class ImageCapture:
    def __init__(self,imgsize=(320,240),pic_format="RGB",loc="/home/pi/"):
          # pic_format could be RGB, YUV, HSV
          pygame.init()
          pygame.camera.init()
          cameras = pygame.camera.list_cameras()
          if not cameras :
                    raise ValueError("There is not camera attached")
                    self.camera=None
          self.camera=pygame.camera.Camera(cameras[0],imgsize,pic_format)
          self.is_end=False
          self.img_loc=loc


    def create_img_name(self):
          exp="%Y_%m_%d-%H_%M_%S"
          return "snap_"+time.strftime(exp)+".jpeg"


    def capture(self):
          if self.camera is not None :
          self.camera.start()
          snapshot = self.camera.get_image()
          pygame.image.save(snapshot,self.img_loc+"/"+self.create_img_name())
          self.camera.stop()
          
    def lapse_capture(self,dur=10):
          # dur contains duration of operation in seconds
          if self.camera is not None :
             self.end_time = time.time()+dur
             self.current_time = time.time()
             while self.current_time < self.end_time :
                self.camera.start()
                snapshot = self.camera.get_image()
                pygame.image.save(snapshot,self.img_loc+"/"+self.create_img_name())
                self.camera.stop()
                time.sleep(self.time_interval)
                self.current_time = time.time()
             self.quit()
    
    def quit(self):
        pygame.quit()
