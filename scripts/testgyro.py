import sys
root_folder = sys.path[0] = "/.."
sys.path.insert(1, root_folder)

from lib.hmc5883l import HMC5883L
from time import sleep
from constants import GYRO_SCL_PIN, GYRO_SDA_PIN
from robot.sensors.gyro import GyroSensor

if __name__ == "__main__":
    gyro = GyroSensor(GYRO_SCL_PIN, GYRO_SDA_PIN)
    gyro.reset_angle(0)
    while True:
        reading = gyro.get_angle()
        print(f"angle: {reading}")
        sleep(1)
