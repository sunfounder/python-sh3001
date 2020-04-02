#!/usr/bin/env python3
from sh3001.sh3001 import Sh3001
from sh3001.i2c import I2C


def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    # print(result)
    # print(status)
    return status, result


class LxAutoStart(object):
    ''' 
        To setup /home/pi/.config/lxsession/LXDE-pi/autostart
    '''

    def __init__(self, file="/home/pi/.config/lxsession/LXDE-pi/autostart"):
        self.file = file
        with open(self.file, 'r') as f:
            cmdline = f.read()
        self.cmdline = cmdline.strip()
        self.cmds = self.cmdline.split('\n')

    def remove(self, expected):
        for cmd in self.cmds:
            if expected in cmd:
                self.cmds.remove(cmd)
        return self.write_file()

    def set(self, cmd):
        have_excepted = False
        for tmp in self.cmds:
            if tmp == cmd:
                have_excepted = True
                break

        if not have_excepted:
            self.cmds.append(cmd)
        return self.write_file()

    def write_file(self):
        try:
            cmdline = '\n'.join(self.cmds)
            # print(cmdline)
            with open(self.file, 'w') as f:
                f.write(cmdline)
            return 0, cmdline
        except Exception as e:
            return -1, e


def usage():
    print("Usage auto-rotator [install/uninstall]")
    quit()


def rotate():
    import time
    from math import asin
    import math
    import sys

    sensor = Sh3001()
    lxAutoStart = LxAutoStart()

    if len(sys.argv) > 2:
        usage()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "install":
            lxAutoStart.set("@auto-rotator")
            # run_command("auto-rotator 2&>1 1>/dev/null &")
            print("auto-rotator installed successfully")
            quit()
        elif sys.argv[1] == "uninstall":
            lxAutoStart.remove("@auto-rotator")
            print("auto-rotator uninstalled successfully")
            quit()
        elif sys.argv[1] == "calibrate":
            # while True:
            sensor.acc_calibrate_cmd()
            # lxAutoStart.remove("@auto-rotator")
            print("auto-rotator calibrate successfully")
            quit()
        else:
            usage()
    

    while True:
        # print("1")
        acc_list = sensor.sh3001_getimudata('acc','xyz')
        # print(acc_list)
        acc_list = [min(2046,i) for i in acc_list]
        acc_list = [max(-2046,i) for i in acc_list]
        # print(asin(acc_list[0] / 2100.0))
        current_angle_x = (asin(acc_list[0] / 2046.0)) / math.pi * 180
        current_angle_y = (asin(acc_list[1] / 2046.0)) / math.pi * 180
        # print((asin(acc_list[1] / 2046.0)) / math.pi * 180)
        time.sleep(0.1)
        print("current_angle_x: ",current_angle_x)
        print("current_angle_y: ",current_angle_y)
        if current_angle_x > 45:
            print("left")
            run_command("rotate-helper left")

        elif current_angle_x < -45:
            print("right")
            run_command("rotate-helper right")

        if current_angle_y > 45:
            print("normal")
            run_command("rotate-helper normal")
        elif current_angle_y < -45:
            print("inverted")
            run_command("rotate-helper inverted")
        else:
            print("no")
        time.sleep(1)

# if __name__ == '__main__':
#     # run_command("rotate-helper normal")
#     while True:
#         rotate()
