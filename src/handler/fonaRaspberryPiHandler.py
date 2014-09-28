from subprocess import call
from time import sleep

import logging, RPi.GPIO as GPIO


class FonaRaspberryPiHandler:
    def __str__(self):
        return str(self.__dict__)
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
    
    def onSetup(self, **kwargs):
        self.turnOnOrOff(True, **kwargs)
    
    def onTearDown(self, **kwargs):
        self.turnOnOrOff(False, **kwargs)
    
    def onConnectionFailed(self, **kwargs):
        pass
    
    def onConnectionRestored(self, **kwargs):
        pass
    
    def onConnected(self, **kwargs):
        pass
    
    def onAvailable(self, **kwargs):
        pass

    def httpPost(self, urlSuffix):
        pass
    
    def turnOnOrOff(self, turnOnRequest, **kwargs):
        try:
            powerStatusPin = kwargs.get('powerStatusPin')
            keyPin = kwargs.get('keyPin')
            GPIO.setmode(GPIO.BCM)
            
            GPIO.setup(powerStatusPin, GPIO.IN)
            GPIO.setup(keyPin, GPIO.OUT)
            
            isOff = (0 == GPIO.input(powerStatusPin))
            if (isOff and turnOnRequest) or (not isOff and not turnOnRequest):
                GPIO.output(keyPin, False)
                sleep(2)
                GPIO.output(keyPin, True)
                #TODO: Move this out and check if process is running
                if turnOnRequest:
                    call('pon fona', shell=True)
                else:
                    call('poff fona', shell=True)
        except Exception as e:
            logging.error(e)
        finally:
            GPIO.cleanup()
