import os
import cv2
import numpy as np
import time
import random

# 匹配第一层界面
tmep_ui1 = cv2.imread('ui1.jpg', 0)
# 匹配新三板入口
tmep_entry1 = cv2.imread('entry1.jpg', 0)
# 匹配新三板交易界面
tmep_ui2 = cv2.imread('ui2.jpg', 0)
# 匹配申购入口
tmep_entry2 = cv2.imread('entry2.jpg', 0)
# 匹配申购交易界面
tmep_ui3 = cv2.imread('ui3.jpg', 0)

#主要流程：
#1、找到屏幕的标记图，判断当前所在的界面
#2、根据标记图，做对应的反应

def get_screenshot(id):
    os.system('adb shell screencap -p /sdcard/%s.png' % str(id))
    os.system('adb pull /sdcard/%s.png .' % str(id))
	
def check_current_ui(img_rgb):
    res_end = cv2.matchTemplate(img_rgb, tmep_ui1, cv2.TM_CCOEFF_NORMED)
    if cv2.minMaxLoc(res_end)[1] > 0.95:
        print('now is at 1st ui')
        return 1
    res_end = cv2.matchTemplate(img_rgb, tmep_ui2, cv2.TM_CCOEFF_NORMED)
    if cv2.minMaxLoc(res_end)[1] > 0.95:
        print('now is at 2nd ui')
        return 2
    res_end = cv2.matchTemplate(img_rgb, tmep_ui3, cv2.TM_CCOEFF_NORMED)
    if cv2.minMaxLoc(res_end)[1] > 0.95:
        print('now is at 3rd ui')
        return 3
    return 0

#手指滑动xdis的水平距离和ydis的垂直距离
def input_swipe(xdis,ydis):
    cmd = ('adb shell input swipe %i %i %i %i ') \
          % (300, 600, 300 + xdis, 600 + ydis)
    print(cmd)
    os.system(cmd)

#手指点击
def click(x,y):
    cmd = ('adb shell input tap %i %i') % (x, y)
    print(cmd)
    os.system(cmd)

#手指点击某个图案，xdis,ydis为偏移距离
def clickUi(img_rgb,ui_rgb,xdis,ydis):
    res = cv2.matchTemplate(img_rgb, ui_rgb, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > 0.95:
        click(max_loc1[0]+xdis,max_loc1[1] + ydis)
    else
        print('not find entry ,something wrong')
        
# 循环直到申购成功
for i in range(100):
    get_screenshot(0)
    img_rgb = cv2.imread('%s.png' % 0, 0)
    
    now_ui = check_current_ui(img_rgb)
    if now_ui == 0:
        print('not in trader app,please enter app')
        break
    if now_ui == 1:
        print('try enter 2nd ui')
        input_swipe(1,-100);
        #点击进入新三板界面
        clickUi(img_rgb,tmep_entry1,20,20)
    elif now_ui == 2:
        print('try enter 3nd ui')
        #点击进入新三板界面
        clickUi(img_rgb,tmep_entry2,20,20)
    elif now_ui == 3:
        print('Subscribe stocks')
        #点击进入新三板界面
        #clickUi(img_rgb,tmep_entry2,20,20)
        break
    time.sleep(0.3)
        