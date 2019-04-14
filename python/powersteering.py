# Interface to steering servo and power controller
#    Input values:
#        Steering: from -500 (full left) to +500 (full right)
#        Power:    from -500 (full reverse) to +500 (full forward)
#
#        All values are further constained to limit steering and
#        (especially) power.

from serial import Serial
import time

STEER_MAX = 500
POWER_MAX = 150
STEER_TRIM = 0

class PowerSteering:

    def __init__(self, port_name, baud_rate, logger):
        self._running = False
        self.logger = logger
        self.logger.write("PowerSteering: started.")
        self.power = 0
        self.steering = 0
        self.new_values = False

	self.Serial = Serial(port_name, baud_rate, timeout=None)

    def stop(self):
        self.logger.write("PowerSteering: stop")
        self.set_power_and_steering(0, 0)
        
    def get_power(self):
        return self.power
        
    def set_power(self, power_value):
        self.logger.write("Powersteering set_power: power=%d" % (power_value))
        if power_value > POWER_MAX:
            power_value = POWER_MAX
        elif power_value < -POWER_MAX:
            power_value = -POWER_MAX
        self.power = power_value
        self.new_values = True
        
    def set_steering(self, steer_value):
        self.logger.write("Powersteering set_steering: steer_value=%d" % (steer_value))
        if steer_value > STEER_MAX - STEER_TRIM:
            steer_value = STEER_MAX - STEER_TRIM
        elif steer_value < -STEER_MAX - STEER_TRIM:
            steer_value = -STEER_MAX - STEER_TRIM
        self.steering = steer_value
        self.new_values = True               
        
    def set_power_and_steering(self, power_value, steer_value):
        self.logger.write("PowerSteering set_power_and_steering: power=%d, steer=%d" % (power_value, steer_value))
                          
        # Condition values past
        if steer_value > STEER_MAX - STEER_TRIM:
            steer_value = STEER_MAX - STEER_TRIM
        elif steer_value < -STEER_MAX - STEER_TRIM:
            steer_value = -STEER_MAX - STEER_TRIM
        if power_value > POWER_MAX:
            power_value = POWER_MAX
        elif power_value < -POWER_MAX:
            power_value = -POWER_MAX
        self.power = power_value
        self.steering = steer_value
        self.new_values = True
    
    def terminate(self):
        self.logger.write("Powersteering: terminated")
        self._running = False
        time.sleep(1)
        
        steer_value = 1500
        power_value = 1500
    	commandstring = str(int(steer_value)) + "," + str(int(power_value))
        self.Serial.write(str(int(steer_value)) + "," + str(int(power_value)) + "\n")
        self.Serial.flush()
        
        
    def run(self):
        self._running = True
        self.logger.write("PowerSteering: running")
        while (self._running == True):
                
            if self.new_values == True:
                steer_value = 1500+self.steering+STEER_TRIM
                power_value = 1500+self.power
    	        commandstring = str(int(steer_value)) + "," + str(int(power_value))
                self.logger.write("Writing command string; %s" % commandstring)
                self.Serial.write(commandstring + "\n")
                self.new_values = False
                
            time.sleep(0.2) 
