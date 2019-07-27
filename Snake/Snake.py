#########################################
# Programmer: Hayden Wolff
# Date: 5/2/2018
# File Name: snake.py
# Description: The classic snake game with a pacman twist
#########################################

import pygame
pygame.init()

from math import sqrt
from random import randint, choice

#---------------------------------------#
# screen settings                       #
#---------------------------------------#

HEIGHT = 650
WIDTH  = 800
screen=pygame.display.set_mode((WIDTH,HEIGHT))


#---------------------------------------#
# colours                               #
#---------------------------------------#

WHITE = (255,255,255)
BLACK = (  0,  0,  0)
RED = (255, 0, 0)
RCL = (255,0,255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (251, 188, 5)

#---------------------------------------#
# starting variables                    #
#---------------------------------------#
outline=0                               # Outline of the shape
state = 1                               # Starting state of the game
score = 0                               # Starting score
timer = 20                              # Starting time on the clock
delay = 50                              # Starting delay of the game
position = 3                            # Starting position of the snake's head


#---------------------------------------#
# Audio variables                       #
#---------------------------------------#
hit_apple = pygame.mixer.Sound("When Pac-Man Dies (3).wav")
hit_apple.set_volume(0.8)
hit_ghost = pygame.mixer.Sound("When Pac-Man Dies (1).wav")
hit_ghost.set_volume(0.8)


#---------------------------------------#
# snake's properties                    #
#---------------------------------------#
BODY_SIZE = 10
APPLE_SIZE = 10
HSPEED = 20
VSPEED = 20

speedX = 0
speedY = -VSPEED
segx = [int(WIDTH/2.)]*3
segy = [HEIGHT-100, HEIGHT-100+VSPEED, HEIGHT-100+2*VSPEED]


#---------------------------------------#
# apple's properties                    #
#---------------------------------------#
locationX = [i for i in range(20,WIDTH-20,20)]
locationY = [i for i in range(70,HEIGHT-20,20)]
goodX = choice(locationX)
goodY = choice(locationY)
badX = choice(locationX)
badY = choice(locationY)


#---------------------------------------#
# snake head images                     #
#---------------------------------------#

snakeHeadUp = pygame.image.load("SnakeHead-Up.png")
snakeHeadDown = pygame.image.load("SnakeHead-Down.png")
snakeHeadRight = pygame.image.load("SnakeHead-Right.png")
snakeHeadLeft = pygame.image.load("SnakeHead-Left.png")
snakeHeadUp = snakeHeadUp.convert_alpha()
snakeHeadDown = snakeHeadDown.convert_alpha()
snakeHeadRight = snakeHeadRight.convert_alpha()
snakeHeadLeft = snakeHeadLeft.convert_alpha()
snakeHeadUp = pygame.transform.scale(snakeHeadUp,(20,20))
snakeHeadDown = pygame.transform.scale(snakeHeadDown,(20,20))
snakeHeadRight = pygame.transform.scale(snakeHeadRight,(20,20))
snakeHeadLeft = pygame.transform.scale(snakeHeadLeft,(20,20))
rectSnakeHeadUp = snakeHeadUp.get_rect()
rectSnakeHeadDown = snakeHeadDown.get_rect()
rectSnakeHeadLeft = snakeHeadLeft.get_rect()
rectSnakeHeadRight = snakeHeadRight.get_rect()


#---------------------------------------#
# pictures                              #
#---------------------------------------#
background = pygame.image.load("grassField.jpg")
background = pygame.transform.scale(background,(WIDTH,600))
pacMan = pygame.image.load("Pacman.png")
pacMan = pygame.transform.scale(pacMan, (400,100))
snakeEdition = pygame.image.load("Snake.png")
snakeEdition = pygame.transform.scale(snakeEdition, (WIDTH,150))
gameOverPic = pygame.image.load("GameOver.jpg")
gameOverPic = pygame.transform.scale(gameOverPic, (WIDTH,HEIGHT))
ghost = pygame.image.load("ghost.png")
ghost = pygame.transform.scale(ghost, (20, 20))
rectGhost = ghost.get_rect()


#---------------------------------------#
# Functions                             #
#---------------------------------------#
def distance(x1, y1, x2, y2):                                                       # Function that calculates distance between two points in a coordinate system
    return sqrt((x1-x2)**2 + (y1-y2)**2)                                            # Pythagorean theorem

def redraw_screen():                                                                # Function that redraws all objects
    screen.fill(BLACK)                                                              # Sets the colour of the screen to black
    screen.blit(background, (0,50))                                                 # Sets the background of the game to be an image loaded in the beginning
    myFont = pygame.font.SysFont("Arial Black", 30)                                 # Creates a variable for the font for the text
    scores = myFont.render(("Score: " +str(score)),1,WHITE)                         # Creates a message that is displayed for the current score
    time = myFont.render("Time: "+str(round((timer),0)),1,WHITE)                    # Creates a message that is displayed for the time remaining
    screen.blit(time,(5,0))                                                         # Writes the message for the time remaining on the screen                      
    screen.blit(scores,(625,0))                                                     # Writes the message for the current score on the screen
    snakeHead()                                                                     # Runs the snake head function
    for i in range(1,len(segx),1):                                                  # For loop that sets the variable i to the number 1 through the length of the x segment of the snake
        pygame.draw.circle(screen, YELLOW, (segx[i], segy[i]), BODY_SIZE, outline)  # Draws the remaining segments of the snake (the body segments)
    pygame.draw.circle(screen, WHITE, (goodX, goodY), APPLE_SIZE, outline)          # Draws the white pellets
    rectGhost.center = (badX, badY)                                                 # Centres the image of the ghost
    screen.blit(ghost, rectGhost)                                                   # Draws the ghost on the screen
    pygame.display.update()                                                         # Display must be updated, in order to show the drawing
    
def snakeHead():                                                                    # Function that draws the snake head
    if position == 1:                                                               # Runs if the position of the snake's head is 1
        rectSnakeHeadLeft.center = (segx[0],segy[0])                                # Centres the image of the snake's head
        screen.blit(snakeHeadLeft, rectSnakeHeadLeft)                               # The snake's head appears to be facing to the left
    if position == 2:                                                               # Runs if the position of the snake's head is 2
        rectSnakeHeadRight.center = (segx[0],segy[0])                               # Centres the image of the snake's head
        screen.blit(snakeHeadRight,rectSnakeHeadRight)                              # The snake's head appears to be facing to the right
    if position == 3:                                                               # Runs if the position of the snake's head is 3
        rectSnakeHeadUp.center = (segx[0],segy[0])                                  # Centres the image of the snake's head
        screen.blit(snakeHeadUp,rectSnakeHeadUp)                                    # The snake's head appears to be facing upwards
    if position == 4:                                                               # Runs if the position of the snake's head is 4
        rectSnakeHeadDown.center = (segx[0],segy[0])                                # Centres the image of the snake's head
        screen.blit(snakeHeadDown,rectSnakeHeadDown)                                # The snake's head appears to be facing downwards

        
def introScreen():                                                                                                                  # Function for the intro screen
    screen.fill(WHITE)                                                                                                              # Fills the screen in the colour White
    screen.blit(pacMan,(0,125))                                                                                                     # Draws the "PAC-MAN Edition" text at those (x,y) coordinates
    screen.blit(snakeEdition,(0,0))                                                                                                 # Draws the "Snake" text at those (x,y) coordinates
    myFont = pygame.font.SysFont("Arial Black", 30)                                                                                 # Creates 1 of 3 variables for the font for the text with a size of 30 pixels
    myFont2 = pygame.font.SysFont("Arial Black", 17)                                                                                # Creates 2 of 3 variables for the font for the text with a size of 17 pixels
    myFont3 = pygame.font.SysFont("Arial Black", 25)                                                                                # Creates 3 of 3 variables for the font for the text with a size of 25 pixels
    instructions1 = myFont.render("INSTRCUTIONS",1,BLACK)                                                                           # Creates the text instructions1 at size 30 in black
    instructions2 = myFont.render("The Rules are simple:",1,BLACK)                                                                  # Creates the text instructions2 at size 30 in black
    instructions3 = myFont.render("Use the arrow keys to move",1,BLACK)                                                             # Creates the text instructions3 at size 30 in black
    instructions4 = myFont.render("Eat the white pellets and avoid the ghosts",1,BLACK)                                             # Creates the text instructions4 at size 30 in black
    instructions5 = myFont3.render("Every time your score increases, so does your time",1,BLACK)                                    # Creates the text instructions5 at size 25 in black
    instructions6 = myFont2.render("When you are out of time, run out of the map or collide with yourself, the game ends",1,BLACK)  # Creates the text instructions6 at size 17 in black
    instructions7 = myFont.render("Press Space to begin...",1,BLACK)                                                                # Creates the text instructions7 at size 30 in black
    screen.blit(instructions1, (250,250))                                                                                           # Draws the instructions1 text at those (x,y) coordinates
    screen.blit(instructions2, (210,300))                                                                                           # Draws the instructions2 text at those (x,y) coordinates
    screen.blit(instructions3, (160,350))                                                                                           # Draws the instructions3 text at those (x,y) coordinates
    screen.blit(instructions4, (70,400))                                                                                            # Draws the instructions4 text at those (x,y) coordinates
    screen.blit(instructions5, (70,450))                                                                                            # Draws the instructions5 text at those (x,y) coordinates
    screen.blit(instructions6, (10,500))                                                                                            # Draws the instructions6 text at those (x,y) coordinates
    screen.blit(instructions7, (220,600))                                                                                           # Draws the instructions7 text at those (x,y) coordinates
    pygame.display.update()                                                                                                         # Display must be updated, in order to show the drawing

def gameOver():                                                 # Function for the end screen
    screen.blit(gameOverPic,(0,0))                              # Draws the end screen picture
    pygame.display.update()                                     # Display must be updated, in order to show the drawing

    
def keyPressed():                                               # Function that checks if there is a key pressed
    global speedX                                               # Globalize the speedX variable so it can be used in other functions without calling this function in other functions
    global speedY                                               # Globalize the speedY variable so it can be used in other functions without calling this function in other functions
    global position                                             # Globalize the position variable so it can be used in other functions without calling this function in other functions
    keys = pygame.key.get_pressed()                             # Variable that is assigned when a key is pressed
    if speedY == -VSPEED or speedY == VSPEED and speedX == 0:   # Prevents the snake from moving opposite of the direction it is currently moving in
        if keys[pygame.K_LEFT]:                                 # Checks to see if the left arrow is pressed
            speedX = -HSPEED                                    # Sets the speedX to move in the negative direction (towards the left)
            speedY = 0                                          # Sets the speedY to not move up or down
            position = 1                                        # Sets the position of the snake's head to 1
    if speedY == -VSPEED or speedY == VSPEED and speedX == 0:   # Prevents the snake from moving opposite of the direction it is currently moving in
        if keys[pygame.K_RIGHT]:                                # Checks to see if the right arrow is pressed
            speedX = HSPEED                                     # Sets the speedX to move in the positive direction (towards the right)
            speedY = 0                                          # Sets the speedY to not move up or down
            position = 2                                        # Sets the position of the snake's head to 2
    if speedX == -HSPEED or speedX == HSPEED and speedY == 0:   # Prevents the snake from moving opposite of the direction it is currently moving in
        if keys[pygame.K_UP]:                                   # Checks to see if the up arrow is pressed
            speedX = 0                                          # Sets the speedX to not move left or right
            speedY = -VSPEED                                    # Sets the speedY to move in the negative direction (upwards)
            position = 3                                        # Sets the position of the snake's head to 3
    if speedX == -HSPEED or speedX == HSPEED and speedY == 0:   # Prevents the snake from moving opposite of the direction it is currently moving in
        if keys[pygame.K_DOWN]:                                 # Checks to see if the down arrow is pressed
            speedX = 0                                          # Sets the speedX to not move left or right
            speedY = VSPEED                                     # Sets the speedY to move in the positive direction (downwards)
            position = 4                                        # Sets the position of the snake's head to 4

            
def collision():                                                # Function that checks if the snake hits either apple
    global goodX                                                # Globalize the goodX variable so it can be used in other functions without calling this function in other funtions
    global goodY                                                # Globalize the goodY variable so it can be used in other functions without calling this function in other funtions
    global badX                                                 # Globalize the badX variable so it can be used in other functions without calling this function in other funtions
    global badY                                                 # Globalize the badY variable so it can be used in other functions without calling this function in other funtions
    global score                                                # Globalize the score variable so it can be used in other functions without calling this function in other funtions
    global timer                                                # Globalize the timer variable so it can be used in other functions without calling this function in other funtions
    if distance(segx[0], segy[0], goodX, goodY)<APPLE_SIZE:     # Checks to see if the distance between the snake and the good apple is less than the size of the apple
        segx.append(segx[-1])                                   # Adds a new x segment to the snake
        segy.append(segy[-1])                                   # Adds a new y segment to the snake
        score+=1                                                # Increases the score by 1
        timer += 3                                              # Increases the timer by 3
        hit_apple.play()                                        # Plays a sound to tell the user they have hit the apple 
        goodX = choice(locationX)                               # Reassigns the x variable of the good apple
        goodY = choice(locationY)                               # Reassigns the y variable of the good apple
    if distance(segx[0], segy[0], badX, badY)<APPLE_SIZE:       # Checks to see if the distance between the snake and the bad apple is less than the size of the apple
        segx.remove(segx[-1])                                   # Removes an x segment from the snake
        segy.remove(segy[-1])                                   # Removes a y segment from the snake
        timer -= 3                                              # Decreases the timer by 3
        hit_ghost.play()                                        # Plays a sound to tell the user they have hit the ghost
        badX = choice(locationX)                                # Reassigns the x variable of the bad apple
        badY = choice(locationY)                                # Reassigns the y variable of the bad apple

            
def moveSnake():                        # Function that moves the snake
                                        # move all segments
    for i in range(len(segx)-1,0,-1):   # start from the tail, and go backwards:
        segx[i]=segx[i-1]               # every segment takes the coordinates
        segy[i]=segy[i-1]               # of the previous one
                                        # move the head
    segx[0] = segx[0] + speedX          # The X segment of the head moves in the amount of pixels that is the pre-determined speed
    segy[0] = segy[0] + speedY          # The Y segment of the head moves in the amount of pixels that is the pre-determined speed

def changeSpeed():                      # Function that changes the speed of the snake depending on the score
    global timer                        # Globalize the timer variable so it can be used in other functions without calling this function in other funtions
    global delay                        # Globalize the delay variable so it can be used in other functions without calling this function in other funtions
    if score<10:                        # Checks to see if the score is between 0 and 10
        pygame.time.delay(delay)        # The snake moves / the game updates every 50 milliseconds 
    if score >= 10 and score<20:        # Checks to see if the score is between 10 and 20
        delay = 40                      # Sets the delay to 40 milliseconds
        pygame.time.delay(delay)        # The snake moves / the game updates every 40 milliseconds 
    if score >= 20 and score<30:        # Checks to see if the score is between 20 and 30
        delay = 30                      # Sets the delay to 30 milliseconds
        pygame.time.delay(delay)        # The snake moves / the game updates every 30 milliseconds
    if score >= 30:                     # Checks to see if the score is greater than 30
        delay = 20                      # Sets the delay to 20 miilliseconds
        pygame.time.delay(delay)        # The snake moves / the game updates every 20 milliseconds
    timer -= 0.001*delay                # The ingame timer decreases every 1 second
    
#---------------------------------------#
# the main program begins here          #
#---------------------------------------#
inPlay = True                                                                                                                   # Boolean that checks if the x button in the top right is pressed.
while inPlay:                                                                                                                   # Loop that runs while the boolean is set to true
    for event in pygame.event.get():                                                                                            # check for any events
        if event.type == pygame.QUIT:                                                                                           # If user clicked close
            inPlay = False                                                                                                      # Flag that we are done so we exit this loop
    if state == 1:                                                                                                              # Checks to see the current "state" of the game, runs if the game is in the first state
        introScreen()                                                                                                           # Runs the intro screen function
        keys = pygame.key.get_pressed()                                                                                         # Variable that is assigned when a key is pressed
        if keys[pygame.K_SPACE]:                                                                                                # Runs the following code if the spacebar is pressed
            state = 2                                                                                                           # Changes the game to "state" 2 or the snake game state
    if state == 2:                                                                                                              # Checks to see the current "state" of the game, runs if the game is in the second state
        redraw_screen()                                                                                                         # Runs the redraw_screen function to constantly update the snake and its movement
        moveSnake()                                                                                                             # Runs the moveSnake function that checks moves the head of the snake and each segment
        collision()                                                                                                             # Runs the collision function that checks if the snake runs into a good or bad apple
        keyPressed()                                                                                                            # Runs the keyPressed function that checks if the Up, Down, Right or Left key is pressed to move the snake
        changeSpeed()                                                                                                           # Runs the changeSpeed function that changes the speed of the snake based on it's score
        for i in range(1, len(segx),1):                                                                                         # For loop that sets the variable i to the number 1 through the length of the x segment of the snake
            if distance(segx[0],segy[0],segx[i],segy[i])<BODY_SIZE:                                                             # Checks for a collision between the snake and its segments
                hit_ghost.play()                                                                                                # Plays a sound to tell the user they have lost
                state = 3                                                                                                       # Changes the game to "state" 3 or the end screen state
        if not segx or not segy or segx[0] < 10 or segx[0] > WIDTH-10 or segy[0] < 59 or segy[0] > HEIGHT-10 or timer <= 0:     # Checks to see if the snake has 0 segments left, if the snake hit the border or if the timer is 0
            hit_ghost.play()                                                                                                    # Plays a sound to tell the user they have lost
            state = 3                                                                                                           # Changes the game to "state" 3 or the end screen state
    if state == 3:                                                                                                              # Checks to see the current "state" of the game, runs if the game is in the third state
        gameOver()                                                                                                              # Runs the endScreen function
pygame.quit()                                                                                                                   # always quit pygame when done!
