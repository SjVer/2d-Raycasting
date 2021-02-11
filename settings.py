class Settings:
	"""Settings for raycasting project"""

	def __init__(self):
		import sys, math
		sys.path.append('/home/sjoerdv/python/modules')
		from colors import Colors
		colors = Colors()
		
		"""Init. attributes"""

		# WINDOW
		self.window_width = 1000
		self.window_height = 500 
		self.bg_color = colors.grey
		self.gridlinewidth = 1

		# RENDERING
		self.FOV = math.radians(75)
		self.res = 1 # amount of rays per degree of FOV

		# PLAYER
		self.playerradius = 5
		self.playerstartx = 250
		self.playerstarty = 250
		self.playerstartangle = 2*math.pi
		self.walk_speed = 2
		self.turn_speed = 0.025
		self.wall_test_distance = 5	 # min. distance to wall before blocked

		# GAME
		self.active = True
		self.map_number = 1

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

