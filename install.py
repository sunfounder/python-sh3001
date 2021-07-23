#!/usr/bin/env python3
import os, sys

errors = []

avaiable_options = ['-h', '--help', '--no-dep']

usage = '''
Usage:
    sudo python3 install.py [option]

Options:
               --no-dep    Do not download dependencies
    -h         --help      Show this help text and exit
'''
def install():
    options = []
    if len(sys.argv) > 1:
        options = sys.argv[1:]
        for o in options:
            if o not in avaiable_options:
                print("Option {} is not found.".format(o))
                print(usage)
                quit()
    if "-h" in options or "--help" in options:
        print(usage)
        quit()
    print("Auto rotator service install process starts")
    print("Install dependency")
    if "--no-dep" not in options:
        do(msg="update apt-get",
            cmd='run_command("sudo apt-get update")')
        do(msg="install i2c-tools",
            cmd='run_command("sudo apt-get install i2c-tools -y")')

    print("Setup interfaces")
    do(msg="turn on I2C",
        cmd='Config().set("dtparam=i2c_arm", "on")')
    do(msg="Add I2C module",
        cmd='Modules().set("i2c-dev")')

    print("Setup auto-rotator service")
    do(msg="copy rotate-helper file",
        cmd='run_command("sudo cp ./bin/rotate-helper /usr/bin/")')
    do(msg="add excutable mode for rotate-helper",
        cmd='run_command("sudo chmod +x /usr/bin/rotate-helper")')
    do(msg="delete config",
        cmd='run_command("sudo rm -rf /home/pi/.config/auto-rotator")')
    do(msg="create config",
        cmd='run_command("sudo mkdir /home/pi/.config/auto-rotator/ && touch /home/pi/.config/auto-rotator/config")')
    do(msg="change owner",
        cmd='run_command("sudo chown -R pi:pi /home/pi/.config/auto-rotator/")')
    do(msg="change mode",
        cmd='run_command("sudo chmod -R 700 /home/pi/.config/auto-rotator/")')

    # _, result = run_command("ls /home/pi/.config")
    # if "lxsession" not in result:
    #     print("not..................")
    #     do(msg="create autostart",
    #         cmd='run_command("sudo mkdir /home/pi/.config/lxsession/ && mkdir /home/pi/.config/lxsession/LXDE-pi/ && touch /home/pi/.config/lxsession/LXDE-pi/autostart")')
    if not os.path.isdir("/home/pi/.config/lxsession"):
        do(msg="mkdir lxsession", cmd='run_command("mkdir /home/pi/.config/lxsession/")')
    if not os.path.isdir("/home/pi/.config/lxsession/LXDE-pi"):
        do(msg="mkdir LXDE-pi", cmd='run_command("mkdir /home/pi/.config/lxsession/LXDE-pi")')
    if not os.path.isfile("/home/pi/.config/lxsession/LXDE-pi/autostart"):
        do(msg="copy autostart",
            cmd='run_command("sudo cp /etc/xdg/lxsession/LXDE-pi/autostart /home/pi/.config/lxsession/LXDE-pi/autostart")')
        do(msg="change owner",
            cmd='run_command("sudo chown -R pi:pi /home/pi/.config/lxsession/")')
        do(msg="change mode",
            cmd='run_command("sudo chmod -R 700 /home/pi/.config/lxsession/")')

    os.chdir("./src/sh3001")
    print("Install sh3001 python package")
    do(msg="run setup file",
        cmd='run_command("sudo python3 setup.py install")')
    os.chdir("../")

    if len(errors) == 0:
        print("Finished")
    else:
        print("\n\nError happened in install process:")
        for error in errors:
            print(error)
        print("Try to fix it yourself, or contact service@sunfounder.com with this message")
        sys.exit(1)

def cleanup():
    do(msg="cleanup",
        cmd='run_command("sudo rm -rf sh3001.egg-info")')

class Modules(object):
    ''' 
        To setup /etc/modules
    '''

    def __init__(self, file="/etc/modules"):
        self.file = file
        with open(self.file, 'r') as f:
            self.configs = f.read()
        self.configs = self.configs.split('\n')

    def remove(self, expected):
        for config in self.configs:
            if expected in config:
                self.configs.remove(config)
        return self.write_file()

    def set(self, name):
        have_excepted = False
        for i in range(len(self.configs)):
            config = self.configs[i]
            if name in config:
                have_excepted = True
                tmp = name
                self.configs[i] = tmp
                break

        if not have_excepted:
            tmp = name
            self.configs.append(tmp)
        return self.write_file()

    def write_file(self):
        try:
            config = '\n'.join(self.configs)
            # print(config)
            with open(self.file, 'w') as f:
                f.write(config)
            return 0, config
        except Exception as e:
            return -1, e

class Config(object):
    ''' 
        To setup /boot/config.txt
    '''

    def __init__(self, file="/boot/config.txt"):
        self.file = file
        with open(self.file, 'r') as f:
            self.configs = f.read()
        self.configs = self.configs.split('\n')

    def remove(self, expected):
        for config in self.configs:
            if expected in config:
                self.configs.remove(config)
        return self.write_file()

    def set(self, name, value=None):
        have_excepted = False
        for i in range(len(self.configs)):
            config = self.configs[i]
            if name in config:
                have_excepted = True
                tmp = name
                if value != None:
                    tmp += '=' + value
                self.configs[i] = tmp
                break

        if not have_excepted:
            tmp = name
            if value != None:
                tmp += '=' + value
            self.configs.append(tmp)
        return self.write_file()

    def write_file(self):
        try:
            config = '\n'.join(self.configs)
            # print(config)
            with open(self.file, 'w') as f:
                f.write(config)
            return 0, config
        except Exception as e:
            return -1, e

class Cmdline(object):
    ''' 
        To setup /boot/cmdline.txt
    '''

    def __init__(self, file="/boot/cmdline.txt"):
        self.file = file
        with open(self.file, 'r') as f:
            cmdline = f.read()
        self.cmdline = cmdline.strip()
        self.cmds = self.cmdline.split(' ')

    def remove(self, expected):
        for cmd in self.cmds:
            if expected in cmd:
                self.cmds.remove(cmd)
        return self.write_file()

    def write_file(self):
        try:
            cmdline = ' '.join(self.cmds)
            # print(cmdline)
            with open(self.file, 'w') as f:
                f.write(cmdline)
            return 0, cmdline
        except Exception as e:
            return -1, e


def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    # print(result)
    # print(status)
    return status, result


def do(msg="", cmd=""):
    print(" - %s..." % (msg), end='\r')
    print(" - %s... " % (msg), end='')
    status, result = eval(cmd)
    # print(status, result)
    if status == 0 or status == None or result == "":
        print('Done')
    else:
        print('Error')
        errors.append("%s error:\n  Status:%s\n  Error:%s" %
                      (msg, status, result))

if __name__ == "__main__":
    try:
        install()
    except KeyboardInterrupt:
        print("Canceled.")
        cleanup()

# if __name__ == "__main__":
#     test()
