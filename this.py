# IMPORTING
import pygame, time, os, sys, math
pygame.font.init()
pygame.mixer.init()
pygame.init()
sys.setrecursionlimit(10000)
clock = pygame.time.Clock()
sys.path.append('/home/sjoerdv/python/modules')
from colors import Colors
colors = Colors()
from settings import Settings
settings = Settings()
import maps
from player import Player

class Raycasting:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        self.running = True
        pygame.init()
        self.settings = Settings()

        self.WIN = pygame.display.set_mode((settings.window_width, settings.window_height))
        pygame.display.set_caption("Raycasting")
        self.FONT = pygame.font.SysFont(os.path.join('fonts', 'OpenSans-Regular.ttf'), 20)

        #create player
        self.player = Player(self)

        # map number
        self.map_number = self.settings.map_number

    def run_game(self):
        """Start the main loop for the game."""
        while self.running:
            self._check_events()

            if self.settings.active:
                self.player.update()
                self._update_rays()

            self._update_screen()
        sys.exit()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_s:
            self.player.moving_down = True
        elif event.key == pygame.K_w:
            self.player.moving_up = True
        elif event.key == pygame.K_a:
            self.player.moving_left = True
        elif event.key == pygame.K_d:
            self.player.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.player.looking_left = True
        elif event.key == pygame.K_RIGHT:
            self.player.looking_right = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_s:
            self.player.moving_down = False
        elif event.key == pygame.K_w:
            self.player.moving_up = False
        elif event.key == pygame.K_a:
            self.player.moving_left = False
        elif event.key == pygame.K_d:
            self.player.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.player.looking_left = False
        elif event.key == pygame.K_RIGHT:
            self.player.looking_right = False

    def _update_rays(self):
        pass

    def draw_map(self):
        """Draws the given map"""
        ypos = 0
        for column in maps.maps[self.map_number-1]:
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
                pygame.draw.rect(self.WIN, color, square, 0)

                # draw grid
                if xpos > 0:
                    pygame.draw.line(self.WIN, colors.grey, (square[0] - settings.gridlinewidth / 2, 0), (square[0] - settings.gridlinewidth / 2 , settings.window_height) , settings.gridlinewidth)
                if ypos > 0:
                    pygame.draw.line(self.WIN, colors.grey, (0, square[1] - settings.gridlinewidth / 2), (settings.window_width/2, square[1] - settings.gridlinewidth / 2), settings.gridlinewidth)
            
                xpos += 1
            ypos += 1

    def draw_view(self):
        pygame.draw.rect(self.WIN, colors.grey, (self.settings.window_width/2, 0, self.settings.window_width/2, self.settings.window_height/2), 0)
        pygame.draw.rect(self.WIN, colors.darkgrey, (self.settings.window_width/2, self.settings.window_height/2, self.settings.window_width/2, self.settings.window_height/2), 0)
        pygame.draw.line(self.WIN, colors.black, (self.settings.window_width/2-1, 0), (self.settings.window_width/2-1, self.settings.window_height), 2)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.WIN.fill(self.settings.bg_color)
        self.draw_map()
        self.player.drawme()
        self.player.rays()
        self.draw_view()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    game = Raycasting()
    game.run_game()