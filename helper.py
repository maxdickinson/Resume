import pygame
import sys
import os
import math
import copy
pygame.init()
os.chdir("C:\\Users\\max\\Desktop\\pigwalk")

# create white screen
screen = pygame.display.set_mode((600, 600))
screen.fill((255, 255, 255))

from colour import Color
red = Color("black")
colors = list(red.range_to(Color("red"),10))


# initial buttons

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
screen.blit(bgnd1.image, bgnd1.rect)

# 4 RECTANGLES COVERING SCREEN EVENLY

a = (0, 0, screen.get_width() / 2, screen.get_height() / 2)
b = (screen.get_width() / 2, 0, screen.get_width() / 2, screen.get_height() / 2)
c = (0, screen.get_height() / 2, screen.get_width() / 2, screen.get_height() / 2)
d = (screen.get_width() / 2, screen.get_height() / 2, screen.get_width() / 2, screen.get_height() / 2)
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
    print(circle)
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
curr = bgnd1
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
while True:
    x, y = pygame.mouse.get_pos()

    # erase
    # screen.blit(a.cover,a.rect)
    recs1 = list(map(pygame.Rect, recs))
    rp = list(map(radpos, recs))

    for event in pygame.event.get():
        # print(circle[0].collidepoint(pygame.mouse.get_pos()))
        # print(gc.clickcounter
        # print(event.type)

        if event.type == pygame.QUIT:
            sys.exit()
        elif start[0:4] == [False]*4 and nextBut.rect.collidepoint(pygame.mouse.get_pos()) and (event.type == pygame.MOUSEBUTTONDOWN):

            start = [True] * 4
            curr = bgnd2
            recs = [a, b, c, d]
            bl = [q ,r ,s ,t]
            recs1 = [a, b, c, d]
        elif event.type == pygame.MOUSEBUTTONDOWN and curr == bgnd2 and index < 4 :
            bl2[index].colr +=1
            if bl2[index].colr == len(colors):
                cols[index] = True
                bl2[index].colr =len(colors)-1
                index +=1
            #makes the other box change colors first
    if curr == bgnd1:
        for i in range(len(px)):

            if math.sqrt((px[i] - x) ** 2 + (py[i] - y) ** 2) <= radius and start[i] ==True :
                recs.remove(recs2[i])
                recs1.remove(recs3[i])
                print(bl)
                print(bl2[i])
                bl.remove(bl2[i])
                start[i] = False
                #start[i::] == [True] * (4 - i) and start[0:i] == [False] * i
    elif curr == bgnd2:


        if math.sqrt((px[index2] - x) ** 2 + (py[index2] - y) ** 2) <= radius and cols[index2] == True and start[i] == True and index2<4:
            recs.remove(recs2[index2])
            recs1.remove(recs3[index2])
            bl.remove(bl2[index2])
            start[index2] = False
            if index2==3:
                index2 = 3
            else:
                index2+=1


    # circle=[targetingCircle(screen, (int(a[0] + a[2] / 2), int(a[1] + a[3] / 2)), a[2] / 2)]

    # update background image
    screen.blit(curr.image, curr.rect)
    if len(recs) == 0:
        nextBut = createText(300, 300, "Next", 200)
        screen.blit(nextBut.tex,nextBut.rect)

    # draw blockers
    color = (0, 0, 0)

    for rec in bl:

        pygame.draw.rect(screen, (colors[rec.colr].rgb[0]*255 , colors[rec.colr].rgb[1]*255 , colors[rec.colr].rgb[2]*255), rec.coord)
    # shrink circle

    for oo in rp:
        drew2 = [drawCircle2(oo, radius)]
    if radius > 4:
        radius -= 3
    else:
        radius = int(a[2] / 2)
    # update
    pygame.display.update()
    pygame.display.flip()
    pygame.time.wait(30)
    timer.tick(25)
