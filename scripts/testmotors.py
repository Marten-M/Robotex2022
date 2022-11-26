import sys
root_folder = sys.path[0] + "/.."
sys.path.insert(1, root_folder)

from robot.motors.DualMotorDriverCarriers import DualMotorDriverCarrier
import time
from constants import LEFT_MOTOR_ENABLE_PIN, LEFT_MOTOR_PHASE_PIN, \
                      RIGHT_MOTOR_ENABLE_PIN, RIGHT_MOTOR_PHASE_PIN, \
                      MOTOR_DRIVER_CARRIER_MODE_PIN

if __name__ == "__main__":
    motors = DualMotorDriverCarrier(LEFT_MOTOR_ENABLE_PIN, LEFT_MOTOR_PHASE_PIN, RIGHT_MOTOR_ENABLE_PIN, RIGHT_MOTOR_PHASE_PIN, MOTOR_DRIVER_CARRIER_MODE_PIN)

    # Test left motor
    motors.set_left_motor_speed(100)
    time.sleep(2)
    motors.set_left_motor_speed(-100)
    time.sleep(2)
    motors.set_left_motor_speed(50)
    time.sleep(2)
    motors.set_left_motor_speed(0)

    # Test right motor
    motors.set_right_motor_speed(100)
    time.sleep(2)
    motors.set_right_motor_speed(-100)
    time.sleep(2)
    motors.set_right_motor_speed(50)
    time.sleep(2)
    motors.set_right_motor_speed(0)

    # Test motors together
    motors.set_left_motor_speed(100)
    motors.set_right_motor_speed(100)
    time.sleep(2)
    motors.set_left_motor_speed(-100)
    motors.set_right_motor_speed(-100)
    time.sleep(2)
    motors.set_left_motor_speed(0)
    motors.set_right_motor_speed(0)
