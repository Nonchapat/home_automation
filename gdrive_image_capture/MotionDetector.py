import RPi.GPIO as GPIO

class MotionDetector :
   def __init__(self,pir_pin=7,gpio_mode="board"):
      self.pir_pin=pir_pin
      if gpio_mode == "board" :
         GPIO.setmode(GPIO.BOARD)
      else :
         GPIO.setmode(GPIO.BCM)
         GPIO.setup(pir_pin,GPIO.IN)

    def get_state(self):
      return GPIO.input(self.pir_pin)

    def cleanup(self):
      GPIO.cleanup()
