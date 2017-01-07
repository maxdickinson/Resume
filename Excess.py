class Utility:
    #smorgasboard of assisting functions
    def __init__(self):
        #set the number of ms to wait as a delay
        #controls the animatin speed, not the walk speed
        self.ms = 1
        self.movement_speed = 1
    def speed(self):
        #wrapper
        return pygame.time.wait(self.ms)
    def wraptext(self,x,y,text,cutoff):
        #implements minimum cost algorithm to wrap text,
        # must set the paragraph length,
        #arranges the text in seperate rectangles, and puts in list
        textLis = text.split(" ")
        spaceLeft = cutoff
        cls = []
        line = []
        i = 0
        for word in textLis:
            #print(word)
            if self.fon.size(word)[0] + self.fon.size(" ")[0] > spaceLeft:
                cls.append(TextBlock(x, y + i * self.fon.size(word)[1], " ".join(line),))
                i += 1
                spaceLeft = cutoff - self.fon.size(word)[0]
                line = []
                line.append(word)

                if textLis.index(word) == len(textLis)-1:

                    cls.append(TextBlock(x, y + i * self.fon.size(word)[1], " ".join(line),))
            else:
                spaceLeft = spaceLeft - (self.fon.size(word)[0] + self.fon.size(" ")[0])
                line.append(word)
                if textLis.index(word) == len(textLis) - 1:
                    cls.append(TextBlock(x, y + i * self.fon.size(word)[1], " ".join(line),))
        return cls
class TestSprite(pygame.sprite.Sprite,Utility):
    #basic sprite class to test how images work
    def __init__(self,x,y,w,h):

        super().__init__()
        Utility.__init__(self)
        #images preloaded into sprite as array
        self.images = []
        self.images.append(pygame.image.load("pig1.png"))
        self.images.append(pygame.image.load("pig2.png"))
        self.images.append(pygame.image.load("pig3.png"))
        self.images.append(pygame.image.load("pig4.png"))
        self.index = 0
        #set current image of the sprite
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x,y, w, h) #
        #create white surface to act as eraser of sprite so the drag effect doesn't happen
        self.cover = pygame.Surface((w, h))
        self.cover.fill((255, 255, 255))

    def update(self):
        '''This method iterates through the elements inside self.images and
        displays the next one each tick. uses speed for slower animation'''
        self.index = self.index + 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.rect.x += 1
        self.speed()
class spriteSheet(pygame.sprite.Sprite,Utility):
    def __init__(self,x,y,frameWidth,frameHeight,startFrame,endFrame):
        os.chdir("C:\\Users\\max\\Desktop\\pigwalk")

        self.rect = pygame.Rect(x,y,frameWidth,frameHeight)
        self.sheet = pygame.image.load("fireworks.png")
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
            self.images.append(self.sheet.subsurface(col * frameWidth, row * frameHeight, frameWidth, frameHeight))
            self.currentFrame += 1
        self.currentFrame = 0
        self.image= self.images[self.currentFrame]

        self.cover = pygame.Surface((self.image.get_rect().size))
        self.cover.fill((255, 255, 255))

    def update(self,speed):
        if self.counter == speed:

            self.currentFrame = (self.currentFrame + 1) % len(self.sequence)

        self.counter += 1
        if self.counter > speed:
            self.counter = 0
        self.image = self.images[self.currentFrame]
    def draw(self,screen):

        screen.blit(self.image,(self.rect.x,self.rect.y))
    def moveUp(self,screen):
        #takes care of erasing as well
        screen.blit(self.cover, self.rect)
        self.rect.y += 10
    def moveDown(self,screen):
        screen.blit(self.cover, self.rect)
        self.rect.y -= 10
    def reset(self):
        screen.blit(self.cover, self.rect)
        self.rect.x = self.originx
        self.rect.y= self.originy




a=spriteSheet(0,0,67,46,7,13) # yellow explosion on white background, all frames
a.draw(screen)
leftFirework=spriteSheet(0,600,67,46,15,20)

def fullExplosion(sprite):
    while sprite.rect.y < 100:
        sprite.moveUp(screen)
        sprite.draw(screen)
        pygame.display.update()
        pygame.display.flip()
        pygame.time.wait(100)

    while sprite.currentFrame < len(sprite.sequence)-1:
        sprite.update(1)
        sprite.draw(screen)
        pygame.display.update()
        pygame.display.flip()
        pygame.time.wait(100)

    while sprite.rect.y > 0:
        sprite.moveDown(screen)
        pygame.time.wait(100)
        sprite.draw(screen)
        pygame.display.update()
        pygame.display.flip()

    sprite.reset()

def fireworkDisplay(sprite):
    while sprite.rect.y > (1*screen.get_rect().h)/5:
        sprite.moveDown(screen)
        sprite.draw(screen)
        pygame.display.update()
        pygame.display.flip()
        pygame.time.wait(50)

    while sprite.currentFrame < len(sprite.sequence)-1:
        sprite.update(2)
        sprite.draw(screen)
        pygame.display.update()
        pygame.display.flip()
        pygame.time.wait(100)

    while sprite.rect.y < (3*screen.get_rect().h)/5:
        sprite.moveUp(screen)
        pygame.time.wait(50)
        sprite.draw(screen)
        pygame.display.update()
        pygame.display.flip()

    sprite.reset()
class TextBlock(Utility):
    #make a text block that can move, not wrapped yet
    # doesnt do the blit just the creation
    def __init__(self,x,y,text):
        super().__init__()
        self.fon = pygame.font.SysFont(None, 16)
        w,h = self.fon.size(text)
        self.rect = pygame.Rect(x,y,w,h)
        self.tex=self.fon.render(text,True,(255,0,255))
        #create eraser
        self.cover = pygame.Surface((w,h))
        self.cover.fill((255,255,255))

    def update(self):
        self.rect = pygame.Rect(self.rect.left + 1, self.rect.top , self.rect.h,self.rect.w)
        self.speed()



def createText(x,y,text,cutoff):
    #make the text blocks
    b=TextBlock(0,0,text)#not doing xy
    cls = b.wraptext(x,y,text,cutoff)
    return cls


def create(cls):
    #create the sprites
    #for i in cls:
        #screen.blit(i.tex,i.rect)
    d = TestSprite(-5,-5,0,0)
    w,h = d.image.get_rect().size
    c = TestSprite(cls[0].rect.left-w,cls[0].rect.top,w,h) # linking by width
    return c


#for i in groups:
   # print(i)
  #  i.update()
   # i.draw(screen)

#update
pygame.display.update()
pygame.display.flip()

class useSound:
    def __init__(self,file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(1)



class gameControl:
    def __init__(self):
        #counters for arrays
        self.i = 0
        self.j=0
        self.k =0
        self.clickcounter=0
        self.rewards = [0,3,10,30,100,300,1000]

        # make all the text boxes

        cls = createText(0, 0, """ Max Dickinson 503-956-3213 max.dickinson58@gmail.com Github: maxdickinson""", 100)
        cls2 = createText(0, cls[-1].rect.bottom + 5,
                          """Education University of Oregon (Sep. 2011 – Dec. 2016) Applied Physics and Math-Computer Science double major""",
                          200)
        cls3 = createText(0, cls2[-1].rect.bottom + 5,
                          """Technical skills: Python, R, Javascript, Matlab C, C++ SQL Git Microsoft Office Suite""",
                          200)
        cls4 = createText(0, cls3[-1].rect.bottom + 5,
                          """Work experience Math Research Assistant (April 2016 – June 2016) Developed a pipeline in R to analyze mixed data and explored different R packages related to clustering and visualization for inter-university NSF project about clustering with applications for mental health. Use multiple packages to cluster and visualize data""",
                          200)
        cls5 = createText(0, cls4[-1].rect.bottom + 5,
                          """Tutor (July 2015 – December 2016) Taught math and physics of all levels to over 50 high school and college students.""",
                          200)
        cls6 = createText(0, cls5[-1].rect.bottom + 5,
                          """Paper Marker, University of Oregon Mathematics Department (July 2014 – July 2016) Graded papers for calculus, differential equations, elementary linear algebra, and discrete dynamical systems. Communicated progres and results with professors""",
                          200)
        cls7 = createText(0, cls6[-1].rect.bottom + 5,
                          """Biophysics Research Assistant (April 2013 – May 2013)Used an optical trap to pull pieces of a cell membrane which was collected and analyzed in Matlab. """,
                          200)
        cls8 = createText(0, cls7[-1].rect.bottom + 5,
                          """Physics Research Assistant (June 2012 – Nov. 2013) Built a scanning wavelength program to tune lab equipment """,
                          200)
        cls9 = createText(0, cls8[-1].rect.bottom + 5,
                          """Mission: Citizen board member (Sep. 2010 – Sep. 2012) Founding member of a 501c3 nonprofit. Developed and taught civics courses to first generation US immigrants Helped over 10 people pass the citizenship test. """,
                          200)

        self.clsss = [cls, cls2, cls3, cls4, cls5, cls6, cls7, cls8, cls9]

        self.creates = list(map(create, self.clsss))

        self.groups = list(map(pygame.sprite.Group, self.creates))
        self.flags= [0 for i in range(len(self.clsss)+2)]
        self.level = 0

    def checkDone(self,array,num1,num2):
        if array[self.i] == num1 and array[self.j] == num2:
            return True
    def fromLeft(self,sprite,screen):
        return sprite[self.k].rect.right < screen.get_rect().width / 2


    def walkOn(self,screen, cls, my_group, c):
        # block the sprite and text, can somehow combine group and c
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
        # update screen
        pygame.display.update()
        pygame.display.flip()
  """
        elif event.type == pygame.BUTTON_X1:
            if gc.clickcounter in gc.rewards:
                useSound('ogg sounds\\collect_point_00.ogg')
                fireworkDisplay(leftFirework)
                gc.clickcounter += 1
            else:
                gc.clickcounter += 1
                color += 10
                if color > 255:
                    color = 0
            # make buttons automatically adujust to screen
            button = pygame.draw.rect(screen, (color, 0, 0), (560, 20, 40, 40))
            pygame.display.update()
            pygame.display.flip()


        elif event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(pygame.mouse.get_pos()) and gc.k< len(gc.clsss):
            if gc.checkDone(gc.flags,0,0):
                useSound('ogg sounds\\jingle_win_00.ogg')
            #thread is locked while this is happening
            #mark done move to next one
                gc.flags[gc.i] = 1
                gc.j+=1
                #movement and how to move
                while gc.fromLeft(gc.creates,screen):
                    gc.walkOn(screen,gc.clsss[gc.k],gc.groups[gc.k],gc.creates[gc.k])
                gc.k+=1
            #every 10 clicks run the next one
            elif ((gc.clickcounter % 10) == 2) & gc.checkDone(gc.flags,1,0):

            #thread is locked while this is happening
            #mark done move to next one
                useSound('ogg sounds\\jingle_win_00.ogg')
                gc.flags[gc.j] = 1
                gc.i+=1
                gc.j+=1
                #movement and how to move
                while gc.fromLeft(gc.creates,screen):
                    gc.walkOn(screen,gc.clsss[gc.k],gc.groups[gc.k],gc.creates[gc.k])

                gc.k+=1
                gc.clickcounter +=1

            else:
                break
"""