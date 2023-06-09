# Imports go at the top
from microbit import *
import random, music, speech, time

start = False
Exit =True
points = 0 #初始得分0
panel = []
# 由于单片机只能显示红色，可以用亮度区分目标点，player点和地雷
# 设定player点亮度9，目标点亮度6，地雷亮度3
pl = 9 #player亮度playerlight
gl = 6 #goal亮度goallight
bl = 3 #bomb亮度bomblight
interval = [4000, 3000, 2000, 1000, 500]
level = 0

#单片机上显示所有点的坐标
lst = [[0,0],[0,1],[0,2],[0,3],[0,4],[1,0],[1,1],[1,2],[1,3],
      [1,4],[2,0],[2,1],[2,2],[2,3],[2,4],[3,0],[3,1],[3,2],
      [3,3],[3,4],[4,0],[4,1],[4,2],[4,3],[4,4]]
num = ['1234','1324','1342','1423','1432','1243','2134','2143','2314','2341','2413','2431',
       '3124','3142','3214','3241','3412','3421','4123','4132','4213','4231','4312','4321']

player = [2,2]
goalset = []
bombset = []
bombTime = time.ticks_ms()

#控制player随加速度变化移动位置
def movecontrol():
    global player
    '''每次刷新player点位置，先将上一轮的player亮度设置为0，再重新设置新一轮的player亮度'''
    display.set_pixel(player[0],player[1],0)
    x = (accelerometer.get_x()+1000)//400
    y = (accelerometer.get_y()+1000)//400
    if x > 4:
        x = 4
    if y > 4:
        y = 4
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    player = [x, y]
    display.set_pixel(x, y, pl) 

#随机生成一个目标点并将目标点放进goalset
def setgoal():
    global panel
    goalindex = random.randint(0, 24)
    currentgoal = lst[goalindex]
    if (currentgoal not in goalset and currentgoal not in bombset
        and currentgoal != player):
        '''保证新加入的目标点和player，地雷不重合'''
        display.set_pixel(currentgoal[0], currentgoal[1], gl)
        goalset.append(currentgoal)
        panel[currentgoal[0]+1][currentgoal[1]+1] = 1
    else:
        setgoal()

#随机生成一个地雷并将地雷放进bombset
def setbomb(): 
    global bombset
    bomb = random.randint(0,24)
    while ((lst[bomb] in goalset) or (lst[bomb] in bombset) or
    (lst[bomb] == player)):
        '''保证新加入的地雷与先前的player，目标点都不重合'''    
        bomb = random.randint(0,24)
    bombset.append(lst[bomb])
    display.set_pixel(lst[bomb][0], lst[bomb][1], bl)

#地雷（怪物）追逐玩家
def bombmove():
    global bombTime, bombset, panel, num, interval, level
    currentTime = time.ticks_ms() #记录时间
    dir = [[1,0],[-1,0],[0,1],[0,-1]] #移动放下：上下左右
    if time.ticks_diff(currentTime, bombTime) >= interval[level]: #判断时间间隔
        for i in range(len(bombset)):
            order = random.choice(num) #随机设置移动顺序，处理bomb与goal重合的情况
            bomb = bombset[i] #选取一个bomb
            display.set_pixel(bomb[0], bomb[1], 0) #将上一轮的该bomb的亮度调0
            XorY = random.randint(0,1) #XorY=0在x方向移动；XorY=1在y方向移动
            xDst = player[0] - bomb[0] #判断与player在x方向的距离
            yDst = player[1] - bomb[1] #判断与player在y方向的距离
            if xDst == 0: #如果已经和player的x坐标值相同，就在y方向移动
                XorY = 1
            elif yDst == 0: #如果已经和player的y坐标值相同，就在x方向移动
                XorY = 0
            if XorY == 0 and xDst > 0: #在x方向移动
                if [bomb[0]+1, bomb[1]] in goalset: #如果移动后的位置和goal重合
                    for d in order: #order是随机生成的移动顺序
                        d = int(d) - 1
                        if panel[bomb[0]+dir[d][0]+1][bomb[1]+dir[d][1]+1] == 0: 
                            bomb = [bomb[0]+dir[d][0],bomb[1]+dir[d][1]]
                            break
                else:
                    bomb[0] += 1
            elif XorY == 0 and xDst < 0: #类比
                if [bomb[0]-1, bomb[1]] in goalset:
                    for d in order:
                        d = int(d) - 1
                        if panel[bomb[0]+dir[d][0]+1][bomb[1]+dir[d][1]+1] == 0:
                            bomb = [bomb[0]+dir[d][0],bomb[1]+dir[d][1]]
                            break
                else:
                    bomb[0] -= 1
            elif XorY == 1 and yDst > 0: #类比
                if [bomb[0], bomb[1]+1] in goalset:
                    for d in order:
                        d = int(d) - 1
                        if panel[bomb[0]+dir[d][0]+1][bomb[1]+dir[d][1]+1] == 0:
                            bomb = [bomb[0]+dir[d][0],bomb[1]+dir[d][1]]
                            break
                else:
                    bomb[1] += 1
            elif XorY == 1 and yDst < 0: #类比
                if [bomb[0], bomb[1]-1] in goalset:
                    for d in order:
                        d = int(d) - 1
                        if panel[bomb[0]+dir[d][0]+1][bomb[1]+dir[d][1]+1] == 0:
                            bomb = [bomb[0]+dir[d][0],bomb[1]+dir[d][1]]
                            break
                else:
                    bomb[1] -= 1
            print(bomb)
            display.set_pixel(bomb[0], bomb[1], bl)
            bombset[i] = bomb
            bombTime = time.ticks_ms()
            
#初始化设置
def initial():
    global goalset, panel
    panel = [[1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1]
        ]
    display.set_pixel(player[0], player[1], pl)
    i = 0
    while i < 3:
        '''初始时随机生成三个目标点'''
        index = random.randint(0, 24)
        if lst[index] not in goalset and lst[index] != player:
            '''保证三个目标点各不相同而且和player不重合'''
            goalset.append(lst[index])
            panel[lst[index][0]+1][lst[index][1]+1] = 1
            display.set_pixel(lst[index][0],lst[index][1],gl)
            i += 1

#当player与某一个目标点重合调用eat()
def eat():
    global goalset, player, points
    music.play(['C5:1']) #声音提示吃到目标点
    #print(player) #打印吃掉的点，在调试代码时帮助很大
    goalset.remove(player)
    panel[player[0]+1][player[1]+1] = 0
    points += 1

#当player与某一个地雷重合调用dead()
def dead():
    music.play(['D4:1']) #声音提示踩到地雷
    '''结束流程：显示骷髅头，speech嘲讽，滚动U r dead, 显示得分'''
    display.show(Image.SKULL)
    sleep(400)
    speech.say('ha, ha, You are Dead')
    display.scroll('U r dead', delay=80)
    display.scroll('Got')
    display.scroll(points)
    sleep(2000)
    display.clear()

#当得分超过30，本轮游戏胜利，调用win()
def win():
    music.play(music.PRELUDE, wait=False) #在悦耳的音乐中迎接胜利吧
    '''结束流程：显示笑脸，滚动U win，显示得分'''
    display.show(Image.HAPPY)
    sleep(2000)
    display.scroll('U win', delay=80) 
    display.scroll('Got')
    display.scroll(points)
    sleep(2000)
    display.clear()

#按pin_logo选择难度，调整bomb移动的时间间隔
#难度默认为最低=1，每按一次难度+1
def levelAdjust():
    global interval, level
    if pin_logo.is_touched():
        music.play(['E4:1'])
        level += 1
        if level > 4:
            level = 0
        display.show(level+1)

music.play(music.RINGTONE, wait=False) #欢迎音乐
display.show(Image.PACMAN)
sleep(500)
while Exit:   
    levelAdjust()
    if button_a.was_pressed():
        movecontrol()
        display.clear()
        bombset = []
        goalset = []
        points = 0
        initial()
        start = True
        Exit = False
        #setbomb() #此行供测试使用
    while start:
        movecontrol()
        bombmove()
        if button_b.was_pressed():
            #按button_b可以强制退出，显示已有得分
            display.scroll('Got')
            display.scroll(points)
            sleep(500)
            goalset = []
            bombset = []
            start = False
            Exit = True
            display.clear()
            display.show(Image.PACMAN)
            break
        if player in goalset: #吃到目标点
            eat()
            print(points)
        if player in bombset: #踩到地雷
            start = False
            dead()
            Exit = True
            display.show(Image.PACMAN)
            break
        if len(goalset) == 1: #如果吃掉了两个目标点，就更新goalset
            setgoal()
            setgoal()
        if points//8 - len(bombset): #每多吃掉8个目标点，增设一个地雷
            setbomb()
            bombTime = time.ticks_ms()
        if points == 30: #points达到30，成功通关
            win()
            Exit = True
            start = False
            display.show(Image.PACMAN)
            break