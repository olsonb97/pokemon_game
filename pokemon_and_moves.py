import random
import time

def slow_type(text, delay=0.005):

    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def new_line():
    slow_type("------------------------------------")

def get_valid_input(prompt, options=[]):
    while True:
        try:
            user_input = input(prompt)
            if int(user_input) in options:
                return int(user_input)
            slow_type("That's not a valid option. Please try again.")
        except ValueError:
            slow_type("That's not a valid option. Please try again.")

class Move:
    
    def __init__(self, name, mtype, power, accuracy, special=False, status=None, stat=None, stat_change=None, stat_target=None):
        self.name = name
        self.mtype = mtype
        self.power = power
        self.accuracy = accuracy
        self.special = special
        self.status = status
        self.stat = stat
        self.stat_change = stat_change
        self.stat_target = stat_target

    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name

#Types:
#'water'
#'fire'
#'grass'
#'normal'
#'electric'
#'ground'
#'rock'
#'poison'

# moves
ember = Move("Ember", 'fire', 5.5, 90)
water_gun = Move("Water Gun", 'water', 5.5, 90)
vine_whip = Move("Vine Whip", 'grass', 5.5, 90)
tackle = Move("Tackle", 'normal', 5, 100)
yawn = Move("Yawn", 'normal', 0, 50, special=True, status='asleep')
confuse_ray = Move("Confuse Ray", 'ghost', 0, 100, special=True, status='confused')
supersonic = Move("Supersonic", 'normal', 0, 55, special=True, status='confused')
thunder_wave = Move("Thunder Wave", 'electric', 0, 90, special=True, status='paralyzed')
electro_ball = Move("Electro Ball", 'electric', 5.5, 100)
thunderbolt = Move("Thunderbolt", 'electric', 9, 100)
thunder = Move("Thunder", 'electric', 11, 70)
splash = Move("Spash", 'normal', 0, 50)
wing_attack = Move("Wing Attack", 'flying', 7, 90)
peck = Move("Peck", 'flying', 5, 100)
horn_attack = Move("Horn Attack", 'normal', 7, 100)
waterfall = Move("Waterfall", 'water', 8, 100)
megahorn = Move("Megahorn", 'bug', 11, 85)
scratch = Move("Scratch", 'normal', 5.5, 95)
spark = Move("Spark", 'normal', 6, 100)
bulldoze = Move("Bulldoze", 'ground', 6.5, 85)
confusion = Move("Confusion", 'psychic', 6.5, 100)
toxic = Move("Toxic", 'poison', 0, 80, special=True, status='poisoned')
paralyze = Move("Paralyze", 'electric', 0, 60, special=True, status='paralyzed')
bug_bite = Move("Bug Bite", 'bug', 5.5, 85)
psychic = Move("Psychic", 'psychic', 9, 90)
shadow_ball = Move("Shadow Ball", 'ghost', 8, 90)
rock_throw = Move("Rock Throw", 'rock', 6.5, 85)
low_kick = Move("Low Kick", 'fighting', 6, 90)
aqua_tail = Move("Aqua Tail", 'water', 7, 90)
flame_wheel = Move("Flame Wheel", 'fire', 7, 90)
razor_leaf = Move("Razor Leaf", 'grass', 7, 95)
earthquake = Move("Earthquake", 'ground', 9, 90)
bug_buzz = Move("Bug Buzz", 'bug', 8, 90)
aerial_ace = Move("Aerial Ace", 'flying', 8, 90)
leer = Move("Leer", 'normal', 0, 100, stat='defense', stat_change=0.15, stat_target='enemy')
tail_whip = Move("Tail Whip", 'normal', 0, 100, stat='defense', stat_change=0.15, stat_target='enemy')
growth = Move("Growth", 'normal', 0, 100, stat='attack', stat_change=0.15, stat_target='user')
growl = Move("Growl", 'normal', 0, 100, stat='attack', stat_change=0.15, stat_target='enemy')
fire_fang = Move("Fire Fang", 'fire', 8, 95)
slash = Move("Slash", 'normal', 7, 100)
flamethrower = Move("Flamethrower", 'fire', 9, 100)
flare_blitz = Move("Flare Blitz", 'fire', 11, 60)
nuzzle = Move("Nuzzle", 'electric', 5, 100)
poison_powder = Move("Poison Powder", 'poison', 0, 75, special=True, status='poisoned')
sleep_powder = Move("Sleep Powder", 'normal', 0, 75, special=True, status='asleep')
seed_bomb = Move("Seed Bomb", 'grass', 8, 100)
power_whip = Move("Power Whip", 'grass', 11, 60)
rapid_spin = Move("Rapid Spin", 'normal', 7, 100)
water_pulse = Move("Water Pulse", 'water', 7, 100)
shell_smash = Move("Shell Smash", 'normal', 0, 100, stat='defense', stat_change=0.2, stat_target='enemy')
iron_defense = Move("Iron Defense", 'normal', 0, 100, stat='defense', stat_change=0.2, stat_target='user')
hydro_pump = Move("Hydro Pump", 'water', 11, 60)
psybeam = Move("Psybeam", 'psychic', 8, 100)
power_gem = Move("Power Gem", 'rock', 8, 100)
harden = Move("Harden", 'normal', 0, 100, stat='defense', stat_change = 0.15, stat_target='user')
venoshock = Move("Venoshock", 'poison', 7, 100)
poison_jab = Move("Poison Jab", 'poison', 8, 100)

# move sets
fire_moves = [ember, tackle, yawn, confuse_ray]
grass_moves = [vine_whip, tackle, toxic, confuse_ray]
water_moves = [water_gun, tackle, yawn, confuse_ray]
god_moves = [growth, ember, leer, toxic]

class Pokemon:
	
    id = 1

    def __init__(self, species, hp, ptype, attack, defense, level, move_set, name="", player_owned=False):
        self.base_hp = hp
        self.base_attack = attack
        self.base_defense = defense
        self.species = species
        self.ptype = ptype        
        self.maxhp = round(self.base_hp*(level/5))
        self.hp = self.maxhp
        self.attack = round(self.base_attack*(level/5), 2)
        self.defense = round(self.base_defense/(level/5), 2)
        self.level = level
        self.move_set = move_set
        self.name = self.species
        if name != "":
            self.name = name
        self.player_owned = player_owned
        self.xp = 0
        self.asleep_counter = 0
        self.confused_counter = 0
        self.poisoned_counter = 1
        self.paralyzed = False
        self.poisoned = False
        self.asleep = False
        self.confused = False
        self.evolved1 = False
        self.evolved2 = False
        self.learnable_moves = {}
        self.id = Pokemon.id
        Pokemon.id += 1

        # weaknesses
        if ptype == 'fire':
            self.weakness = ['water', 'ground', 'rock']
        if ptype == 'water':
            self.weakness = ['grass', 'electric']
        if ptype == 'grass':
            self.weakness = ['fire', 'flying', 'poison', 'bug', 'ice']
        if ptype == 'normal':
            self.weakness = ['fighting']
        if ptype == 'electric':
            self.weakness = ['ground']
        if ptype == 'ground':
            self.weakness = ['water', 'grass', 'ice']
        if ptype == 'rock':
            self.weakness = ['water', 'grass', 'ground', 'fighting']
        if ptype == 'poison':
            self.weakness = ['ground', 'psychic', 'bug']
        if ptype == 'psychic':
            self.weakness = ['bug']
        if ptype == 'fighting':
            self.weakness = ['flying', 'psychic']
        if ptype == 'flying':
            self.weakness = ['rock', 'electric', 'ice']
        if ptype == 'bug':
            self.weakness = ['flying', 'poison', 'rock', 'fire']
        if ptype == 'ghost':
            self.weakness = ['ghost']
        if ptype == 'ice':
            self.weakness = ['fighting', 'rock', 'fire']

        # resistances
        if ptype == 'fire':
            self.resistance = ['grass', 'fire', 'bug']
        if ptype == 'water':
            self.resistance = ['fire', 'water', 'ice']
        if ptype == 'grass':
            self.resistance = ['water', 'grass', 'ground', 'electric']
        if ptype == 'normal':
            self.resistance = ['ghost']
        if ptype == 'electric':
            self.resistance = ['electric', 'flying']
        if ptype == 'ground':
            self.resistance = ['electric', 'poison', 'rock']
        if ptype == 'rock':
            self.resistance = ['fire', 'normal', 'flying', 'poison']
        if ptype == 'fighting':
            self.resistance = ['rock', 'bug']
        if ptype == 'flying':
            self.resistance = ['fighting', 'ground', 'bug', 'grass']
        if ptype == 'poison':
            self.resistance = ['fighting', 'poison', 'grass']
        if ptype == 'bug':
            self.resistance = ['fighting', 'ground', 'grass']
        if ptype == 'ghost':
            self.resistance = ['normal', 'fighting', 'poison', 'bug']
        if ptype == 'psychic':
            self.resistance = ['fighting', 'ghost', 'psychic']
        if ptype == 'ice':
            self.resistance = ['ice']

    def update_stats(self, level):
        self.maxhp = round(self.base_hp*(level/5))
        self.attack = round(self.base_attack*(level/5), 2)
        self.defense = round(self.base_defense/(level/5), 2)
    
    def __repr__(self):
        return self.name
    
    def level_up(self):
        new_level = self.level + 1
        slow_type(f"{self} leveled up from LVL {self.level} to LVL {new_level}!")
        self.level = new_level

    def xp_boost(self, xp):
        if self.player_owned:
            new_line()
            self.xp += xp
            slow_type(f"{self.name} gained {xp} XP. {self.xp}/100")
            while self.xp >= 100:
                self.level_up()
                for key, val in self.__class__.learnable_moves.items():
                    self.learn_move(key, val)
                self.xp -= 100
            time.sleep(0.5)


    def learn_move(self, level, moves):
        if self.level == level:
            time.sleep(0.5)
            new_line()
            for move in moves:
                if len(self.move_set) < 4:
                    slow_type(f"{self.name} learned {move}!")
                    self.move_set.append(move)
                    time.sleep(0.5)
                else:
                    new_line()
                    slow_type(f"{self.name} is trying to learn {move}.\nDelete a move to make room?\n1. Yes\n2. No")
                    choice = get_valid_input("Enter number: ", [1, 2])
                    if choice == 1:
                        new_line()
                        slow_type(f"\n{move}" + (f" | Power: {move.power}" if not move.special else f" | Status: {move.status.capitalize()}") + (f" | Accuracy: {move.accuracy}\n"))
                        for index, value in enumerate(self.move_set):
                            slow_type(f"{index + 1}. {value}" + (f" | Power: {value.power}" if not value.special else f" | Status: {value.status.capitalize()}") + (f" | Accuracy: {value.accuracy}"))
                        move_index = get_valid_input("Enter number: ", [1, 2, 3, 4])-1
                        slow_type(f"{self.name} forgot {self.move_set[move_index]}...")
                        time.sleep(1)
                        slow_type(f"...and learned {move}!")
                        self.move_set[move_index] = move
                    elif choice == 2:
                        continue
    
    @classmethod
    def generate_moves(cls, level):
        possible_moves = []
        while len(possible_moves) < 2:
            for key, val in cls.learnable_moves.items():
                if key <= level:
                    for move in val:
                        if move not in possible_moves and random.randint(1,101) < 70:
                            possible_moves.append(move)
        if len(possible_moves) > 4:
            while len(possible_moves) > 4:
                possible_moves.pop()
        return possible_moves

    def status_heal(self):
        self.asleep = False
        self.confused = False
        self.poisoned = False
        self.paralyzed = False
        self.asleep_counter = 0
        self.poisoned_counter = 1
        self.confused_counter = 0

    def evolve(self):
        if self.evolve_level1 <= self.level and self.evolved1 == False:
            new_line()
            slow_type(f"Your {self.name} is evolving!")
            time.sleep(1)
            slow_type("......", 0.5)
            slow_type("Congratulations!")
            time.sleep(1)
            slow_type(f"Your {self.name} evolved into {self.evolve_pokemon1}!")
            time.sleep(0.5)
            self.species = self.evolve_pokemon1.species
            self.base_attack = self.evolve_pokemon1.base_attack
            self.base_defense = self.evolve_pokemon1.base_defense
            self.base_hp = self.evolve_pokemon1.base_hp
            self.update_stats(self.level)
            check_pokedex(self.evolve_pokemon1, player)
            slow_type(f"{self.evolve_pokemon1} was registered in the Pokedex.")
            time.sleep(1)
            self.evolved1 = True
        elif self.evolve_level2 <= self.level and self.evolved2 == False:
            new_line()
            slow_type(f"Your {self.name} is evolving!")
            time.sleep(1)
            slow_type("......", 0.5)
            slow_type("Congratulations!")
            time.sleep(1)
            slow_type(f"Your {self.name} evolved into {self.evolve_pokemon2}!")
            time.sleep(0.5)
            self.species = self.evolve_pokemon2.species
            self.base_attack = self.evolve_pokemon2.base_attack
            self.base_defense = self.evolve_pokemon2.base_defense
            self.base_hp = self.evolve_pokemon2.base_hp
            self.update_stats(self.level)
            check_pokedex(self.evolve_pokemon2, player)
            slow_type(f"{self.evolve_pokemon2} was registered in the Pokedex.")
            time.sleep(1)
            self.evolved2 = True

    @classmethod
    def generate(cls, level, moves=None):
        if moves is None:
            moves = cls.generate_moves(level)
        yield cls(level=level, moves=moves)

# pokemon subclasses
class Charmander(Pokemon):

    learnable_moves = {1: [growl, scratch], 4: [ember], 16: [fire_fang], 20: [slash], 24: [flamethrower], 36: [flare_blitz]}
    
    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Charmander', 35, 'fire', 1.09, 1.11, level, moves, name, player_owned)
        self.evolve_level1 = 16
        self.evolve_pokemon1 = Charmeleon()
        self.evolve_level2 = 36
        self.evolve_pokemon2 = Charizard()

class Charmeleon(Pokemon):

    learnable_moves = Charmander.learnable_moves
    
    def __init__(self, level=8, name='', moves=None, player_owned=False):
        super().__init__('Charmeleon', 40, 'fire', 1.1, 1.11, level, moves, name, player_owned)
        self.evolve_level1 = 36
        self.evolve_pokemon1 = Charizard()

class Charizard(Pokemon):

    learnable_moves = Charmander.learnable_moves
    
    def __init__(self, level=12, name='', moves=None, player_owned=False):
        super().__init__('Charizard', 45, 'fire', 1.13, 1.11, level, moves, name, player_owned)

class Bulbasaur(Pokemon):

    learnable_moves = {1: [growl, tackle], 4: [vine_whip], 7: [confuse_ray], 15: [poison_powder], 15: [sleep_powder], 18: [seed_bomb], 33: [power_whip]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Bulbasaur', 40, 'grass', 1.07, 1.08, level, moves, name, player_owned)
        self.evolve_level1 = 16
        self.evolve_pokemon1 = Ivysaur()
        self.evolve_level2 = 32
        self.evolve_pokemon2 = Venusaur()

class Ivysaur(Pokemon):

    learnable_moves = Bulbasaur.learnable_moves

    def __init__(self, level=8, name='', moves=None, player_owned=False):
        super().__init__('Ivysaur', 43, 'grass', 1.08, 1.07, level, moves, name, player_owned)
        self.evolve_level1 = 32
        self.evolve_pokemon1 = Venusaur()

class Venusaur(Pokemon):

    learnable_moves = Bulbasaur.learnable_moves

    def __init__(self, level=12, name='', moves=None, player_owned=False):
        super().__init__('Venusaur', 44, 'grass', 1.11, 1.06, level, moves, name, player_owned)
    
class Squirtle(Pokemon):

    learnable_moves = {1: [tackle, tail_whip], 4: [water_gun], 9: [rapid_spin], 15: [water_pulse], 24: [aqua_tail], 27: [shell_smash], 30: [iron_defense], 33: [hydro_pump]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Squirtle', 38, 'water', 1.08, 1.09, level, moves, name, player_owned)
        self.evolve_level1 = 16
        self.evolve_pokemon1 = Wartortle()
        self.evolve_level2 = 32
        self.evolve_pokemon2 = Blastoise()

class Wartortle(Pokemon):

    learnable_moves = Squirtle.learnable_moves

    def __init__(self, level=8, name='', moves=None, player_owned=False):
        super().__init__('Wartortle', 42, 'water', 1.08, 1.09, level, moves, name, player_owned)
        self.evolve_level1 = 32
        self.evolve_pokemon1 = Blastoise()

class Blastoise(Pokemon):

    learnable_moves = Squirtle.learnable_moves

    def __init__(self, level=12, name='', moves=None, player_owned=False):
        super().__init__('Blastoise', 42, 'water', 1.11, 1.08, level, moves, name, player_owned)

class Rattata(Pokemon):

    learnable_moves = {1: [tackle, tail_whip], 8: [scratch], 20: [slash]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Rattata', 40, 'normal', 1.08, 1.11, level, moves, name, player_owned)
        self.evolve_pokemon1 = Raticate()
        self.evolve_level1 = 20

class Raticate(Pokemon):

    learnable_moves = Rattata.learnable_moves

    def __init__(self, level=8, name='', moves=None, player_owned=False):
        super().__init__('Raticate', 42, 'normal', 1.09, 1.11, level, moves, name, player_owned)

class Staryu(Pokemon):

    learnable_moves = {1: [harden, tackle], 4: [water_gun], 8: [confuse_ray], 12: [rapid_spin], 20: [psybeam], 27: [water_pulse], 36: [power_gem], 50: [hydro_pump]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Staryu', 38, 'water', 1.1, 1.11, level, moves, name, player_owned)
        self.evolve_pokemon1 = Starmie()
        self.evolve_level1 = 36
        
class Starmie(Pokemon):

    learnable_moves = Staryu.learnable_moves

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Starmie', 41, 'water', 1.12, 1.07, level, moves, name, player_owned)
        
class Goldeen(Pokemon):

    learnable_moves = {1: [peck, tail_whip], 5: [supersonic], 10: [water_pulse], 15: [horn_attack], 25: [aqua_tail], 35: [waterfall], 45: [megahorn]}
    
    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Goldeen', 37, 'water', 1.09, 1.11, level, moves, name, player_owned)
        self.evolve_level1 = 33
        self.evolve_pokemon1 = Seaking()
        
class Seaking(Pokemon):

    learnable_moves = Goldeen.learnable_moves
    
    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Seaking', 42, 'water', 1.11, 1.09, level, moves, name, player_owned)

class Magikarp(Pokemon):

    learnable_moves = {1: [splash], 15: [tackle], 21: [waterfall], 32: [aqua_tail], 40: [hydro_pump]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Magikarp', 38, 'water', 1, 1, level, moves, name, player_owned)
        self.evolve_level1 = 20
        self.evolve_pokemon1 = Gyarados()
        self.learnable_moves = {20: water_gun, 20: tackle}

class Gyarados(Pokemon):

    learnable_moves = Magikarp.learnable_moves

    def __init__(self, level=12, name='', moves=None, player_owned=False):
        super().__init__('Gyarados', 42, 'water', 1.14, 1.09, level, moves, name, player_owned)

class Caterpie(Pokemon):

    learnable_moves = {1: [harden, tackle], 4: [supersonic], 9: [bug_bite], 10: [confusion], 12: [sleep_powder, poison_powder], 16: [psybeam], 24: [aerial_ace], 32: [bug_buzz]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Caterpie', 36, 'bug', 1.07, 1.1, level, moves, name, player_owned)
        self.evolve_level1 = 7
        self.evolve_pokemon1 = Metapod()
        self.evolve_level2 = 10
        self.evolve_pokemon2 = Butterfree()

class Metapod(Pokemon):

    learnable_moves = Caterpie.learnable_moves

    def __init__(self, level=8, name='', moves=None, player_owned=False):
        super().__init__('Metapod', 42, 'bug', 1.05, 1, level, moves, name, player_owned)
        self.evolve_level1 = 10
        self.evolve_pokemon1 = Butterfree()

class Butterfree(Pokemon):

    learnable_moves = Caterpie.learnable_moves

    def __init__(self, level=12, name='', moves=None, player_owned=False):
        super().__init__('Butterfree', 41, 'bug', 1.09, 1.08, level, moves, name, player_owned)

class Vulpix(Pokemon):

    learnable_moves = {1: [ember, tail_whip], 10: [flame_wheel], 20: [confuse_ray], 32: [flamethrower], 45: [flare_blitz]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Vulpix', 38, 'fire', 1.09, 1.09, level, moves, name, player_owned)

class Pidgey(Pokemon):

    learnable_moves = {1: [growl, tackle], 7: [peck], 20: [wing_attack], 30: [aerial_ace]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Pidgey', 37, 'flying', 1.08, 1.09, level, moves, name, player_owned)
        self.evolve_pokemon1 = Pidgeotto()
        self.evolve_level1 = 18
        self.evolve_pokemon2 = Pidgeot()
        self.evolve_level2 = 36

class Pidgeotto(Pokemon):

    learnable_moves = Pidgey.learnable_moves

    def __init__(self, level=8, name='', moves=None, player_owned=False):
        super().__init__('Pidgeotto', 38, 'flying', 1.1, 1.09, level, moves, name, player_owned)
        self.evolve_level1 = 36
        self.evolve_pokemon1 = Pidgeot()

class Pidgeot(Pokemon):

    learnable_moves = Pidgey.learnable_moves

    def __init__(self, level=12, name='', moves=None, player_owned=False):
        super().__init__('Pidgeot', 41, 'flying', 1.12, 1.07, level, moves, name, player_owned)

class Weedle(Pokemon):

    learnable_moves = {1: [growl, poison_powder], 7: [harden], 11: [bug_bite], 20: [venoshock], 35: [poison_jab]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Weedle', 37, 'bug', 1.07, 1.1, level, moves, name, player_owned)
        self.evolve_level1 = 7
        self.evolve_pokemon1 = Kakuna()
        self.evolve_level2 = 10
        self.evolve_pokemon2 = Beedrill()

class Kakuna(Pokemon):

    learnable_moves = Weedle.learnable_moves

    def __init__(self, level=8, name='', moves=None, player_owned=False):
        super().__init__('Kakuna', 42, 'bug', 1.05, 1, level, moves, name, player_owned)
        self.evolve_level1 = 10
        self.evolve_pokemon1 = Beedrill()

class Beedrill(Pokemon):

    learnable_moves = Weedle.learnable_moves

    def __init__(self, level=12, name='', moves=None, player_owned=False):
        super().__init__('Beedrill', 41, 'bug', 1.09, 1.1, level, moves, name, player_owned)

class Pikachu(Pokemon):

    learnable_moves = {1: [growl, nuzzle, tackle, tail_whip], 4: [thunder_wave], 12: [electro_ball], 20: [spark], 32: [thunderbolt], 42: [thunder]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Pikachu', 40, 'electric', 1.09, 1.1, level, moves, name, player_owned)

class Diglett(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Diglett', 40, 'ground', 1.11, 1.09, level, moves, name, player_owned)
        self.evolve_level1 = 26
        self.evolve_pokemon1 = Dugtrio()

class Dugtrio(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=8, name='', moves=None, player_owned=False):
        super().__init__('Dugtrio', 43, 'ground', 1.12, 1.09, level, moves, name, player_owned)

class Cubone(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Cubone', 40, 'ground', 1.1, 1.09, level, moves, name, player_owned)
        self.evolve_level1 = 28
        self.evolve_pokemon1 = Marowak()

class Marowak(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=8, name='', moves=None, player_owned=False):
        super().__init__('Marowak', 42, 'ground', 1.13, 1.1, level, moves, name, player_owned)

class Magnemite(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Magnemite', 40, 'electric', 1.07, 1.07, level, moves, name, player_owned)
        self.evolve_level1 = 30
        self.evolve_pokemon1 = Magneton()

class Magneton(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=8, name='', moves=None, player_owned=False):
        super().__init__('Magneton', 41, 'electric', 1.09, 1.07, level, moves, name, player_owned)

class Geodude(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Geodude', 40, 'rock', 1.07, 1.07, level, moves, name, player_owned)
        self.evolve_pokemon1 = Graveler()
        self.evolve_level1 = 25

class Graveler(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=8, name='', moves=None, player_owned=False):
        super().__init__('Graveler', 43, 'rock', 1.1, 1.07, level, moves, name, player_owned)
        
class Onix(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Onix', 41, 'rock', 1.09, 1.07, level, moves, name, player_owned)
        
class Bellsprout(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Bellsprout', 35, 'grass', 1.07, 1.09, level, moves, name, player_owned)
        self.evolve_level1 = 21
        self.evolve_pokemon1 = Weepinbell()
        
class Weepinbell(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Weepinbell', 39, 'grass', 1.09, 1.09, level, moves, name, player_owned)
        
class Oddish(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Oddish', 37, 'grass', 1.1, 1.09, level, moves, name, player_owned)
        self.evolve_level1 = 21
        self.evolve_pokemon1 = Gloom()
        
class Gloom(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Gloom', 39, 'grass', 1.12, 1.09, level, moves, name, player_owned)

class Spearow(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Spearow', 38, 'flying', 1.1, 1.09, level, moves, name, player_owned)
        self.evolve_level1 = 21
        self.evolve_pokemon1 = Fearow()
        
class Fearow(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Fearow', 41, 'flying', 1.13, 1.08, level, moves, name, player_owned)
        
class Ekans(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Ekans', 38, 'poison', 1.11, 1.09, level, moves, name, player_owned)
        self.evolve_level1 = 22
        self.evolve_pokemon1 = Arbok()
        
class Arbok(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Arbok', 39, 'poison', 1.12, 1.09, level, moves, name, player_owned)
        
class Sandshrew(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Sandshrew', 38, 'ground', 1.13, 1.09, level, moves, name, player_owned)
        self.evolve_level1 = 22
        self.evolve_pokemon1 = Sandslash()
        
class Sandslash(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Sandslash', 39, 'ground', 1.13, 1.09, level, moves, name, player_owned)
        
class Mankey(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Mankey', 37, 'fighting', 1.12, 1.1, level, moves, name, player_owned)
        self.evolve_level1 = 28
        self.evolve_pokemon1 = Primeape()
        
class Primeape(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Primeape', 40, 'fighting', 1.14, 1.11, level, moves, name, player_owned)
        
class Zubat(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):

        super().__init__('Zubat', 36, 'flying', 1.08, 1.11, level, moves, name, player_owned)
        self.evolve_level1 = 22
        self.evolve_pokemon1 = Golbat()
        
class Golbat(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Golbat', 40, 'flying', 1.1, 1.1, level, moves, name, player_owned)