import os
import cv2
import numpy as np
import time
import random
from datetime import datetime
from datetime import timedelta

#主要流程：
#1、直接在上层界面等待0点
#2、根据预设的坐标直接模拟点击，加快速度

#手指滑动xdis的水平距离和ydis的垂直距离
def input_swipe(xdis,ydis):
    cmd = ('adb shell input swipe %i %i %i %i ') \
          % (300, 600, 300 + xdis, 600 + ydis)
    print(cmd)
    os.system(cmd)

#手指点击
def click(x,y):
    t1 = time.perf_counter()
    cmd = ('adb shell input tap %i %i') % (x, y)
    print(cmd)
    os.system(cmd)
    t2 = time.perf_counter()
    print('点击命令花费时间:%0.02f ms'%((t2-t1)*1000))

            
isRealRun = True
def getNextDayZeroTime():
    now = datetime.now()
    if isRealRun:
        return datetime(now.year, now.month, now.day) + timedelta(days=1)
    return datetime(now.year, now.month, now.day) + timedelta(seconds=3)
    
def waitTradeTime():
    while True:#run time is 11:59:59
        now = datetime.now()
        diff = getNextDayZeroTime().timestamp() - now.timestamp()
        if diff < 0.4:
            print ('时间到，开始行动')
            break
        print ('%s,倒计时%f秒'%(now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],diff),end='\r')
        
waitTradeTime()
start = time.perf_counter()
#直接执行点击    
click(30, 1636)     #点申购入口
click(1219,1134)    #点第一个加
click(1219,2144)    #点第二个加
click(917, 2969)    #点申购按键
click(810, 2002)    #点确定按键
nowt = time.perf_counter()
print('花费时间%0.02f ms'%((nowt-start)*1000))
        
        