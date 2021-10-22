import os
import cv2
import numpy as np
import time
import random

# 匹配第一层界面
temp_ui1 = cv2.imread('ui1.png', 0)
# 匹配新三板入口
temp_entry1 = cv2.imread('entry1.png', 0)
# 匹配新三板交易界面
temp_ui2 = cv2.imread('entry2.png', 0)
# 匹配申购入口
temp_entry2 = cv2.imread('entry2.png', 0)
# 匹配申购交易界面
temp_ui3 = cv2.imread('ui3.png', 0)
# 匹配申购加按键 --- 
temp_plus = cv2.imread('ui3.png', 0) 
# 匹配申购按键 ---
temp_ok = cv2.imread('ui3.png', 0)

#主要流程：
#1、找到屏幕的标记图，判断当前所在的界面
#2、根据标记图，做对应的反应

def get_screenshot(id):
    t1 = time.perf_counter()
#    os.system('adb shell screencap -p /sdcard/%s.png' % str(id))
#    os.system('adb pull /sdcard/%s.png .' % str(id))
    os.system('adb exec-out screencap -p > %s.png' % str(id))
    t2 = time.perf_counter()
    print('截屏花费时间:%0.02f ms'%((t2-t1)*1000))
    
def check_current_ui(img_rgb):
    res_end = cv2.matchTemplate(img_rgb, temp_entry1, cv2.TM_CCOEFF_NORMED)
    if cv2.minMaxLoc(res_end)[1] > 0.95:
        print('现在可以点击新三板入口了')
        return 4
    res_end = cv2.matchTemplate(img_rgb, temp_ui1, cv2.TM_CCOEFF_NORMED)
    if cv2.minMaxLoc(res_end)[1] > 0.95:
        print('现在在第一层界面')
        return 1
    res_end = cv2.matchTemplate(img_rgb, temp_ui2, cv2.TM_CCOEFF_NORMED)
    if cv2.minMaxLoc(res_end)[1] > 0.95:
        print('现在在第二层界面')
        return 2
    res_end = cv2.matchTemplate(img_rgb, temp_ui3, cv2.TM_CCOEFF_NORMED)
    if cv2.minMaxLoc(res_end)[1] > 0.95:
        print('现在在第三层界面')
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
    t1 = time.perf_counter()
    cmd = ('adb shell input tap %i %i') % (x, y)
    print(cmd)
    os.system(cmd)
    t2 = time.perf_counter()
    print('点击命令花费时间:%0.02f ms'%((t2-t1)*1000))

#手指点击某个图案，xdis,ydis为偏移距离
def clickUi(img_rgb,ui_rgb,xdis,ydis):
    t1 = time.perf_counter()
    res = cv2.matchTemplate(img_rgb, ui_rgb, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val > 0.95:
        print(max_loc)
        click(max_loc[0]+xdis,max_loc[1] + ydis)
    else:
        print('没找到入口，有问题')
    t2 = time.perf_counter()
    print('点击UI花费时间:%0.02f ms'%((t2-t1)*1000))
    
#手指点击所有图案，xdis,ydis为偏移距离
def clickAllUi(img_rgb,ui_rgb,xdis,ydis):
    res = cv2.matchTemplate(img_rgb, ui_rgb, cv2.TM_CCOEFF_NORMED)
    # fake out max_val for first run through loop
    max_val = 1
    while max_val > 0.95:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val > 0.95:
            res[max_loc[1]-h//2:max_loc[1]+h//2+1, max_loc[0]-w//2:max_loc[0]+w//2+1] = 0   
            #image = cv2.rectangle(image,(max_loc[0],max_loc[1]), (max_loc[0]+w+1, max_loc[1]+h+1), (0,255,0) )
            print('点击了(%d,%d)'%(max_loc[0]+xdis,max_loc[1] + ydis))
            click(max_loc[0]+xdis,max_loc[1] + ydis)

isRealRun = False
#def waitTradeTime():
#    while isRealRun:#真实运行需要等到11:59:59才开始
        

start = time.perf_counter()
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
        input_swipe(1,-500);
    elif now_ui == 2:
        print('try enter 3nd ui')
        #点击进入申购界面
        clickUi(img_rgb,temp_entry2,20,20)
    elif now_ui == 3:
        print('Subscribe stocks')
        #点击加按键
        #clickUi(img_rgb,temp_entry2,20,20)
        #点击申购
        #clickUi(img_rgb,temp_entry2,20,20)
        break
    elif now_ui == 4:
        #点击进入新三板界面
        clickUi(img_rgb,temp_entry1,20,20)
        
nowt = time.perf_counter()
print('花费时间%0.02f ms'%((nowt-start)*1000))
        
        