import sys
import random
import math

# print(matrix, file=sys.stderr, flush=True) -> debug

class Game:

	def __init__(self, matrix):
		self.matrix = matrix
		self.life = 6

		# Choix des coordonnés de départ random
		x = random.randint(0, 14)
		y = random.randint(0, 14)
		while not self.can_move(x, y):
			x = random.randint(0, 14)
			y = random.randint(0, 14)
		self.set_my_position(x, y)
		self.update_matrix_point(x, y, 1)

	def set_my_position(self, x, y):
		self.my_position_x = x
		self.my_position_y = y

	def update_matrix_point(self, x, y, value):
		self.matrix[y][x] = value

	def can_move(self, x, y, way='NA'):
		if way == 'N':
			y = y - 1
		elif way == 'S':
			y = y + 1
		elif way == 'E':
			x = x + 1
		elif way == 'W':
			x = x - 1

		# Vérification si coordonnées dans les limites et si jamais passé dessus ou île
		return x >= 0 and x <= 14 and y >= 0 and y <= 14 and self.matrix[y][x] == 0

	def euclidean_ditance(self, x, y):
		euclidean_ditance = int(math.sqrt((y-self.my_position_y)**2 + (x-self.my_position_x)**2))
		return euclidean_ditance

	def manhattan_distance(self, x, y):
		manhattan_distance = 0
		for p_i,q_i in zip([self.my_position_x, self.my_position_y], [x, y]):
			manhattan_distance += abs(p_i - q_i)
		return manhattan_distance

	def list_torpedable(self):
		list_torpedables = []
		for x in range(max(self.my_position_x - 4, 0), min(self.my_position_x + 4, len(matrix))):
			for y in range(max(self.my_position_y - 4, 0), min(self.my_position_y + 4, len(matrix))):
				# On vérifie que ce n'est pas une ile et que c'est à une distance de manhattan max 4 et min 2 (évite de s'auto bombarder)
				if self.matrix[y][x] != 2 and self.euclidean_ditance(x, y) >= 2 and self.manhattan_distance(x, y) <= 4:
					list_torpedables.append([x, y])
		return list_torpedables

	def torpedo(self):
		shoot_position = random.choice(self.list_torpedable())
		return 'TORPEDO ' + str(shoot_position[0]) + ' ' + str(shoot_position[1])

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
		return 'MOVE ' + str(way) + ' TORPEDO'

	def surface(self):
		# On vide les cases visitées (surface => réinitialisation du chemin)
		for x in range(0, len(matrix)):
			for y in range(0, len(matrix)):
				if self.matrix[y][x] == 1:
					self.update_matrix_point(x, y, 0)
		self.matrix[self.my_position_y][self.my_position_x] = 1 # On remet "1" dans la case où l'on se trouve
		return 'SURFACE'

matrix = []

width, height, my_id = [int(i) for i in input().split()]
for i in range(height):
	line = input()
	matrix.append([eval(i) for i in [*line.replace('.', '0').replace('x', '2')]]) # 2 = il y a une île

# ------------------------------------------------------
# Starting the game
game = Game(matrix)
print(game.my_position_x, game.my_position_y)

# GAME LOOP
while True:
	x, y, my_life, opp_life, torpedo_cooldown, sonar_cooldown, silence_cooldown, mine_cooldown = [int(i) for i in input().split()]
	
	sonar_result = input()
	opponent_orders = input()
	print("MY LIFE : " + str(my_life), file=sys.stderr, flush=True)
	print("OPP LIFE : " + str(opp_life), file=sys.stderr, flush=True)
	action = '' # The action to do each turn
	cardinality = ['N','S','E','W']
	game.life = my_life

	game.set_my_position(x, y)
	if torpedo_cooldown == 0:
		action += game.torpedo() + ' | '

	direction = random.choice(cardinality)
	while not game.can_move(game.my_position_x, game.my_position_y, direction):
		cardinality.remove(direction)
		# S'il n'y a plus de possibilité, on fait un surface
		if not cardinality: 
			action = game.surface()
			break
		direction = random.choice(cardinality)
	if cardinality:
		action += game.move(direction)
	print(action)

# BUGS :
#  Est déjà revenu sur la case précédente (délai pour intégrer dans la matrice le "1" ?)
#  S'est placé sur une êle ... while à vérifier (prendre dans le tableau)
#  Chemin de torpille ne doit pas passer par une île
#  Concatener les messages pour faire plus d'action --> RIEN dans les méthodes !
