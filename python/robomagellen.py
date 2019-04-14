#
# RoboMagellan Main Program
#
import time
import traceback

from robot import Robot

robot = Robot()
robot.initialize()
time.sleep(3)

try:
    robot.set_power_and_steering(80, 0)
    time.sleep(10)

except:
    robot.logger.write(traceback.format_exc())

robot.terminate()
