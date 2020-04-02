# auto-rotator - screen rotate

Usage:
```shell
pi@raspberrypi:~ $ sudo auto-rotator install       ##enable the auto-rotate

pi@raspberrypi:~ $ sudo auto-rotator install         ##disable the auto-rotate

pi@raspberrypi:~ $ sudo auto-rotator calibrate       ##calibrate the Gsensor
```
## Constructors
```class sh3001.Sh3001()```
Create an sh3001 object associated with the given pin. This allows you to then read analog values on that pin.

## 校准Methods
- 运行如下所示命令：
```shell
pi@raspberrypi:~ $ sudo auto-rotator calibrate         ##calibrate the Gsensor
```
- 然后屏幕会输出:    
```shell
pi@raspberrypi:~ $ sudo auto-rotator calibrate         ##calibrate the Gsensor
                   press s to start calibrate
                   quit use ctrl c
```
- 拿起raspad到合适位置然后点击键盘的s键，向三个轴的不同方向慢慢翻转radpad，并且观察最大最小值，一般单个值不应该超过+-2400，待每个值都基本不变时，保持radpad不动，然后按下ctrl + c，至此校准结束