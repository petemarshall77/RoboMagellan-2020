#
# MONTY III - Main Robot class
#
from threading import Thread
import time

from logger import Logger
from powersteering import PowerSteering
import usb_probe

class Robot:

    def __init__(self):
        self.logger = Logger()
        self.logger.write("Robot: creating robot object")
        ports = usb_probe.probe()
        self.logger.write("Robot: found USB ports...")
        for port in ports:
            self.logger.write("       %s, %s" % (ports[port], port))
        self.powersteering = PowerSteering(ports['chias'], 9600, self.logger)
       
    def initialize(self, powersteering = True):
        self.logger.write("Robot: initializing")
        if powersteering == True:
            self.powersteering_thread = Thread(target = self.powersteering.run)
            self.powersteering_thread.start()
       
    def terminate(self):
        self.logger.write("Robot: terminating")
        self.powersteering.terminate()
       
    def set_power_and_steering(self, power_value, steer_value):
        self.powersteering.set_power_and_steering(power_value, steer_value)

