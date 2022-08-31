import pygame, sys, time, random
from pygame.locals import *

#Set up pygame
pygame.init()
mainClock = pygame.time.Clock()

#Setting up the window
window_height = 400
window_width = 400
windowSurface = pygame.display.set_mode((window_width, window_height), 0, 32)
pygame.display.set_caption('Sprites and Sounds')

#setting up the colors
white = (255,255,255)

#Set up the block data structures
player = pygame.Rect(300, 100, 40, 40)
playerImage = pygame.image.load('player.png')
playerStretchedImage = pygame.transform.scale(playerImage, (40,40))
foodImage = pygame.image.load('cherry.png')
foods = []
for i in range(20):
    foods.append(pygame.Rect(random.randint(0, window_width - 20), random.randint(0, window_height - 20), 20,20))

foodCounter = 0
newfood = 40

#Set up the keyboard variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

move_speed = 6

#Setting up the music
pickUpSound = pygame.mixer.Sound('pickup.wav')
pygame.mixer.music.load('background.mid')
pygame.mixer.music.play(-1,0.0)
musicPlaying = True

#Run the gameloop
while True:
    for event in pygame.event.get():
         #Check for the QUIT Event always first thing
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #If the key directional arrow keys are pressed down    
        if event.type == KEYDOWN:
            #Change the keyboard variables
            if event.key == K_LEFT or event.key == K_a:
                moveLeft =  True
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
         
        #If the directional keys are released
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            #Terminate any directional actions that were going on
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False
            #Make the player teleport to a random position
            if event.key == K_x:
                player.top = random.randint(0, window_height - player.height)
                player.left = random.randint(0, window_width - player.width)
            if event.key == K_m: #This allows the player to start or pause the song by pressing m
                if musicPlaying:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1, 0.0)
                musicPlaying = not musicPlaying #This will change the musicPlaying variable from to false or vice versa
            
        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0] - 10, event.pos[1] - 10, 20, 20))
        
    foodCounter += 1
    if foodCounter >= newfood:
        #add new food
        foodCounter = 0
        foods.append(pygame.Rect(random.randint(0, window_width - 20), random.randint(0, window_height - 29), 20, 20))
        
    #Draw the white background onto the surface
    windowSurface.fill(white)
    
    #move the player
    if moveDown and player.bottom < window_height:
        player.top += move_speed
    if moveUp and player.top > 0:
        player.top -= move_speed
    if moveLeft and player.left > 0:
        player.left -= move_speed
    if moveRight and player.right < window_width:
        player.right += move_speed
    
    #Draw the blocks onto the surface
    windowSurface.blit(playerStretchedImage, player)
    
    #Check whether the block has intersected with any food squares
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
            player = pygame.Rect(player.left, player.top, player.width + 2, player.height + 2)
            playerStretchedImage = pygame.transform.scale(playerImage, (player.width, player.height))
            if musicPlaying:
                pickUpSound.play()
    #Draw the food
    for food in foods:
        windowSurface.blit(foodImage, food)
        
    #Draw the window onto the screen
    pygame.display.update()
    mainClock.tick(40)
    