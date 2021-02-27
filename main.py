# IMPORTING
import pygame, time, os, sys, math
pygame.font.init()
pygame.mixer.init()
pygame.init()
sys.setrecursionlimit(10000)
clock = pygame.time.Clock()
sys.path.append('/home/sjoerdv/python/modules')
import easycolors as colors
from settings import Settings
settings = Settings()
import maps

# CONTSTANTS
WIN = pygame.display.set_mode((settings.window_width, settings.window_height))
pygame.display.set_caption("Raycasting")
FONT = pygame.font.SysFont(os.path.join('fonts', 'OpenSans-Regular.ttf'), 20)

# VARIABLES
playerX = settings.playerstartx
playerY = settings.playerstarty
angle = 0
down = False
up = False
left = False
right = False

# FUNCTIONS
def draw_map(map_number):
	"""Draws the given map"""
	ypos = 0
	for column in maps.maps[map_number-1]:
		xpos = 0
		for square in column:
			
			# read color
			if square == 1:
				color = colors.white
			elif square == 2:
				color = colors.green
			elif square == 3:
				color = colors.red
			else:
				color = colors.black

			# draw squares
			square = settings.get_square(xpos, ypos)
			pygame.draw.rect(WIN, color, square, 0)

			# draw grid
			if xpos > 0:
				pygame.draw.line(WIN, colors.grey, (square[0] - settings.gridlinewidth / 2, 0), (square[0] - settings.gridlinewidth / 2 , settings.window_height) , settings.gridlinewidth)
			if ypos > 0:
				pygame.draw.line(WIN, colors.grey, (0, square[1] - settings.gridlinewidth / 2), (settings.window_width, square[1] - settings.gridlinewidth / 2), settings.gridlinewidth)
			
			xpos += 1
		ypos += 1

def draw_player(playerX, playerY, angle):
	pygame.draw.circle(WIN, colors.yellow, (playerX, playerY), settings.playerradius)


def draw_window(map_number=1, playerX=settings.playerstartx, playerY=settings.playerstarty, angle=0):
	draw_map(map_number)
	draw_player(playerX, playerY, angle)

	draw_view()

	pygame.display.flip()

def check_events(playerX, playerY, angle):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			break

		if event.type == pygame.KEYDOWN:
			# key down
			if event.key == pygame.K_w:
				up = True
				break
			if event.key == pygame.K_s:
				down = True
				break
		if event.type == pygame.KEYUP:
			# key up
			if event.key == pygame.K_w:
				up = False
				break
			if event.key == pygame.K_s:
				down = False
				break

	if up:
		playerY -= settings.walk_speed
	if down:
		playerY += settings.walk_speed

	return playerX, playerY, angle


# MAIN GAME LOOP
while True:
	playerX, playerY, angle = check_events(playerX, playerY, angle)
	draw_window(1, playerX, playerY, angle)
