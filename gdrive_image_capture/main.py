from ImageCapture import  ImageCapture
from MotionDetector import MotionDetector
import time

if __name__ == "__main__" :
    cap = ImageCapture((480,360),"RGB","/home/pi/gdrive/")
    md = MotionDetector()
    c_state=0
    p_state=0
    try:
      print "Wait for initiate."
      while md.get_state() == 1:
         c_state=0
         print "Ready"
         while True:
            c_state=md.get_state()
            if c_state==1 and p_state==0:
               print "Motion detected"
               cap.capture()

            elif  c_state==0 and p_state==1:
               print "Ready"
               p_state=c_state
            time.sleep(1)
      cap.quit()
   except KeyboardInterrupt:
    print "Exit"
    md.cleanup()
    cap.quit()
