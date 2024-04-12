import pygame
import time
from object import *
import sys
from utilit import *
import json
import math
import random
import copy
from PIL import Image


# 参数(可更改)
brick_image_path = 'material/鸽鸽.jpg' # 砖块展示图片 如果None则换为白色圆球
ball_image_path = 'material/篮球.png' # 球展示图片
sound_path = 'material/你干嘛.mp3' # 音效路径
bgimage = False # 是否背后添加背景图
bottom_opening_num = 8 # 低边框开口格数
ball_radius = 10 # 球的半径
brick_width = 20 # 砖块宽度为偶数
paddle_height = 20 # 板子高度
interval = 1 # 砖块间隔
num_brick_x = 28 # 一行有多少砖块
num_brick_y = 28 # 一列有多少砖块
bottom_interval = 230 # 底部空出的距离
bg_color = (0,0,0) # 背景颜色
brick_color = (22, 43, 70) # 边框砖块颜色
# 道具刷出概率函数
def prop_probability():
    probability = 2**(-(len(ball_list)-0.5)//120)
    return probability



star = time.time()
# 初始化pygame
pygame.init()
# 初始化不需要赋值
win = None 
win_width = None 
win_height = None 
rgb_list = None
ball_list:list[ball] = []
brick_list:list[brick] = []
prop_list:list[prop] = []
mypaddle = None 

distance_ball_brick = ball_radius + brick_width//2 # 砖块和球的贴上时中心点距离 不需要处理
distance_ball_paddle = ball_radius + paddle_height//2 # 挡板和球的贴上时中心点距离 不需要处理


if sound_path != None:
    pygame.mixer.init()
    crash_sound = pygame.mixer.Sound(sound_path)
else:
    crash_sound = None
# 绝对值上取整
def custom_round(x):
    if x >= 0:
        return math.ceil(x)
    else:
        return -math.ceil(-x)

# 处理图片
def image_processing(image_path):    
    global rgb_list,num_brick_x,num_brick_y
    image = Image.open(image_path)
    # 是否加背景图  
    if bgimage:
        image = image.resize((num_brick_x*(brick_width+2*interval),num_brick_y*(brick_width+2*interval)))
        image.save('other\\背景.png')
        images['背景'] = pygame.image.load('other\\背景.png')
    image = image.resize((num_brick_x,num_brick_y))
    # 获取图像的 RGB 数据
    rgb_data = list(image.getdata())

    # 将一维的 RGB 数据转换为二维数组
    rgb_list = [rgb_data[i * num_brick_x:(i + 1) * num_brick_x] for i in range(num_brick_y)]

    # # 存储为 JSON 文件
    # output_file = "rgb.json"
    # with open(output_file, 'w') as file:
    #     json.dump(rgb_list, file)
    if ball_image_path != None:
        image = Image.open(ball_image_path)
        image = image.resize((ball_radius*2, ball_radius*2))
        image.save('other\\球.png')
        images['球'] = pygame.image.load('other\\球.png')


# 初始化游戏数据
def setup(rgb_list,ball_radius,brick_width):
    global  mypaddle,ball_list,win_width,win_height,brick_list,prop_list,win,num_brick_y,num_brick_x
    # num_brick_x = len(rgb_list)
    # num_brick_y = len(rgb_list[0])
    win_width = (2 + num_brick_x)*(brick_width + 2*interval)
    win_height = (num_brick_y)*(brick_width + 2*interval) + bottom_interval + 30
    win = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("打砖块游戏")
    # 初始化球的位置、大小等参数
    # for i in range(10):
    for i in range(20):
        ball_list.append(ball([win_width // 2, win_height - 48]))

    # 初始化砖块
    # 顶部砖块
    creat_frame(num_brick_x,num_brick_y, brick_color)
    creat_picture(rgb_list, brick_width)
    paddle_width = 150
    paddle_x = win_width // 2
    paddle_y = win_height - 30
    mypaddle = paddle([paddle_x, paddle_y], paddle_width, paddle_height)

# 跟具大方格位置创建砖块
def creat_brick(x,y,color=(22, 43, 70),destructible = True):
    position = [brick_width//2+interval + x * (brick_width+2*interval), brick_width//2+interval + y * (brick_width+2*interval)]
    brick_list.append(brick(position, color,destructible, width=brick_width))

# 创建边框
def creat_frame(num_brick_x,num_brick_y,color):
    # 上下
    for i in range(num_brick_x+2):
        creat_brick(i,0,color,False)
        # 下边界开口
        left_opening_num = bottom_opening_num//2
        if  i <= num_brick_x//2+ left_opening_num and i >= num_brick_x//2 - bottom_opening_num+left_opening_num:
            continue
        creat_brick(i, num_brick_y+1,color, False)
    
    for i in range(num_brick_y+1):
        # 左侧
        creat_brick(0, i, color, False)
        # 右侧
        creat_brick(num_brick_x+1, i, color, False)

# 创建图片
def creat_picture(rgb_list, brick_width):
    for y,line in enumerate(rgb_list):
        for x,rgb in enumerate(line):
            creat_brick(x+1, y+1, rgb)

# 小球碰撞检测
def ball_colliding(myball:ball):
    # 下一帧的y的移动距离
    is_colliding = False
    min_multiple = [1,None]
    for mybrick in brick_list:
        is_colliding = ball_is_colliding(myball,mybrick,distance_ball_brick,distance_ball_brick,min_multiple)
        if is_colliding:
            myball.bounce(mybrick.position)
            if crash_sound:
                crash_sound.play()
            min_multiple = [1,None]
            if mybrick.destructible:
                brick.num_destructible -= 1
                brick_list.remove(mybrick)
                # 如果砖块破坏则生成道具
                if random.random() < prop_probability():
                
                    prop_list.append(prop(mybrick.position))
            # 如果砖块没了结束游戏
            if brick.num_destructible == 0:
                brick.num_destructible = -1
                show_game_over_screen('你赢了')

            # 如果已经检测到碰撞则不在检测碰撞
            break
        ball_is_colliding(myball,mybrick,distance_ball_brick,distance_ball_brick,min_multiple)
    
    if not is_colliding:
        is_colliding =  ball_is_colliding(myball, mypaddle,ball_radius + mypaddle.width//2,distance_ball_paddle,min_multiple)
        if is_colliding:
            myball.bounce((mypaddle.position[0],mypaddle.position[1]+20))

    # 选出最近的碰撞点改变
    if min_multiple[0] != 1 and not is_colliding:
        myball.position[0] += custom_round(myball.velocity_vector[0]*min_multiple[0])
        myball.position[1] += custom_round(myball.velocity_vector[1]*min_multiple[0])
        myball.bounce(min_multiple[1].position)
        if crash_sound:
            crash_sound.play()
        if type(min_multiple[1]) == brick and min_multiple[1].destructible:
            brick.num_destructible -= 1
            # 如果砖块破坏则生成道具
            if random.random() < prop_probability():
                prop_list.append(prop(min_multiple[1].position))
            brick_list.remove(min_multiple[1])


# 道具碰撞检测
def prop_colliding(myprop:prop, mypaddle:paddle):
    if prop_is_colliding(myprop,mypaddle):
        if myprop.type == '分裂':
            if len(ball_list) > 8:
                new_list = []
                for i in range(8):
                    new_list.append(copy.copy(ball_list[i]))
            else:
                new_list= copy.deepcopy(ball_list)
            ball_list.extend(new_list)
        else :
            ball_list.append(ball(myprop.position,[0,-15]))
        prop_list.remove(myprop)

# 小球出界处理
def out_of_bounds(myball:ball):
    if myball.position[1] > win_height+ball_radius or myball.position[1] < -ball_radius:
        ball_list.remove(myball)
    if myball.position[0] > win_width or myball.position[0] < 0 :
        myball.velocity_vector[0] *= -1
    if len(ball_list) == 0:
        print(time.time() - star)
        show_game_over_screen('你输了')

# 处理下一帧数据
def object_calculate():
    # 道具移动
    for prop in prop_list:
        prop.move()
        prop_colliding(prop, mypaddle)
        if prop.position[1] > win_height:
            prop_list.remove(prop)
    # 球碰撞和移动
    for myball in ball_list:
        myball.move()
        ball_colliding(myball)
        out_of_bounds(myball)

# 鼠标监听
def mouse():
    global mypaddle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 点击窗口的关闭按钮
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:  # 鼠标移动事件
            mouse_x, mouse_y = event.pos
            # 处理鼠标移动事件
            mypaddle.move(mouse_x)

# 根据数据画出对应图
def draw():
    global ball_list,prop_list,brick_list,mypaddle
    # 绘制游戏画面
    win.fill(bg_color)  # 用白色填充整个窗口
    if bgimage:
        win.blit(images['背景'], [brick_width+2, brick_width+2])
    # 绘制球
    if ball_image_path != None:
        for ball in ball_list:
            win.blit(images['球'], [ball.position[0]-ball_radius, ball.position[1]-ball_radius])
    else:
        for ball in ball_list:
            pygame.draw.circle(win, ball.color, ball.position, ball_radius)
        
    for brick in brick_list:
        pygame.draw.rect(win, brick.color, (brick.position[0]-brick.width//2, brick.position[1]-brick.width//2, brick.width, brick.width))

    for prop in prop_list:
        win.blit(images[prop.type], [prop.position[0]-15,prop.position[1]-15])
    # 绘制挡板
    paddle_color = (140, 162, 250)
    pygame.draw.rect(win, paddle_color, (mypaddle.position[0]-mypaddle.width//2, mypaddle.position[1]-mypaddle.height//2,mypaddle.width, mypaddle.height))
    pygame.draw.circle(win, paddle_color, (mypaddle.position[0] - mypaddle.width//2, mypaddle.position[1]), mypaddle.height // 2)
    pygame.draw.circle(win, paddle_color, (mypaddle.position[0] + mypaddle.width//2, mypaddle.position[1]), mypaddle.height // 2)
    
    # 更新画面
    pygame.display.update()

# 结束画面函数
def show_game_over_screen(message,size=100,color=(70, 130, 180)):
    # 创建字体对象
    font = pygame.font.Font('C:\Windows\Fonts\STHUPO.TTF',size)

    # 渲染文本
    text = font.render(message, True, color)

    for i in range(30):
        mouse()
        object_calculate()
        draw()
        time.sleep(0.03)
    # 主循环
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 居中绘制文本
        text_rect = text.get_rect(center=(win_width // 2, win_height // 2))
        win.blit(text, text_rect)

        # 更新屏幕
        pygame.display.flip()

image_processing(brick_image_path)
setup(rgb_list,ball_radius,brick_width)
draw()
font = pygame.font.Font('C:\Windows\Fonts\STHUPO.TTF',100)
for i in range(3):
    text = font.render(str(3-i), True, (70, 130, 180))
    text_rect = text.get_rect(center=(win_width // 2, win_height // 2))
    win.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(1)

# 主循环
while True:
    star_1 = time.time()
    mouse()
    object_calculate()
    draw()
    sleep_time = 0.04-time.time()+star_1
    if sleep_time > 0:
        time.sleep(sleep_time)
    else:
        print('掉帧了')
