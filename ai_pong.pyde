################################################################################################
# IMPORTS
# import random function
from random import randint
# import sound library
add_library("sound")
################################################################################################
# HELPER FUNCTIONS
# set a random direction to the ball
# either -3 (up) or 3 (down)
# each time the game resets it goes in a different direction
def random_dy():
    while True:
        dy = random(-3,3)
        # ensure that the y is not too horizontal
        if not -0.5 < dy < 0.5:
            break
    return dy
################################################
class Player(): # scores class
    def __init__(self,x): # initialize attributes
        # set initial score value
        self.score = 0
        # set score location
        self.x = x
        
    def scored(self): # add point to player score
        self.score += 1
        
    def draw(self): # draw score on game board
        # set pixel font
        textFont(myFont)
        textSize(100)
        text(str(self.score), self.x, 80) 
        
    def reset(self): # after one match ends, reset player scores
        self.score = 0
################################################
class Ball(): # pong ball class
    def __init__(self): # initialize ball attributes
        # set ball location
        self.ball_x = 400 
        self.ball_y = 300 
        # set ball direction
        self.dx = 3 
        self.dy = random_dy()
        
    def move(self): # move game ball
        self.ball_x += self.dx
        self.ball_y += self.dy
        
    def draw(self): # draw game ball
        ellipse(self.ball_x,self.ball_y, 20, 20)
    
    def reset(self,direction): 
        # reset ball location and direction 
        # after point is scored or game is won
        # ball location
        self.ball_x = 400
        self.ball_y = 300
        
        # send ball in correct direction
        # if the previous point scored was by p1
        # i.e. hit the right wall
        # send it to the left side
        if direction == "left":
            self.dx = -3
            self.dy = random_dy()
        # if the previous point scored was by p2
        # i.e. hit the left wall
        # send it to the right side
        elif direction == "right":
            self.dx = 3
            self.dy = random_dy()

    def collide(self): # checking ball's collision with walls
        # check if hitting top/bottom wall
        if self.ball_y > 590 or self.ball_y < 10:
            bounce.play()
            self.dy *= -1
      
        # check if hitting right wall / point for player 1 (right)
        if self.ball_x > 790:
            # bounce sound effect
            bounce.play()
            # add point for p1
            p1_score.scored() 
            # ball will go towards player 1
            self.reset("left") 
            # reset paddle locations
            player_1.reset()
            player_2.reset()
              
        # check if hitting left wall / point for player 2 (left)
        if self.ball_x == 10:
            # bounce sound effect
            bounce.play()
            # add point for p2 
            p2_score.scored() 
            # ball will go towards player 2
            self.reset("right") 
            # reset paddle locations
            player_1.reset()
            player_2.reset()
            
    def bounce_x(self): # bounce ball off of paddle 
        self.dx *= -1
        
################################################
class Paddle(): # paddle class
    def __init__(self,x): # initialize paddle attributes
        # set paddle position
        self.x = x
        self.y = 300
        # set paddle direction
        self.dy = 0 # -4 is up, 0 is not moving, 4 is down
        # set ai mode False
        self.ai = False
        # set paddle speed
        self.speed = 4
    
    def make_ai(self): # setting ai true for ai mode
        self.ai = True
        
    def move_up(self): # moving paddles up
        # moving the ai paddle up
        if self.ai:
            self.dy = -self.speed
        else:
            # move normal paddle
            self.dy = -4
            
    def stop_moving(self): # stop paddle movement
        self.dy = 0
        
    def move_down(self): # moving paddles down
        # moving the ai paddle down
        if self.ai:
            self.dy += self.speed
        else:
            # move normal paddle
            self.dy = 4
    
    def rand(self): # generate random number for random AI paddle speed
        # speed can be any value between 0 to 5
        # (starting at zero, and up to, but not including, 5)
        self.speed = random(0, 5)
    
    def move(self): # moving the paddles
        if self.ai: # if in AI mode
            if ball.ball_y-50 == self.y:
                # if ball is the same as the paddle's center
                self.stop_moving() # self.dy = 0
            elif ball.ball_y - 50 <= self.y: 
                # if ball is lower than paddle's center
                self.move_up() 
            else: # if ball is higher than paddle's center
                # ball.ball_y - 50 >= self.y:
                self.move_down()
                
        # normal move function in 2 player mode
        self.y += self.dy
            
    def draw(self): # drawing paddles
        # width: 20 / height: 100
        rect(self.x, self.y,20,100)
        
    def reset(self): # reset paddle positions
        # reset location
        self.y = 300
        # stop movement
        self.stop_moving() # setting self.dy = 0
            
################################################################################################
# GLOBAL VARIABLES
mode = "instruction-screen" 
# modes: instruction-screen, game-on, pause, game-over
dotted_line_x = 399 # center line

ball = Ball() # create ball object

# paddle locations
player_1 = Paddle(30)
player_2 = Paddle(750)

# score locations
p1_score = Player(250)
p2_score = Player(500)

# pause mode
pause = True
################################################################################################
def setup():
    # declare global so that sounds and fonts can be used anywhere
    global bgm,bounce,gameover, myFont
    # canvas size
    size(800,600)
    # loading pixel font from data files
    myFont = createFont("Pixel.ttf",48)

    # loading main game music
    bgm = SoundFile(this, "pongbgm.wav")
    bgm.loop()
    
    # loading bounce sound (when ball hits paddles or top/bottom walls)
    bounce = SoundFile(this, "pongbounce.wav")
    
    # loading game over sound
    gameover = SoundFile(this, "pongwinner.wav")
    
################################################
def draw():
    # setting background colour
    background(0);
    global pause, mode
    ################################################
    # INSTRUCTION SCREEN
    if mode == "instruction-screen":
        textFont(myFont)
        # Title
        textSize(100)
        fill(247,239,106)
        text("PONG", 320, 120)
        # Instructions
        textSize(25)
        fill(255,255,255)
        text("1. Each player must move their respective paddle to",120,200) 
        text("prevent the ball from hitting the wall. When one side",120,225) 
        text("reaches 5 points, the game ends.",120,250)
        text("2. Player  1 uses the keys 'w' and 's' to move up and down.",120,295)
        text("3. Player  2 uses the keys 'i' and 'k' to move up and down.",120,320)
        text("4. Press 'p' to pause and 'o' to resume.", 120, 355)
        # Game mode buttons
        textSize(40)
        fill(255,0,0)
        text("Click to select game mode", 190, 520)
        fill(70,92,139)
        stroke(0)
        rect(100,400,160,50)
        rect(550,400,160,50)
        textSize(30)
        fill(247,239,106)
        text("1 PLAYER", 130, 435)
        text("2 PLAYER", 580, 435)
    ################################################
    # PAUSE SCREEN
    if mode == "pause":
        textFont(myFont)
        fill(0,0,255)
        textSize(50)
        text("GAME IS PAUSED", 260, 300)
        textSize(35)
        fill(247,239,106)
        text("Press 'o' to resume the game", 215, 330)
    ################################################
    # MAIN GAME SCREEN    
    if mode == "game-on":
        
        # draw ball
        fill(255,255,255)
        ball.draw()
        # move ball
        ball.move()
        
        # draw paddles and scores, move paddles
        # P1 draw paddles and scores, move paddles
        fill(255,0,0)
        stroke(0)
        player_1.draw()
        p1_score.draw()
        player_1.move()
        
        # P2 / AI draw paddles and scores, move paddles
        fill(0,0,255)
        player_2.draw()
        p2_score.draw()
        player_2.move()
        
        # drawing center line
        stroke(255,255,255)
        # making it a dashed line
        for y in range(50,600,20):
            rect(dotted_line_x, y, 1, 10)
        
        ##############################################
        # COLLISION
        # check if ball is hitting walls and paddles
        ball.collide()
        
        # check if ball bounces off paddles
        '''
        did not use other method 
        ball.dx *= -1 (reversing the direction)
        bc the ball would sometimes bounce in a zig zag along the paddle
        '''
        # check if hitting left PADDLE
        if (player_1.y < ball.ball_y < player_1.y+100) and 30 < ball.ball_x < 50:
            bounce.play() # sound effect
            # set direction to right
            ball.dx = abs(ball.dx)
    
        # check if hitting right PADDLE
        elif (player_2.y < ball.ball_y < player_2.y+100) and 750 < ball.ball_x < 770:
            bounce.play() # sound effect
            # set direction to left
            ball.dx = -abs(ball.dx)
        ##############################################
        # lowering ai's framecount/speed to make it beatable
        # every 300 frames (5 s), AI paddle speed is randomised
        # speed can be any value between 0 to 5
        # (starting at zero, and up to, but not including, 5)
        if frameCount % 300 == 0:
            player_2.rand()
        
        # draw title
        fill(247,239,106)
        textSize(60)
        text("Pong",345, 40)
            
        # check if game over
        if p1_score.score == 5:
            mode = "game-over"
            gameover.play() # sound effect
        if p2_score.score == 5:
            mode = "game-over"
            gameover.play() # sound effect
################################################################################################ 
    # GAME OVER SCREEN
    if mode == "game-over":
        textFont(myFont)
        fill(247,239,106)
        if p1_score > p2_score:
            textSize(60)
            text("Player 1 wins!", 245, 250)
            textSize(40)
            fill(255,0,0)
            text("Press m to return to main menu", 170,350)
            fill(0,0,255)
            text("Press n to play again", 240,390)
        else:
            textSize(60)
            fill(247,239,106)
            text("Player 2 wins!", 245, 250)
            textSize(40)
            fill(255,0,0)
            text("Press m to return to main menu", 170,350)
            fill(0,0,255)
            text("Press n to play again", 240,390)
            
################################################
def keyPressed():
    global pause, mode
    
    # game over, return to main menu
    if key == "m" and mode == "game-over": 
        mode = "instruction-screen"
        # resetting game components
        pause = True
        player_1.reset()
        player_2.reset()
        p1_score.reset()
        p2_score.reset()
    # game over, play again
    if key == "n" and mode == "game-over": 
        mode = "game-on"
        # resetting game components
        pause = True
        player_1.reset()
        player_2.reset()
        p1_score.reset()
        p2_score.reset()
    
    # pause game
    if key == "p":
        mode = "pause"
        if pause == True:
            mode = "pause"
    # resume game
    if key == "o":
        mode = "game-on"
        if pause == True:
            mode = "game-on"
        
    # move left paddle / p1
    if key == "w":
        player_1.move_up()
    elif key == "s":
        player_1.move_down()
        
    # move right paddle / p2
    if key == "i":
        player_2.move_up()
    elif key == "k":
        player_2.move_down()
################################################        
def keyReleased():
    # left player /  p1
    if key == "w":
        player_1.stop_moving()
    elif key == "s":
        player_1.stop_moving()
    
    # right player / p2
    if key == "i":
        player_2.stop_moving()
    elif key == "k":
        player_2.stop_moving()
################################################
def mousePressed():
    global mode
    
    # game mode selection on instruction screen
    if (100 < mouseX < 260) and (400 < mouseY < 450):
        mode = "game-on" # 1 player mode
        player_2.make_ai() # setting ai True
    elif (550 < mouseX < 710) and (400 < mouseY < 450):
        mode = "game-on" # 2 player mode
