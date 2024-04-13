import pygame
from object import *
from typing import Union

images = {
    '发射':pygame.image.load("other\发射.png"),
    '分裂':pygame.image.load("other\分裂.png")
    }

def select_minimum(a,b,c):
    if a < b and a < c:
        return a
    elif b < c:
        return b
    else:
        return False

def ball_is_colliding(myball:ball,myobject:Union[brick, paddle],width,height,min_multiple):
    '''
    注意这里的width,heigt指的是两物体宽之和,高之和的一半
    '''
    def sign(n):
        if n >= 0:
            return 1
        else:
            return -1
    distance_x = myball.position[0] - myobject.position[0]
    # 检测下一帧是否会碰撞
    # 如果会陷进去降低这一帧的速度
    if abs(distance_x + myball.velocity_vector[0]) <= width :
        distance_y =  myball.position[1] - myobject.position[1]
        if abs(distance_y + myball.velocity_vector[1]) <= height:
            # print('下一帧碰撞')
            # 检测这一帧是否碰到
            if abs(distance_x) <= width and abs(distance_y) <= height:
                # print("碰撞")
                return True
            x = -1*sign(distance_x)*(abs(distance_x)-width)
            y = -1*sign(distance_y)*(abs(distance_y)- height)
            
            a = float('inf')
            b = float('inf')
            if myball.velocity_vector[0] != 0:
                x_ = x / myball.velocity_vector[0]
                a = x_ if x_ > 0 else float('inf')
            if myball.velocity_vector[1] != 0:
                y_ = y / myball.velocity_vector[1]
                b = y_ if y_ > 0 else float('inf')
            min_mul = select_minimum(a, b, min_multiple[0])
            if min_mul != False:
                min_multiple[0] = min_mul
                min_multiple[1] = myobject


    return False

def prop_is_colliding(myprop:prop, mypaddle:paddle):
    distance_x = myprop.position[0] - mypaddle.position[0]
    distance_y = myprop.position[1] - mypaddle.position[1]

    if abs(distance_x) <= mypaddle.width + 7 and abs(distance_y) <= mypaddle.height + 7:
        return True
    return False
