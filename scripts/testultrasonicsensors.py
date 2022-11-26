"""Test ultrasonic sensors."""
import sys
root_folder = sys.path[0] = "/.."
sys.path.insert(1, root_folder)

from constants import LEFT_ULTRASONIC_ECHO_PIN, LEFT_ULTRASONIC_TRIGGER_PIN, \
                      RIGHT_ULTRASONIC_ECHO_PIN, RIGHT_ULTRASONIC_TRIGGER_PIN, \
                      FRONT_ULTRASONIC_ECHO_PIN, FRONT_ULTRASONIC_TRIGGER_PIN
from robot.sensors.ultrasonic import UltraSonicSensor
from time import sleep


if __name__ == "__main__":
    left = UltraSonicSensor(LEFT_ULTRASONIC_TRIGGER_PIN, LEFT_ULTRASONIC_ECHO_PIN)
    front = UltraSonicSensor(FRONT_ULTRASONIC_TRIGGER_PIN, FRONT_ULTRASONIC_ECHO_PIN)
    right = UltraSonicSensor(RIGHT_ULTRASONIC_TRIGGER_PIN, RIGHT_ULTRASONIC_ECHO_PIN)

    while True:
        l_reading = left.measure_distance()
        f_reading = front.measure_distance()
        r_reading = right.measure_distance()

        print(f"Left distance: {l_reading} cm")
        print(f"Front distance: {f_reading} cm")
        print(f"Right distance: {r_reading} cm")
        print()
        sleep(0.01)
