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

def get_section(x, y):
	if x < 5 and y < 5 :
		return 1
	elif x >= 5 and x < 10 and y < 5:
		return 2
	elif x >= 10 and x < 15 and y < 5:
		return 3
	elif x < 5 and y >= 5 and y < 10:
		return 4
	elif x >= 5 and x < 10 and y >= 5 and y < 10:
		return 5
	elif x >= 10 and x < 15 and y >= 5 and y < 10:
		return 6
	elif x < 5 and y >= 10 and y < 15:
		return 7
	elif x > 5 and x <= 10 and y >= 10 and y < 15:
		return 8
	elif x > 10 and x <= 15 and y >= 10 and y < 15:
		return 9
	return -1

class Game:

	def __init__(self, matrix):
		self.my_matrix = matrix
		self.opp_matrix = copy.deepcopy(matrix)
		self.opp_moves = []

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
		list_torpedable = []
		for x in range(max(self.my_position_x - 4, 0), min(self.my_position_x + 4, 15)):
			for y in range(max(self.my_position_y - 4, 0), min(self.my_position_y + 4, 15)):
				# On vérifie que ce n'est pas une ile et que c'est à une distance de manhattan max 4 et min 2 (évite de s'auto bombarder)
				if self.my_matrix[y][x] != 2 and euclidean_distance(self.my_position_x, self.my_position_y, x, y) >= 2 and manhattan_distance(self.my_position_x, self.my_position_y, x, y) <= 4:
					list_torpedable.append([x, y])
		return list_torpedable

	def torpedo(self, list_possible_opp_position):
		# on récupère la liste d'où on peut tirer
		list_torpedable = self.list_torpedable()

		list_shoot = []
		# on recherche les torpedo qui sont dans les positions possibles de l'opp
		for torpedo in list_torpedable:
			if torpedo in list_possible_opp_position:
				list_shoot.append(torpedo)
		# s'il y a des possibilites, on shoot random dans les possibilites
		shoot_position = ''
		if list_shoot:
			shoot_position = random.choice(list_shoot)
		# sinon on shoot random
		else:
			shoot_position = random.choice(list_torpedable)

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
				j = self.my_position_y - 1
				while j >= 0 and self.my_matrix[j][self.my_position_x] == 0:
					count += 1
					j -= 1
			elif card == 'S':
				j = self.my_position_y + 1
				while j <= 14 and self.my_matrix[j][self.my_position_x] == 0:
					count += 1
					j += 1
			elif card == 'E':
				i = self.my_position_x + 1
				while i <= 14 and self.my_matrix[self.my_position_y][i] == 0:
					count += 1
					i += 1
			elif card == 'W':
				i = self.my_position_x - 1
				while i >= 0 and self.my_matrix[self.my_position_y][i] == 0:
					count += 1
					i -= 1
			if count > max_count:
				max_count = count
				best_cardinality = card

		return best_cardinality
	
	def silence(self, way, dist):
		if way == 'N':
			self.set_my_position(self.my_position_x, self.my_position_y - dist)
		elif way == 'S':
			self.set_my_position(self.my_position_x, self.my_position_y + dist)
		elif way == 'E':
			self.set_my_position(self.my_position_x + dist, self.my_position_y)
		elif way == 'W':
			self.set_my_position(self.my_position_x - dist, self.my_position_y)

		return 'SILENCE ' + way + ' ' + str(dist)

	# on simule le parcours de l'opp pour chaque case et on retourne les cases possibles
	def get_possible_opp_position(self):
		possibilities = []
		for i in range(15):
			for j in range(15):
				if self.opp_matrix[j][i] == 0:
					x = i
					y = j
					not_possible = []
					for way in self.opp_moves:
						if way == 'N':
							y -= 1
						elif way == 'S':
							y += 1
						elif way == 'E':
							x += 1
						elif way == 'W':
							x -= 1
						if not can_move(self.opp_matrix, x, y) or [x, y] in not_possible:
							break
						else:
							not_possible.append([x, y])
					if can_move(self.opp_matrix, x, y):
						possibilities.append([x, y])

		return possibilities


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

matrix_opp = copy.deepcopy(matrix)
# ------------------------------------------------------
# Starting the game
game = Game(matrix)
print(game.my_position_x, game.my_position_y)

# GAME LOOP
while True:
	x, y, my_life, opp_life, torpedo_cooldown, sonar_cooldown, silence_cooldown, mine_cooldown = [int(i) for i in input().split()]
	
	sonar_result = input()
	opponent_orders = input()

	opp_section = ''

	if "MOVE" in opponent_orders:
		game.opp_moves.append(opponent_orders.partition("MOVE")[2][1])

	# si l'opp fait SURFACE, on réduit les possibilités de sa position
	if "SURFACE" in opponent_orders:
		opp_section = opponent_orders.partition("SURFACE")[2][1]
		for i in range(15):
			for j in range(15):
				if game.opp_matrix[j][i] == 0 and get_section(i, j) != opp_section:
					game.update_opp_matrix(i, j, 1)
	
	# si l'opp fait SILENCE, on réinitialise la recherche de sa position
	if "SILENCE" in opponent_orders and "SILENCE" not in opponent_orders.partition("MOVE")[2]:
		game.opp_moves = []
		game.opp_matrix = copy.deepcopy(matrix_opp)
	
	# if "TORPEDO" in opponent_orders and not "TORPEDO" in opponent_orders.partition("MOVE")[1]:
	# s'il fait TORPEDO, chercher sa possible position dans un rayon de 4 ?
	

	print("MY LIFE : " + str(my_life), file=sys.stderr, flush=True)
	print("OPP LIFE : " + str(opp_life), file=sys.stderr, flush=True)
	action = '' # The action to do each turn
	cardinality = ['N','S','E','W']
	game.set_my_position(x, y)

	action = ''

	# si on peut tirer
	if torpedo_cooldown == 0:
		possible_opp_positions = game.get_possible_opp_position()
		# et qu'on a trouvé l'opp, on lui tire dessus
		if len(possible_opp_positions) == 1:
			action += "TORPEDO " + str(possible_opp_positions[0][0]) + " " + str(possible_opp_positions[0][1]) + " | "
		else:
			# sinon on tire aléatoirement dans toutes les possibilitiés
			action += game.torpedo(possible_opp_positions) + ' | '

	# recherche de où on peut se déplacer
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