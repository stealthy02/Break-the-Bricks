import random

class ball:
    def __init__(self,position:tuple,velocity_vector:tuple = [0,-15],color:tuple=(255,255,255)) -> None:
        # self.radius = radius
        self.position = position
        self.velocity_vector = velocity_vector
        self.color = color

    def move(self):
        self.position = [self.position[0] + self.velocity_vector[0], self.position[1] + self.velocity_vector[1]]

    def bounce(self,crash_position):
        # 为了防止两个砖块内卡死加随机值
        x = self.position[0] - crash_position[0] + random.randint(-3,3)
        y = self.position[1] - crash_position[1] + random.randint(-3,3)
        v = 15
        try:
            self.velocity_vector = [v*x//(abs(x)+abs(y)),v*y//(abs(x)+abs(y))]
        except:
            self.velocity_vector = [0, v]
        # print('回弹',self.velocity_vector)


class brick:
    num_destructible = 0
    def __init__(self,position:tuple,color:tuple = (22, 43, 70),destructible:bool = True,width = 18) -> None:
        self.position = position
        self.color = color
        self.destructible = destructible
        self.width = width
        if destructible:
            brick.num_destructible += 1

class prop:
    def __init__(self, position:tuple,type:str = None) -> None:
        '''
        type:道具种类
        分裂:弹球一分为二
        发射:从底部发射两个
        '''
        self.position = position
        if type == None:
            self.type = random.choice(['分裂', '发射'])
            # self.type = random.choice(['分裂'])
        else:
            self.type = type

    def move(self):
        self.position[1] += 5

class paddle:
    def __init__(self, position:list, width:int, height:int) -> None:
        self.position = position
        self.width = width
        self.height = height


    def move(self, direction:str) -> None:
        self.position[0] = direction