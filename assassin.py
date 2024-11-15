import pygame,sys,random

pygame.init()
clock = pygame.time.Clock()
pygame.mixer.init()
#game_variables
gameInProgress = True
screen_width = 1000
screen_height = 560
population = 1
score = 0
highscore = 0
soundCooldown = False
target_img = pygame.image.load('mafia.png')
target_img = pygame.transform.scale(target_img,(40,40))
peasant_img = pygame.image.load('peasant.png')
peasant_img = pygame.transform.scale(peasant_img,(40,40))
#characters
target = pygame.Rect(random.randint(200,screen_width-40),random.randint(0,screen_height-40),40,40)
def createTarget():
    global target
    x = random.randint(200,screen_width-40)
    y = random.randint(0,screen_height-40)
    target = pygame.Rect(x,y,40,40)
    
peasants = []
def createPeasants():
    peasants.clear()
    for i in range(population):
        x = random.randint(200,screen_width-40)
        y = random.randint(0,screen_height-40)
        peasants.append(pygame.Rect(x,y,40,40))
createPeasants()  
#background
bg = pygame.image.load('bg_img.jpg')
bg = pygame.transform.scale(bg,(1000,560))      
#building screen and other initializing
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Assassin")
score_board = pygame.Rect(0,0,200,screen_height)
def createBoard():
    pygame.draw.rect(screen,pygame.Color('grey'),score_board)
    
    font = pygame.font.SysFont('oldenglishtext', 32)
    text = font.render('Your Target', True, pygame.Color("black"),)
    textRect = text.get_rect()
    textRect.center = (100, 100)
    screen.blit(text, textRect)
    
    placeholder = pygame.transform.scale(target_img,(100,100))
    screen.blit(placeholder,placeholder.get_rect(topleft = (50,140))) 
    # pygame.draw.rect(screen,target_color,(75,160,60,60))
       
    text = font.render('Score: '+str(score), True, pygame.Color("black"))
    textRect = text.get_rect()
    textRect.center = (100, screen_height // 2)
    screen.blit(text, textRect) 

    text = font.render('Time: '+str(counter), True, pygame.Color("black"))
    textRect = text.get_rect()
    textRect.center = (100, screen_height // 2 + 50)
    screen.blit(text, textRect) 
    
    text = pygame.font.SysFont('berlinsansfb', 32).render('by @Duong', True, (135,135,135))
    textRect = text.get_rect()
    textRect.center = (100, 500)
    screen.blit(text, textRect) 
#cursor
CURSOR_IMG = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.circle(CURSOR_IMG, pygame.Color('black'), (20, 20), 15, 3)
pygame.draw.circle(CURSOR_IMG, pygame.Color('black'), (20, 20), 2)
pygame.draw.rect(CURSOR_IMG, pygame.Color('black'), (0,18,10,4))
pygame.draw.rect(CURSOR_IMG, pygame.Color('black'), (30,18,10,4))
pygame.draw.rect(CURSOR_IMG, pygame.Color('black'), (18,0,4,10))
pygame.draw.rect(CURSOR_IMG, pygame.Color('black'), (18,30,4,10))
cursor_rect = CURSOR_IMG.get_rect()       
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
#countdown
counter = 10
pygame.time.set_timer(pygame.USEREVENT, 1000)
#audio
gunshot1 = pygame.mixer.Sound("GunShotSnglShotEx PE1097508.mp3")
gunshot2 =pygame.mixer.Sound("GunShotSnglFireIn PE1097304.mp3")
gunshot3 =pygame.mixer.Sound("GunShotSnglShotIn PE1097906.mp3")
laugh1 = pygame.mixer.Sound("laugh1.mp3")
laugh2 = pygame.mixer.Sound("laugh2.mp3")
laugh3 = pygame.mixer.Sound("laugh3.mp3")
laugh4 = pygame.mixer.Sound("laugh4.mp3")
laugh5 = pygame.mixer.Sound("laugh5.mp3")

pygame.mixer.music.load('bg_theme.mp3')   
pygame.mixer.music.set_volume(0.04)
pygame.mixer.music.play(-1)

def playGunshot():
    num = random.randint(1,3)
    if num == 1:
        gunshot1.play()
    elif num ==2:
        gunshot2.play()
    elif num ==3:
        gunshot3.play()  
def playLaugh():
    num = random.randint(1,5)
    if num ==1:
        laugh1.play()
    elif num ==2:
        laugh2.play()  
    elif num ==3:
        laugh3.play()
    elif num ==4:
        laugh4.play()
    elif num ==5:
        laugh5.play()                    
#pause game
paused = pygame.Surface((800,560),pygame.SRCALPHA)
font = pygame.font.SysFont('oldenglishtext', 32)
replay = font.render('Replay', True, pygame.Color("black"))
replayRect = replay.get_rect()
replayRect.center = (500, screen_height // 2 + 50)

quit = font.render('Quit', True, pygame.Color("black"))
quitRect = quit.get_rect()
quitRect.center = (700, screen_height // 2 + 50)                        

#rungame
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if target.collidepoint(pos) and gameInProgress:
                population+=6
                createTarget()
                createPeasants()
                score+=1
                playGunshot()
                counter+=1
            elif replayRect.collidepoint(pos) and not gameInProgress:
                counter = 15
                score = 0
                population = 1
                gameInProgress = True 
                soundCooldown = False
                createPeasants() 
                createTarget()
                playGunshot()
            elif quitRect.collidepoint(pos) and not gameInProgress:  
                pygame.quit()   
                sys.exit()      
        elif e.type == pygame.MOUSEMOTION:
            cursor_rect.center = e.pos    
        elif e.type == pygame.USEREVENT and gameInProgress: 
            counter -= 1                  
    screen.blit(bg,paused.get_rect())
    createBoard()
    screen.blit(target_img,target)
    for i in peasants:
        screen.blit(peasant_img,i)
    if counter <=0:
        gameInProgress = False
        if score > highscore:
            highscore = score
        if soundCooldown == False:
            playLaugh()
            soundCooldown = True    
        
        paused.fill((255,255,255,200))
        screen.blit(paused,(200,0))
        
        font = pygame.font.SysFont('oldenglishtext', 64)
        
        text = font.render('Highest score: '+str(highscore), True, pygame.Color("black"))
        textRect = text.get_rect()
        textRect.center = (600, screen_height // 2 )
        screen.blit(text, textRect)
            
        text = font.render('Score: '+str(score), True, pygame.Color("black"))
        textRect = text.get_rect()
        textRect.center = (600, screen_height // 2 - 50)
        screen.blit(text, textRect)
        
        screen.blit(replay, replayRect)
        
        screen.blit(quit, quitRect)
        
    screen.blit(CURSOR_IMG, cursor_rect)   
    pygame.display.flip()
    clock.tick(60)