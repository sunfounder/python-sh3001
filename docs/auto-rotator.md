# auto-rotator - screen rotate

Usage:
```shell
pi@raspberrypi:~ $ sudo auto-rotator install       ##enable the auto-rotate

pi@raspberrypi:~ $ sudo auto-rotator uninstall         ##disable the auto-rotate

pi@raspberrypi:~ $ sudo auto-rotator calibrate       ##calibrate the Gsensor
```
## Constructors
```class sh3001.Sh3001()```
Create an sh3001 object associated with the given pin. This allows you to then read analog values on that pin.

## Calibration method
- Run the command as follows：
```shell
pi@raspberrypi:~ $ sudo auto-rotator calibrate         ##calibrate the Gsensor
```
- The screen output is as follows:    
```shell
pi@raspberrypi:~ $ sudo auto-rotator calibrate         ##calibrate the Gsensor
                   press s to start calibrate
                   quit use ctrl c
```
- 举起raspad到适合旋转位置，然后点击键盘的s键，沿着x,y,z三个轴的不同方向慢慢翻转radpad，并且观察最大最小值，一般单个值不应该超过+-2400，待每个值都基本不变时，保持radpad不动，然后按下ctrl + c，至此校准结束

## recognize input device
- Run the command as follows
```shell
pi@raspberrypi:~ $ xinput -list         ##calibrate the Gsensor
```
- 找到对应的dev的名称，并且在sh3001/bin/rotate-helper文件里修改最底下的dev名称
