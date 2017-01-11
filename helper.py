import pygame
import sys
import os
import math
#import numpy
import copy
import random
pygame.init()
os.chdir("C:\\Users\\max\\Desktop\\pigwalk")

# create white screen
screen = pygame.display.set_mode((620, 600))
screen.fill((255, 255, 255))

screen1 = pygame.Rect(0,0,600,600)

from colour import Color
red = Color("black")
colors = list(red.range_to(Color("red"),10))

wh = (255,255,255)
b = (0,0,0)
# initial buttons
class spriteSheet(pygame.sprite.Sprite):
    wh = (255, 255, 255)
    def __init__(self,file,x,y,frameWidth,frameHeight,startFrame,endFrame):
        wh = (255, 255, 255)
        os.chdir("C:\\Users\\max\\Desktop\\pigwalk")

        self.rect = pygame.Rect(x,y,frameWidth,frameHeight)
        self.sheet = pygame.image.load(file).convert_alpha()
        self.sheet.set_colorkey(wh)
         #alpha channel already exists
        #self.sheet.set_alpha(255)

        self.originx = x
        self.originy = y
        w, h = self.sheet.get_rect().size
        self.images = []

        self.framesOnRow = w//self.rect.w
        self.framesOnCol = h // self.rect.h
        self.sequence = [i for i in range(startFrame, endFrame)]
        self.counter = 0
        self.currentFrame = 0



        while self.currentFrame < len(self.sequence):
            row = self.sequence[self.currentFrame] // self.framesOnRow
            col = self.sequence[self.currentFrame] % self.framesOnRow
            self.row = row
            self.col = col
            self.images.append(self.sheet.subsurface(col * frameWidth, row * frameHeight, frameWidth, frameHeight))
            self.currentFrame += 1
        self.currentFrame = 0
        self.image= self.images[self.currentFrame]

        self.image = self.image.convert_alpha()
        #self.image = self.image.convert_alpha()
        #self.image.set_alpha(0)
        self.image.set_colorkey(wh)

        self.cover = pygame.Surface((self.image.get_rect().size))
        #self.cover.set_colorkey(wh)
        self.cover.fill((255, 255, 255))
    def speed(self):
        #wrapper
        return pygame.time.wait(self.ms)
    def update(self,speed):
        if self.counter == speed:

            self.currentFrame = (self.currentFrame + 1) % len(self.sequence)
            #print(self.currentFrame)
        self.counter += 1
        if self.counter > speed:
            self.counter = 0
        self.image = self.images[self.currentFrame]


        self.image = self.image.convert_alpha()

        self.image.set_colorkey((wh))
    def draw(self,screen):


        screen.blit(self.image,(self.rect.x,self.rect.y))
    def moveUp(self,screen):
        #takes care of erasing as well
        screen.blit(self.cover, self.rect)
        self.rect.y += 2
    def moveDown(self,screen):

        #screen.blit(self.cover, self.rect)
        self.rect.y -= 30
    def reset(self,screen):
        screen.blit(self.cover, self.rect)
        #self.rect.x = self.originx
        #self.rect.y= self.originy
frameHeight = 150
ladArray = [i for i in range(screen.get_height() // frameHeight)]
ladders =[]
for i in ladArray:
    ladders.append(spriteSheet("ladder.png",600,i*frameHeight,20,150,0,1))
climber = spriteSheet("climber.png",600,560,19,32,0,2)
#print(climber.image.get_alpha())


vineBlocks = []
frameHeight = 20
ladArray = [i for i in range(screen.get_height() // frameHeight)]

for i in ladArray[0:19]:
    vineBlocks.append(spriteSheet("vine_bricks.png",600,i*frameHeight,20,20,i,i+1))
for j in ladArray[0:19]:
    #print(j)
    vineBlocks.append(spriteSheet("vine_bricks.png", 600, (i+j) * frameHeight, 20, 20, j, j + 1))

#green bricks has (84,103), want to fill up screen1.w / 2, screen1.h / 2 place at a[0:2]
gb = spriteSheet("green_bricks.png",0,0,100,80,0,1)

#print((screen1.w / 2) // 100)
#print((screen1.h / 2) //80)


def tileScreen(file,x,y,ww,hh,frameHeight,frameWidth):
    #must have one dimension of screen evenylly divide into frame dimension
    gb = []
    for i in range(int(ww // frameWidth)):
        for j in range(int(hh //frameHeight)):


            gb.append(spriteSheet(file, x+frameWidth*i, y+frameHeight*j, frameWidth, frameHeight, 0, 1))
            if j == int((hh) //frameHeight)-1 and (hh-frameHeight* int((hh) // frameHeight)) > 0:
                gb.append(spriteSheet(file, x+frameWidth*i, y+frameHeight*int((hh) //frameHeight), frameWidth, hh-frameHeight*int((hh) //frameHeight), 0, 1))
            if i == int((ww) // frameWidth) - 1 and (ww-frameWidth* int((ww) // frameWidth)) > 0:
                #print(j)
                gb.append(spriteSheet(file, x+frameWidth * int((ww) // frameWidth), y+frameHeight * j, ww-frameWidth* int((ww) // frameWidth), frameHeight , 0, 1))
    return gb
ww = screen1.w / 2
hh =screen1.h / 2
frameHeight = 80
frameWidth = 100
gb = tileScreen("green_bricks.png",0,0,ww,hh,frameHeight,frameWidth)

sandBrick = tileScreen("sand_brick.png",0,300,ww,hh,50,150)
#strange bug that brick rects are added to this list
sandBrick=sandBrick[0::]
castleBrick = tileScreen('castle_bricks.png' , 300,0,ww,hh,42,75)

longBrick = tileScreen('long_bricks.png' , 300,300,ww,hh,40,100)


gb2 = tileScreen("green_bricks.png",0,0,ww,hh,frameHeight,frameWidth)

sandBrick2 = tileScreen("sand_brick.png",0,300,ww,hh,50,150)
#strange bug that brick rects are added to this list
sandBrick2=sandBrick2[0::]
castleBrick2 = tileScreen('castle_bricks.png' , 300,0,ww,hh,42,75)

longBrick2 = tileScreen('long_bricks.png' , 300,300,ww,hh,40,100)

class TextBlock:
    #make a text block that can move, not wrapped yet
    # doesnt do the blit just the creation
    def __init__(self,x,y,text):
        self.fon = pygame.font.SysFont(None, 16)
        #w,h = self.fon.size(text)
        w,h = 40,40
        self.rect = pygame.Rect(x,y,w,h)

        self.tex=self.fon.render(text,True,(0,0,255))
        #create eraser
        self.cover = pygame.Surface((w,h))
        self.cover.fill((5,255,255))

    def update(self):
        self.rect = pygame.Rect(self.rect.left + 1, self.rect.top , self.rect.h,self.rect.w)



def createText(x,y,text,cutoff):
    #make the text blocks

    b=TextBlock(x,y,text)#not doing xy
    pygame.draw.rect(screen, (0, 0, 0), b.rect)
    return b

class Background(pygame.sprite.Sprite):
    def __init__(self, file, location):
        self.image = pygame.image.load(file)  # this is a surface
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


bgnd1 = Background("background1.png", (0, 0))
bgnd2 = Background("background2.png", (0, 0))
bgnd3 = Background("back3.png", (0, 0))
bgnd4 = Background("back4.png", (0, 0))
bgnd5 = Background("back5.png", (0, 0))

screen.blit(bgnd1.image, bgnd1.rect)

# 4 RECTANGLES COVERING SCREEN EVENLY

a = (0, 0, screen1.w / 2, screen1.h / 2)
b = (screen1.w / 2, 0, screen1.w / 2, screen1.h / 2)
c = (0, screen1.h / 2, screen1.w / 2, screen1.h / 2)
d = (screen1.w / 2, screen1.h / 2, screen1.w / 2, screen1.h / 2)




recs = [a, b, c, d]
recs1 = list(map(pygame.Rect, recs))
recs3 = list(map(pygame.Rect, recs))
# put targeting circles in center of 4 squares
recs2 = [a, b, c, d]

start = [True] * 4
repeat = True
cols =  [False] * 4


def radpos(a):
    radius = int(a[2] / 2)
    pos = (int(a[0] + a[2] / 2), int(a[1] + a[3] / 2))
    return (radius, pos)


rp = list(map(radpos, recs2))

timer = pygame.time.Clock()


def drawCircle(rp):
    radius = rp[0]
    pos = rp[1]
    circle = pygame.draw.circle(screen, (0, 255, 0), pos, radius, 1)
    #print(circle)
    return circle


drew = list(map(drawCircle, rp))


def drawCircle2(rp, i):
    radius = i
    pos = rp[1]
    circle = pygame.draw.circle(screen, (0, 255, 0), pos, radius, 1)
    return circle

px = []
py = []
p_x, p_y = rp[0][1]
for p in rp:
    px.append(p[1][0])
    py.append(p[1][1])


radius = int(a[2] / 2)
nextBut = createText(300, 300, "Next", 200)
curr = bgnd5
colr = 0

class block:
    def __init__(self,colorin,coord):
        self.colr =colorin
        self.coord = coord
q = block(0,a)
r = block(0,b)
s = block(0,c)
t =  block(0 , d)
bl = [q,r,s,t]
bl2 =[q,r,s,t]
index = 0
index2 = 0
events = []
unrun = True
pxx = []
pxy = []
recbri = [gb[0].rect, sandBrick[0].rect, castleBrick[0].rect, longBrick[0].rect]
recbri2 = [gb[0].rect, sandBrick[0].rect, castleBrick[0].rect, longBrick[0].rect]
#recbri=[]
#recbri2 = []



class circleActor(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.pos = (300,300)
        self.radius = 50
        self.speed = random.randint(0, 1)
        self.i_hat = random.randint(-4, 4)
        self.j_hat = random.randint(-4, 4)

        self.rect = pygame.draw.circle(screen, (255, 255, 0), self.pos, self.radius, 1)
        self.personality = random.randint(1, 3)
        #self.personality = 1

        if self.j_hat == 0:
            self.j_hat = 0.1
        print("ran")
        self.threshold_v = 1
    def personalityCheck(self,position,v,a):

        if self.personality == 1:


            if abs(position[0] - self.rect.centerx) < 60 and abs (position[1] - self.rect.centery) < 60 and abs(position[0] - self.rect.centerx) >5 and abs (position[1] - self.rect.centery) > 5:
                #approach fast and precise
                if self.threshold_v > v:
                    x1 = self.pos[0]
                    x2 = position[0]
                    y1 = self.pos[1]
                    y2 = position[1]
                    my =(y2-y1)
                    mx = (x2-x1)
                    self.pos = (x1 - mx//1, y1 - my//1)
                    print("run2")
                    #self.draw()

        elif self.personality == 2:
            x1 = self.pos[0]

            y1 = self.pos[1]

            self.pos = (x1 , y1 )

            if abs(position[0] - self.rect.centerx) < 500 and abs (position[1] - self.rect.centery) < 500:
               #slow and wide, scatter??
                if self.threshold_v < v:
                    x1 = self.pos[0]
                    x2 = position[0]
                    y1 = self.pos[1]
                    y2 = position[1]
                    my =(y2-y1)
                    mx = (x2-x1)
                    self.pos = (x1 - mx//19, y1 - my//19)
                    print("run2")
                    #self.draw()
        elif self.personality == 3:
            #teleport to left
            if abs(position[0] - self.rect.centerx) < 10 and abs(position[1] - self.rect.centery) < 10:
                x1 = self.pos[0]
                x2 = position[0]
                y1 = self.pos[1]
                y2 = position[1]
                my = (y2 - y1)
                mx = (x2 - x1)
                self.pos = (0, y1 - my*10)
                print("run2")
                # self.draw()
                # dont touch center
    def draw(self):
        self.rect = pygame.draw.circle(screen, (255, 255, 0), self.pos, self.radius, 1)
    def update(self):
        if self.radius > 4:
            self.radius -= 3
        else:
            self.radius = int(a[2] / 2)
    def moveUp(self):
        amount = self.j_hat
        amount = abs(amount)
        self.pos =  (int(self.pos[0]),int(self.pos[1]-amount))

    def moveDown(self):
        amount = self.j_hat
        amount = abs(amount)

        self.pos = (int(self.pos[0]),int(self.pos[1]+amount))
    def moveLeft(self):
        amount = self.i_hat
        amount = abs(amount)
        self.pos =  (self.pos[0] -amount ,self.pos[1])
    def moveRight(self):
        amount = self.i_hat
        amount = abs(amount)
        self.pos = (int(self.pos[0]+amount),int(self.pos[1]))
        '''upRight
        upLeft
        downRight
        downLeft
    '''
    def updatePos(self):
        for i in range(self.speed):
            if self.i_hat <= 0 and self.j_hat <0:
                self.moveDown()
                self.moveLeft()
            elif self.i_hat <= 0 and self.j_hat > 0:
                self.moveUp()
                self.moveLeft()
            elif self.i_hat >= 0 and self.j_hat < 0:
                self.moveDown()
                self.moveRight()
            elif self.i_hat >= 0 and self.j_hat > 0:
                self.moveUp()
                self.moveRight()


eee = circleActor(300 ,300)
unrun2 = False
rp = list(map(radpos, recs))
circles2 = [circleActor(i[1][0], i[1][1]) for i in rp]
circles2i = [circleActor(i[1][0], i[1][1]) for i in rp]
circles4=[]
circles5 = []
#[print(circles2[i].pos) for i in range(len(circles2))]
popper = 0
draw = [i for i in range(len(circles2))]
#print(circles2i)
curr= bgnd5
E_col_cir = pygame.USEREVENT  + 1
pygame.time.set_timer(E_col_cir, 5000)

xxxx = random.randint(0, screen1.w)
yyyy = random.randint(0, screen1.h)

circles5.append(circleActor(xxxx, yyyy))

buf = []
vels = []
acc = []
import math
while True:
    print(timer.get_time())

    (x, y) = pygame.mouse.get_pos()
    if len(buf) < 3:
        buf.append((x,y))
    elif len(buf) == 3:
        buf.pop(0)
        buf.append((x,y))
    position = buf[-1]
    if len(buf) == 3:
        velocity = math.sqrt( (buf[1][1] - buf[0][1])**2 + (buf[1][0] - buf[0][0])**2 ) / timer.get_time() # (y2-y1 )**2+ (x2 -x1)**2 dist / time
        if len(vels) < 2:
            vels.append((velocity))
        elif len(vels) == 2:
            vels.pop(0)
            vels.append(velocity)
    if len(vels) ==2:
        acceleration = (vels[1] - vels[0]) / timer.get_time()                           # pixels per frame
        if len(acc) < 1:
            acc.append((velocity))
        elif len(vels) == 2:
            acc.pop(0)
            acc.append(acceleration)
    print(timer.get_time())
    print(buf,vels,acc)
    # erase
    # screen.blit(a.cover,a.rect)
    recs1 = list(map(pygame.Rect, recs))

    for event in pygame.event.get():
        # print(circle[0].collidepoint(pygame.mouse.get_pos()))
        # print(gc.clickcounter
        # print(event.type)

        if event.type == pygame.QUIT:
            sys.exit()
        elif start[0:4] == [False]*4 and nextBut.rect.collidepoint(pygame.mouse.get_pos()) and (event.type == pygame.MOUSEBUTTONDOWN) and curr == bgnd1:

            start = [True] * 4
            curr = bgnd2
            recs = [a, b, c, d]
            bl = [q ,r ,s ,t]
            recs1 = [a, b, c, d]
        elif event.type == pygame.MOUSEBUTTONDOWN and curr == bgnd2 and index < 4 :
            bl2[index].colr +=5
            if bl2[index].colr == len(colors):
                cols[index] = True
                bl2[index].colr =len(colors)-1
                index +=1
            #makes the other box change colors first
        elif start[0:4] == [False]*4 and nextBut.rect.collidepoint(pygame.mouse.get_pos()) and (event.type == pygame.MOUSEBUTTONDOWN) and curr == bgnd2:
           # print('ran')
            for i in range(len(bl2)):
                bl2[i].colr = 0
            start = [True,True,True,True]
            curr = bgnd3
            recs = [a, b, c, d]
            bl = [q ,r ,s ,t]
            recs1 = [a, b, c, d]
            index2=0
        elif start[0:4] == [False]*4 and nextBut.rect.collidepoint(pygame.mouse.get_pos()) and (event.type == pygame.MOUSEBUTTONDOWN) and curr == bgnd3:
            #print('ran')
            for i in range(len(bl2)):
                bl2[i].colr = 0
            start = [True,True,True,True]
            curr = bgnd4
            recs = [a, b, c, d]
            bl = [q ,r ,s ,t]
            recs1 = [a, b, c, d]
            index2=0
            gb = tileScreen("green_bricks.png", 0, 0, ww, hh, frameHeight, frameWidth)

            sandBrick = tileScreen("sand_brick.png", 0, 300, ww, hh, 50, 150)
            # strange bug that brick rects are added to this list
            sandBrick = sandBrick[0::]
            castleBrick = tileScreen('castle_bricks.png', 300, 0, ww, hh, 42, 75)

            longBrick = tileScreen('long_bricks.png', 300, 300, ww, hh, 40, 100)
        elif nextBut.rect.collidepoint(pygame.mouse.get_pos()) and (event.type == pygame.MOUSEBUTTONDOWN) and curr == bgnd4:
           # print('ran')
            for i in range(len(bl2)):
                bl2[i].colr = 0
            start = [True, True, True, True]
            curr = bgnd5
            recs = [a, b, c, d]
            bl = [q, r, s, t]
            recs1 = [a, b, c, d]
            index2 = 0
            gb = tileScreen("green_bricks.png", 0, 0, ww, hh, frameHeight, frameWidth)

            sandBrick = tileScreen("sand_brick.png", 0, 300, ww, hh, 50, 150)
            # strange bug that brick rects are added to this list
            sandBrick = sandBrick[0::]
            castleBrick = tileScreen('castle_bricks.png', 300, 0, ww, hh, 42, 75)

            longBrick = tileScreen('long_bricks.png', 300, 300, ww, hh, 40, 100)
        elif event.type == E_col_cir and curr ==bgnd4:
            xxx = random.randint(0, screen1.w)
            yyy = random.randint(0, screen1.h)
            if len(circles4) > 0:
                circles4.pop(0)
            circles4.append(circleActor(xxx, yyy))
        elif math.sqrt((circles5[0].pos[0] - x) ** 2 + (circles5[0].pos[1] - y) ** 2) <= circles5[0].radius and (event.type == pygame.MOUSEBUTTONDOWN) and curr == bgnd5:
            events.append("climbdown")
            xxxx = random.randint(0, screen1.w)
            yyyy = random.randint(0, screen1.h)
            circles5.pop(0)
            circles5.append(circleActor(xxxx, yyyy))
            rand1 = random.randint(0, 3)
            if rand1 == 0 and len(gb) > 0:
                rand = random.randint(0, len(gb) - 1)
                gb.pop(rand)
            elif rand1 == 1 and len(sandBrick) > 0:
                rand = random.randint(0, len(sandBrick) - 1)
                sandBrick.pop(rand)
            elif rand1 == 2 and len(castleBrick) > 0:
                rand = random.randint(0, len(castleBrick) - 1)
                castleBrick.pop(rand)
            elif rand1 == 3 and len(longBrick) > 0:
                rand = random.randint(0, len(longBrick) - 1)
                longBrick.pop(rand)

    [gb2[i].reset(screen) for i in range(len(gb2))]
    [sandBrick2[i].reset(screen) for i in range(len(sandBrick2))]
    [castleBrick2[i].reset(screen) for i in range(len(castleBrick2))]
    [longBrick2[i].reset(screen) for i in range(len(longBrick2))]


    screen.blit(curr.image, curr.rect)

    # shrink circle
    #curr = bgnd3

    if curr == bgnd1:

        if unrun2 == True:
            #circles2i.pop(popper)
            #circles2 = [circleActor(i[1][0], i[1][1]) for i in rp]
            #circles2i = [circleActor(i[1][0], i[1][1]) for i in rp]
            unrun2 = False

        for i in range(len(circles2)):

            if math.sqrt((circles2[i].pos[0] - x) ** 2 + (circles2[i].pos[1] - y) ** 2) <= circles2[i].radius and start[i] ==True :
                events.append("climbdown")
                draw.remove(i)
                #popper = i
                recs.remove(recs2[i])
                recs1.remove(recs3[i])
               # print(bl)
                #print(bl2[i])
                bl.remove(bl2[i])
                start[i] = False
                unrun2 = True
                #start[i::] == [True] * (4 - i) and start[0:i] == [False] * i
    elif curr == bgnd2:
        if unrun2 == True:
            circles2 = [circleActor(i[1][0], i[1][1]) for i in rp]
            unrun2 = False

        if math.sqrt((px[index2] - x) ** 2 + (py[index2] - y) ** 2) <= radius and cols[index2] == True and start[index2] == True and index2<4:
            events.append("climbdown")


            recs.remove(recs2[index2])
            recs1.remove(recs3[index2])
            bl.remove(bl2[index2])
            start[index2] = False
            if index2==3:
                index2 = 3
            else:
                index2+=1
    # update background image

    elif curr == bgnd3:

        if len(recbri) ==0:
            if len(gb) > 0:
                recbri.append(gb[0].rect)
            if len(sandBrick) > 0:
                recbri.append(sandBrick[0].rect)
            if len(castleBrick) > 0:
                recbri.append(castleBrick[0].rect)
            if len(longBrick) > 0:
                recbri.append(longBrick[0].rect)
            unrun = True
        rpp = list(map(radpos, recbri))

        if unrun == True:
            circles = [circleActor(i[1][0], i[1][1]) for i in rpp]

            pxx=[]
            pxy=[]
            for p in rpp:
                pxx.append(p[1][0])
                pxy.append(p[1][1])
            unrun = False
            recbri2 = copy.deepcopy(recbri)
            start = [True, True, True, True]
            #alter recbri and recbri 2
        #start = [True] * len(pxx)
        for i in range(len(pxx)):
           # print(pxx[i], pxy[i] , i,radius )
            #print(start[i])
            if math.sqrt((pxx[i] - x) ** 2 + (pxy[i] - y) ** 2) <= radius and start[i] == True:
                #print(i)
                events.append("climbdown")
            #recbri.remove(recbri2[index2])
                recbri.remove(recbri2[i])
                w = recbri2[i]
                try : gb.remove(w)
                except : ValueError
                try:
                    sandBrick.remove(w)
                except:
                    ValueError
                try:
                    castleBrick.remove(w)
                except:
                    ValueError
                try:
                    longBrick.remove(w)
                except:
                    ValueError

            #recs.remove(recs2[index2])
            #recs1.remove(recs3[index2])
            #bl.remove(bl2[index2])
                start[i] = False

    elif curr == bgnd4:


        for i in range(len(circles4)):

            if math.sqrt((circles4[i].pos[0] - x) ** 2 + (circles4[i].pos[1] - y) ** 2) <= circles4[i].radius and start[i] == True:
                events.append("climbdown")
                rand1 = random.randint(0,3)
                if rand1 == 0 and len(gb) > 0:
                    rand = random.randint(0, len(gb)-1)
                    gb.pop(rand)
                elif rand1 == 1 and len(sandBrick) > 0:
                    rand = random.randint(0, len(sandBrick)-1)
                    sandBrick.pop(rand)
                elif rand1 == 2 and len(castleBrick) > 0:
                    rand = random.randint(0, len(castleBrick)-1)
                    castleBrick.pop(rand)
                elif rand1 == 3 and len(longBrick) > 0:
                    rand = random.randint(0, len(longBrick)-1)
                    longBrick.pop(rand)
    elif curr == bgnd5:
        if len(buf) != 0 and len(vels) != 0 and len(acc) != 0 and len(circles5)>0:
            print("run3")
            circles5[0].personalityCheck(buf[0],vels[0],acc[0])
        if circles5[0].pos[0] > screen1.w:
            circles5[0].pos = (screen1.w - circles5[0].radius, circles5[0].pos[1])
        if circles5[0].pos[0] < 0:
            circles5[0].pos = (circles5[0].radius, circles5[0].pos[1])
        if circles5[0].pos[1] > screen1.h:
            circles5[0].pos = (circles5[0].pos[0], screen1.h - circles5[0].radius)
        if circles5[0].pos[1] < 0:
            circles5[0].pos = (circles5[0].pos[0], circles5[0].radius)


        '''    if circles5[0].pos[0] > screen1.w:
            circles5[0].pos = (screen1.w-circles5[0].radius,circles5[0].radius)
        if circles5[0].pos[0] < 0:
            circles5[0].pos = (screen1.w, circles5[0].pos[1])
        if circles5[0].pos[1] > screen1.h:
            circles5[0].pos = ( circles5[0].pos[0], 0)
        if circles5[0].pos[1] < 0:
            circles5[0].pos = (circles5[0].pos[0], screen1.h)
            '''
        # wall checks stop at wall


                #radius and angle and create movement lists


    # circle=[targetingCircle(screen, (int(a[0] + a[2] / 2), int(a[1] + a[3] / 2)), a[2] / 2)]


    if len(recs) == 0:
        nextBut = createText(300, 300, "Next", 200)
        screen.blit(nextBut.tex,nextBut.rect)
    if len(gb) == 0 and len(sandBrick) ==0 and len(castleBrick) ==0 and len(longBrick) ==0:
        nextBut = createText(300, 300, "Next", 200)
        screen.blit(nextBut.tex,nextBut.rect)
    # draw blockers
    color = (0, 0, 0)
    if curr == bgnd1 or curr == bgnd2:
        for rec in bl:
            pygame.draw.rect(screen, (colors[rec.colr].rgb[0]*255 , colors[rec.colr].rgb[1]*255 , colors[rec.colr].rgb[2]*255), rec.coord)
        # shrink circle
        #rp2 = list(map(radpos, circles2))
        for oo in rp:
            drew2 = [drawCircle2(oo, radius)]
        if radius > 4:
            radius -= 3
        else:
            radius = int(a[2] / 2)

        [circles2[i].draw() for i in draw]
        [circles2[i].update() for i in range(len(circles2i))]
    elif curr == bgnd3:
        #print(len(gb))
        #print(len(sandBrick))
        #screen.blit(curr.image, curr.rect) doesnt work because surface on surface??
        #gb2 = copy.deepcopy(gb)


        [gb[i].draw(screen) for i in range(len(gb))]

        [sandBrick[i].draw(screen) for i in range(len(sandBrick))]

        [castleBrick[i].draw(screen) for i in range(len(castleBrick))]

        [longBrick[i].draw(screen) for i in range(len(longBrick))]
        for oo in rpp:

            drew2 = [drawCircle2(oo, radius)]
        [circles[i].draw() for i in  range(len(circles))]
        [circles[i].update() for i in  range(len(circles))]
        if radius > 4:
            radius -= 3
        else:
            radius = int(a[2] / 4)

    elif curr == bgnd4:
        [gb[i].draw(screen) for i in range(len(gb))]

        [sandBrick[i].draw(screen) for i in range(len(sandBrick))]

        [castleBrick[i].draw(screen) for i in range(len(castleBrick))]

        [longBrick[i].draw(screen) for i in range(len(longBrick))]


        [circles4[i].draw() for i in range(len(circles4))]
    elif curr == bgnd5:
        [gb[i].draw(screen) for i in range(len(gb))]

        [sandBrick[i].draw(screen) for i in range(len(sandBrick))]

        [castleBrick[i].draw(screen) for i in range(len(castleBrick))]

        [longBrick[i].draw(screen) for i in range(len(longBrick))]


        circles5[0].updatePos()
        circles5[0].draw()
        [circles5[i].draw() for i in range(len(circles5))]

    [vineBlocks[i].draw(screen) for i in range(len(vineBlocks))]

    [ladders[i].draw(screen) for i in range(len(ladders))]




    if len(events) > 0:
        #print(events)
        if events.pop() == "climbdown":
            climber.update(0)
            #if climber.currentFrame > len(climber.sequence):
                #climber.currentFrame = 0
            climber.moveDown(screen)
            climber.draw(screen)
            pygame.display.update()
            pygame.display.flip()
            #pygame.time.wait(500)
        if climber.rect.y < 0:
            climber.rect.y = screen1.h
    climber.draw(screen)

    # update
    pygame.display.update()
    pygame.display.flip()
    #pygame.time.wait(30)
    timer.tick(25) #wait 25 frames in the milllisecond. gives 1000/40 = 25
