import pygame
import sys
import random
import time

pygame.init()
screen = pygame.display.set_mode((576, 650))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont(None, 40)


gravity = 0.2  #changed
bird_movement = 0
game_active = False
score = 0
floor_x_pos = 0

# Load the necessary images

bg_surface = pygame.image.load('flappy_assets/background.png').convert_alpha()
bg_surface=pygame.transform.scale(bg_surface,((576, 650)))
# bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('flappy_assets/floor.png')
floor_surface = pygame.transform.scale2x(floor_surface)

bird_surface = pygame.transform.scale2x(pygame.image.load('flappy_assets/bluebird.png'))
bird_rect = bird_surface.get_rect(center=(100, 200))  #changed

pipe_surface = pygame.image.load('flappy_assets/pipe.png')
# pipe_surface = pygame.transform.scale2x(pipe_surface)

game_over_surface = pygame.transform.scale2x(pygame.image.load('flappy_assets/message.png'))
game_over_rect = game_over_surface.get_rect(center=(288, 512))


pipe_list = []

# We have created this custom event which will be automatically trigerred according to the time set
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 2400) #changed
pipe_height = [400, 600, 800]


def create_pipe():
	"""
	Create and return rects for 2 pipes using pip_surface(one at top and other at bottom) You can use functions from random
	to change the height of the pipes.(but keeping the size of opening constant)
	"""
	global pipe_list
	global floor_x_pos
	global pipe_surface
	opening=200
	h=random.randrange(50,350,50)

	pipe_surface=pygame.transform.scale(pipe_surface,(80, 550))
	pipe_img1=pipe_surface
	pipe_rect1=pipe_img1.get_rect()
	pipe_rect1.bottomleft=(576,550+pipe_rect1.height-h)  #30px floor

	pipe_img2=pipe_surface
	pipe_img2=pygame.transform.rotate(pipe_img2,180)
	pipe_rect2=pipe_img1.get_rect()
	pipe_rect2.topleft=(576,-pipe_rect1.height+(550-opening-h))  #30px floor

	pipe_list.append([pipe_img1,pipe_rect1,pipe_img2,pipe_rect2])

def move_pipes(pipes):
	"""
	Move the pipes back in order to give the feeling that the bird is moving forward.
	"""
	pipes[1].left-=2
	pipes[3].left-=2


def draw_pipes(pipes):
	"""
	Draw the pipes on the screen using the rects and pipe_surface. Use blit(). You will have to judge whether its a top pipe or
	a bottom pipe and appropriately use the image. You can use pygame.transform.flip() to flip an image.
	"""
	global screen

	screen.blit(pipes[0],pipes[1])
	screen.blit(pipes[2],pipes[3])

def remove_pipes(pipes):
	"""
	As the pipes reach the left side of the screen remove them.
	"""
	global pipe_list
	if(pipes[1].right<0):
		pipe_list.remove(pipes)

def draw_floor():
	"""Draw the floor surfaces on the screen. Hint: Use 2 floor surfaces to ensure proper motion of the floor"""
	global floor_surface
	global screen
	global floor_x_pos
	floor_surface1=pygame.transform.scale(floor_surface,(576,100))
	floor_surface2=pygame.transform.scale(floor_surface,(576,100))
	floor_rect1=floor_surface1.get_rect()
	floor_rect1.bottomleft=(floor_x_pos,650)
	floor_rect2=floor_surface2.get_rect()
	floor_rect2.bottomleft=(floor_x_pos+576,650)
	floor_x_pos-=2
	if(floor_x_pos<=-576):
		floor_x_pos=0
	screen.blit(floor_surface1,floor_rect1)
	screen.blit(floor_surface2,floor_rect2)

def check_collision(pipes):
	"""
	check whether the bird might have collided with any of the pipes you can use
	colliderect(). Or the bird might have hit the floor or crossed the top.
	"""
	global bird_rect
	global game_active
	global pipe_list
	global bird_movement
	if( bird_rect.colliderect(pipes[1])  or   bird_rect.colliderect(pipes[3]) or bird_rect.top<0 or bird_rect.bottom>550):
		time.sleep(0.3)
		game_active=False
		bird_rect.center=(100, 200)
		pipe_list=[]
		bird_movement=0
	

def score_display(game_state):
	"""
	display the score on the screen. Note depending on what the game state is
	score will have to be displayed at different places.
	"""
	global screen
	global score
	global game_font
	if (game_state=='main_game'):
		score_img=game_font.render(str(score),True,(255,255,255))
		score_rect=score_img.get_rect()
		score_rect.center=(576/2,50)
		screen.blit(score_img,score_rect)

	if(game_state=="game_over"):
		score_img1=game_font.render("SCORE:",True,(255,255,255))
		score_rect1=score_img1.get_rect()
		score_rect1.topright=(576/2+30,50)
		score_img2=game_font.render(str(score),True,(255,255,255))
		score_rect2=score_img2.get_rect()
		score_rect2.topleft=(576/2+30,50)

		screen.blit(score_img1,score_rect1)
		screen.blit(score_img2,score_rect2)

def check_for_events():
	"""
	Will contain main for loop listening for events. It should have code to respond to
	quitting, pressing the spacebar(if game is active it causes the jump, use bird_movement attribute and if not
	it should turn the game active and start it). It should also listen for the SPAWNPIPE event
	"""
	global game_active
	global bird_movement
	global bird_rect
	global SPAWNPIPE
	global score

	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			sys.exit()

		elif event.type==pygame.KEYDOWN:
			if event.key==pygame.K_SPACE:
				if(not game_active):
					game_active=True
					score=0
				else:
					bird_movement=6
		if(game_active):
			if event.type==SPAWNPIPE:
				create_pipe()


def update_bird(pipe_list):
	"""
	Update the postion of the bird, update the bird_movement variable for gravity, 
	check for collisions with the pipes
	"""
	global bird_surface
	global bird_rect
	global bird_movement
	global screen
	bird_rect.centery -=bird_movement
	bird_movement-=gravity
	screen.blit(bird_surface,bird_rect)

	for pipes in pipe_list:
		check_collision(pipes)
		break

def update_pipes():
	"""
	Using the above defined functions, move, remove and draw the pipes
	"""
	global pipe_list
	global floor_x_pos

	for pipes in pipe_list:
		move_pipes(pipes)
		remove_pipes(pipes)
		draw_pipes(pipes)

def update_score():
	"""
	Update the score if the bird has passed through the opening
	"""
	global pipe_list
	global bird_rect
	global score
	for pipes in pipe_list:
		if(bird_rect.left==pipes[1].right):
			score+=1

while True:
	check_for_events()
	screen.blit(bg_surface,(0,0))

	if game_active:
		update_bird(pipe_list)
		update_pipes()

		update_score()
		score_display('main_game')
		
	else:
		screen.blit(game_over_surface,game_over_rect)
		score_display('game_over')


	# Change the position of the floor and draw it. Make sure if it reaches the left end reset it
	
	draw_floor()


	

	pygame.display.flip()

	# set the speed of the game
	clock.tick(120)