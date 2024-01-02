import pygame
import time
from pygame import mixer
from pygame.locals import *
from pygame import mixer

#Initialize the game
pygame.init()

#set display
screen = pygame.display.set_mode((1360, 770))
background = pygame.image.load('background1.png')
pygame.display.set_caption("Chip's Challenge")
clock = pygame.time.Clock()
fps = 60

#define game variables
textX = 10
textY = 725
tile_size = 34
game_over = 0
main_menu = True
level = 0
max_levels = 2
clock = pygame.time.Clock()
time_limit = 0
start_time = time.time()

#Load images 
bg_img = pygame.image.load('background1.png')
restart_img = pygame.image.load('restart1_btn.png')
start_img = pygame.image.load('start_btn.png')
exit_img = pygame.image.load('exit_btn.png')

#Fonts
font1 = pygame.font.Font('retro.ttf', 18)
font2 = pygame.font.Font('retro.ttf', 50)


#Add sounds
mixer.music.load("bg.wav")
mixer.music.play(-10)
pygame.mixer.music.set_volume(0.09)

def inventory(x,y):
    '''
    Description:    displays the inventory for the game which updates as different items are acquired together with the level and time updates
    Arguments:
    x, y            position in the map

    Returns:
                    inventory for the entire game
    '''
    title = font1.render("CHIP'S CHALLENGE", True, (255,255,255))
    screen.blit(title, (x,y-715))
    levels = font1.render("LEVEL: " +str(level+1), True, (255,255,255))
    screen.blit(levels, (x+1210,y-715))
    score = font1.render("Score: "+str(score_val), True, (255,255,255))
    screen.blit(score, (x,y-10))
    ykeys = font1.render("Yellow Keys: "+str(ykey), True, (255,255,0))
    screen.blit(ykeys, (x+200,y-10))
    gkeys = font1.render("Green Keys: "+str(gkey), True, (154,205,50))
    screen.blit(gkeys, (x+400,y-10))
    bkeys = font1.render("Blue Keys: "+str(bkey), True, (0,255,255))
    screen.blit(bkeys, (x+600,y-10))
    chips = font1.render("Chips collected: "+str(chip), True, (255,255,255))
    screen.blit(chips, (x+800,y-10))
    chips2 = font1.render("Chips remaining: "+str(chips1), True, (255,255,255))
    screen.blit(chips2, (x+1100,y-10))
    immunity = font1.render("IMMUNITY: ", True, (255,255,255))
    screen.blit(immunity, (x,y+12))
    if len(fireboots_group) == 0 and len(flippers_group) == 1:
        boots = font1.render("PLAYER IS IMMUNE TO FIRE!", True, (164, 40, 33))
        screen.blit(boots, (x+150,y+12))
    if len(flippers_group) == 0:
        boots = font1.render("PLAYER IS IMMUNE TO WATER!", True, (164, 40, 33))
        screen.blit(boots, (x+150,y+12))

def reset_level(level):
    '''
    Description:    Takes in the int of level to reset previous level then load new level
    Arguments:
    level           int of level to be displayed

    Returns:
    game_map(map to be used)      
    '''
    if level == 0:
        player.reset(646,272)
    elif level == 1:
        player.reset(17, 702)
    elif level == 2:
        player.reset(75, 614)
    passable_group.empty()
    yellowlocks_group.empty()
    bluelocks_group.empty()
    greenlocks_group.empty()
    yellowkeys_group.empty()
    bluekeys_group.empty()
    greenkeys_group.empty()
    chips_group.empty()
    firetiles_group.empty()
    watertiles_group.empty()
    flippers_group.empty()
    fireboots_group.empty()
    enemy_group.empty()
    thief_group.empty()
    exittile_group.empty()
    
    #load in level data and create world
    world_data = mapreader(f"maps/map{level}_tiles.txt")
    world = World(world_data)
    return world

def reset_level1(level):
    '''
    Description:    Takes in the int of level to reset previous level then load new level where the map is displayed
    Arguments:
    level           int of level to be displayed

    Returns:
    wall            displays wall when game resets    
    '''
    #load in level data and create world
    world_data = mapreader(f"maps/map{level}_tiles.txt")
    wall = Wall(world_data)
    return wall

def reset_level2(level):
    '''
    Description:    Takes in the int of level to reset previous level then load new level where the slide up tile is displayed
    Arguments:
    level           int of level to be displayed

    Returns:
    slideup         displays slide up tiles    
    '''
    #load in level data and create world
    world_data = mapreader(f"maps/map{level}_tiles.txt")
    slideup = upslide(world_data)
    return slideup

def reset_level3(level):
    '''
    Description:    Takes in the int of level to reset previous level then load new level and displays slide down tiles
    Arguments:
    level           int of level to be displayed

    Returns:
    slidedown       displays slide down tiles     
    '''
    #load in level data and create world
    world_data = mapreader(f"maps/map{level}_tiles.txt")
    slidedown = downslide(world_data)
    return slidedown

def reset_level4(level):
    '''
    Description:    Takes in the int of level to reset previous level then load new level and displays slide left tiles
    Arguments:
    level           int of level to be displayed

    Returns:
    slideleft       displays slide left tiles 
    '''
    #load in level data and create world
    world_data = mapreader(f"maps/map{level}_tiles.txt")
    slideleft = leftslide(world_data)
    return slideleft

def reset_level5(level):
    '''
    Description:    Takes in the int of level to reset previous level then load new level and displays slide right tiles
    Arguments:
    level           int of level to be displayed

    Returns:
    slideright      displays slide right tiles    
    '''
    #load in level data and create world
    world_data = mapreader(f"maps/map{level}_tiles.txt")
    slideright = rightslide(world_data)
    return slideright

class Button():
    
    def __init__(self, x, y, image):
        '''
        Description:    Load images to be used as buttons
        Arguments:
        self            the button itself
        x               x- coordinate of button
        y               y-coordinate of button
        image           selected image for buttons

        Returns:
                        initialized variables for the class Button       
        '''
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    
    def draw(self):
        '''
        Description:    Draws the button on the screen and checks if it has been clicked using the mouse
        Arguments:
        self            the button itself

        Returns:
        action          boolean, True - if action is performed, otherwise, not
        '''
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #draw button
        screen.blit(self.image, self.rect)

        return action

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    prepares the needed variables for the other functions in order for the player to function well
        Arguments:
        self            player itself
        x, y            takes in the position of the player from start to end (all movements)

        Returns:
                        everything inside the def reset function
        '''
        self.reset(x,y)

    def update(self, game_over):
        '''
        Description:    updates the movements, controls, and conditions of collisions(walls) of the player
        Arguments:
        self            pertains to the player

        Returns:
        game_over       variable that checks the game status
        '''
        dx = 0
        dy = 0
        rBorder = 1360
        lBorder = 0
        uBorder = 34
        dBorder = 750 - 34
        tile_size = 34
        fireboots_list = []
        flippers_list = []
        if game_over == 0:
            pressed_keys = pygame.key.get_pressed()
            #movement controls of the player(WASD or arrow keys)
            if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
                dx -= tile_size
                self.direction = -1
            elif pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
                dx += tile_size
                self.direction = 1
            elif pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
                dy -= tile_size
                self.vel_y = -1
            elif pressed_keys[pygame.K_DOWN]or pressed_keys[pygame.K_s]:
                dy += tile_size
                self.vel_y = 1
            #checking collision with the borders of the map
            if self.rect.right > rBorder:
                self.rect.right = rBorder
            if self.rect.left < lBorder:
                self.rect.left = lBorder
            if self.rect.bottom > dBorder:
                self.rect.bottom = dBorder
            if self.rect.top < uBorder:
                self.rect.top = uBorder

            #checking collision with walls
            for tile in wall.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    if self.direction < 0:
                        dx = tile[1].right - self.rect.left
                        self.direction = 0
                    elif self.direction >= 0:
                        dx = tile[1].left - self.rect.right
                        self.direction = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
            #checking collision with slide up tiles
            for tile in slideup.tile_list:
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy -= tile_size
                        self.vel_y = -1
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0    
            #checking collision with slide down tiles
            for tile in slidedown.tile_list:
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y >= 0:
                        dy += tile_size
                        self.vel_y = 1     
                    elif self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0       
            #checking collision with slide left tiles
            for tile in slideleft.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    if self.direction < 0:
                        dx -= tile_size
                        self.direction = -1
                    elif self.direction >= 0:
                        dx = tile[1].left - self.rect.right
                        self.direction = 0
            #checking collision with slide right tiles
            for tile in slideright.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    if self.direction >= 0:
                        dx += tile_size
                        self.direction = 1
                    if self.direction < 0:
                        dx = tile[1].right - self.rect.left
                        self.direction = 0
             
            if len(fireboots_group) == 0:
                fireboots_list.append(1)

            if len(flippers_group) == 0:
                flippers_list.append(1)
            
            if len(fireboots_list) > 0:
                if len(flippers_list) > 0:
                    fireboots_list.pop(0)
            
            if len(flippers_list) > 0:
                if len(fireboots_list) > 0:
                    flippers_list.pop(0)
                   
            #check for collision with watertiles
            if len(flippers_list) == 0:
                if pygame.sprite.spritecollide(self, watertiles_group, False):
                        game_over = -1
    
            #check for collision with firetiles
            if len(fireboots_list) == 0:
                if pygame.sprite.spritecollide(self, firetiles_group, False):
                    game_over = -1
            #check for collision with enemy
            if pygame.sprite.spritecollide(self, enemy_group, False):
                    game_over = -1
                
            #check for collision with exit
            if chip == total_chips:
                if pygame.sprite.spritecollide(self, exittile_group, False):
                    game_over = 1
            #check for collision with thief
            if pygame.sprite.spritecollide(self, thief_group, False):
                world_data = []
                world = reset_level(level)
                game_over = 0
                       
            #check for collision with locks
            if yellow == 0:
                for yellowlocks in yellowlocks_group:
                    if pygame.sprite.collide_rect(self, yellowlocks):
                        if self.direction >= 0:
                            dx = yellowlocks.rect.left - self.rect.right
                            self.direction = 0
                        if self.direction < 0:
                            dx = yellowlocks.rect.right - self.rect.left
                            self.direction = 0
                        if self.vel_y >= 0:
                            dy = yellowlocks.rect.top - self.rect.bottom
                            self.vel_y = 0
                        if self.vel_y < 0:
                            dy = yellowlocks.rect.bottom - self.rect.top
                            self.vel_y = 0
            if blue == 0:
                for bluelocks in bluelocks_group:
                    if pygame.sprite.collide_rect(self, bluelocks):
                        if self.direction >= 0:
                            dx = bluelocks.rect.left - self.rect.right
                            self.direction = 0
                        if self.direction < 0:
                            dx = bluelocks.rect.right - self.rect.left
                            self.direction = 0
                        if self.vel_y >= 0:
                            dy = bluelocks.rect.top - self.rect.bottom
                            self.vel_y = 0
                        if self.vel_y < 0:
                            dy = bluelocks.rect.bottom - self.rect.top
                            self.vel_y = 0 
            if green == 0:
                for greenlocks in greenlocks_group:
                    if pygame.sprite.collide_rect(self, greenlocks):
                        if self.direction >= 0:
                            dx = greenlocks.rect.left - self.rect.right
                            self.direction = 0
                        if self.direction < 0:
                            dx = greenlocks.rect.right - self.rect.left
                            self.direction = 0
                        if self.vel_y >= 0:
                            dy = greenlocks.rect.top - self.rect.bottom
                            self.vel_y = 0
                        if self.vel_y < 0:
                            dy = greenlocks.rect.bottom - self.rect.top
                            self.vel_y = 0

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy


        #draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, -1)

        return game_over

    def reset(self, x, y):
        '''
        Description:    prepares the needed variables for the other functions in order for the player to function well
        Arguments:
        self            player itself
        x, y            takes in the position of the player from start to end (all movements)

        Returns:
                        initialization of variables
        '''
        self.images_right = []
        self.index = 0
        player1 = pygame.image.load('char.png')
        img_right = pygame.transform.scale(player1, (25,29))
        self.images_right.append(img_right)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x+3
        self.rect.y = y+2
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.direction = 0

class Wall():
    def __init__(self, data):
        '''
        Description:    function that places the appropriate image for the wall and adds it to the list
        Arguments:
        self            Wall
        data            refers to the contents of the map

        Returns:
                        walls prepared for placement in screen
        '''  
        self.tile_list = []

        #load images
        bgg_img = pygame.image.load('tilesbgg.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == "#":
                    img = bgg_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1


    def draw(self):
        '''
        Description:    displays the wall (not passable tiles) to the screen
        Arguments:
        self            Wall

        Returns:
                        walls on the screen
        '''
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], -5)

class World():
    def __init__(self, data):
        '''
        Description:    function that places the appropriate loaded images with their corresponding symbols in the text file and are added to the list
        Arguments:
        self            World
        data            refers to the contents of the map

        Returns:
                        complete map
        '''
        self.tile_list = []

        #load images
        bgg_img = pygame.image.load('tilesbgg.png')
        passable_img = pygame.image.load('tiles.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == " ":
                    img = passable_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "f":
                    img = bgg_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "Y":
                    Yellowlocks = yellowlocks(col_count * tile_size, row_count * tile_size)
                    yellowlocks_group.add(Yellowlocks)
                if tile == "Y":
                    img = passable_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "B":
                    Bluelocks = bluelocks(col_count * tile_size, row_count * tile_size)
                    bluelocks_group.add(Bluelocks)
                if tile == "B":
                    img = passable_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "G":
                    Greenlocks = greenlocks(col_count * tile_size, row_count * tile_size)
                    greenlocks_group.add(Greenlocks)
                if tile == "G":
                    img = passable_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "y":
                    Yellowkeys = yellowkeys(col_count * tile_size, row_count * tile_size)
                    yellowkeys_group.add(Yellowkeys)
                if tile == "y":
                    img = passable_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "b":
                    Bluekeys = bluekeys(col_count * tile_size, row_count * tile_size)
                    bluekeys_group.add(Bluekeys)
                if tile == "b":
                    img = passable_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "g":
                    Greenkeys = greenkeys(col_count * tile_size, row_count * tile_size)
                    greenkeys_group.add(Greenkeys)
                if tile == "g":
                    img = passable_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "C":
                    Chips = chips(col_count * tile_size, row_count * tile_size)
                    chips_group.add(Chips)
                if tile == "C":
                    img = passable_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "F":
                    Firetiles = firetiles(col_count * tile_size, row_count * tile_size)
                    firetiles_group.add(Firetiles)
                if tile == "W":
                    Watertiles = watertiles(col_count * tile_size, row_count * tile_size)
                    watertiles_group.add(Watertiles)
                if tile == "L":
                    Flippers = flippers(col_count * tile_size, row_count * tile_size)
                    flippers_group.add(Flippers)
                if tile == "L":
                    img = passable_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "a":
                    Fireboots = fireboots(col_count * tile_size, row_count * tile_size)
                    fireboots_group.add(Fireboots)
                if tile == "a":
                    img = passable_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "e":
                    Enemy = enemy(col_count * tile_size, row_count * tile_size)
                    enemy_group.add(Enemy)
                if tile == "e":
                    img = passable_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "T":
                    Thief = thief(col_count * tile_size, row_count * tile_size)
                    thief_group.add(Thief)
                if tile == "T":
                    img = passable_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == "E":
                    Exittile = exittile(col_count * tile_size, row_count * tile_size)
                    exittile_group.add(Exittile)
                if tile == "S":
                    img = passable_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1


    def draw(self):
        '''
        Description:    prints the placed images to the screen
        Arguments:
        self            World

        Returns:
                        maps for the game
        '''
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], -1)

class yellowlocks(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    loads the image for the yellow locked tiles and initializes variables
        Arguments:
        self            yellowlocks
        x, y            position of the yellow locked tiles in the map

        Returns:
                        prepared yellow locks
        '''
        super().__init__()

        self.image = pygame.image.load("yellowt.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y

    def update(self, Player):
        '''
        Description:    updates the conditions for the yellow locks when right key is given
        Arguments:
        self            yellowlocks
        ykey            requirement for the collision condition
        Player          class calling for the class attributes

        Returns:
                        kills the locked tile allowing the player to permenantly access the tile when opened once
        '''
        if ykey > 0:
            if self.rect.colliderect(Player.rect.x,Player.rect.y, Player.width, Player.height):
                self.kill()
  
class bluelocks(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    loads the image for the blue locked tiles and initializes variables
        Arguments:
        self            bluelocks
        x, y            position of the blue locked tiles in the map

        Returns:
                        prepared blue locks
        '''
        super().__init__()
        self.image = pygame.image.load("bluet.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, Player):
        '''
        Description:    updates the conditions for the blue locks when right key is given
        Arguments:
        self            bluelocks
        bkey            requirement for the collision condition
        Player          class calling for the class attributes

        Returns:
                        kills the locked tile allowing the player to permenantly access the tile when opened once
        '''
        if bkey > 0:
            if self.rect.colliderect(Player.rect.x,Player.rect.y, Player.width, Player.height):
                self.kill()

class greenlocks(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    loads the image for the green locked tiles and initializes variables
        Arguments:
        self            greenlocks
        x, y            position of the green locked tiles in the map

        Returns:
                        prepared green locks
        '''
        super().__init__()
        self.image = pygame.image.load("greent.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, Player):
        '''
        Description:    updates the conditions for the green locks when right key is given
        Arguments:
        self            greenlocks
        gkey            requirement for the collision condition
        Player          class calling for the class attributes

        Returns:
                        kills the locked tile allowing the player to permenantly access the tile when opened once
        '''
        if gkey > 0:
            if self.rect.colliderect(Player.rect.x,Player.rect.y, Player.width, Player.height):
                self.kill()

class yellowkeys(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    loads the image for the yellow keys and initializes variables
        Arguments:
        self            yellowKeys
        x, y            position of the yellow keys in the map

        Returns:
                        prepared yellow keys
        '''
        super().__init__()
        self.image = pygame.image.load("ykey.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, Player):
        '''
        Description:    checks for collisions, attains the keys, and updates the held key
        Arguments:
        self            yellowKeys
        Player          class calling for the class attributes

        Returns:
                        kills the key allowing the player to open the locked tiles
        '''
        if self.rect.colliderect(Player.rect.x,Player.rect.y, Player.width, Player.height):
            self.kill()

class bluekeys(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    loads the image for the blue keys and initializes variables
        Arguments:
        self            bluekeys
        x, y            position of the blue keys in the map

        Returns:
                        prepared blue keys
        '''
        super().__init__()
        self.image = pygame.image.load("bkey.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, Player):
        '''
        Description:    checks for collisions, attains the keys, and updates the held key
        Arguments:
        self            bluekeys
        Player          class calling for the class attributes

        Returns:
                        kills the key allowing the player to open the locked tiles
        '''
        if self.rect.colliderect(Player.rect.x,Player.rect.y, Player.width, Player.height):
            self.kill()

class greenkeys(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    loads the image for the green keys and initializes variables
        Arguments:
        self            greenkeys
        x, y            position of the green keys in the map

        Returns:
                        prepared green keys
        '''
        super().__init__()
        self.image = pygame.image.load("gkey.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, Player):
        '''
        Description:    checks for collisions, attains the keys, and updates the held key
        Arguments:
        self            greenkeys
        Player          class calling for the class attributes

        Returns:
                        kills the key allowing the player to open the locked tiles
        '''
        if self.rect.colliderect(Player.rect.x,Player.rect.y, Player.width, Player.height):
            self.kill()

class chips(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    loads the image for the chips and initializes variables
        Arguments:
        self            chips
        x, y            position of the chips in the map

        Returns:
                        prepared chips
        '''
        super().__init__()
        self.image = pygame.image.load("chips.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


    def update(self, Player):
        '''
        Description:    checks for collisions, attains the chips and updates the collected chips
        Arguments:
        self            chips
        Player          class calling for the class attributes

        Returns:
                        kills the chips which means it is collected once all chips for the level is collected, player can level up
        '''
        if self.rect.collidepoint(Player.rect.center):
            self.kill()

class firetiles(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    loads the image for the fire tiles and initializes variables
        Arguments:
        self            firetiles
        x, y            position of the tiles in the map

        Returns:
                        prepared fire tiles
        '''
        super().__init__()

        self.image = pygame.image.load("bluefire.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class watertiles(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    loads the image for the water tiles and initializes variables
        Arguments:
        self            watertiles
        x, y            position of the tiles in the map

        Returns:
                        prepared water tiles
        '''
        super().__init__()

        self.image = pygame.image.load("water.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class flippers(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    loads the image for the flippers and initializes variables
        Arguments:
        self            Flippers
        x, y            position of the flippers in the map

        Returns:
                        prepared flippers
        '''
        super().__init__()
        self.image = pygame.image.load("Flippers.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, Player):
        '''
        Description:    checks for collisions, attains the immunity item and updates the collected immunity item
        Arguments:
        self            flippers
        Player          class calling for the class attributes

        Returns:
                        kills the immunity item allowing for pass in the element tile of pair
        '''
        if self.rect.colliderect(Player.rect.x,Player.rect.y, Player.width, Player.height):
            self.kill()

class fireboots(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    loads the image for the fire boots and initializes variables
        Arguments:
        self            Fireboots
        x, y            position of the fire boots in the map

        Returns:
                        prepared fire boots
        '''
        super().__init__()
        self.image = pygame.image.load("fireb.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, Player):
        '''
        Description:    checks for collisions, attains the immunity item and updates the collected immunity item
        Arguments:
        self            fireboots
        Player          class calling for the class attributes

        Returns:
                        kills the immunity item allowing for pass in the element tile of pair
        '''
        if self.rect.colliderect(Player.rect.x,Player.rect.y, Player.width, Player.height):
            self.kill()

class enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        '''
        Description:    loads the image of the enemy and initializes variables
        Arguments:
        self            enemy
        x, y            position of the enemy in the map

        Returns:
                        prepared enemies on tiles
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        '''
        Description:    updates the movement of the enemies, blocking the passageway of the player
        Arguments:
        self            enemy

        Returns:
                        moving enemies in the upward and downward direction
        '''
        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 34:
            self.move_direction *= -1
            self.move_counter *= -1

class thief(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    loads the image for the thief tiles and initializes variables
        Arguments:
        self            thief
        x, y            position of the thief tiles in the map

        Returns:
                        prepared thief tiles
        '''
        super().__init__()
        self.image = pygame.image.load("thief.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class upslide(pygame.sprite.Sprite):
    def __init__(self, data):
        '''
        Description:    loads the image for the slide up tiles and initializes variables
        Arguments:
        self            upslide
        data            the contents of the map

        Returns:
                        prepared slide up tiles
        '''
        self.tile_list = []

        #load images
        slide_img = pygame.image.load('slideU.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == "u":
                    img = slide_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1


    def draw(self):
        '''
        Description:    draws the image for the slide up tiles
        Arguments:
        self            slideup

        Returns:
                        upward slide tiles displayed on screen
        '''
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], -1)

class downslide(pygame.sprite.Sprite):
    def __init__(self, data):
        '''
        Description:    loads the image for the slide down tiles and initializes variables
        Arguments:
        self            slidedown
        data            the contents of the map
        Returns:
                        prepared slide down tiles
        '''
        self.tile_list = []

        #load images
        slide_img = pygame.image.load('slideD.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == "d":
                    img = slide_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1


    def draw(self):
        '''
        Description:    draws the image for the slide down tiles
        Arguments:
        self            slidedown

        Returns:
                        downward slide tiles displayed on screen
        '''
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], -1)

class leftslide(pygame.sprite.Sprite):
    def __init__(self, data):
        '''
        Description:    loads the image for the slide left tiles and initializes variables
        Arguments:
        self            slideleft
        data            the contents of the map

        Returns:
                        prepared slide left tiles
        '''
        self.tile_list = []

        #load images
        slide_img = pygame.image.load('slideL.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == "l":
                    img = slide_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1


    def draw(self):
        '''
        Description:    draws the image for the slide left tiles
        Arguments:
        self            slideleft

        Returns:
                        left slide tiles displayed on screen
        '''       
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], -1)

class rightslide(pygame.sprite.Sprite):
    def __init__(self, data):
        '''
        Description:    loads the image for the slide right tiles and initializes variables
        Arguments:
        self            slideright
        data            the contents of the map

        Returns:
                        prepared slide right tiles
        '''
        self.tile_list = []

        #load images
        slide_img = pygame.image.load('slideR.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == "r":
                    img = slide_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1


    def draw(self):
        '''
        Description:    draws the image for the slide right tiles
        Arguments:
        self            slideright

        Returns:
                        right slide tiles displayed on screen
        '''
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], -1)

class exittile(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        '''
        Description:    loads the image for the exit tile and initializes variables
        Arguments:
        self            Exit
        x, y            position of the tile in the map

        Returns:
                        prepared exit
        '''
        super().__init__()
        self.image = pygame.image.load("exit.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    # code that applies to all levels here.

#creation of sprite groups
player = Player(646,272)
passable_group = pygame.sprite.Group()
yellowlocks_group = pygame.sprite.Group()
bluelocks_group = pygame.sprite.Group()
greenlocks_group = pygame.sprite.Group()
yellowkeys_group = pygame.sprite.Group()
bluekeys_group = pygame.sprite.Group()
greenkeys_group = pygame.sprite.Group()
chips_group = pygame.sprite.Group()
firetiles_group = pygame.sprite.Group()
watertiles_group = pygame.sprite.Group()
flippers_group = pygame.sprite.Group()
fireboots_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
thief_group = pygame.sprite.Group()
exittile_group = pygame.sprite.Group()

#load in level data and create world

def mapreader(filename):
    """
    Description:        reads map from a text file
    Arguments:
        filename        path of the text file
    Returns:
        map             map, type 'list'
    """

    with open(filename, "r") as f:
        map = f.readlines()

    map_processed = []

    for element in map:
        map_processed.append(element.replace('\n', ''))

    return map_processed

world_data = mapreader(f"maps/map{level}_tiles.txt")
world = World(world_data)
wall = Wall(world_data)
slideup = upslide(world_data)
slidedown = downslide(world_data)
slideleft = leftslide(world_data)
slideright = rightslide(world_data)



#create buttons
restart_button = Button(1360 // 2 - 140, 770 // 2 + 100, restart_img)
start_button = Button(1360 // 2 - 200, 155, start_img)
exit_button = Button(1360 // 2 - 200, 400, exit_img)


run = True
while run:
    clock.tick(60)
    screen.blit(bg_img, (0, 0))
    #default total variables per level
    if level == 0:
        total_chips = 10
        total_ykey = 3
        total_bkey = 4
        total_gkey = 4
        total_ylocks = 3
        total_glocks = 4
        total_blocks = 4
        time_limit = 90
        
    if level == 1:
        total_chips = 15
        total_ykey = 5
        total_bkey = 6
        total_gkey = 6
        total_ylocks = 5
        total_glocks = 6
        total_blocks = 6
        time_limit = 120
        
    if level == 2:
        total_chips = 20
        total_ykey = 1
        total_bkey = 1
        total_gkey = 1
        total_ylocks = 1
        total_glocks = 1
        total_blocks = 1
        time_limit = 150
    
    fireboots_c = 1 - len(fireboots_group)
    flippers_c = 1 - len(flippers_group)
    chips1 = len(chips_group)
    chip = total_chips - chips1
    ykey = total_ykey - len(yellowkeys_group) - (total_ylocks - len(yellowlocks_group))
    bkey = total_bkey - len(bluekeys_group) - (total_blocks - len(bluelocks_group))
    gkey = total_gkey - len(greenkeys_group) - (total_glocks - len(greenlocks_group))
    yellow = len(yellowkeys_group) - len(yellowlocks_group)
    green = len(greenkeys_group) - len(greenlocks_group)
    blue = len(bluekeys_group) - len(bluelocks_group)
    score_val = chip*2
    
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()
        wall.draw()
        slideup.draw()
        slidedown.draw()
        slideleft.draw()
        slideright.draw()
        if game_over == 0:
            yellowlocks_group.update(player)
            bluelocks_group.update(player)
            greenlocks_group.update(player)
            yellowkeys_group.update(player)
            bluekeys_group.update(player)
            greenkeys_group.update(player)
            chips_group.update(player)
            flippers_group.update(player)
            fireboots_group.update(player)
            enemy_group.update()
            
           
        yellowlocks_group.draw(screen)
        bluelocks_group.draw(screen)
        greenlocks_group.draw(screen)
        yellowkeys_group.draw(screen)
        bluekeys_group.draw(screen)
        greenkeys_group.draw(screen)
        chips_group.draw(screen)
        firetiles_group.draw(screen)
        watertiles_group.draw(screen)
        flippers_group.draw(screen)
        fireboots_group.draw(screen)
        enemy_group.draw(screen)
        thief_group.draw(screen)
        exittile_group.draw(screen)
        inventory(textX,textY)
        
        game_over = player.update(game_over)
        #set up timer
        elapsed_time = int(time.time()-start_time)
        remaining_time = time_limit - elapsed_time
        if elapsed_time > time_limit:
            over = font1.render("YOU'VE RAN OUT OF TIME", True, (255,255,255))
            screen.blit(over, (textX+580,textY-715))
            game_over = -1
        
        else:
            timer = font1.render(f"TIME LEFT: {remaining_time} SECONDS", True, (255,255,255))
            screen.blit(timer, (textX+500,textY-715))
        #if player has died
        if game_over == -1:
            clock = pygame.time.Clock()
            start_time = time.time()
            gameover = pygame.image.load("gameover.png")
            gameOver = pygame.transform.scale(gameover, (1360,800))
            score = font2.render("Score: "+str(score_val), True, (255,255,255))
            screen.blit(gameOver, (0,0))
            screen.blit(score, (textX+510,textY-300))
            
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                wall = reset_level1(level)
                slideup = reset_level2(level)
                slidedown = reset_level3(level)
                slideleft = reset_level4(level)
                slideright = reset_level5(level)
                game_over = 0

        #if player has completed the level
        if game_over == 1:
            #reset game and go to next level
            level += 1
            if level <= max_levels:
                clock = pygame.time.Clock()
                start_time = time.time()
                #reset level
                world_data = []
                world = reset_level(level)
                wall = reset_level1(level)
                slideup = reset_level2(level)
                slidedown = reset_level3(level)
                slideleft = reset_level4(level)
                slideright = reset_level5(level)
                game_over = 0
            else:
                #if maximum level has been won, display a player wins image and if player presses restart, then player goes back to level 0
                gamewin= pygame.image.load("win.png")
                gameWin = pygame.transform.scale(gamewin, (1360,800))
                screen.blit(gameWin, (0,0))
               
                
                if restart_button.draw():
                    level = level - level
                    #reset level
                    clock = pygame.time.Clock()
                    start_time = time.time()
                    world_data = []
                    world = reset_level(level)
                    wall = reset_level1(level)
                    slideup = reset_level2(level)
                    slidedown = reset_level3(level)
                    slideleft = reset_level4(level)
                    slideright = reset_level5(level)
                    game_over = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()