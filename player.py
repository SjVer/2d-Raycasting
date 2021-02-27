import pygame, sys, math, os, time, maps, numpy
sys.path.append('/home/sjoerdv/python/modules')
import easycolors as colors
from goto import with_goto

class Player():
    """A class to manage the ship."""
 
    def __init__(self, game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.WIN = game.WIN
        self.settings = game.settings
        self.WIN_rect = game.WIN.get_rect()
        self.map_number = game.settings.map_number
        self.distances = []

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

        # direction flags
        self.dir_up = False
        self.dir_down = False
        self.dir_left = False
        self.dir_right = False

        self.FONT = pygame.font.SysFont(os.path.join('fonts', 'OpenSans-Regular.ttf'), 20)

    def update(self):
        """Update the player's position based on movement flags."""
        if self.moving_right:
            #self.x += self.settings.walk_speed
            dx = math.cos(-1*(self.angle-math.pi))*self.settings.walk_speed
            dy = math.sin(-1*(self.angle-math.pi))*self.settings.walk_speed
            if not self.find_cell(self.x + dx * self.settings.max_wall_dist, self.y + dy * self.settings.max_wall_dist):
                self.x += dx
                self.y += dy

        if self.moving_left:
            #self.x -= self.settings.walk_speed
            dx = math.cos(-1*(self.angle))*self.settings.walk_speed
            dy = math.sin(-1*(self.angle))*self.settings.walk_speed
            if not self.find_cell(self.x + dx * self.settings.max_wall_dist, self.y + dy * self.settings.max_wall_dist):
                self.x += dx
                self.y += dy

        if self.moving_up:
            #self.y += self.settings.walk_speed
            dx = math.cos(-1*(self.angle-math.pi/2))*self.settings.walk_speed
            dy = math.sin(-1*(self.angle-math.pi/2))*self.settings.walk_speed
            if not self.find_cell(self.x + dx * self.settings.max_wall_dist, self.y + dy * self.settings.max_wall_dist):
                self.x += dx
                self.y += dy

        if self.moving_down:
            #self.y -= self.settings.walk_speed
            dx = math.cos(-1*(self.angle-math.pi/2))*self.settings.walk_speed
            dy = math.sin(-1*(self.angle-math.pi/2))*self.settings.walk_speed
            if not self.find_cell(self.x - dx * self.settings.max_wall_dist, self.y - dy * self.settings.max_wall_dist):
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
        try:
            if maps.maps[self.map_number-1][yi][xi]:
                cell_is_wall = True
            else:
                cell_is_wall = False
            return cell_is_wall
        except IndexError:
            return True

    def find_cell_pos(self):
        self.deltaX = self.x % self.settings.get_size(self.x, self.y)[0]
        self.deltaY = self.y % self.settings.get_size(self.x, self.y)[1]

        # Get cell number 
        self.xi = int((self.x - self.deltaX) / self.settings.get_size(self.x, self.y)[0])
        self.yi = int((self.y - self.deltaY) / self.settings.get_size(self.x, self.y)[1])            

    def cell_border_check(self, direct, x, y):
        """Find the contents of a cell based any of its borders"""
        if direct == "up":
            return self.find_cell(x, y-self.settings.added_at_bordercheck)
        if direct == "down":
            return self.find_cell(x, y+self.settings.added_at_bordercheck)
        if direct == "left":
            return self.find_cell(x-self.settings.added_at_bordercheck, y)
        if direct == "right":
            return self.find_cell(x+self.settings.added_at_bordercheck, y)

    @with_goto
    def rays(self):

        self.distances = []

        step = math.radians(1)/self.settings.res
        for angle in numpy.arange(self.angle - self.settings.FOV/2, self.angle + self.settings.FOV/2, step):

            horshortestx = 0
            horshortesty = 0
            vershortestx = 0
            vershortesty = 0
            firstx, firsty = 0, 0
            self.dir_left = False
            self.dir_right = False
            self.dir_up = False
            self.dir_down = False
            newx, newy = 0, 0
            endx, endy = self.radius*math.sin(self.angle)+self.x, self.radius*math.cos(self.angle)+self.y
            #a = math.atan(( endx - self.x ) / ( endy - self.y))

            if angle > math.pi:    # Looking left
                self.dir_left = True
                self.dir_right = False
            if angle < math.pi:    # Looking right
                self.dir_left = False
                self.dir_right = True
            if angle > 0.5*math.pi and angle < 1.5*math.pi: # Looking up
                self.dir_up = True
                self.dir_down = False
            if angle < 0.5*math.pi or angle > 1.5*math.pi: # Looking down
                self.dir_down = True
                self.dir_up = False
            
            #angle = self.angle
            # CALCULATION FOR RAY HORIZONTAL:
            #angle = self.angle # should change with loop through FOV

            if self.dir_up: # UP:
                # first intersect:
                alpha = math.degrees(angle)-90

                firsty = self.deltaY
                try:     
                    firstx = self.deltaY/math.tan(alpha * math.pi / 180)
                except ZeroDivisionError:
                    firstx = self.deltaY
                    print('ZeroDivisionError')

                #pygame.draw.circle(self.WIN, colors.red, (self.x + firstx, self.y - firsty), 4)

                if self.cell_border_check("up", self.x + firstx, self.y - firsty):
                    #pygame.draw.line(self.WIN, colors.red,(self.x, self.y), (self.x + firstx, self.y - firsty), 1)
                    horshortestx, horshortesty = self.x + firstx, self.y - firsty
                    goto .gohere1

                # other intersects:
                for step in range(1, 10):

                    newy = self.y - firsty - self.settings.get_size(self.x, self.y)[1] * step
                    newx = self.x + firstx + (step * self.settings.get_size(self.x, self.y)[1]) / math.tan(alpha * math.pi / 180)

                    #pygame.draw.circle(self.WIN, colors.red, (newx, newy), 4)

                    if self.cell_border_check("up", newx, newy):
                        #pygame.draw.line(self.WIN, colors.red,(self.x, self.y), (newx, newy), 1)
                        horshortestx, horshortesty = newx, newy
                        break

            elif self.dir_down: # DOWN:
                # first intersect
                alpha = math.degrees(angle)-90

                firsty = self.settings.get_size(self.x, self.y)[1] - self.deltaY
                try:  
                    firstx = (self.settings.get_size(self.x, self.y)[1] - self.deltaY)/(math.tan(alpha * math.pi / 180) * -1)
                except ZeroDivisionError:
                    firstx = self.settings.get_size(self.x, self.y[1]) - self.deltaY
                    print('ZeroDivisionError')

                #pygame.draw.circle(self.WIN, colors.red, (self.x + firstx, self.y + firsty), 4)

                if self.cell_border_check("down", self.x + firstx, self.y + firsty):
                    #pygame.draw.line(self.WIN, colors.red,(self.x, self.y), (self.x + firstx, self.y + firsty), 1)
                    horshortestx, horshortesty = self.x + firstx, self.y + firsty
                    goto .gohere1

                # other intersects:
                for step in range(1, 10):

                    newy = self.y + firsty + self.settings.get_size(self.x, self.y)[1] * step
                    newx = self.x + firstx - (step * self.settings.get_size(self.x, self.y)[1]) / math.tan(alpha * math.pi / 180)

                    #pygame.draw.circle(self.WIN, colors.red, (newx, newy), 4)

                    if self.cell_border_check("down", newx, newy):
                        #pygame.draw.line(self.WIN, colors.red,(self.x, self.y), (newx, newy), 1)
                        horshortestx, horshortesty = newx, newy
                        break

            label .gohere1
            # CALCULATION FOR RAY VERTICAL:
            #angle = self.angle # should change with loop through FOV

            if self.dir_right: # RIGHT:
                # first intersect:
                alpha = math.degrees(angle)-90

                firstx = self.settings.get_size(self.x, self.y)[0] - self.deltaX
                firsty = (self.settings.get_size(self.x, self.y)[0] - self.deltaX) * (math.tan(-1*alpha * math.pi / 180) * -1)

                #pygame.draw.circle(self.WIN, colors.blue, (self.x + firstx, self.y - firsty), 4)

                if self.cell_border_check("right", self.x + firstx, self.y - firsty):
                    #pygame.draw.line(self.WIN, colors.blue,(self.x, self.y), (self.x + firstx, self.y - firsty), 1)
                    vershortestx, vershortesty = self.x + firstx, self.y - firsty
                    goto .gohere2

                # other intersects:
                for step in range(1, 10):
                    
                    newx = self.x + firstx + self.settings.get_size(self.x, self.y)[0] * step
                    newy = self.y - firsty - (step * self.settings.get_size(self.x, self.y)[0]) * math.tan(alpha * math.pi / 180)

                    #pygame.draw.circle(self.WIN, colors.blue, (newx, newy), 4)

                    if self.cell_border_check("right", newx, newy):
                        #pygame.draw.line(self.WIN, colors.blue,(self.x, self.y), (newx, newy), 1)
                        vershortestx, vershortesty = newx, newy
                        break

            elif self.dir_left: # LEFT:
                # first intersect:
                alpha = math.degrees(angle)-90

                firstx = self.deltaX
                firsty = self.deltaX * (math.tan(-1*alpha * math.pi / 180) * -1)

                #pygame.draw.circle(self.WIN, colors.blue, (self.x - firstx, self.y + firsty), 4)

                if self.cell_border_check("left", self.x - firstx, self.y + firsty):
                    #pygame.draw.line(self.WIN, colors.blue,(self.x, self.y), (self.x - firstx, self.y + firsty), 1)
                    vershortestx, vershortesty = self.x - firstx, self.y + firsty
                    goto .gohere2

                # other intersects:
                for step in range(1, 10):
                    
                    newx = self.x - firstx - self.settings.get_size(self.x, self.y)[0] * step
                    newy = self.y + firsty + (step * self.settings.get_size(self.x, self.y)[0]) * math.tan(alpha * math.pi / 180)

                    #pygame.draw.circle(self.WIN, colors.blue, (newx, newy), 4)

                    if self.cell_border_check("left", newx, newy):
                        #pygame.draw.line(self.WIN, colors.blue,(self.x, self.y), (newx, newy), 1)
                        vershortestx, vershortesty = newx, newy
                        break

            label .gohere2

            hordist = math.sqrt( (horshortestx - self.x)**2 + (horshortesty - self.y)**2 )
            verdist = math.sqrt( (vershortestx - self.x)**2 + (vershortesty - self.y)**2 )

            if hordist < verdist:
                shortestx, shortesty = horshortestx, horshortesty
                newdist = hordist * math.cos(self.angle - angle)
                #print(f"newdist: {newdist}      hordist: {hordist}")
                self.distances.append((newdist, "hor"))
            else:
                shortestx, shortesty = vershortestx, vershortesty
                newdist = verdist * math.cos(self.angle - angle)
                self.distances.append((newdist, "ver"))

            pygame.draw.line(self.WIN, colors.green, (self.x, self.y), (shortestx, shortesty), 1)


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
        text_surface = self.FONT.render(f"angle: {math.degrees(self.angle)-90}", True, colors.red)
        self.WIN.blit(text_surface, dest=(3,40))

    def center_player(self):
        """Put player on starting pos"""
        self.x = self.settings.playerstartx
        self.y = self.settings.playerstarty