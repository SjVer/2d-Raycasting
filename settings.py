class Settings:
	"""Settings for raycasting project"""

	def __init__(self):
		import sys, math
		sys.path.append('/home/sjoerdv/python/modules')
		import easycolors as colors
		
		"""Init. attributes"""

		# WINDOW
		self.window_width = 1200
		self.window_height = 600 
		self.bg_color = colors.grey
		self.gridlinewidth = 1
		self.added_at_bordercheck = 5
		self.max_wall_dist = 1

		# RENDERING
		self.FOV = math.radians(45)		
		self.res = 3 # res 3 and FOV 45 is good
		self.wall_height_divider = 1.3
		self.wall_color = colors.green
		self.sky_color = colors.grey
		self.ground_color = colors.blue
		self.color_scalar = 60

		# PLAYER
		self.playerradius = 5
		self.playerstartx = 283
		self.playerstarty = 232
		self.playerstartangle = math.radians(90)
		self.walk_speed = 5
		self.turn_speed = 0.05

		# GAME
		self.active = True
		self.map_number = 3

	def get_square(self, xpos, ypos):
		 """Get size and pos of squares"""
		 import maps

		 width = self.window_width / 2 / maps.mapsize[0]
		 height = self.window_height / maps.mapsize[1]

		 x = xpos * width
		 y = ypos * height

		 return x, y, width, height

	def get_size(self, xpos, ypos):
		"""Get square size for calcs"""
		import maps

		width = self.window_width / 2 / maps.mapsize[0]
		height = self.window_height / maps.mapsize[1]

		return (width, height)

