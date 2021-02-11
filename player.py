import pygame, sys, math, os, time, maps
sys.path.append('/home/sjoerdv/python/modules')
from colors import Colors
colors = Colors()
 
class Player():
    """A class to manage the ship."""
 
    def __init__(self, game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.WIN = game.WIN
        self.settings = game.settings
        self.WIN_rect = game.WIN.get_rect()
        self.map_number = game.settings.map_number

        self.x = game.settings.playerstartx
        self.y = game.settings.playerstarty
        self.angle = game.settings.playerstartangle
        self.deltaX = game.settings.playerstartx % 50
        self.deltaY = game.settings.playerstarty % 50
        self.cell_is_wall = False
        self.xi = 0
        self.yi = 0
        self.radius = 1000

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.looking_left = False
        self.looking_right = False

        self.FONT = pygame.font.SysFont(os.path.join('fonts', 'OpenSans-Regular.ttf'), 20)

    def update(self):
        """Update the player's position based on movement flags."""
        if self.moving_right:
            #self.x += self.settings.walk_speed
            dx = math.cos(-1*(self.angle-math.pi))*self.settings.walk_speed
            dy = math.sin(-1*(self.angle-math.pi))*self.settings.walk_speed
            if not self.find_cell(self.x + dx, self.y + dy):
                self.x += dx
                self.y += dy

        if self.moving_left:
            #self.x -= self.settings.walk_speed
            dx = math.cos(-1*(self.angle))*self.settings.walk_speed
            dy = math.sin(-1*(self.angle))*self.settings.walk_speed
            if not self.find_cell(self.x + dx, self.y + dy):
                self.x += dx
                self.y += dy

        if self.moving_up:
            #self.y += self.settings.walk_speed
            dx = math.cos(-1*(self.angle-math.pi/2))*self.settings.walk_speed
            dy = math.sin(-1*(self.angle-math.pi/2))*self.settings.walk_speed
            if not self.find_cell(self.x + dx, self.y + dy):
                self.x += dx
                self.y += dy

        if self.moving_down:
            #self.y -= self.settings.walk_speed
            dx = math.cos(-1*(self.angle-math.pi/2))*self.settings.walk_speed
            dy = math.sin(-1*(self.angle-math.pi/2))*self.settings.walk_speed
            if not self.find_cell(self.x - dx, self.y - dy):
                self.x -= dx
                self.y -= dy

        # looking
        if self.looking_right:
            self.angle -= self.settings.turn_speed
            if self.angle < 0:
                self.angle = 2*math.pi

        if self.looking_left:
            self.angle += self.settings.turn_speed
            if self.angle > 2*math.pi:
                self.angle = 0

        self.cell_is_wall = self.find_cell(self.x, self.y)
        self.find_cell_pos()

    def find_cell(self, x, y):
        """Find the cell based on any coordinate"""

        # Get deltaX and deltaY
        deltaX = x % self.settings.get_size(x, y)[0]
        deltaY = y % self.settings.get_size(x, y)[1]

        # Get cell number 
        xi = int((x - deltaX) / self.settings.get_size(x, y)[0])
        yi = int((y - deltaY) / self.settings.get_size(x, y)[1])

        # Find cell content
        if maps.maps[self.map_number-1][yi][xi]:
            cell_is_wall = True
        else:
            cell_is_wall = False
        return cell_is_wall

    def find_cell_pos(self):
        self.deltaX = self.x % self.settings.get_size(self.x, self.y)[0]
        self.deltaY = self.y % self.settings.get_size(self.x, self.y)[1]

        # Get cell number 
        self.xi = int((self.x - self.deltaX) / self.settings.get_size(self.x, self.y)[0])
        self.yi = int((self.y - self.deltaY) / self.settings.get_size(self.x, self.y)[1])            

    def rays(self):
        
        endx, endy = self.radius*math.sin(self.angle)+self.x, self.radius*math.cos(self.angle)+self.y
        #a = math.atan(( endx - self.x ) / ( endy - self.y))

        print(self.deltaY)

        if self.angle > math.pi:    # Looking left
            pass
        if self.angle < math.pi:    # Looking right
            pass
        if self.angle > 0.5*math.pi and self.angle < 1.5*math.pi: # Looking up
            pass
        if self.angle < 0.5*math.pi or self.angle > 1.5*math.pi: # Looking down
            pass
        








        pygame.draw.line(self.WIN, colors.green,(self.x, self.y), (endx, endy), 1)


        """
        step = int(self.settings.FOV*1000/75)
        # loop through fov to cast rays
        for angle in range(int(self.angle*1000) - int(self.settings.FOV/2*1000), int(self.angle*1000) + int(self.settings.FOV/2*1000+1) + step, step):

            # find ending pos using looking direction and maths n shit
            endx, endy = self.radius*math.sin(angle/1000)+self.x, self.radius*math.cos(angle/1000)+self.y
            # draw ray
            pygame.draw.line(self.WIN, colors.green,(self.x, self.y), (endx, endy), 1)
            # find angle of ray relative to x axis
            a = math.atan(( endx - self.x ) / ( endy - self.y))
        """

    def drawme(self):
        """Draw the player and rays at its current location."""
        pygame.draw.circle(self.WIN, colors.yellow, (self.x, self.y), self.settings.playerradius)
        #pygame.draw.line(self.WIN, colors.red,(self.x, self.y), (self.radius*math.sin(self.angle)+self.x, self.radius*math.cos(self.angle)+self.y), 1)
        #pygame.draw.line(self.WIN, colors.red,(self.x, self.y), (self.radius*math.sin(self.angle-self.settings.FOV/2)+self.x, self.radius*math.cos(self.angle-self.settings.FOV/2)+self.y), 1)
        #pygame.draw.line(self.WIN, colors.red,(self.x, self.y), (self.radius*math.sin(self.angle+self.settings.FOV/2)+self.x, self.radius*math.cos(self.angle+self.settings.FOV/2)+self.y), 1)

        # text
        text_surface = self.FONT.render(f"({self.x}, {self.y})", True, colors.red)
        self.WIN.blit(text_surface, dest=(3,0))
        text_surface = self.FONT.render(f"cell: ({self.xi}, {self.yi})  wall: {self.cell_is_wall}", True, colors.red)
        self.WIN.blit(text_surface, dest=(3,20))
        text_surface = self.FONT.render(f"angle: {math.degrees(self.angle)}", True, colors.red)
        self.WIN.blit(text_surface, dest=(3,40))

    def center_player(self):
        """Put player on starting pos"""
        self.x = self.settings.playerstartx
        self.y = self.settings.playerstarty