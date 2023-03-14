import sys
import random
import math
import copy

def euclidean_distance(x1, y1, x2, y2):
	euclidean_distance = int(math.sqrt((y2 - y1)**2 + (x2 - x1)**2))
	return euclidean_distance

def manhattan_distance(x1, y1, x2, y2):
	manhattan_distance = 0
	for p_i,q_i in zip([x1, y1], [x2, y2]):
		manhattan_distance += abs(p_i - q_i)
	return manhattan_distance

class Game:

	def __init__(self, matrix):
		self.my_matrix = matrix
		self.opp_matrix = copy.deepcopy(matrix)
		self.set_opp_position(-1, -1)
		self.found_opp_position = False

		# Choix des coordonnés de départ random
		x = random.randint(0, 14)
		y = random.randint(0, 14)
		while not can_move(self.my_matrix, x, y):
			x = random.randint(0, 14)
			y = random.randint(0, 14)
		self.set_my_position(x, y)
		self.update_my_matrix(x, y, 1)

	def set_my_position(self, x, y):
		self.my_position_x = x
		self.my_position_y = y

	def set_opp_position(self, x, y):
		self.opp_position_x = x
		self.opp_position_x = y
	
	def update_my_matrix(self, x, y, value):
		self.my_matrix[y][x] = value
	
	def update_opp_matrix(self, x, y, value):
		self.opp_matrix[y][x] = value

	def list_torpedable(self):
		list_torpedables = []
		for x in range(max(self.my_position_x - 4, 0), min(self.my_position_x + 4, 15)):
			for y in range(max(self.my_position_y - 4, 0), min(self.my_position_y + 4, 15)):
				# On vérifie que ce n'est pas une ile et que c'est à une distance de manhattan max 4 et min 2 (évite de s'auto bombarder)
				if self.my_matrix[y][x] != 2 and euclidean_distance(self.my_position_x, self.my_position_y, x, y) >= 2 and manhattan_distance(self.my_position_x, self.my_position_y, x, y) <= 4:
					list_torpedables.append([x, y])
		return list_torpedables

	def torpedo(self):
		shoot_position = random.choice(self.list_torpedable())
		return 'TORPEDO ' + str(shoot_position[0]) + ' ' + str(shoot_position[1])

	def move(self, way, type_charge='TORPEDO'):
		if way == 'N':
			self.set_my_position(self.my_position_x, self.my_position_y - 1)
		elif way == 'S':
			self.set_my_position(self.my_position_x, self.my_position_y + 1)
		elif way == 'E':
			self.set_my_position(self.my_position_x + 1, self.my_position_y)
		elif way == 'W':
			self.set_my_position(self.my_position_x - 1, self.my_position_y)

		self.update_my_matrix(self.my_position_x, self.my_position_y, 1)
		return 'MOVE ' + str(way) + ' ' + str(type_charge)

	def surface(self):
		# On vide les cases visitées (surface => réinitialisation du chemin)
		for x in range(15):
			for y in range(15):
				if self.my_matrix[y][x] == 1:
					self.update_my_matrix(x, y, 0)
		self.update_my_matrix(self.my_position_x, self.my_position_y, 1) # On remet "1" dans la case où l'on se trouve
		return 'SURFACE'

	# retourne la direction où il y a le plus de cases libres
	def best_direction(self, cardinality):
		best_cardinality = cardinality[0]
		max_count = 0
		for card in cardinality:
			count = 0
			if card == 'N':
				for i in range (15):
					for j in range(0, self.my_position_y - 1):
						if self.my_matrix[j][i] == 0:
							count += 1
			elif card == 'S':
				for i in range (15):
					for j in range(self.my_position_y + 1, 15):
						if self.my_matrix[j][i] == 0:
							count += 1
			elif card == 'E':
				for i in range (self.my_position_x + 1, 15):
					for j in range(15):
						if self.my_matrix[j][i] == 0:
							count += 1
			elif card == 'W':
				for i in range (0, self.my_position_x - 1):
					for j in range(15):
						if self.my_matrix[j][i] == 0:
							count += 1
			if count > max_count:
				max_count = count
				best_cardinality = card

		return best_cardinality

def can_move(matrix, x, y, way='NA'):
	if way == 'N':
		y = y - 1
	elif way == 'S':
		y = y + 1
	elif way == 'E':
		x = x + 1
	elif way == 'W':
		x = x - 1

	# Vérification si coordonnées dans les limites et si jamais passé dessus ou île
	return x >= 0 and x <= 14 and y >= 0 and y <= 14 and matrix[y][x] == 0


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
	game.set_my_position(x, y)

	action = ''

	if torpedo_cooldown == 0:
		action += game.torpedo() + '|'

	possible_cardinality = []
	for card in cardinality:
		if can_move(game.my_matrix, game.my_position_x, game.my_position_y, card):
			possible_cardinality.append(card)

	# Si on peut se déplacer, on va dans la meilleure direction
	if possible_cardinality:
		direction = game.best_direction(possible_cardinality)
		action += game.move(direction)
	# Sinon on fait surface
	else:
		action += game.surface()
	
	print(action)

# BUGS :
#  Est déjà revenu sur la case précédente (délai pour intégrer dans la matrice le "1" ?)
#  S'est placé sur une êle ... while à vérifier (prendre dans le tableau)
#  Chemin de torpille ne doit pas passer par une île