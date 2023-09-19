# -*- coding: utf-8 -*-
import pygame
import time
import random
import math
import csv
import sys
#from pylsl import StreamInfo, StreamOutlet
from psychopy import visual, core
import psychopy
import egi.simple as egi

# from psychopy.hardware import joystick
#from psychopy import sound, gui, visual, core, data, event, logging, clock ,parallel

# P = parallel.ParallelPort(address=0x0378)
# P.setData(0)
# time.sleep(1)
# def sendcode(code):
#     P.setData(code)
#     time.sleep(0.006)
#     P.setData(0)
#     time.sleep(0.05)
#     return code
def get_result(N):
    a = []
    b = []
    c = []
    d = []
    e = []
    for i in range(0,N):
        x=random.random()
        if x>0.95:
            a.append(0)
        elif x>0.9:
            a.append(0.25)
        elif x>0.8:
            a.append(0.5)
        elif x>0.55:
            a.append(0.75)
        else:
            a.append(1)
        y=random.random()
        if y>0.95:
            b.append(1)
        elif y>0.9:
            b.append(0.75)
        elif y>0.8:
            b.append(0.5)
        elif y>0.55:
            b.append(0.25)
        else:
            b.append(0)
        if random.random()<0.5:
            c.append(1)
        else:
            c.append(0)
        if random.random()<0.5:
            d.append(1)
        else:
            d.append(0)
        if random.random()<0.25:
            e.append(0)
        else :
            e.append(1)
    return a,b,c,d,e

    # 收集被试的基本信息
# 收集被试的基本信息
ns = egi.Netstation()
ns.connect("10.10.10.42", 55513)  # sample address and port -- change according to your network settings
# # This sends some initialization info to NetStation for recording events.
ns.BeginSession()
# # This synchronizes the clocks of the stim computer and the NetStation computer.
ns.sync()

sub_info = [input(u'请输入被试编号：'),
            input(u'请输入性别（1=male，2=female）：'),
            input(u'请输入年龄：')]
                           
# 打开窗口，设置一些参数
pygame.init()  # pygame初始化
x_pixels, y_pixels = pygame.display.list_modes()[0]  # 获取屏幕分辨率
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # 打开窗口
x_center = int(win.get_width() / 2)  # 获取屏幕中心坐标
y_center = int(win.get_height() / 2)
win.fill((0, 0, 0))  # 将窗口设置为黑色
pygame.font.init()
font = pygame.font.SysFont('Kaiti', 50)  # 字体 & 字号
pygame.mouse.set_visible(False)  # 隐藏鼠标指针

trial_num = 2
high_result, low_result, no_result, ask_result, noask_result = get_result(trial_num)
rt_1 = []
rt_2 = []
resp_1 = []
resp_2 = []
high_num = 0
low_num = 0
ask_num = 0
no_num = 0
apple_tot= 0
apple=[]
Context = [] #0:no ,1:high ,2:low

cross = font.render('+', True, (255, 255, 255)) 
cross_x, cross_y = cross.get_size()
text_00 = font.render(u'此次可以询问', True, (255, 255, 255)) 
text_00_x, text_00_y = text_00.get_size()
text_0 = font.render(u'此次不能询问', True, (255, 255, 255)) 
text_0_x, text_0_y = text_0.get_size()

text_1 = font.render('-1', True, (255, 255, 255))
text_1_x, text_1_y = text_1.get_size()

choose = pygame.image.load('choose.png')
choose_size = choose.get_rect()

ifask = pygame.image.load('ifask.png')
ifask_size = ifask.get_rect()

ifask_no = pygame.image.load('ifask_no.png')
ifask_no_size = ifask_no.get_rect()

ifask_ask = pygame.image.load('ifask_ask.png')
ifask_ask_size = ifask_ask.get_rect()

LR_context1 = pygame.image.load('LR_context1.png')
LR_context1_size = LR_context1.get_rect()

LR_context2 = pygame.image.load('LR_context2.png')
LR_context2_size = LR_context2.get_rect()

LR_context0 = pygame.image.load('LR_context0.png')
LR_context0_size = LR_context0.get_rect()

R_context1 = pygame.image.load('R_context1.png')
R_context1_size = R_context1.get_rect()

L_context1 = pygame.image.load('L_context1.png')
L_context1_size = L_context1.get_rect()

R_context2 = pygame.image.load('R_context2.png')
R_context2_size = R_context2.get_rect()

L_context2 = pygame.image.load('L_context2.png')
L_context2_size = L_context2.get_rect()

L_context0 = pygame.image.load('L_context0.png')
L_context0_size = L_context0.get_rect()

R_context0 = pygame.image.load('R_context0.png')
R_context0_size = R_context0.get_rect()

plus12 = pygame.image.load('plus12.png')
plus12_size = plus12.get_rect()

plus9 = pygame.image.load('plus9.png')
plus9_size = plus9.get_rect()

plus6 = pygame.image.load('plus6.png')
plus6_size = plus6.get_rect()

plus3 = pygame.image.load('plus3.png')
plus3_size = plus3.get_rect()

plus0 = pygame.image.load('plus0.png')
plus0_size = plus0.get_rect()

context1 = pygame.image.load('context1.png')
context1_size = context1.get_rect()

context2 = pygame.image.load('context2.png')
context2_size = context2.get_rect()

context0 = pygame.image.load('context0.png')
context0_size = context0.get_rect()

ns.StartRecording()

win.fill((0, 0, 0))
win.blit(cross, (int(x_center - cross_x / 2), int(y_center - cross_y / 2)))
pygame.display.update()
wait = True
while wait:  # 等待按键
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            wait = False


# 呈现指导语
instruction = pygame.image.load('instruction.png')
instruction_size = instruction.get_rect()
win.blit(instruction, (x_center - instruction_size[2]//2, y_center - instruction_size[3]//2))
pygame.display.update()
wait = True
while wait:  # 等待按键
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            wait = False

for i in range(0,trial_num):
    noask = False
    win.fill((0, 0, 0))
    win.blit(cross, (int(x_center - cross_x / 2), int(y_center - cross_y / 2)))
    pygame.display.update()
    time.sleep((random.random()*0.4+0.6))
    win.fill((0, 0, 0))
    if noask_result[i] == 0 :
        noask = True
        win.blit(text_0, (int(x_center - text_0_x//2 ), int(y_center - text_0_y//2 )))
        pygame.display.update()
        
        ns.sync()
        ns.send_event('0001', timestamp=bytes(egi.ms_localtime()), label='noask')
        # if noask :
        #     code = sendcode('66')

        # else :
        #     code = sendcode('88')
        time.sleep(1.5)
    else :
        win.blit(text_00, (int(x_center - text_00_x//2 ), int(y_center - text_00_y//2 )))
        pygame.display.update()
        
        # if noask :
        #     code = sendcode('66')

        # else :
        #     code = sendcode('88')
        ns.sync()
        ns.send_event('0002', timestamp=bytes(egi.ms_localtime()), label='canask')
        time.sleep(1.5)
        
        win.fill((0, 0, 0))
        win.blit(cross, (int(x_center - cross_x / 2), int(y_center -cross_y / 2)))
        pygame.display.update()
        time.sleep((random.random()*0.4+0.6))
        win.fill((0, 0, 0))
        win.blit(ifask, (x_center - ifask_size[2]//2, y_center - ifask_size[3]//2))
        pygame.display.update()
        ns.sync()
        ns.send_event('0024', timestamp=bytes(egi.ms_localtime()), label='choose1')
        time.sleep(1.5)
        win.fill((0, 0, 0))
        win.blit(ifask, (x_center - ifask_size[2]//2, y_center - ifask_size[3]//2))
        win.blit(choose, (x_center - choose_size[2]//2, y_center - ifask_size[3]//2 - choose_size[3]))
        pygame.display.update()


    key_check = False
    context = False
    if_ask = False
    pygame.event.clear()
    t0 = time.time()
    while ( not key_check ) :        
        if noask :
            key_check = True
            Context.append(0)
            resp_1.append(' ')
            rt_1.append(0)
            win.fill((0, 0, 0))
            win.blit(cross, (int(x_center - cross_x / 2), int(y_center -cross_y / 2)))
            pygame.display.update()
            time.sleep((random.random()*0.4+0.6))
            win.fill((0, 0, 0))
            win.blit(context0, (x_center - context0_size[2]//2, y_center - context0_size[3]//2))
        else :
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if not key_check:
                        key_check = True
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        else:
                            rt_1.append(time.time() - t0)
                            if event.key ==pygame.K_LEFT :
                                Context.append(0)
                                resp_1.append('left')

                                win.fill((0, 0, 0))
                                win.blit(choose, (x_center - choose_size[2]//2, y_center - ifask_no_size[3]//2 - choose_size[3]))
                                win.blit(ifask_no, (x_center - ifask_no_size[2]//2, y_center - ifask_no_size[3]//2))
                                pygame.display.update()
                                time.sleep(0.5)
                                win.fill((0, 0, 0))
                                win.blit(cross, (int(x_center - cross_x / 2), int(y_center -cross_y / 2)))
                                pygame.display.update()
                                time.sleep((random.random()*0.4+0.6))
                                win.fill((0, 0, 0))
                                win.blit(context0, (x_center - context0_size[2]//2, y_center - context0_size[3]//2))
                            elif event.key ==pygame.K_RIGHT :
                                resp_1.append('right')
                                if_ask = True
                                if ask_result[ask_num] == 1 :
                                    Context.append(1)
                                    context = True
                                    win.fill((0, 0, 0))
                                    win.blit(ifask_ask, (x_center - ifask_ask_size[2]//2, y_center - ifask_ask_size[3]//2))
                                    win.blit(text_1, (int(x_center + text_1_x ), int(y_center + ifask_ask_size[3]*0.52 )))
                                    win.blit(choose, (x_center - choose_size[2]//2, y_center - ifask_ask_size[3]//2 - choose_size[3]))
                                    pygame.display.update()
                                    time.sleep(0.5)
                                    win.fill((0, 0, 0))
                                    win.blit(cross, (int(x_center - cross_x / 2), int(y_center -cross_y / 2)))
                                    pygame.display.update()
                                    time.sleep((random.random()*0.4+0.6))
                                    win.fill((0, 0, 0))
                                    win.blit(context1, (x_center - context1_size[2]//2, y_center - context1_size[3]//2))
                                else :
                                    Context.append(2)
                                    context = False
                                    win.fill((0, 0, 0))
                                    win.blit(ifask_ask, (x_center - ifask_ask_size[2]//2, y_center - ifask_ask_size[3]//2))
                                    win.blit(text_1, (int(x_center + text_1_x ), int(y_center + ifask_ask_size[3]*0.52 )))
                                    win.blit(choose, (x_center - choose_size[2]//2, y_center - ifask_ask_size[3]//2 - choose_size[3]))
                                    pygame.display.update()
                                    time.sleep(0.5)
                                    win.fill((0, 0, 0))
                                    win.blit(cross, (int(x_center - cross_x / 2), int(y_center -cross_y / 2)))
                                    pygame.display.update()
                                    time.sleep((random.random()*0.4+0.6))
                                    win.fill((0, 0, 0))
                                    win.blit(context2, (x_center - context2_size[2]//2, y_center - context2_size[3]//2))
                            else :
                                key_check = False
                            
                                                    

    key_check = False

    pygame.display.update()
    
    # if context and if_ask :
    #     code = sendcode('11')
    # elif (not if_ask) :
    #     code = sendcode('00')
    # else :
    #     code = sendcode('10')
    if context and if_ask :
        ns.sync()
        ns.send_event('0003', timestamp=bytes(egi.ms_localtime()), label='case1')
    elif (not if_ask) :
        ns.sync()
        ns.send_event('0004', timestamp=bytes(egi.ms_localtime()), label='donotask')
    else :
        ns.sync()
        ns.send_event('0005', timestamp=bytes(egi.ms_localtime()), label='case2')

    time.sleep(2)
    win.fill((0, 0, 0))
    win.blit(cross, (int(x_center - cross_x / 2), int(y_center -cross_y / 2)))
    pygame.display.update()
    time.sleep((random.random()*0.4+0.6))
    win.fill((0, 0, 0))
    
    if Context[i] == 0 :
        win.blit(LR_context0, (x_center - LR_context0_size[2]//2, y_center - LR_context0_size[3]//2))
    elif Context[i] == 1 :
        win.blit(LR_context1, (x_center - LR_context1_size[2]//2, y_center - LR_context1_size[3]//2))
    else :
        win.blit(LR_context2, (x_center - LR_context2_size[2]//2, y_center - LR_context2_size[3]//2))

    pygame.display.update()
    ns.sync()
    ns.send_event('0025', timestamp=bytes(egi.ms_localtime()), label='choose2')
    time.sleep(1.5)
    win.blit(choose, (x_center - choose_size[2]//2, y_center - LR_context2_size[3]//2 - choose_size[3])) 
    pygame.display.update()
    pygame.event.clear()
    t0 = time.time()    
    while ( not key_check ) :        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if not key_check:
                    key_check = True
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    else:
                        rt_2.append(time.time() - t0)
                        if event.key ==pygame.K_LEFT :
                            resp_2.append(0) #0:safe(left) 1:risk(right)
                            apple.append(6)
                            win.fill((0, 0, 0))
                            if Context[i] == 0 :
                                win.blit(L_context0, (x_center - L_context0_size[2]//2, y_center - L_context0_size[3]//2))
                            elif Context[i] == 1 :
                                win.blit(L_context1, (x_center - L_context1_size[2]//2, y_center - L_context1_size[3]//2))
                            else :
                                win.blit(L_context2, (x_center - L_context2_size[2]//2, y_center - L_context2_size[3]//2))
                            win.blit(choose, (x_center - choose_size[2]//2, y_center - LR_context2_size[3]//2 - choose_size[3])) 
                            pygame.display.update()
                            time.sleep(0.5)
                            win.fill((0, 0, 0))
                            win.blit(cross, (int(x_center - cross_x / 2), int(y_center -cross_y / 2)))
                            pygame.display.update()
                            time.sleep((random.random()*0.4+0.6))
                            win.fill((0, 0, 0))
                            win.blit(plus6, (x_center - plus6_size[2]//2, y_center - plus6_size[3]//2))
                            if if_ask :
                                apple_tot = apple_tot + apple[i] - 1
                            else :
                                apple_tot = apple_tot + apple[i]
                        elif event.key ==pygame.K_RIGHT :
                            resp_2.append(1)
                            if context and if_ask :
                                apple.append(high_result[high_num]*12)
                                high_num += 1
                                win.fill((0, 0, 0))
                                win.blit(R_context1, (x_center - R_context1_size[2]//2, y_center - R_context1_size[3]//2))
                                win.blit(choose, (x_center - choose_size[2]//2, y_center - LR_context2_size[3]//2 - choose_size[3])) 
                                pygame.display.update()
                                time.sleep(0.5)
                                win.fill((0, 0, 0))
                                win.blit(cross, (int(x_center - cross_x / 2), int(y_center -cross_y / 2)))
                                pygame.display.update()
                                time.sleep((random.random()*0.4+0.6))
                                win.fill((0, 0, 0))
                                if apple[i] == 12 :
                                    win.blit(plus12, (x_center - plus12_size[2]//2, y_center - plus12_size[3]//2))
                                elif apple[i] == 9 :
                                    win.blit(plus9, (x_center - plus9_size[2]//2, y_center - plus9_size[3]//2))
                                elif apple[i] == 6 :
                                    win.blit(plus6, (x_center - plus6_size[2]//2, y_center - plus6_size[3]//2))
                                elif apple[i] == 3 :
                                    win.blit(plus3, (x_center - plus3_size[2]//2, y_center - plus3_size[3]//2))
                                else :
                                    win.blit(plus0, (x_center - plus0_size[2]//2, y_center - plus0_size[3]//2))
                            elif not if_ask :
                                apple.append(no_result[no_num]*12)
                                win.fill((0, 0, 0))
                                win.blit(R_context0, (x_center - R_context0_size[2]//2, y_center - R_context0_size[3]//2))
                                win.blit(choose, (x_center - choose_size[2]//2, y_center - LR_context2_size[3]//2 - choose_size[3])) 
                                pygame.display.update()
                                time.sleep(0.5)
                                win.fill((0, 0, 0))
                                win.blit(cross, (int(x_center - cross_x / 2), int(y_center -cross_y / 2)))
                                pygame.display.update()
                                time.sleep((random.random()*0.4+0.6))
                                win.fill((0, 0, 0))
                                if apple[i] == 12 :
                                    win.blit(plus12, (x_center - plus12_size[2]//2, y_center - plus12_size[3]//2))
                                else :
                                    win.blit(plus0, (x_center - plus0_size[2]//2, y_center - plus0_size[3]//2))
                                no_num += 1
                                
                            else :
                                apple.append(low_result[low_num]*12)
                                low_num += 1
                                win.fill((0, 0, 0))
                                win.blit(R_context2, (x_center - R_context2_size[2]//2, y_center - R_context2_size[3]//2))
                                win.blit(choose, (x_center - choose_size[2]//2, y_center - LR_context2_size[3]//2 - choose_size[3])) 
                                pygame.display.update()
                                time.sleep(0.5)
                                win.fill((0, 0, 0))
                                win.blit(cross, (int(x_center - cross_x / 2), int(y_center -cross_y / 2)))
                                pygame.display.update()
                                time.sleep((random.random()*0.4+0.6))
                                win.fill((0, 0, 0))
                                if apple[i] == 12 :
                                    win.blit(plus12, (x_center - plus12_size[2]//2, y_center - plus12_size[3]//2))
                                elif apple[i] == 9 :
                                    win.blit(plus9, (x_center - plus9_size[2]//2, y_center - plus9_size[3]//2))
                                elif apple[i] == 6 :
                                    win.blit(plus6, (x_center - plus6_size[2]//2, y_center - plus6_size[3]//2))
                                elif apple[i] == 3 :
                                    win.blit(plus3, (x_center - plus3_size[2]//2, y_center - plus3_size[3]//2))
                                else :
                                    win.blit(plus0, (x_center - plus0_size[2]//2, y_center - plus0_size[3]//2))
                            if if_ask :
                                apple_tot = apple_tot + apple[i] - 1
                            else :
                                apple_tot = apple_tot + apple[i]
                        else:
                            key_check = False
                        
    
                            
    if context and if_ask :
        if apple[i] == 0 :
            ns.sync()
            ns.send_event('0006', timestamp=bytes(egi.ms_localtime()), label='case1+0')
        elif apple[i] == 3 :
            ns.sync()
            ns.send_event('0007', timestamp=bytes(egi.ms_localtime()), label='case1+3')
        elif apple[i] == 6 :
            if resp_2 == 0:  #left
                ns.sync()
                ns.send_event('0008', timestamp=bytes(egi.ms_localtime()), label='Lcase1+6')
            else : #right
                ns.sync()
                ns.send_event('0009', timestamp=bytes(egi.ms_localtime()), label='Rcase1+6')
        elif apple[i] == 9 :
            ns.sync()
            ns.send_event('0010', timestamp=bytes(egi.ms_localtime()), label='case1+9')
        else :
            ns.sync()
            ns.send_event('0011', timestamp=bytes(egi.ms_localtime()), label='case1+12')
    elif (not if_ask) :
        if apple[i] == 0 :
            ns.sync()
            ns.send_event('0012', timestamp=bytes(egi.ms_localtime()), label='no+0')
        elif apple[i] == 3 :
            ns.sync()
            ns.send_event('0013', timestamp=bytes(egi.ms_localtime()), label='no+3')
        elif apple[i] == 6 :
            if resp_2 == 0:  #left
                ns.sync()
                ns.send_event('0014', timestamp=bytes(egi.ms_localtime()), label='Lno+6')
            else : #right
                ns.sync()
                ns.send_event('0015', timestamp=bytes(egi.ms_localtime()), label='Rno+6')
        elif apple[i] == 9 :
            ns.sync()
            ns.send_event('0016', timestamp=bytes(egi.ms_localtime()), label='no+9')
        else :
            ns.sync()
            ns.send_event('0017', timestamp=bytes(egi.ms_localtime()), label='no+12')
    else :
        if apple[i] == 0 :
            ns.sync()
            ns.send_event('0018', timestamp=bytes(egi.ms_localtime()), label='case2+0')
        elif apple[i] == 3 :
            ns.sync()
            ns.send_event('0019', timestamp=bytes(egi.ms_localtime()), label='case2+3')
        elif apple[i] == 6 :
            if resp_2 == 0:  #left
                ns.sync()
                ns.send_event('0020', timestamp=bytes(egi.ms_localtime()), label='Lcase2+6')
            else : #right
                ns.sync()
                ns.send_event('0021', timestamp=bytes(egi.ms_localtime()), label='Rcase2+6')
        elif apple[i] == 9 :
            ns.sync()
            ns.send_event('0022', timestamp=bytes(egi.ms_localtime()), label='case2+9')
        else :
            ns.sync()
            ns.send_event('0023', timestamp=bytes(egi.ms_localtime()), label='case2+12')
    
    # if context and if_ask :
    #     if apple[i] == 6 :
    #         code = sendcode('1100')
    #     elif apple[i] == 0 :
    #         code = sendcode('1110')
    #     else :
    #         code = sendcode('1111')
    # elif (not if_ask) :
    #     if apple[i] == 6 :
    #         code = sendcode('0000')
    #     elif apple[i] == 0 :
    #         code = sendcode('0010')
    #     else :
    #         code = sendcode('0011')
    # else :
    #     if apple[i] == 6 :
    #         code = sendcode('1000')
    #     elif apple[i] == 0 :
    #         code = sendcode('1010')
    #     else :
    #         code = sendcode('1011')
    pygame.display.update()
    time.sleep(2)
    win.fill((0, 0, 0))
    win.blit(cross, (int(x_center - cross_x / 2), int(y_center - cross_y / 2)))
    pygame.display.update()
    time.sleep((random.random()*0.4+0.6))
    win.fill((0, 0, 0))
    text5 = '总共' + str(apple_tot)
    text_5 = font.render(text5, True, (255, 255, 255))
    text_5_x, text_5_y = text_5.get_size()
    win.blit(text_5, (int(x_center - text_5_x / 2), int(y_center - text_5_y//2 )))
    pygame.display.update()
    time.sleep(1)

pygame.quit()
    
print('aaa')
date = (time.strftime("%Y_%b_%d_%H%M%S"))  # 获取时间
c = open('uncertainty_{}_{}.csv'.format(sub_info[0], date),
         'w', encoding='utf-8', newline='')  # 创建csv表格
csv_writer = csv.writer(c)  # 基于文件对象构建csv写入对象
csv_writer.writerow(['NoAsk', 'Resp_1', 'Rt_1', 'Context', 'Resp_2', 'Rt_2',
                     'Apple'])  # 表头
for trial in range(0, trial_num):  # 写入csv
    csv_writer.writerow([noask_result[trial], resp_1[trial], rt_1[trial], Context[trial], resp_2[trial],
                         rt_2[trial], apple[trial]])
c.close()  # 关闭csv表格

print('Succeed!')
