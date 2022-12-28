"""
James Hom
Bubble Shubble Bros.
May 25, 2017
"""
 
import pygame
import random
import time

IMAGE_COLOUR = (0, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 233, 0)
GREY = (145, 145, 145)
CLOSEDOWN_GREY = (190, 190, 190)

pygame.init()
size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Bubble Shubble Bros.")
done = False
clock = pygame.time.Clock()

#Graphics
background_position = [0, 0]
background_image = pygame.image.load("Background.jpg").convert()
bubble_player_K_d = pygame.image.load("bubble_player_K_d.png").convert()
bubble_player_K_d.set_colorkey(WHITE)
bubble_player_K_a = pygame.image.load("bubble_player_K_a.png").convert()
bubble_player_K_a.set_colorkey(WHITE)
bubble_enemy1 = pygame.image.load("bubble_enemy1.png").convert()
bubble_enemy1.set_colorkey(WHITE)
bubble_enemy2 = pygame.image.load("bubble_enemy2.png").convert()
bubble_enemy2.set_colorkey(WHITE)
bubble_enemy3 = pygame.image.load("bubble_enemy3.png").convert()
bubble_enemy3.set_colorkey(WHITE)
bubble_enemy4 = pygame.image.load("bubble_enemy4.png").convert()
bubble_enemy4.set_colorkey(WHITE)
bubble_enemy5 = pygame.image.load("bubble_enemy5.png").convert()
bubble_enemy5.set_colorkey(WHITE)
bubble_enemy6 = pygame.image.load("bubble_enemy6.png").convert()
bubble_enemy6.set_colorkey(WHITE)
bubble_enemy_star = pygame.image.load("bubble_enemy_star.png").convert()
bubble_enemy_star.set_colorkey(WHITE)

#Dimensions
enemy_image_height = bubble_enemy2.get_height()
enemy_image_width = bubble_enemy2.get_width()
bubble_player_K_d_width = bubble_player_K_d.get_width()

#Variables
x_coord = 1280/2 - 48
y_coord = 0
game_screen_width = 1280
game_screen_height = 720
bubble_enemy_ingame_list = []           
position_x = random.randrange(100, game_screen_width - 100)
position_y = random.randrange(100, game_screen_height - 100)
seconds = 0
max_bullet = 1
score = 0
highscore = 0
lives = 1

#Classes
class Bubble_Enemy(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = bubble_enemy3
        self.image.set_colorkey(WHITE)
 
        self.rect = self.image.get_rect()
        
        # -- Attributes
        # Set speed vector
        self.x = 0
        self.y = 0        
        self.change_x = random.randrange(-3, 3)
        self.change_y = random.randrange(-3, 3)
        
        self.walls = None
        
    def changespeed(self, x, y):
        """ Change the speed of the player"""
        self.change_x += x
        self.change_y += y 
                
    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x
    
        # Did this update cause us to hit a wall?
        bubble_enemy_list = pygame.sprite.spritecollide(self, wall_list, False)
        
        #if len(bubble_enemy_list) > 0:
        for bubble_enemy in bubble_enemy_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = bubble_enemy.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = bubble_enemy.rect.right
            
            self.change_x *= -1
 
        self.rect.y += self.change_y 
 
        # Check and see if we hit anything
        bubble_enemy_list = pygame.sprite.spritecollide(self, wall_list, False)
        
        for bubble_enemy in bubble_enemy_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = bubble_enemy.rect.top
            else:
                self.rect.top = bubble_enemy.rect.bottom    
                
            self.change_y *= -1
        
 
class Bubble_Player(pygame.sprite.Sprite):
    """ This class represents the Player. """
 
    # -- Methods
    def __init__(self, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()
 
        # Set height, width
        self.image = bubble_player_K_d
        self.image.set_colorkey(WHITE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = game_screen_width/2
        self.rect.y = 500
 
        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None
 
    def changespeed(self, x, y):
        """ Change the speed of the player"""
        self.change_x += x
        self.change_y += y
 
    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        bubble_player_list = pygame.sprite.spritecollide(self, self.walls, False)
        for bubble_player in bubble_player_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = bubble_player.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = bubble_player.rect.right
 
        self.rect.y += self.change_y
        
        # Check and see if we hit anything
        bubble_player_list = pygame.sprite.spritecollide(self, self.walls, False)
        for bubble_player in bubble_player_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = bubble_player.rect.top
            else:
                self.rect.top = bubble_player.rect.bottom        
 
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([4, 720])
        self.image.fill(GREY)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        self.rect.y -= 5

class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super().__init__()
 
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(YELLOW)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
# --- Sprite Lists
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
 
# List of each block in the game
bubble_enemy_list = pygame.sprite.Group()

#List of player in game
bubble_player_list = pygame.sprite.Group()
 
# List of each bullet
bullet_list = pygame.sprite.Group()

# Make the walls. (x_pos, y_pos, width, height)
wall_list = pygame.sprite.Group()

# --- Create the sprites
#Left Border
wall = Wall(0, 0, 13, 587)
wall_list.add(wall)
all_sprites_list.add(wall)

#Top Border
wall = Wall(10, 0, 1267, 13)
wall_list.add(wall)
all_sprites_list.add(wall)

#Right Border
wall = Wall(1267, 0, 13, 587)
wall_list.add(wall)
all_sprites_list.add(wall)

#Bottom Border
wall = Wall(0, 574, 1280, 13)
wall_list.add(wall)
all_sprites_list.add(wall)

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Create the player object
bubble_player = Bubble_Player(None, None)
bubble_player.walls = wall_list
all_sprites_list.add(bubble_player)

#Create the Bubble object
bubble_enemy = Bubble_Enemy(None, None)
bubble_enemy.walls = wall_list
all_sprites_list.add(bubble_enemy)

# Use this boolean variable to trigger if the game is over.
game_over = False
restart = False

# -------- Introduction Screen Loop -----------
title_font = pygame.font.SysFont('freesansbold.ttf', 85, True, False)
header_font = pygame.font.SysFont('freesansbold.ttf', 65, True, False)
font = pygame.font.SysFont('freesansbold.ttf', 45, True, False)
display_intro = True
intro_screen = 1

while not done and display_intro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                intro_screen += 1
                if intro_screen == 4:
                    display_intro = False
        
    screen.fill(BLACK)
                 
    if intro_screen == 1:
        # Draw instructions, page 1
        # This could also load an image created in another program.
        # That could be both easier and more flexible.
 
        text = title_font.render("HOM PRODUCTIONS", True, WHITE) #360
        screen.blit(text, [300, 300])
 
        text = font.render("PRESS ENTER TO CONTINUE", True, WHITE)
        screen.blit(text, [370, 420])  
        
    elif intro_screen == 2:
        text = title_font.render("BUBBLE SHUBBLE BROS.", True, WHITE) #360
        screen.blit(text, [220, 300])
        
        text = font.render("PRESS ENTER TO CONTINUE", True, WHITE)
        screen.blit(text, [370, 420])  
        
    elif intro_screen == 3:
        text = header_font.render("INSTRUCTIONS", True, WHITE) #360
        screen.blit(text, [420, 40])
        
        text = font.render("W - SHOOT", True, WHITE)
        screen.blit(text, [520, 200])
        
        text = font.render("A - MOVE LEFT", True, WHITE)
        screen.blit(text, [520, 250])      
        
        text = font.render("D - MOVE RIGHT", True, WHITE)
        screen.blit(text, [520, 300])           
        
        text = font.render("PRESS ENTER TO CONTINUE", True, WHITE)
        screen.blit(text, [370, 420])     
        
    clock.tick(60)
 
    # Limit to 60 frames per second
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
# -------- Selection Screen Loop -----------
display_selection = True
selection_screen = 1

while not done and display_selection:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_2:
                selection_screen += 1
                if selection_screen == 2:
                    display_selection = False
            elif event.key == pygame.K_1:
                None
    
    screen.fill(BLACK)
                 
    if selection_screen == 1:
        # Draw instructions, page 1
        # This could also load an image created in another program.
        # That could be both easier and more flexible.
        
        text = header_font.render("STORY MODE", True, CLOSEDOWN_GREY) #341
        screen.blit(text, [140, 175])   
        
        #text = font.render("PRESS 1", True, CLOSEDOWN_GREY)
        #screen.blit(text, [230, 500])
        
        text = font.render("COMING SOON", True, CLOSEDOWN_GREY) #341
        screen.blit(text, [180, 500])   
    
        text = header_font.render("ARCADE MODE", True, WHITE) #386
        screen.blit(text, [750, 175])
        
        screen.blit(bubble_enemy_star, [850, 260])
 
        text = font.render("PRESS 2", True, WHITE)
        screen.blit(text, [870, 500])  
    
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()    
    
#---------- Mode Selection Screen -----------
display_mode_selection = True
mode_selection_screen = 1
mode = 0

while not done and display_mode_selection:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode_selection_screen += 1
                mode = 150
                play_mode = "EASY MODE"
                play_mode_coord = 10
                if mode_selection_screen == 2:
                    display_mode_selection = False                
            elif event.key == pygame.K_2:
                mode_selection_screen += 1
                mode = 100
                play_mode = "NORMAL MODE"
                play_mode_coord = -15
                if mode_selection_screen == 2:
                    display_mode_selection = False                
            elif event.key == pygame.K_3:
                mode_selection_screen += 1
                mode = 50
                play_mode = "HARD MODE"
                play_mode_coord = 10
                if mode_selection_screen == 2:
                    display_mode_selection = False
            elif event.key == pygame.K_4:
                mode_selection_screen += 1
                mode = 25
                play_mode = "EXPERT MODE"
                play_mode_coord = -12 
                if mode_selection_screen == 2:
                    display_mode_selection = False  
            elif event.key == pygame.K_5:
                mode_selection_screen += 1
                mode = 12
                play_mode = "GOD MODE"
                play_mode_coord = 20
                if mode_selection_screen == 2:
                    display_mode_selection = False              
    
    screen.fill(BLACK)
    
    if mode_selection_screen == 1:
        text = header_font.render("SELECT MODE", True, WHITE)
        screen.blit(text, [440, 20])
        
        text = font.render("1 - EASY MODE", True, WHITE)
        screen.blit(text, [450, 130])
        
        text = font.render("2 - NORMAL MODE", True, WHITE)
        screen.blit(text, [450, 200])
        
        text = font.render("3 - HARD MODE", True, WHITE)
        screen.blit(text, [450, 270])
        
        text = font.render("4 - EXPERT MODE", True, WHITE)
        screen.blit(text, [450, 340])
        
        text = font.render("5 - GOD MODE", True, WHITE)
        screen.blit(text, [450, 410])            
        
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()   
    
# -------- Main Program Loop -----------
while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                bubble_player.changespeed(-3, 0)
                bubble_player.image = bubble_player_K_a
                bubble_player_K_a.set_colorkey(WHITE)  
                
            elif event.key == pygame.K_d:
                bubble_player.changespeed(3, 0)
                bubble_player.image = bubble_player_K_d
                bubble_player_K_d.set_colorkey(WHITE)    
                
            elif event.key == pygame.K_w:
                max_bullet -= 1
                if not max_bullet < 0:
                    # Fire a bullet if the user clicks the mouse button
                    bullet = Bullet()
                    # Set the bullet so it is where the player is
                    bullet.rect.x = bubble_player.rect.x + 25
                    bullet.rect.y = bubble_player.rect.y
                    # Add the bullet to the lists
                    all_sprites_list.add(bullet)
                    bullet_list.add(bullet)
                    
        # Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                bubble_player.changespeed(3, 0)
            elif event.key == pygame.K_d:
                bubble_player.changespeed(-3, 0) 
                
    # --- Game logic should go here
    if not game_over:
        # Call the update() method on all the sprites
        all_sprites_list.update()
        
        #Arcade Random Level Function
        bubble_enemy_chance = random.randrange(mode)
        if bubble_enemy_chance == 1:
            #for i in range(10):
            # This represents a block
            bubble_enemy = Bubble_Enemy(None, None)
                
            # Set a random location for the block
            bubble_enemy.rect.x += random.randrange(game_screen_width - 26)
            bubble_enemy.rect.y += random.randrange(250)
         
            # Add the block to the list of objects
            bubble_enemy_list.add(bubble_enemy)
            all_sprites_list.add(bubble_enemy) 
                
        # Calculate mechanics for each bullet
        for bullet in bullet_list:
     
            # See if bullet hit a bubble
            bubble_enemy_hit_list = pygame.sprite.spritecollide(bullet, bubble_enemy_list, True)
     
            # For each block hit, remove the bullet and add to the score
            for bubble_enemy in bubble_enemy_hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 100
                if max_bullet <= 0:
                    max_bullet = 1
                
            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < 13:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                if max_bullet <= 0:
                    max_bullet = 1
            
            #Max Bullet Capacity
            if max_bullet <= 0 or max_bullet > 1:
                max_bullet = 0
            
        #When a bubble hits a player   
        for bubble_enemy in bubble_enemy_list:
            bubble_player_hit_list = pygame.sprite.spritecollide(bubble_player, bubble_enemy_list, True)
            for bubble_player in bubble_player_hit_list:
                lives = 0
                game_over = True
        
        if score > highscore:
            highscore = score
            
    # --- Drawing code should go here
    screen.blit(background_image, background_position)
    
    # Draw all the sprites
    all_sprites_list.draw(screen)
    
    #Draw Bottom Border
    pygame.draw.rect(screen, YELLOW, [0, 574, 1280, 13])
        
    #Drawing Stat Box
    pygame.draw.rect(screen, BLACK, [0, 587, 1280, 133])
    font = pygame.font.SysFont('freesansbold.ttf', 45, True, False)
    world_text = font.render("DEATHMOON", True, WHITE)
    #time_text = font.render("TIME: " + str(seconds), True, WHITE)
    player_text = font.render("PLAYER 1", True, WHITE)
    lives_text = font.render("LIVES: " + str(lives), True, WHITE)
    score_text = font.render("SCORE: " + str(score), True, WHITE)
    highscore_text = font.render("HIGHSCORE: " + str(highscore), True, WHITE)
    play_mode_text = font.render(play_mode, True, WHITE)
    screen.blit(world_text, [game_screen_width/2 - 110, 610])
    #screen.blit(time_text, [game_screen_width/2 - 75, 660])
    screen.blit(player_text, [game_screen_width/2 - 600, 610])
    screen.blit(lives_text, [game_screen_width/2 - 600, 660])
    screen.blit(score_text, [game_screen_width/2 + 350, 610])
    screen.blit(highscore_text, [game_screen_width/2 + 260, 660])
    screen.blit(play_mode_text, [game_screen_width/2 - 110 + play_mode_coord, 660])
    
    if game_over:
        # If game over is true, draw game over
        text = font.render("GAME OVER", True, WHITE)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y - 50])
        max_bullet = 0
        #text = font.render("PLAY AGAIN", True, WHITE)
        #screen.blit(text, [text_x, text_y])
        #text = font.render("Y/N", True, WHITE)
        #screen.blit(text, [text_x + 70, text_y + 25])
        #for event in pygame.event.get():
            #if event.type == pygame.QUIT:
                #done = True            
            #if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_y:
                    #restart = True
                #if event.key == pygame.K_n:
                    #done = True
        

    pygame.display.flip()
    clock.tick(60)
     
pygame.quit()