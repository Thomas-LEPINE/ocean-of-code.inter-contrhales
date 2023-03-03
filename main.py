import sys
import random

class Game:

	def __init__(self, matrix):
		self.matrix = matrix
		self.life = 6

		# temporaire, choix des coordonnés de départ random
		x = random.randint(0, 14)
		y = random.randint(0, 14)
		self.my_position_x = x
		self.my_position_y = y

		while not self.can_move(x, y):
			x = random.randint(0, 14)
			y = random.randint(0, 14)
		self.set_my_position(x, y)
		self.update_matrix_point(y, x, 1)

	def set_my_position(self, x, y):
		self.my_position_x = x
		self.my_position_y = y

	def update_matrix_point(self, x, y, value):
		self.matrix[x][y] = value

	def can_move(self, x, y, way='Z'):
		if way == 'N':
			y = y - 1
		elif way == 'S':
			y = y + 1
		elif way == 'E':
			x = x + 1
		elif way == 'W':
			x = x - 1

		# vérification si coordonnées dans les limites et si jamais passé dessus ou île
		return x >= 0 and x <= 14 and y >= 0 and y <= 14 and self.matrix[y][x] == 0

	def manhattan_distance(self, x, y):
		distance = 0
		for p_i,q_i in zip([self.my_position_x, self.my_position_y], [x, y]):
			distance += abs(p_i - q_i)
		return distance

	def list_torpedable(self):
		list_torpedables = []
		for x in range(0, 14):
			for y in range(0, 14):
				# on vérifie que ce n'est pas une ile et que c'est à une distance de manhattan max 4
				if self.matrix[y][x] != 2 and self.manhattan_distance(x, y) <= 4 and self.manhattan_distance(x, y) > 1:
					list_torpedables.append([x, y])
		return list_torpedables

	def torpedo(self):
		shoot_position = random.choice(self.list_torpedable())
		print("TORPEDO", shoot_position[0], shoot_position[1])

	def move(self, way):
		if way == 'N':
			self.set_my_position(self.my_position_x, self.my_position_y - 1)
		elif way == 'S':
			self.set_my_position(self.my_position_x, self.my_position_y + 1)
		elif way == 'E':
			self.set_my_position(self.my_position_x + 1, self.my_position_y)
		elif way == 'W':
			self.set_my_position(self.my_position_x - 1, self.my_position_y)

		self.matrix[self.my_position_y][self.my_position_x] = 1
		print("MOVE", way, "TORPEDO")

	def surface(self):
		for x in range(0, 14):
			for y in range(0, 14):
				if self.matrix[x][y] == 1 and x != self.my_position_x and y != self.my_position_y:
					self.update_matrix_point(x, y, 0)
		print("SURFACE")

matrix = []

width, height, my_id = [int(i) for i in input().split()]
for i in range(height):
	line = input()
	matrix.append([eval(i) for i in [*line.replace('.', '0').replace('x', '2')]])

# print(matrix, file=sys.stderr, flush=True)

game = Game(matrix)

print(game.my_position_x, game.my_position_y)

# game loop
while True:
	x, y, my_life, opp_life, torpedo_cooldown, sonar_cooldown, silence_cooldown, mine_cooldown = [int(i) for i in input().split()]
	sonar_result = input()
	opponent_orders = input()
	print("MY LIFE : " + str(my_life), file=sys.stderr, flush=True)
	print("OPP LIFE : " + str(opp_life), file=sys.stderr, flush=True)

	cardinality = ['N','S','E','W']
	game.life = my_life

	# for line in game.matrix:
	#	print(*line, file=sys.stderr, flush=True)

	# print(toperdo_cooldown, file=sys.stderr, flush=True)
	game.set_my_position(x, y)
	if torpedo_cooldown == 0:
		game.torpedo()
	else :
		direction = random.choice(cardinality)
		while not game.can_move(x, y, direction):
			cardinality.remove(direction)
			# s'il n'y a plus de possibilité, on fait un surface
			if not cardinality:
				game.surface()
				break
			direction = random.choice(cardinality)
		if cardinality:
			game.move(direction)