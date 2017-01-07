import pygame
import sys
import os
import math

pygame.init()
os.chdir("C:\\Users\\max\\Desktop\\pigwalk")

# create white screen
screen = pygame.display.set_mode((600, 600))
screen.fill((255, 255, 255))


# initial buttons


class Background(pygame.sprite.Sprite):
    def __init__(self, file, location):
        self.image = pygame.image.load(file)  # this is a surface
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


bgnd1 = Background("background1.png", (0, 0))

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


# circle=[targetingCircle(screen, (int(a[0] + a[2] / 2), int(a[1] + a[3] / 2)), a[2] / 2)]


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
        print(event)
        if event.type == pygame.QUIT:
            sys.exit()
    for i in range(len(px)):
        if math.sqrt((px[i] - x) ** 2 + (py[i] - y) ** 2) <= radius and start[i] == True:
            recs.remove(recs2[i])
            recs1.remove(recs3[i])
            start[i] = False


    # update background image
    screen.blit(bgnd1.image, bgnd1.rect)
    # draw blockers
    for rec in recs1:
        pygame.draw.rect(screen, (0, 0, 0), rec)
    # shrink circle

    for q in rp:
        drew2 = [drawCircle2(q, radius)]
    if radius > 4:
        radius -= 3
    else:
        radius = int(a[2] / 2)
    # update
    pygame.display.update()
    pygame.display.flip()
    pygame.time.wait(30)
    timer.tick(25)
