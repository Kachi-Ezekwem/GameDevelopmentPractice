import pygame, random, sys
from pygame.locals import *

window_width = 600
window_height = 600
textcolor = (0,0,0)
backgroundcolor = (255,255,255)
FPS = 60
baddieminsize = 10
baddiemaxsize = 40
baddieminspeed = 1
baddiemaxspeed = 8
addnewbaddierate = 6
playermoverate = 5

def terminate():
    pygame.quit()
    sys.exit()
    
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get(): #If the player quits instead of starting, allow it
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return #If not continue witht the code
            
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True #Once the player is hit, the game ends
    return False

def drawText(text, font, surface, x,y):
    textobj = font.render(text,1,textcolor)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj,textrect)
    
#Set up the pygame, the window and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

#Set up the fonts
font = pygame.font.SysFont(None, 48)

#Set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

#Set up images
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')

#Show the "Start" screen
windowSurface.fill(backgroundcolor)
drawText('Dodger', font, windowSurface, (window_width/3),(window_height/3))
drawText('Press a key to start.', font, windowSurface, (window_width/3) - 30, (window_height/3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    #set up the start of the game
    baddies = []
    score = 0
    playerRect.topleft = (window_width/2, window_height - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1,0.0)
    
    while True:#The game loops run while the game part is playing
        score += 1 #increasing the score
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
                
            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = True
                    moveRight = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveUp = True
                    moveDown = False
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True
            
            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()
                
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False
                    
            if event.type == MOUSEMOTION:
                #If the mouse moves, move the player to the cursor
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]
        #Add new baddies at the top of the screen, if needed
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == addnewbaddierate:
            baddieAddCounter = 0
            baddieSize = random.randint(baddieminsize, baddiemaxsize)
            newBaddie = {'rect': pygame.Rect(random.randint(0,window_width - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                         'speed': random.randint(baddieminspeed,baddiemaxspeed),
                         'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                         }
            
            baddies.append(newBaddie)
            
        #Move the player around
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1*playermoverate, 0)
        if moveRight and playerRect.right < window_width:
            playerRect.move_ip(playermoverate, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0,-1*playermoverate)
        if moveDown and playerRect.bottom < window_height:
            playerRect.move_ip(0, playermoverate)
            
        #move the baddies down
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0,b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)
                
        #Delete baddies that have fallen past the bottom
        for b in baddies[:]:
            if b['rect'].top > window_height:
                baddies.remove(b)
            
        #Draw the game world on the window
        windowSurface.fill(backgroundcolor)
        
        #Draw the score and the top score
        drawText('Score: %s' %(score), font, windowSurface, 10,0)
        drawText('Top Score: %s' %(topScore), font, windowSurface, 10,40)
        
        #Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)
        
        #Draw each baddie
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])
            
        pygame.display.update()
        
        #Check if any of the baddies have hit the player
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score #Set the new top score
            break
        
        mainClock.tick(FPS)
        
    #Stop the game and the show the "GAME OVER" screen
    pygame.mixer.music.stop()
    gameOverSound.play()
    
    drawText('GAME OVER', font, windowSurface, (window_width/3), (window_height/3))
    drawText('Press a key to play again', font, windowSurface, (window_width/3) - 80, (window_height/3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()
    
    gameOverSound.stop()
                         
    