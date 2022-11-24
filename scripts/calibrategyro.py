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

    Xmin=1000
    Xmax=-1000
    Ymin=1000
    Ymax=-1000

    while True:
        try:
            sleep(0.2)
            x, y, z = sensor.read()
            Xmin=min(x,Xmin)
            Xmax=max(x,Xmax)
            Ymin=min(y,Ymin)
            Ymax=max(y,Ymax)
            print(sensor.format_result(x, y, z))
            print("Xmin="+str(Xmin)+"; Xmax="+str(Xmax)+"; Ymin="+str(Ymin)+"; Ymax="+str(Ymax))

        except KeyboardInterrupt:
            print()
            print('Got ctrl-c')

            xs=1
            ys=(Xmax-Xmin)/(Ymax-Ymin)
            xb =xs*(1/2*(Xmax-Xmin)-Xmax)
            yb =xs*(1/2*(Ymax-Ymin)-Ymax)
            print("Calibration corrections:")
            print("xs="+str(xs))
            print("xb="+str(xb))
            print("ys="+str(ys))
            print("yb="+str(yb))
            break
