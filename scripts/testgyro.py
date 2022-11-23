#              .';:cc;.
#            .,',;lol::c.
#            ;';lddddlclo
#            lcloxxoddodxdool:,.
#            cxdddxdodxdkOkkkkkkkd:.
#          .ldxkkOOOOkkOO000Okkxkkkkx:.
#        .lddxkkOkOOO0OOO0000Okxxxxkkkk:
#       'ooddkkkxxkO0000KK00Okxdoodxkkkko
#      .ooodxkkxxxOO000kkkO0KOxolooxkkxxkl
#      lolodxkkxxkOx,.      .lkdolodkkxxxO.
#      doloodxkkkOk           ....   .,cxO;
#      ddoodddxkkkk:         ,oxxxkOdc'..o'
#      :kdddxxxxd,  ,lolccldxxxkkOOOkkkko,
#       lOkxkkk;  :xkkkkkkkkOOO000OOkkOOk.
#        ;00Ok' 'O000OO0000000000OOOO0Od.
#         .l0l.;OOO000000OOOOOO000000x,
#            .'OKKKK00000000000000kc.
#               .:ox0KKKKKKK0kdc,.
#                      ...
#
# Author: peppe8o
# Date: Dec 11th, 2021
# Version: 1.0
# https://peppe8o.com

import sys
import os
root_folder = os.path.join(sys.path[0], "..")
sys.path.insert(1, root_folder)

from lib.hmc5883l import HMC5883L
from time import sleep
from constants import GYRO_SCL_PIN, GYRO_SDA_PIN

if __name__ == "__main__":
    sensor = HMC5883L(GYRO_SCL_PIN, GYRO_SDA_PIN)

    while True:
        sleep(1)
        x, y, z = sensor.read()
        print(sensor.format_result(x, y, z))
