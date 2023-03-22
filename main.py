import sys
import random
import math
import copy

# print(matrix, file=sys.stderr, flush=True) -> debug

def euclidean_distance(x1: int, y1: int, x2: int, y2: int) -> float:
    euclidean_distance = int(math.sqrt((y2 - y1)**2 + (x2 - x1)**2))
    return euclidean_distance

def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    manhattan_distance = 0
    for p_i,q_i in zip([x1, y1], [x2, y2]):
        manhattan_distance += abs(p_i - q_i)
    return manhattan_distance

def can_move(matrix: list, x: int, y: int, way: str = 'NA', distance: int = 1) -> bool:
    if way == 'N':
        y = y - distance
    elif way == 'S':
        y = y + distance
    elif way == 'E':
        x = x + distance
    elif way == 'W':
        x = x - distance
    # Vérification si coordonnées dans les limites et si jamais passé dessus ou île
    return x >= 0 and x <= 14 and y >= 0 and y <= 14 and matrix[y][x] == 0

def can_move_distance(matrix: list, x: int, y: int, way: str, distance: int = 1) -> bool:
    for dist in range(1, distance + 1)[::-1]:
        if not can_move(matrix, x, y, way, dist):
            return False
    return True

def get_section(x: int, y: int) -> int:
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
    else:
        return -1

def opponent_orders_managing(opponent_orders: str) -> None:
    # print(str(opponent_orders), file=sys.stderr, flush=True)
    if 'MOVE' in opponent_orders:
        game.opp_moves.append(opponent_orders.partition('MOVE')[2][1])

    # Si l'opp fait SURFACE, on réduit les possibilités de sa position
    if 'SURFACE' in opponent_orders:
        opp_section = opponent_orders.partition('SURFACE')[2][1]
        for i in range(15):
            for j in range(15):
                if game.opp_matrix[j][i] == 0 and get_section(i, j) != opp_section:
                    game.update_opp_matrix(i, j, 1)
    
    # Si l'opp fait SILENCE, on réinitialise la recherche de sa position
    if 'SILENCE' in opponent_orders and "SILENCE" not in opponent_orders.partition('MOVE')[2]:
        game.opp_moves = []
        game.reset_matrix(game.opp_matrix, False)

    # TODO : récupérer l'ordre s'il a tiré !

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

    def set_my_position(self, x: int, y: int) -> None:
        self.my_position_x = x
        self.my_position_y = y
    
    def set_opp_position(self, x: int, y: int) -> None:
        self.opp_position_x = x
        self.opp_position_x = y
    
    def update_my_matrix(self, x: int, y: int, value: int) -> None:
        self.my_matrix[y][x] = value
    
    def update_opp_matrix(self, x: int, y: int, value: int) -> None:
        self.opp_matrix[y][x] = value
    
    def list_torpedable(self) -> list:
        list_torpedable = []
        for x in range(max(self.my_position_x - 4, 0), min(self.my_position_x + 4, 15)):
            for y in range(max(self.my_position_y - 4, 0), min(self.my_position_y + 4, 15)):
                # On vérifie que ce n'est pas une ile et que c'est à une distance de manhattan max 4 et min 2 (évite de s'auto bombarder)
                if self.my_matrix[y][x] != 2 and euclidean_distance(self.my_position_x, self.my_position_y, x, y) >= 2 and manhattan_distance(self.my_position_x, self.my_position_y, x, y) <= 4:
                    list_torpedable.append([x, y])
        return list_torpedable

    def list_torpedable_opp(self, list_possible_opp_position: list, list_torpedable: list = []) -> list:
        list_shoot = []
        if len(list_torpedable) == 0:
            list_torpedable = self.list_torpedable()
        # On recherche les torpedo qui sont dans les positions possibles de l'opp
        for torpedo in list_torpedable:
            if torpedo in list_possible_opp_position:
                list_shoot.append(torpedo)
        return list_shoot

    # On récupère la liste d'où on peut tirer
    def torpedo(self, list_possible_opp_position: list) -> str:
        list_torpedable = self.list_torpedable()
        list_shoot = self.list_torpedable_opp(list_torpedable, list_possible_opp_position)
        shoot_position = ''
        if list_shoot: # S'il y a des possibilités, on shoot aléatoirement dans ces possibilites
            shoot_position = random.choice(list_shoot)
        else: # Sinon on shoot complètement aléatoirement
            shoot_position = random.choice(list_torpedable)

        return self.shoot_torpedo(shoot_position[0], shoot_position[1])
    
    def shoot_torpedo(self, shoot_position_x: int, shoot_position_y: int) -> str:
        return 'TORPEDO ' + str(shoot_position_x) + ' ' + str(shoot_position_y)

    def move(self, way: str, type_charge: str = 'TORPEDO') -> str:
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

    def silence(self, way: str, distance: int = 1) -> str:
        for dist in range(1, distance + 1):
            if way == 'N':
                self.set_my_position(self.my_position_x, self.my_position_y - 1)
            elif way == 'S':
                self.set_my_position(self.my_position_x, self.my_position_y + 1)
            elif way == 'E':
                self.set_my_position(self.my_position_x + 1, self.my_position_y)
            elif way == 'W':
                self.set_my_position(self.my_position_x - 1, self.my_position_y)
            self.update_my_matrix(self.my_position_x, self.my_position_y, 1)
        return 'SILENCE ' + way + ' ' + str(distance)
    
    def surface(self) -> str:
        self.reset_matrix(self.my_matrix, True)
        self.update_my_matrix(self.my_position_x, self.my_position_y, 1) # On remet "1" dans la case où l'on se trouve
        return 'SURFACE'
    
    def reset_matrix(self, matrix: list, is_my_matrix: bool) -> None:
        # On vide les cases visitées (surface => réinitialisation du chemin)
        for x in range(len(matrix)):
            for y in range(len(matrix)):
                if matrix[y][x] == 1:
                    if is_my_matrix:
                        self.update_my_matrix(x, y, 0)
                    else:
                        self.update_opp_matrix(x, y, 0)

    # Retourne la direction où il y a le plus de cases libres
    def best_direction(self, cardinality: list) -> str:
        best_cardinality: str = cardinality[0]
        max_count: int = 0
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
    
    # On simule le parcours de l'opp pour chaque case et on retourne les cases possibles
    def get_possible_opp_position(self) -> list:
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
        print('Possibilities opp (' + str(len(possibilities)) + '):\n' + str(possibilities), file=sys.stderr, flush=True)
        return possibilities

width, height, my_id = [int(i) for i in input().split()]
matrix = []

for i in range(height):
    line = input()
    matrix.append([eval(i) for i in [*line.replace('.', '0').replace('x', '2')]]) # 2 = il y a une île

# ------------------------------------------------------
# Starting the game
game: Game = Game(matrix)
print(game.my_position_x, game.my_position_y) # Setup la position de départ

my_old_life = 6
type_charge = 'TORPEDO'
must_silence = False
nb_rounds = 1
silence_max_dist = 2
previous_position = [game.my_position_x, game.my_position_y]

# GAME LOOP
while True:
    x, y, my_life, opp_life, torpedo_cooldown, sonar_cooldown, silence_cooldown, mine_cooldown = [int(i) for i in input().split()]
    sonar_result = input()
    opponent_orders = input()

    opponent_orders_managing(opponent_orders)

    action = '' # The action to do each turn
    cardinality = ['N','S','E','W']
    
    # On a fait une faute de jeu, on réinitialise la matrice
    if x != game.my_position_x or y != game.my_position_y:
        game.reset_matrix(game.my_matrix, True)
    game.set_my_position(x, y)
    
    if my_old_life - 2 >= my_life:
        must_silence = True # On s'est fait tirer dessus (théoriquement)
    
    possible_opp_positions = game.get_possible_opp_position()

    # Si on peut tirer, on tire
    if torpedo_cooldown == 0:
        action += game.torpedo(possible_opp_positions) + ' | '
    else:
        print('list_torpedable_opp: ' + str(len(game.list_torpedable_opp(possible_opp_positions))), file=sys.stderr, flush=True)
        if (silence_cooldown != 0 and len(game.list_torpedable_opp(possible_opp_positions)) >= 12) or nb_rounds <= 6:
            type_charge = 'SILENCE' # On priviligie le silence si le random est peut fructueux
        else:
            type_charge = 'TORPEDO'

    # Recherche vers où on peut se déplacer
    possible_cardinality = []
    for card in cardinality:
        if can_move(game.my_matrix, game.my_position_x, game.my_position_y, card):
            possible_cardinality.append(card)
    
    # Si on peut se déplacer, on va dans la meilleure direction
    if possible_cardinality:
        direction = game.best_direction(possible_cardinality)
        if must_silence and silence_cooldown == 0:
            for distance in range(1, silence_max_dist + 1)[::-1]:
                print('Distance: ' + str(distance), file=sys.stderr, flush=True)
                print('can_move_distance: ' + str(can_move_distance(game.my_matrix, game.my_position_x, game.my_position_y, direction, distance)), file=sys.stderr, flush=True)
                if can_move_distance(game.my_matrix, game.my_position_x, game.my_position_y, direction, distance):
                    action += game.silence(direction, distance)
                    break
            must_silence = False
        else:
            action += game.move(direction, type_charge)
    else: # Sinon on fait surface
        if  ' | ' in action:
            action.strip(' | ') # On ne fait pas surface si on a tiré
        action += game.surface()

    my_old_life = my_life
    nb_rounds += 1
    print('\nAction: ' + action, file=sys.stderr, flush=True)
    print(action)

# BUG :
#  Chemin de torpille ne doit pas passer par une île
#  PB dans la position de l'enemi, une liste fini, mais pas la bonne solution dedans ...
#  Placement sur la carte (vérifer que l'on peut bouger (pas dans une impasse)
#  WTF : https://www.codingame.com/replay/702962964

# TODO :
#  Silence après un surface ?
#  récupérer l'ordre s'il a tiré dans opponent_orders_managing()