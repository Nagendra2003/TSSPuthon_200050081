import pygame, sys, time, random

#initial game variables

# Window size
frame_size_x = 720
frame_size_y = 480

#Parameters for Snake
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
snake_rect_list=[pygame.Rect(snake_body[0],(10,10)),pygame.Rect(snake_body[1],(10,10)),pygame.Rect(snake_body[2],(10,10))]
direction_list=['right','right','right']   #direction for every rectangle
direction = 'right'
change_to = direction

#Parameters for food
food_pos = [0,0]
food_spawn = True   
food_rect=pygame.Rect(food_pos,(10,10))
score = 0


# Initialise game window
pygame.init()
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# FPS (frames per second) controller to set the speed of the game
fps_controller = pygame.time.Clock()

def check_for_events():
    """
    This should contain the main for loop (listening for events). You should close the program when
    someone closes the window, update the direction attribute after input from users. You will have to make sure
    snake cannot reverse the direction i.e. if it turned left it cannot move right next.
    """
    global direction
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                if direction!='left':
                    direction='right'
            elif event.key==pygame.K_LEFT:
                if direction!='right':
                    direction='left'

            elif event.key==pygame.K_UP:
                if direction!='down':
                    direction='up'
            elif event.key==pygame.K_DOWN:
                if direction!='up':
                    direction='down'

def update_snake():
    """
     This should contain the code for snake to move, grow, detect walls etc.
     """
    # Code for making the snake move in the expected direction
    #move
    global frame_size_x
    global frame_size_y 
    global direction
    global snake_rect_list
    global direction_list
    global food_rect
    global food_spawn
    global score

    direction_listcopy=direction_list.copy()
    for i in range(len(direction_list)) :  #change direction one by one of each box in different main loop iterations
        if(i>=1 and direction_listcopy[i]!=direction_listcopy[i-1]):
            direction_list[i]=direction_listcopy[i-1]
    if(direction_list[0]!=direction):
        direction_list[0]=direction

    for i in range(len(direction_list)) :
        if direction_list[i]=='left':
            snake_rect_list[i].move_ip(-10,0)
        elif direction_list[i]=='right':
            snake_rect_list[i].move_ip(10,0)
        elif direction_list[i]=='up':
            snake_rect_list[i].move_ip(0,-10)
        elif direction_list[i]=='down':
            snake_rect_list[i].move_ip(0,10)

    
    # Make the snake's body respond after the head moves. The responses will be different if it eats the food.
    # Note you cannot directly use the functions for detecting collisions 
    # since we have not made snake and food as a specific sprite or surface.
    if(snake_rect_list[0].center==food_rect.center ):
        score+=1
        if(direction=='left'):
            snake_rect_list.insert(0,food_rect.move(-10,0))
            direction_list.insert(0,'left')

        elif(direction=='right'):
            snake_rect_list.insert(0,food_rect.move(10,0))
            direction_list.insert(0,'right')
        
        elif(direction=='up'):
            snake_rect_list.insert(0,food_rect.move(0,-10))
            direction_list.insert(0,'up')

        elif(direction=='down'):
            snake_rect_list.insert(0,food_rect.move(0,10))
            direction_list.insert(0,'down')
        
        food_spawn=True

    # End the game if the snake collides with the wall or with itself. 
    out=snake_rect_list[0].right>frame_size_x or snake_rect_list[0].left<0 or snake_rect_list[0].top<0 or snake_rect_list[0].bottom>frame_size_y
    if(out):
        game_over()

    for i in range(1,len(snake_rect_list)):
        if(snake_rect_list[0].center==snake_rect_list[i].center):
            game_over()
            break
    
def create_food():
    """ 
    This function should set coordinates of food if not there on the screen. You can use randrange() to generate
    the location of the food.
    """
    global food_spawn
    global food_rect
    if(food_spawn):
        x=random.randrange(0,710, 10)
        y=random.randrange(0,470, 10)
        for snake_rect in snake_rect_list:   #x,y should not be on snake body and x,y are topleft coordinate
            while(snake_rect.center==(x+5,y+5)):
                x=random.randrange(0,710, 10)
                y=random.randrange(0,470, 10)
        
        food_rect=pygame.Rect((x,y),(10,10))
        food_spawn=False
    
def show_score(pos, color, font, size):
    """
    It takes in the above arguements and shows the score at the given pos according to the color, font and size.
    """
    global score
    
    score_img1 = pygame.font.SysFont(font,size).render("SCORE:", True, color)
    score_img2 = pygame.font.SysFont(font,size).render(str(score), True, color)
    score_rect1 = score_img1.get_rect()
    score_rect1.topright=pos
    score_rect2 = score_img2.get_rect()
    score_rect2.topleft=pos
    return (score_img1,score_rect1,score_img2,score_rect2)

def update_screen():
    """
    Draw the snake, food, background, score on the screen
    """
    global game_window
    global snake_rect_list
    global direction_list

    game_window.fill((0,0,0))
    for snake_rect in snake_rect_list:
        pygame.draw.rect(game_window,(0,255,0),snake_rect)
    pygame.draw.rect(game_window,(255,255,255),food_rect)

    (score_img1,score_rect1,score_img2,score_rect2)=show_score((150,30),(255,255,255),"sans-serif",22)
    game_window.blit(score_img1,score_rect1)
    game_window.blit(score_img2,score_rect2)

    pygame.display.flip()

def game_over():
    """ 
    Write the function to call in the end. 
    It should write game over on the screen, show your score, wait for 3 seconds and then exit
    """
    global game_window
    global frame_size_x
    global frame_size_y 
    
    time.sleep(1)
    gameover_img = pygame.font.SysFont("Segoe UI", 76).render("YOU DIED", True, (255,0,0))
    gameover_rect = gameover_img.get_rect()
    gameover_rect.center=(frame_size_x/2,frame_size_y/4)

    game_window.fill((0,0,0))
    game_window.blit(gameover_img, gameover_rect)
    (score_img1,score_rect1,score_img2,score_rect2)=show_score((frame_size_x/2,frame_size_y*3/4),(255,0,0),"Segoe UI",16)
    game_window.blit(score_img1,score_rect1)
    game_window.blit(score_img2,score_rect2)

    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()
# Main loop
while True:
    # Make appropriate calls to the above functions so that the game could finally run
    check_for_events()
    create_food()
    update_snake()
    update_screen()

    

    # To set the speed of the screen
    fps_controller.tick(20)