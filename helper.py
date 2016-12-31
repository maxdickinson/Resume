import pygame
import sys
import os
pygame.init()

screen = pygame.display.set_mode((800, 800))
screen.fill((255, 255, 255))

button = pygame.draw.rect(screen, (100, 100, 100), (580, 20, 40, 40))

def speed(ms):
    return pygame.time.wait(ms)

class TestSprite(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h,ms):
        os.chdir("C:\\Users\\max\\Desktop\\pigwalk")
        super().__init__()
        self.images = []
        self.images.append(pygame.image.load("pig1.png"))
        self.images.append(pygame.image.load("pig2.png"))
        self.images.append(pygame.image.load("pig3.png"))
        self.images.append(pygame.image.load("pig4.png"))
        self.index = 0
        self.length = 7
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x,y, w, h) #
        self.cover = pygame.Surface((w, h))
        self.cover.fill((255, 255, 255))
        self.ms=ms
    def update(self):
        '''This method iterates through the elements inside self.images and
        displays the next one each tick. For a slower animation, you may want to
        consider using a timer of some sort so it updates slower.'''
        self.index = self.index + 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.rect.x += 1
        speed(self.ms)

class TextBlock:
    def __init__(self,x,y,text,ms):
        self.fon = pygame.font.SysFont(None, 16)
        w,h = self.fon.size(text)
        self.rect = pygame.Rect(x,y,w,h)
        self.tex=self.fon.render(text,True,(255,0,255))
        self.cover = pygame.Surface((w,h))
        self.cover.fill((255,255,255))
        self.ms=ms
        self.text=text
    def update(self):
        self.rect = pygame.Rect(self.rect.left + 1, self.rect.top , self.rect.h,self.rect.w)
        speed(self.ms)

    def wraptext(self,x,y,speed,cutoff):
        textLis = self.text.split(" ")
        spaceLeft = cutoff
        cls = []
        line = []
        i = 0
        for word in textLis:
            #print(word)
            if self.fon.size(word)[0] + self.fon.size(" ")[0] > spaceLeft:
                cls.append(TextBlock(x, y + i * self.fon.size(word)[1], " ".join(line), speed))
                i += 1
                spaceLeft = cutoff - self.fon.size(word)[0]
                line = []
                line.append(word)

                if textLis.index(word) == len(textLis)-1:

                    cls.append(TextBlock(x, y + i * self.fon.size(word)[1], " ".join(line),speed))
            else:
                spaceLeft = spaceLeft - (self.fon.size(word)[0] + self.fon.size(" ")[0])
                line.append(word)
                if textLis.index(word) == len(textLis) - 1:
                    cls.append(TextBlock(x, y + i * self.fon.size(word)[1], " ".join(line),speed))
        return cls

def walkOn(screen,cls,my_group,c):
    for i in cls:
        screen.blit(i.cover, i.rect)
    screen.blit(c.cover, c.rect)
    # update
    # a.update()
    for i in cls:
        i.update()

    my_group.update()
    my_group.draw(screen)

    for i in cls:
        screen.blit(i.tex, i.rect)
    # draw
    pygame.display.update()
    pygame.display.flip()

def createText(x,y,text,speeed,cutoff):
    b=TextBlock(0,0,text,speeed)#not doing xy
    cls = b.wraptext(x,y, speeed,cutoff)
    return cls

#cls2 = b.wraptext(10,10, " this is also max",speeed)
def create(cls):

    #for i in cls:
        #screen.blit(i.tex,i.rect)
    d = TestSprite(-5,-5,0,0,0)
    w,h = d.image.get_rect().size
    c = TestSprite(cls[0].rect.left-w,cls[0].rect.top,w,h,speeed) # linking by width
    return c
class wrapText(TextBlock):
    def __init__(self,x,y,text):
        super().__init__(x,y,text)

speeed=1

cls=createText(0,0,""" Max Dickinson 503-956-3213 max.dickinson58@gmail.com Github: maxdickinson""", speeed , 100)
cls2 = createText(0,cls[-1].rect.bottom +5,"""Education University of Oregon (Sep. 2011 – Dec. 2016) Applied Physics and Math-Computer Science double major""", speeed , 200)
cls3 = createText(0,cls2[-1].rect.bottom +5,"""Technical skills: Python, R, Javascript, Matlab C, C++ SQL Git Microsoft Office Suite""", speeed , 200)
cls4 = createText(0,cls3[-1].rect.bottom +5,"""Work experience Math Research Assistant (April 2016 – June 2016) Developed a pipeline in R to analyze mixed data and explored different R packages related to clustering and visualization for inter-university NSF project about clustering with applications for mental health. Use multiple packages to cluster and visualize data""", speeed , 200)
cls5 = createText(0,cls4[-1].rect.bottom +5,"""Tutor (July 2015 – December 2016) Taught math and physics of all levels to over 50 high school and college students.""", speeed , 200)
cls6 = createText(0,cls5[-1].rect.bottom +5,"""Paper Marker, University of Oregon Mathematics Department (July 2014 – July 2016) Graded papers for calculus, differential equations, elementary linear algebra, and discrete dynamical systems. Communicated progres and results with professors""", speeed , 200)
cls7 = createText(0,cls6[-1].rect.bottom +5,"""Biophysics Research Assistant (April 2013 – May 2013)Used an optical trap to pull pieces of a cell membrane which was collected and analyzed in Matlab. """, speeed , 200)
cls8 = createText(0,cls7[-1].rect.bottom +5,"""Physics Research Assistant (June 2012 – Nov. 2013) Built a scanning wavelength program to tune lab equipment """, speeed , 200)
cls9 = createText(0,cls8[-1].rect.bottom +5,"""Mission: Citizen board member (Sep. 2010 – Sep. 2012) Founding member of a 501c3 nonprofit. Developed and taught civics courses to first generation US immigrants Helped over 10 people pass the citizenship test. """, speeed , 200)

clsss = [cls,cls2,cls3,cls4,cls5,cls6,cls7,cls8,cls9]

creates= list(map(create,clsss))

groups = list(map(pygame.sprite.Group , creates))

#for i in groups:
   # print(i)
  #  i.update()
   # i.draw(screen)

#update
pygame.display.update()
pygame.display.flip()

first = 0
second = 0
third = 0
fourth = 0
fifth  =0
sixth = 0
seventh = 0
eigth = 0
ninth = 0

clickcounter=0
while True:
    #erase
   # screen.blit(a.cover,a.rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.BUTTON_X1:

            clickcounter +=1
        elif event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(pygame.mouse.get_pos()) and first ==0:
            first = 1

            while creates[0].rect.right < screen.get_rect().width/2:
                walkOn(screen,clsss[0],groups[0],creates[0])
        elif event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(pygame.mouse.get_pos()) and clickcounter >10 and first  == 1 and second == 0  :
            second =1
            while creates[1].rect.right < screen.get_rect().width / 2:
                walkOn(screen, clsss[1], groups[1], creates[1])
        elif event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(pygame.mouse.get_pos()) and clickcounter >10 and second  == 1 and third == 0:
            print("ran")
            third = 1
            while creates[2].rect.right < screen.get_rect().width / 2:
                walkOn(screen, clsss[2], groups[2], creates[2])
        elif event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(pygame.mouse.get_pos()) and clickcounter >10 and second  == 1 and third == 0:
            print("ran")
            third = 1
            while creates[2].rect.right < screen.get_rect().width / 2:
                walkOn(screen, clsss[2], groups[2], creates[2])
