##################################
### Author : Somchai Somphadung ###
### Date : 2014-09-20                          ###
### N3A Media                                     ###
#################################
import os.path
import sys
import gdata.data
import gdata.docs.data
import gdata.docs.client
import ConfigParser

conf_file="gdrive.conf"

class RaspiGData :

 def __init__(self):
         config  = ConfigParser.ConfigParser()
         config.read(conf_file)
  self.ready=False
         self.source=config.get('gdrive','source')   
         self.username=config.get('gmail','user')
         self.pwd=config.get('gmail','pwd')
         self.folder=config.get('upload_folder','folder')
         self.create_client()


 def create_client(self):
  try:
   self.client = gdata.docs.client.DocsClient(source=self.source)
   self.client.http_client.debug = False
   self.client.ClientLogin(self.username,self.pwd,service=self.client.auth_service, source=self.client.source)      
   self.ready=True
  except :
   self.ready=False

 def get_folder(self):
   col = None
   if not self.ready :
     return col
   for resource in self.client.GetAllResources(uri='/feeds/default/private/full/-/folder'):
     if resource.title.text == self.folder :
     col = resource
     break
  return col

 def upload(self, file_path, folder_resource):
  #Upload document file and return
  doc = None
  try:
   doc = gdata.docs.data.Resource(type='document', title=os.path.basename(file_path))
   media = gdata.data.MediaSource()
   media.SetFileHandle(file_path, 'image/jpeg')
   doc = self.client.CreateResource(doc, media=media, collection=folder_resource)
  except:
   pass   
  return doc

 def upload_image(self, image_file_path):
  folder_resource = self.get_folder()
  #if not folder_resource:
  # raise Exception('Could not find the %s folder' % self.folder)
  if folder_resource:
   return self.upload(image_file_path, folder_resource)
  else :
   return None
