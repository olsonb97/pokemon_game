import random
import time
import copy
import pickle
import os

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
ember = Move("Ember", 'fire', 6, 90)
water_gun = Move("Water Gun", 'water', 6, 90)
vine_whip = Move("Vine Whip", 'grass', 6, 90)
tackle = Move("Tackle", 'normal', 5, 100)
yawn = Move("Yawn", 'normal', 0, 50, special=True, status='asleep')
confuse_ray = Move("Confuse Ray", 'ghost', 0, 100, special=True, status='confused')
supersonic = Move("Supersonic", 'normal', 0, 55, special=True, status='confused')
thunder_wave = Move("Thunder Wave", 'electric', 0, 90, special=True, status='paralyzed')
electro_ball = Move("Electro Ball", 'electric', 6, 100)
thunderbolt = Move("Thunderbolt", 'electric', 9, 100)
thunder = Move("Thunder", 'electric', 11, 70)
splash = Move("Spash", 'normal', 0, 50)
wing_attack = Move("Wing Attack", 'flying', 7, 90)
peck = Move("Peck", 'flying', 6, 100)
horn_attack = Move("Horn Attack", 'normal', 7, 100)
waterfall = Move("Waterfall", 'water', 8, 100)
megahorn = Move("Megahorn", 'bug', 11, 85)
scratch = Move("Scratch", 'normal', 6, 95)
spark = Move("Spark", 'normal', 7, 100)
bulldoze = Move("Bulldoze", 'ground', 7, 85)
confusion = Move("Confusion", 'psychic', 7, 100)
toxic = Move("Toxic", 'poison', 0, 80, special=True, status='poisoned')
paralyze = Move("Paralyze", 'electric', 0, 60, special=True, status='paralyzed')
bug_bite = Move("Bug Bite", 'bug', 6, 85)
psychic = Move("Psychic", 'psychic', 9, 90)
shadow_ball = Move("Shadow Ball", 'ghost', 8, 90)
rock_throw = Move("Rock Throw", 'rock', 6, 85)
low_kick = Move("Low Kick", 'fighting', 6, 90)
aqua_tail = Move("Aqua Tail", 'water', 8, 90)
flame_wheel = Move("Flame Wheel", 'fire', 7, 90)
razor_leaf = Move("Razor Leaf", 'grass', 7, 95)
earthquake = Move("Earthquake", 'ground', 9, 90)
bug_buzz = Move("Bug Buzz", 'bug', 9, 90)
aerial_ace = Move("Aerial Ace", 'flying', 9, 90)
leer = Move("Leer", 'normal', 0, 100, stat='defense', stat_change=0.15, stat_target='enemy')
tail_whip = Move("Tail Whip", 'normal', 0, 100, stat='defense', stat_change=0.15, stat_target='enemy')
growth = Move("Growth", 'normal', 0, 100, stat='attack', stat_change=0.15, stat_target='user')
growl = Move("Growl", 'normal', 0, 100, stat='attack', stat_change=0.15, stat_target='enemy')
fire_fang = Move("Fire Fang", 'fire', 8, 95)
slash = Move("Slash", 'normal', 8, 100)
flamethrower = Move("Flamethrower", 'fire', 9, 100)
flare_blitz = Move("Flare Blitz", 'fire', 11, 60)
nuzzle = Move("Nuzzle", 'electric', 5, 100)
poison_powder = Move("Poison Powder", 'poison', 0, 75, special=True, status='poisoned')
sleep_powder = Move("Sleep Powder", 'normal', 0, 75, special=True, status='asleep')
seed_bomb = Move("Seed Bomb", 'grass', 9, 100)
power_whip = Move("Power Whip", 'grass', 11, 60)
rapid_spin = Move("Rapid Spin", 'normal', 7, 100)
water_pulse = Move("Water Pulse", 'water', 8, 100)
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
            self.weakness = ['flying', 'poison', 'rock']
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

    @classmethod
    def check_pokedex(cls, pokemon):
        while True:
            found = False
            for pokedex_entry in player.pokedex.keys():
                if pokedex_entry.species == pokemon.species:
                    found = True
                    break
            if found == True:
                break
            else:
                player.pokedex[pokemon] = True
                break

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
            self.check_pokedex(self.evolve_pokemon1)
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
            self.check_pokedex(self.evolve_pokemon2)
            slow_type(f"{self.evolve_pokemon2} was registered in the Pokedex.")
            time.sleep(1)
            self.evolved2 = True

    @classmethod
    def generate(cls, level):
        moves = cls.generate_moves(level)
        yield cls(level=level, moves=moves)

# pokemon subclasses
class Charmander(Pokemon):

    learnable_moves = {1: [growl, scratch], 6: [ember], 16: [fire_fang], 20: [slash], 24: [flamethrower], 36: [flare_blitz]}
    
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

    learnable_moves = {1: [growl, tackle], 6: [vine_whip], 7: [confuse_ray], 15: [poison_powder], 15: [sleep_powder], 18: [seed_bomb], 33: [power_whip]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Bulbasaur', 40, 'grass', 1.05, 1.07, level, moves, name, player_owned)
        self.evolve_level1 = 16
        self.evolve_pokemon1 = Ivysaur()
        self.evolve_level2 = 32
        self.evolve_pokemon2 = Venusaur()

class Ivysaur(Pokemon):

    learnable_moves = Bulbasaur.learnable_moves

    def __init__(self, level=8, name='', moves=None, player_owned=False):
        super().__init__('Ivysaur', 43, 'grass', 1.08, 1.06, level, moves, name, player_owned)
        self.evolve_level1 = 32
        self.evolve_pokemon1 = Venusaur()

class Venusaur(Pokemon):

    learnable_moves = Bulbasaur.learnable_moves

    def __init__(self, level=12, name='', moves=None, player_owned=False):
        super().__init__('Venusaur', 45, 'grass', 1.11, 1.05, level, moves, name, player_owned)
    
class Squirtle(Pokemon):

    learnable_moves = {1: [tackle, tail_whip], 6: [water_gun], 9: [rapid_spin], 15: [water_pulse], 24: [aqua_tail], 27: [shell_smash], 30: [iron_defense], 33: [hydro_pump]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Squirtle', 38, 'water', 1.05, 1.09, level, moves, name, player_owned)
        self.evolve_level1 = 16
        self.evolve_pokemon1 = Wartortle()
        self.evolve_level2 = 32
        self.evolve_pokemon2 = Blastoise()

class Wartortle(Pokemon):

    learnable_moves = Squirtle.learnable_moves

    def __init__(self, level=8, name='', moves=None, player_owned=False):
        super().__init__('Wartortle', 42, 'water', 1.07, 1.09, level, moves, name, player_owned)
        self.evolve_level1 = 32
        self.evolve_pokemon1 = Blastoise()

class Blastoise(Pokemon):

    learnable_moves = Squirtle.learnable_moves

    def __init__(self, level=12, name='', moves=None, player_owned=False):
        super().__init__('Blastoise', 42, 'water', 1.11, 1.06, level, moves, name, player_owned)

class Rattata(Pokemon):

    learnable_moves = {1: [tackle, tail_whip], 8: [scratch], 20: [slash]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Rattata', 40, 'normal', 1.06, 1.11, level, moves, name, player_owned)
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
        super().__init__('Starmie', 41, 'water', 1.13, 1.06, level, moves, name, player_owned)
        
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
        super().__init__('Butterfree', 41, 'bug', 1.09, 1.06, level, moves, name, player_owned)

class Vulpix(Pokemon):

    learnable_moves = {1: [ember, tail_whip], 10: [flame_wheel], 20: [confuse_ray], 32: [flamethrower], 45: [flare_blitz]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Vulpix', 38, 'fire', 1.09, 1.06, level, moves, name, player_owned)

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
        super().__init__('Beedrill', 41, 'bug', 1.09, 1.06, level, moves, name, player_owned)

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
        super().__init__('Marowak', 42, 'ground', 1.14, 1.1, level, moves, name, player_owned)

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
        super().__init__('Bellsprout', 35, 'grass', 1.06, 1.09, level, moves, name, player_owned)
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
        super().__init__('Arbok', 39, 'poison', 1.14, 1.09, level, moves, name, player_owned)
        
class Sandshrew(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Sandshrew', 38, 'ground', 1.13, 1.09, level, moves, name, player_owned)
        self.evolve_level1 = 22
        self.evolve_pokemon1 = Sandslash()
        
class Sandslash(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Sandslash', 39, 'ground', 1.15, 1.09, level, moves, name, player_owned)
        
class Mankey(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Mankey', 37, 'fighting', 1.12, 1.1, level, moves, name, player_owned)
        self.evolve_level1 = 28
        self.evolve_pokemon1 = Primeape()
        
class Primeape(Pokemon):

    learnable_moves = {1: [growl, tackle]}

    def __init__(self, level=5, name='', moves=None, player_owned=False):
        super().__init__('Primeape', 40, 'fighting', 1.16, 1.11, level, moves, name, player_owned)
        
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

class Battle:

    def __init__(self, trainer_pokemon, wild=False, trainer=False, trainer_name="", runnable=True):
        self.user_pokemon = copy.deepcopy(player.pokemon)
        self.trainer_pokemon = trainer_pokemon
        self.active_enemy_pokemon = self.trainer_pokemon[0]
        self.wild = wild
        self.trainer = trainer
        self.trainer_name = trainer_name
        self.user_items = copy.deepcopy(player.items)
        self.battle_victory = None
        self.runnable = runnable
        for pokemon in self.user_pokemon:
            pokemon.attack_counter = 0
            pokemon.defense_counter = 0
            if pokemon.hp > 0:
                self.active_pokemon = pokemon
                break
        for pokemon in self.trainer_pokemon:
            pokemon.attack_counter = 0
            pokemon.defense_counter = 0

    def opening_statement(self):
        if self.wild:
            return slow_type(f"Wild {self.active_enemy_pokemon.name} appeared!")
        return slow_type(f"{self.trainer_name} challenges you to a battle!\n{self.trainer_name} sent out {self.active_enemy_pokemon.name}!")

    def get_damage(self, attacker, move):
        damage = round(attacker.attack * move.power)
        return damage
    
    def take_damage(self, attacker, defender, move, damage):
        accuracy_roll = random.randint(1, 100)
        if accuracy_roll <= move.accuracy:
            damage = round(defender.defense * damage * 0.9)
            if move.mtype in defender.weakness:
                damage = round(damage * 1.5)
                slow_type("It was super effective!")
            if move.mtype in defender.resistance:
                damage = round(damage * 0.5)
                slow_type("It wasn't very effective...")
            slow_type(f"{defender.name} took {damage} damage.")
            defender.hp -= damage
        else:
            slow_type(f"{attacker.name} missed!")
        if defender.hp <= 0:
            defender.hp = 0
            defender.asleep = False
            defender.confused = False
    
    def print_health(self, pokemon, user=False, enemy=False):
        if user:
            slow_type(f"Player: {pokemon} HP: {pokemon.hp}/{pokemon.maxhp} LVL: {pokemon.level}"+
                      (" (Asleep)" if pokemon.asleep else "")+
                      (" (Poisoned)" if pokemon.poisoned else "")+
                      (" (Paralyzed)" if pokemon.paralyzed else "")+
                      (" (Confused)" if pokemon.confused else ""))
        if enemy:
            pokemon = self.active_enemy_pokemon
            slow_type(f"Enemy: {pokemon} HP: {pokemon.hp}/{pokemon.maxhp} LVL: {pokemon.level}"+
                      (" (Asleep)" if pokemon.asleep else "")+
                      (" (Poisoned)" if pokemon.poisoned else "")+
                      (" (Paralyzed)" if pokemon.paralyzed else "")+
                      (" (Confused)" if pokemon.confused else ""))
            
    def print_user_pokemon(self):
        for index, pokemon in enumerate(self.user_pokemon):
            slow_type(f"{index+1}. {pokemon} HP: {pokemon.hp}/{pokemon.maxhp} LVL: {pokemon.level}"+(" (active)" if pokemon.id == self.active_pokemon.id else "") + (" (Paralyzed)" if pokemon.paralyzed else "") + (" (Poisoned)" if pokemon.poisoned else ""))

    def print_items(self):
        for index, item in enumerate(self.user_items):
            slow_type(f"{index+1}. {item}")

    def print_moves(self):
        for i in self.active_pokemon.move_set:
            if not i.special and i.stat is None:
                slow_type(f"{self.active_pokemon.move_set.index(i)+1}. {i.name} | Power: {i.power} | Type: {i.mtype.capitalize()} | Accuracy: {i.accuracy}")
            elif i.special:
                slow_type(f"{self.active_pokemon.move_set.index(i)+1}. {i.name} | Status: {i.status.capitalize()} | Accuracy: {i.accuracy}")
            elif i.stat is not None:
                slow_type(f"{self.active_pokemon.move_set.index(i)+1}. {i.name} | Stat Change: {i.stat_target.capitalize()}'s {i.stat.capitalize()} | Accuracy: {i.accuracy}")

    def make_asleep(self, sleepee, move):
        random_num = random.randint(1, 100)
        if random_num <= move.accuracy:
            if not sleepee.confused and not sleepee.asleep and not sleepee.paralyzed and not sleepee.poisoned:
                sleepee.asleep_counter = 0
                sleepee.asleep = True
                slow_type(f"{sleepee} fell asleep!")
            else:
                slow_type(f"{sleepee} is already affected by a status.")
        else:
            slow_type("Attack missed!")
        

    def make_confused(self, confusee, move):
        random_num = random.randint(1, 100)
        if random_num <= move.accuracy:
            if not confusee.confused and not confusee.asleep and not confusee.paralyzed and not confusee.poisoned:
                confusee.confused_counter = 0
                confusee.confused = True
                slow_type(f"{confusee} became confused!")
            else:
                slow_type(f"{confusee} is already affected by a status.")
        else:
            slow_type("Attack missed!")

    def make_paralyzed(self, paralyzee, move):
        random_num = random.randint(1, 100)
        if random_num <= move.accuracy:
            if not paralyzee.confused and not paralyzee.asleep and not paralyzee.paralyzed and not paralyzee.poisoned:
                paralyzee.paralyzed = True
                slow_type(f"{paralyzee} became paralyzed!")
            else:
                slow_type(f"{paralyzee} is already affected by a status.")
        else:
            slow_type("Attack missed!")
    
    def make_poisoned(self, poisonee, move):
        random_num = random.randint(1, 100)
        if random_num <= move.accuracy:
            if not poisonee.confused and not poisonee.asleep and not poisonee.paralyzed and not poisonee.poisoned:
                poisonee.poisoned_counter = 1
                poisonee.poisoned = True
                slow_type(f"{poisonee} became poisoned!")
            else:
                slow_type(f"{poisonee} is already affected by a status.")
        else:
            slow_type("Attack missed!")

    def change_stat(self, move, attacker, defender):
        if move.stat == 'attack':
            if move.stat_target == 'user':
                if attacker.attack_counter <= 3:
                    attacker.attack += move.stat_change
                    attacker.attack_counter += 1
                    slow_type(f"{attacker}'s attack was raised.")
                else:
                    slow_type(f"{attacker}'s attack won't go any higher.")
            elif move.stat_target == 'enemy':
                if defender.attack_counter >= -3:
                    defender.attack -= move.stat_change
                    defender.attack_counter -= 1
                    slow_type(f"{defender}'s attack was lowered.")
                else:
                    slow_type(f"{defender}'s attack won't go any lower.")
        elif move.stat == 'defense':
            if move.stat_target == 'user':
                if attacker.defense_counter <= 3:
                    attacker.defense -= move.stat_change
                    attacker.defense_counter += 1
                    slow_type(f"{attacker}'s defense was raised.")
                else:
                    slow_type(f"{attacker}'s defense won't go any higher.")
            elif move.stat_target == 'enemy':
                if defender.defense_counter >= -3:
                    defender.defense += move.stat_change
                    defender.defense_counter -= 1
                    slow_type(f"{defender}'s defense was lowered.")
                else:
                    slow_type(f"{defender}'s defense won't go any lower.")

    def caught_checker(self):
        if self.active_enemy_pokemon.player_owned:
            return True
        return False

    def healthy_checker(self, checkee, attack_turn=False):

        # asleep
        random_num = random.randint(1, 100)
        if attack_turn:
            if checkee.asleep:
                if checkee.asleep_counter > 3:
                    checkee.asleep_counter = 0
                    checkee.asleep = False
                    slow_type(f"{checkee.name} woke up!")
                    return True
                elif random_num < 25 and checkee.asleep_counter > 0:
                    checkee.asleep_counter = 0
                    checkee.asleep = False
                    slow_type(f"{checkee.name} woke up!")
                    return True
                elif random_num < 25 and checkee.asleep_counter <=0:
                    slow_type(f"{checkee.name} is asleep!")
                    checkee.asleep_counter += 1
                    return False
                elif random_num >= 25:
                    slow_type(f"{checkee.name} is asleep!")
                    checkee.asleep_counter += 1
                    return False
                
            # confused
            elif checkee.confused:
                if checkee.confused_counter > 2:
                    checkee.confused_counter = 0
                    checkee.confused = False
                    slow_type(f"{checkee.name} snapped out of confusion!")
                    return True
                elif random_num < 50:
                    checkee.confused = False
                    slow_type(f"{checkee.name} snapped out of confusion!")
                    return True
                elif random_num >= 50:
                    damage = round(5 * checkee.attack * checkee.defense)
                    checkee.hp -= damage
                    slow_type(f"{checkee.name} attacked itself in confusion!")
                    slow_type(f"{checkee.name} took {damage} damage!")
                    checkee.confused_counter += 1
                    return False
            
            # poisoned
            elif checkee.poisoned:
                checkee.poisoned_counter += 1
                poison_damage = round(checkee.poisoned_counter * 0.6)
                slow_type(f"{checkee.name} took {poison_damage} damage from poison!")
                checkee.hp -= poison_damage
                if checkee.hp > 0:
                    return True
                else:
                    return False
                
            # paralyzed
            elif checkee.paralyzed:
                if random_num < 60:
                    return True
                else:
                    slow_type(f"{checkee.name} is paralyzed and couldn't attack!")
                    return False

            else:
                return True
        elif not attack_turn:
            if checkee.confused:
                checkee.confused_counter += 1
                return False
            elif checkee.asleep:
                checkee.asleep_counter += 1
                return False
            return True
        
    def alive_check(self, pokemon):
        if pokemon.hp > 0:
            return True
        pokemon.status_heal()
        return False
    
    def calculate_xp(self):
        average_enemy_level = 0
        average_player_level = 0
        for pokemon in self.trainer_pokemon:
            average_enemy_level += pokemon.level
        for pokemon in self.user_pokemon:
            average_player_level += pokemon.level
        average_enemy_level = average_enemy_level/len(self.trainer_pokemon)
        average_player_level = average_player_level/len(self.user_pokemon)
        return round((random.randint(30, 60)*(average_enemy_level/average_player_level)))
        
    def battle_check(self):
        if not self.alive_check(self.active_pokemon):
            healthy_pokemon = len(self.user_pokemon)
            for index, pokemon in enumerate(self.user_pokemon):
                if self.alive_check(pokemon):
                    slow_type(f"{self.active_pokemon} is too weak to fight.\n{self.user_pokemon[index]} is now the active pokemon.")
                    self.active_pokemon = self.user_pokemon[index]
                    return True
                else:
                    healthy_pokemon -= 1
            if healthy_pokemon == 0:
                new_line()
                slow_type("You lost the battle...")
                self.battle_victory = False
                return False
        if not self.alive_check(self.active_enemy_pokemon):

            # calculate xp
            Pokemon.xp_boost(self.active_pokemon, self.calculate_xp())

            healthy_enemy_pokemon = len(self.trainer_pokemon)
            for index, pokemon in enumerate(self.trainer_pokemon):
                if self.alive_check(pokemon):
                    slow_type(f"{self.active_enemy_pokemon} is too weak to fight.\n{self.trainer_name} sent out {self.trainer_pokemon[index]}!")
                    self.active_enemy_pokemon = self.trainer_pokemon[index]
                    return True
                else:
                    healthy_enemy_pokemon -= 1
            if healthy_enemy_pokemon == 0:
                new_line()
                if not self.wild:
                    slow_type(f"{self.trainer_name} is out of usable Pokemon.\nYou won the battle!")
                else:
                    slow_type(f"{self.active_enemy_pokemon} knocked out!\nYou won the battle!")
                self.battle_victory = True
                
                # money
                if not self.trainer_name == "":
                    money_won = random.randint(50, 100)
                    slow_type(f"{player.name} was rewarded ${money_won}.")
                    time.sleep(0.5)
                    player.money += money_won
                self.battle_victory = True
                return False
        elif self.caught_checker():
            self.battle_victory = True
            return False
        elif self.battle_victory:
            return False
        return True
    
    def return_damaged_pokemon_and_items(self):
        for pokemon in self.trainer_pokemon:
            pokemon.hp = pokemon.maxhp
            pokemon.update_stats(pokemon.level)
            pokemon.status_heal()
        for main_pokemon in player.pokemon:
            for battle_pokemon in self.user_pokemon:
                if battle_pokemon.id == main_pokemon.id:
                    main_pokemon.hp = battle_pokemon.hp
                    main_pokemon.xp = battle_pokemon.xp
                    main_pokemon.poisoned = battle_pokemon.poisoned
                    main_pokemon.paralyzed = battle_pokemon.paralyzed
                    main_pokemon.move_set = battle_pokemon.move_set
                    if main_pokemon.level < battle_pokemon.level:
                        main_pokemon.level = battle_pokemon.level
                        main_pokemon.update_stats(main_pokemon.level)
                        try:
                            main_pokemon.evolve()
                        except:
                            pass
                    
        player.items = self.user_items
    
    def attack_turn(self, attacker, defender, move):
        if not move.special and move.stat == None:
            damage = self.get_damage(attacker, move)*(attacker.level/5)
            self.take_damage(attacker, defender, move, damage)
            if attacker == self.active_pokemon:
                self.print_health(self.active_enemy_pokemon, enemy=True)
            elif attacker == self.active_enemy_pokemon:
                self.print_health(self.active_pokemon, user=True)
        elif move.special:
            if move.status == 'asleep':
                self.make_asleep(defender, move)
            if move.status == 'confused':
                self.make_confused(defender, move)
            if move.status == 'paralyzed':
                self.make_paralyzed(defender, move)
            if move.status == 'poisoned':
                self.make_poisoned(defender, move)
        elif move.stat is not None:
            self.change_stat(move, attacker, defender)

    def use_item(self, item):
        if item.itype == "heal" or item.itype == "status_heal":
            if item.use(self.user_pokemon, self.user_items):
                return True
            return False
        elif item.itype == "attack" or item.itype == "defense":
            if item.itype == "attack":
                if self.active_pokemon.attack_counter <= 3:
                    if item.use(self.active_pokemon, self.user_items):
                        return True
                else:
                    slow_type(f"{self.active_pokemon}'s attack won't go any higher!")
            elif item.itype == "defense":
                if self.active_pokemon.defense_counter <= 3:
                    if item.use(self.active_pokemon, self.user_items):
                        return True
                else:
                    slow_type(f"{self.active_pokemon}'s attack won't go any higher!")
            return False
        elif item.itype == 'catch':
            if self.wild:
                if item.use(self.active_enemy_pokemon, self.user_items):
                    self.active_enemy_pokemon.player_owned=True
                    if len(self.user_pokemon) < 6:
                        nickname = input("Give it a name: ")
                        self.active_enemy_pokemon.name = nickname
                        player.pokemon.append(self.active_enemy_pokemon)
                        slow_type(f"{self.active_enemy_pokemon} was added to your party")
                    else:
                        slow_type(f"Party is full. {self.active_enemy_pokemon} was released.")
                    return True
            else:
                slow_type(f"You can't steal another trainer's Pokemon!")
                return True
        else:
            return False

    def switch(self, switchee, switcher):
        if switcher != self.active_pokemon:
            if self.alive_check(switcher):
                self.active_pokemon = switcher
                slow_type(f"{switcher} is now your active pokemon.")
                if switchee.confused:
                    switchee.confused = False
                    switchee.confused_counter = 0
                    slow_type(f"{switchee} is no longer confused.")
                if switchee.asleep:
                    switchee.asleep = False
                    switchee.asleep_counter = 0
                    slow_type(f"{switchee} is no longer asleep.")
                return True
            else:
                slow_type(f"{switcher} is too weak to fight.")
                return False
        else:
            slow_type(f"{switcher} is already the active pokemon.")
            return False
            
    def user_turn(self):
        done = False
        while done == False:
            new_line()
            self.print_health(self.active_pokemon, user=True,enemy=True)
            slow_type("1. Fight\n2. Items\n3. Switch\n4. Run")
            choice = get_valid_input("Enter number: ", [1, 2, 3, 4])
            if choice == 1:
                new_line()
                self.print_moves()
                move_choice = get_valid_input("Enter number: ", [1, 2, 3, 4])-1
                move = self.active_pokemon.move_set[move_choice]
                new_line()
                if self.healthy_checker(self.active_pokemon, attack_turn=True):
                    slow_type(f"Your {self.active_pokemon.name} used {move.name}!")
                    self.attack_turn(self.active_pokemon, self.active_enemy_pokemon, move)
                done = True
            if choice == 2:
                new_line()
                if len(self.user_items) != 0:
                    self.print_items()
                    item_choice = get_valid_input("Enter number: ", list(range(1, len(self.user_items)+1)))
                    item = self.user_items[item_choice-1]
                    self.healthy_checker(self.active_pokemon, attack_turn=False)
                    done = self.use_item(item)
                else:
                    slow_type("Out of items!")
                    done = False
            if choice == 3:
                new_line()
                self.print_user_pokemon()
                switcher = get_valid_input("Enter number: ", list(range(1, len(self.user_pokemon)+1)))
                done = self.switch(self.active_pokemon, self.user_pokemon[switcher-1])
            if choice == 4:
                if not self.runnable:
                    slow_type("You can't run from this battle!")
                else:
                    slow_type("You got away safely.")
                    self.battle_victory = True
                    done = True

    def enemy_turn(self):
        new_line()
        choice = random.randint(0, len(self.active_enemy_pokemon.move_set)-1)
        move = self.active_enemy_pokemon.move_set[choice]
        if self.healthy_checker(self.active_enemy_pokemon, attack_turn=True):
            slow_type(f"Enemy {self.active_enemy_pokemon.name} used {move.name}!")
            self.attack_turn(self.active_enemy_pokemon, self.active_pokemon, move)

    def battle(self):
        new_line()
        self.opening_statement()
        while True:
            Pokemon.check_pokedex(self.active_enemy_pokemon)
            if self.battle_check():
                time.sleep(0.5)
                self.user_turn()
            else:
                self.return_damaged_pokemon_and_items()
                if self.battle_victory:
                    return True
                slow_type("Out of usable Pokemon...")
                return False
            if self.battle_check():
                time.sleep(0.5)
                self.enemy_turn()
            else:
                self.return_damaged_pokemon_and_items()
                if self.battle_victory:
                    return True
                slow_type("Out of usable Pokemon...")
                return False

class Item:

    id = 1
    def __init__(self, name, itype, power):
        self.name = name
        self.itype = itype
        self.power = power
        self.id = Item.id
        Item.id += 1

    def __repr__(self):
        return self.name

    @classmethod
    def generate(cls):
        yield cls()
    
class Potion(Item):

    id = 1
    def __init__(self):
        super().__init__("Potion", "heal", 20)
        self.cost = 50
        self.id = Potion.id
        Potion.id += 1

    def use(self, party, item_list):
        new_line()
        slow_type("Use on which Pokemon?")
        for index, val in enumerate(party):
            slow_type(f"{index+1}. {val}"+
            (" (Asleep)" if val.asleep else "")+
            (" (Poisoned)" if val.poisoned else "")+
            (" (Paralyzed)" if val.paralyzed else "")+
            (" (Confused)" if val.confused else ""))
        pokemon_index = get_valid_input("Enter number: ", list(range(1, len(party)+1)))-1
        pokemon_choice = party[pokemon_index]
        if pokemon_choice.hp >= pokemon_choice.maxhp:
            slow_type(f"{pokemon_choice} is already at full health.")
            return False
        pokemon_choice.hp += self.power
        if pokemon_choice.hp > pokemon_choice.maxhp:
            pokemon_choice.hp = pokemon_choice.maxhp
        slow_type(f"{pokemon_choice} healed for {self.power} HP.")
        item_list.remove(self)
        return True

class FullHeal(Item):

    id = 1
    def __init__(self):
        super().__init__("Full Heal", "status_heal", 0)
        self.cost = 75
        self.id = Potion.id
        FullHeal.id += 1

    def use(self, party, item_list):
        new_line()
        slow_type("Use on which Pokemon?")
        for index, val in enumerate(party):
            slow_type(f"{index+1}. {val}"+
            (" (Asleep)" if val.asleep else "")+
            (" (Poisoned)" if val.poisoned else "")+
            (" (Paralyzed)" if val.paralyzed else "")+
            (" (Confused)" if val.confused else ""))
        pokemon_index = get_valid_input("Enter number: ", list(range(1, len(party)+1)))-1
        pokemon_choice = party[pokemon_index]
        if not pokemon_choice.confused and not pokemon_choice.asleep and not pokemon_choice.poisoned and not pokemon_choice.paralyzed:
            slow_type(f"{pokemon_choice} is already at full health.")
            return False
        pokemon_choice.status_heal()
        slow_type(f"{pokemon_choice} was cured of status effects.")
        item_list.remove(self)
        return True

class Attack_Boost(Item):

    id = 1
    def __init__(self):
        super().__init__("Attack Boost", "attack", 0.1)
        self.cost = 100
        self.id = Attack_Boost.id
        Attack_Boost.id += 1

    def use(self, pokemon, item_list):
        new_attack = round(pokemon + self.power, 2)
        slow_type(f"{pokemon}'s attack was raised!")
        pokemon.attack = new_attack
        item_list.remove(self)
        return True

class Defense_Boost(Item):

    id = 1
    def __init__(self):
        super().__init__("Defense Boost", "defense", 0.1)
        self.cost = 100
        self.id = Defense_Boost.id
        Defense_Boost.id += 1

    def use(self, pokemon, item_list):
        new_defense = round(pokemon - self.power, 2)
        slow_type(f"{pokemon}'s defense was raised!")
        pokemon.defense = new_defense
        item_list.remove(self)
        return True

class Pokeball(Item):

    id = 1
    def __init__(self):
        super().__init__("Pokeball", "catch", 25)
        self.cost = 50
        self.id = Pokeball.id
        Pokeball.id += 1

    def use(self, pokemon, item_list):
        counter = 0
        while counter < 5:
            slow_type("...")
            time.sleep(0.5)
            if random.randint(1, 100) in range(1, self.power*round(pokemon.maxhp/pokemon.hp)):
                counter += 1
                if counter >= 5:
                    slow_type(f"{pokemon} was caught!")
                    time.sleep(0.5)
                    item_list.remove(self)
                    return True
            else:
                slow_type(f"{pokemon} escaped the {self}...")
                time.sleep(0.5)
                item_list.remove(self)
                return False

class Greatball(Item):

    id = 1
    def __init__(self):
        super().__init__("Great Ball", "catch", 35)
        self.cost = 100
        self.id = Pokeball.id
        Greatball.id += 1

class Ultraball(Item):

    id = 1
    def __init__(self):
        super().__init__("Ultra Ball", "catch", 45)
        self.cost = 150
        self.id = Pokeball.id
        Ultraball.id += 1

class Player:

    def __init__(self, name='Player', money=0):
        self.visited_mom = False
        self.tutorial_beat = False
        self.name = name
        self.money = money
        self.gym_badges= []
        self.pokemon = []
        self.items = []
        self.local_location=""
        self.map_location=""
        self.map = ""
        self.pokedex = {
        Charmander(): False,
        Bulbasaur(): False,
        Squirtle(): False
        }
        self.pokedex = {pokemon: self.pokedex[pokemon] for pokemon in sorted(self.pokedex, key=lambda x: x.name)}
        self.inventory = {
'pokemon': self.pokemon,
'items': self.items,
'map': self.map,
'money': self.money,
'name': self.name,
'gym_badges': self.gym_badges,
'pokedex': self.pokedex,
'local_location': self.local_location,
'map_location': self.map_location
}

    def initialize(self):
        try:
            for place in map_object.map_locations:
                if place.name == self.map_location.name:
                    self.map_location = place
            for place in self.map_location.local_locations:
                if place.name == self.local_location.name:
                    self.local_location = place

        except Exception as e:
            self.map_location = pallet_town
            self.local_location = pallet_town.pokemonlab

    def update_map(self):
        slow_type(f"""
      Pallet Town {"(You)" if self.map_location == pallet_town else "    "}
            V
        Route 1
            V
     Viridian City {"(You)" if self.map_location == viridian_city else "    "}
            V
Route 2: Viridian Forest
            V
       Pewter City {"(You)" if self.map_location == pewter_city else "    "}
            V
         Route 3
            V
   {"(You)" if self.map_location == mount_moon else "    "} Mt Moon -----> Mt Moon Cave
            V
         Route 4
            V
      Cerulean City
"""
        )

    def save(self, filename):
        new_line()
        slow_type("1. Save Game\n2. Delete Save\n3. Back")
        choice = get_valid_input("Enter number: ", [1, 2, 3])
        if choice == 1:
            with open(filename, 'wb') as file:
                pickle.dump(self, file)
                slow_type("......", 0.25)
                slow_type("Game Saved!")
                time.sleep(1)
        if choice == 2:
            if os.path.exists('./savefile'):
                os.remove('./savefile')
                slow_type("......", 0.25)
                print(f"Save has been deleted.")
            else:
                slow_type("No save found!")
            time.sleep(1)
        if choice == 3:
            return

    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as file:
            loaded_player = pickle.load(file)
        return loaded_player

class Location:

    def __init__(self, name="default"):
        self.name = name

    def __repr__(self):
        return self.name

    def wild_battle(self, runnable=True):
        if not Battle([next(random.choice(self.route_pokemon).generate(random.choice(self.route_levels)))], wild=True, runnable=runnable).battle():
            player.map_location.black_out()
            return False
        return True

    def trainer_battle(self, pokemons=[], levels=[]):
        if not Battle([next(random.choice(self.trainer_pokemon).generate(random.choice(self.trainer_levels))) for i in range(2, 3)], wild=False, trainer=True, trainer_name=random.choice(trainer_names), runnable=False).battle():
            player.map_location.black_out()
            return False
        return True

    def gym_battle(self, pokemon=[], name="Gym Leader", badge='', victory_message=''):
        if not Battle(pokemon, wild=False, trainer=True, trainer_name=name, runnable=False).battle():
            player.map_location.black_out()

        else:
            time.sleep(1)
            slow_type(f"You've defeated {name}!")
            time.sleep(1)
            slow_type(f"You earned the {badge}!")
            player.gym_badges.append(badge)
            time.sleep(0.5)
            slow_type(victory_message)
            time.sleep(0.5)
            return True

# pokemon center
class PokemonCenter(Location):

    def __init__(self, name="Pokemon Center", string="Your Pokemon have been healed!"):
        super().__init__(name)
        self.string = string

    def heal(self):
        new_line()
        for pokemon in player.pokemon:
            pokemon.hp = pokemon.maxhp
            pokemon.status_heal()
        slow_type("......", 0.5)
        slow_type(self.string)
        time.sleep(0.5)

    def choose(self):
        slow_type(f"1. Heal Pokemon\n2. Return to {player.map_location}")
        choice = get_valid_input("Enter number: ", [1, 2])
        if choice == 1:
            self.heal()
        if choice == 2:
            return True

# route
class Route(Location):

    def __init__(self, route_pokemon, route_levels, *links, trainer_pokemon = [], trainer_levels = [], name="Route 1"):
        super().__init__(name)
        self.trainer_pokemon = trainer_pokemon
        self.trainer_levels = trainer_levels
        self.route_pokemon = route_pokemon
        self.route_levels = route_levels
        self.links = links

    def choose(self):
        for link in self.links:
            if link == player.map_location or link == player.local_location:
                self.source = link
            else:
                self.destination = link
        slow_type(f"1. Return to {self.source}\n2. Wild Battle" + (f"\n3. Go to {self.destination} (3 Trainer Battles)" if self.destination is not None else ""))
        if self.destination is not None:
            choice = get_valid_input("Enter number: ", [1, 2, 3])
        else:
            choice = get_valid_input("Enter number: ", [1, 2])
        if choice == 1:
            return True
        elif choice == 2:
            self.wild_battle()
        elif choice == 3:
            step_count = 3
            while step_count != 0:
                if not Battle([next(random.choice(self.trainer_pokemon).generate(random.choice(self.trainer_levels))) for i in range(1, random.randint(2, 3))], wild=False, trainer=True, trainer_name=random.choice(trainer_names), runnable=False).battle():
                    player.map_location.black_out()
                    return
                else:
                    step_count -= 1
                    slow_type(f"{step_count} battle(s) left.")
            slow_type(f"You made it to {self.destination}!")
            time.sleep(1)
            player.map_location = self.destination
            return True

# pokemon lab
class PokemonLab(Location):

    def __init__(self, name="Pokemon Lab"):
        super().__init__(name)

    def choose(self):
        slow_type("Nothing left to do here!")
        slow_type(f"1. Return to {player.map_location}")
        choice = get_valid_input("Enter number: ", [1])
        if choice == 1:
            return True

# pokemart
class Pokemart(Location):

    def __init__(self, item_list):
        super().__init__("Pokemart")
        self.item_list = item_list

    def display_items(self):
        new_line()
        slow_type(f"You have ${player.money}")
        slow_type("Choose an item to purchase.")
        new_line()
        item_list = [next(item.generate()) for item in self.item_list]+["Back"]
        for index, item in enumerate(item_list):
            slow_type(f"{index+1}. {item}" + (f" | ${item.cost}" if isinstance(item, Item) else ""))
        choice = get_valid_input("Enter number: ", list(range(1, len(item_list)+2)))-1
        if choice == item_list.index("Back"):
            return True
        item = item_list[choice]
        if player.money >= item.cost:
            player.money -= item.cost
            slow_type(f"{item} obtained.")
            player.items.append(item)
            return True
        elif player.money < item.cost:
            slow_type("You do not have enough money.")
            return False
        
    def choose(self):
        slow_type(f"1. Purchase Items\n2. Return to {player.map_location}")
        choice = get_valid_input("Enter number: ", [1, 2])
        if choice == 1:
            self.display_items()
        if choice == 2:
            return True

# pokemon gym
class PokemonGym(Location):

    def __init__(self, trainer_pokemon = [], trainer_levels = [], leader_pokemon=[], leader_name="Gym Leader", gym_name="", victory_message="", gym_badge=""):
        super().__init__(gym_name)
        self.trainer_pokemon = trainer_pokemon
        self.trainer_levels = trainer_levels
        self.leader_pokemon = leader_pokemon
        self.leader_name = leader_name
        self.victory_message = victory_message
        self.gym_badge = gym_badge

    def choose(self):
        slow_type(f"1. Trainer Battle\n2. Challenge Gym Leader\n3. Return to {player.map_location}")
        choice = get_valid_input("Enter number: ", [1, 2, 3])
        if choice == 1:
            self.trainer_battle(self.trainer_pokemon, self.trainer_levels)
        if choice == 2:
            self.gym_battle(self.leader_pokemon, self.leader_name, badge=self.gym_badge, victory_message=self.victory_message)
        if choice == 3:
            return True

# map location 
class MapLocation:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
    
    def change_location(self):
        slow_type(f"------------ {player.map_location} ------------")
        temp_dict = {}
        temp_index = 1
        for index, value in enumerate(player.map_location.local_locations):
            temp_dict[index+1] = value
            slow_type(f"{index+1}. {value}")
            temp_index += 1
        slow_type(f"{temp_index}. Inventory")
        choice = get_valid_input("Enter number: ", list(range(1, len(temp_dict)+2)))
        if choice == temp_index:
            self.inventory_display()
            return False
        else:
            new_location = temp_dict[choice]
            player.local_location = new_location
            return True
        
    def display_party(self):
        slow_type("------------ Party ------------")
        for pokemon in player.pokemon:
            slow_type(f"{pokemon} | {pokemon.species} | HP: {pokemon.hp}/{pokemon.maxhp}" + (" (Paralyzed)" if pokemon.paralyzed else "") + (" (Poisoned)" if pokemon.poisoned else ""))
        while True:
            slow_type("1. Switch Lead Pokemon\n2. Back")
            if get_valid_input("Enter number: ", [1, 2]) == 1:
                new_line()
                for index, value in enumerate(player.pokemon):
                    slow_type(f"{index+1}. {value}" + (" (Paralyzed)" if pokemon.paralyzed else "") + (" (Poisoned)" if pokemon.poisoned else ""))
                pokemon_choice = get_valid_input("Enter number: ", list(range(1, len(player.pokemon)+1)))
                if pokemon_choice == 1:
                    slow_type(f"{player.pokemon[0]} is already the lead pokemon.")
                    break
                else:
                    slow_type(f"{player.pokemon[pokemon_choice-1]} is now the lead pokemon.")
                    player.pokemon[0], player.pokemon[pokemon_choice-1] = player.pokemon[pokemon_choice-1], player.pokemon[0]
                    break
            else:
                break
    
    def inventory_display(self):
        while True:
            slow_type("------------ Inventory ------------")
            slow_type(f"You have ${player.money}.\n1. Check Pokemon\n2. Check Bag\n3. Check Map\n4. Check Pokedex\n5. Save Data\n6. Back")
            choice = get_valid_input("Enter number: ", [1, 2, 3, 4, 5, 6])
            if choice == 1:
                self.display_party()
            elif choice == 2:
                slow_type("------------ Bag ------------")
                if player.items == []:
                    slow_type("No items left.")
                else:
                    for index, item in enumerate(player.items):
                        slow_type(f"{index+1}. {item}")
                    slow_type(f"{len(player.items)+1}. Back")
                    choice = get_valid_input("Enter number: ", list(range(1, len(player.items)+1)))
                    if choice <= len(player.items):
                        if player.items[choice-1].itype == 'heal' or player.items[choice-1].itype == 'status_heal':
                            player.items[choice-1].use(player.pokemon, player.items)
                        else:
                            slow_type(f"{player.items[choice-1]} can't be used right now.")
                    else:
                        return
            elif choice == 3:
                player.update_map()
            elif choice == 4:
                slow_type("------------ Pokedex ------------")
                for pokemon, value in player.pokedex.items():
                    if value:
                        slow_type(f"{pokemon.species} | Type: {pokemon.ptype.capitalize()} | Weakness: {', '.join([weakness.capitalize() for weakness in pokemon.weakness])}")
            elif choice == 5:
                player.save('./savefile')
            elif choice == 6:
                return

    def location_loop(self):
        while True:
            for map_place in map_object.map_locations:
                if player.map_location == map_place:
                    for local_place in player.map_location.local_locations:
                        if player.local_location == local_place:
                            slow_type(f"------------ {local_place} ------------")
                            if local_place.choose():
                                while True:
                                    if player.map_location.change_location():
                                        break

    def black_out(self):
        player.local_location = player.map_location.pokemon_center
        slow_type("You rushed to the nearest Pokemon Center!")
        player.map_location.pokemon_center.heal()
        return True

# pallet town
class PalletTown(MapLocation):

    def __init__(self):
        super().__init__("Pallet Town")
        self.pokemonlab = PokemonLab()
        self.pokemon_center = PalletTown.MomsHouse()

    def initialize(self, *routes):
        self.local_locations=[self.pokemonlab, self.pokemon_center]
        for route in routes:
            self.local_locations.insert(0, route)

    class MomsHouse(PokemonCenter):

        def __init__(self):
            self.string = "Your Pokemon have been healed.\nTake care, honey. And have fun!"
            self.name = "Mom's House"

        def choose(self):
            slow_type(f"1. Heal Pokemon\n2. Talk to Mom\n3. Return to {player.map_location}")
            choice = get_valid_input("Enter number: ", [1, 2, 3])
            if choice == 1:
                self.heal()
            if choice == 2:
                if not player.visited_mom:
                    new_line()
                    slow_type("Welcome home! I hope you enjoy your adventure.\nI got these items for you!")
                    time.sleep(0.5)
                    slow_type(f"{player.name} obtained Mom's Gifts!")
                    player.items += [next(Potion.generate()), next(Attack_Boost.generate()), next(Defense_Boost.generate()), next(FullHeal.generate())] + [next(Pokeball().generate()) for i in range(3)]
                    player.money += 100
                    time.sleep(1)
                    slow_type("Take care now!")
                    player.visited_mom = True
                else:
                    new_line()
                    slow_type("Welcome home! I hope you're enjoying your adventure.\nBe careful and have fun.")
                    time.sleep(0.5)
            if choice == 3:
                return True

# viridian city
class ViridianCity(MapLocation):

    def __init__(self):
        super().__init__("Viridian City")
        self.pokemon_center = PokemonCenter()
        self.pokemart = Pokemart([Potion, Attack_Boost, Defense_Boost, Pokeball])

    def initialize(self, *routes):
        self.local_locations = [self.pokemon_center, self.pokemart]
        for route in routes:
            self.local_locations.insert(0, route)

# pewter city
class PewterCity(MapLocation):

    def __init__(self):
        super().__init__("Pewter City")
        self.pokemon_center = PokemonCenter()
        self.pokemart = Pokemart([Potion, Attack_Boost, Defense_Boost, Pokeball, FullHeal])
        self.pokemon_gym = PokemonGym([Geodude(), Mankey(), Sandshrew()], [8, 9, 10], [Geodude(8), Onix(12)], "Brock", "Pewter City Gym", (f"Congratulations, {player.name}. You hit like a rock!\nBest of luck on your journey."), "Rock Badge")

    def initialize(self, *routes):
        self.local_locations = [self.pokemon_gym, self.pokemon_center, self.pokemart]
        for route in routes:
            self.local_locations.insert(0, route)

# mount moon
class MountMoon(MapLocation):

    def __init__(self):
        super().__init__("Mount Moon")
        self.pokemart = Pokemart([Potion, Attack_Boost, Defense_Boost, Pokeball, FullHeal])
        self.pokemon_center = PokemonCenter(name="Hiker's House", string="Your Pokemon should be all rested up now...\nTake care. I hear there's some cool Pokemon in the cave...")

    def initialize(self, *routes):
        self.local_locations = [self.pokemart, self.pokemon_center]
        for route in routes:
            self.local_locations.insert(0, route)
            
class CeruleanCity(MapLocation):

    def __init__(self):
        super().__init__("Cerulean City")
        self.pokemon_center = PokemonCenter()
        self.pokemart = Pokemart([Potion, Attack_Boost, Defense_Boost, Pokeball, Greatball])
        self.pokemon_gym = PokemonGym([Goldeen(), Staryu()], [15, 16, 17, 18], [Staryu(18), Starmie(21)], "Misty", "Cerulean City Gym", (f"Congrats, {player.name}! It's a rainy day for me...\nWell, have fun on the rest of your journey!"), "Water Badge")

    def initialize(self, *routes):
        self.local_locations = [self.pokemart]
        for route in routes:
            self.local_locations.insert(0, route)

# create player
player = Player(name="Player", money=0)
try:
    player = Player.load('./savefile')
    slow_type(f"Loading game...")
    time.sleep(1)
except:
    player = Player(money=0)

# create locations
pallet_town = PalletTown()
viridian_city = ViridianCity()
pewter_city = PewterCity()
mount_moon = MountMoon()
cerulean_city = CeruleanCity()

# initializing
trainer_names = ["Janet", "Alissa", "Jim", "Gary", "Kaleb", "Lucas", "Vivian", "Marco", "Jake", "Harry", "Dawn", "May", "Brendan", "Alex", "Shauna", "Liko", "Goh", "Terry", "Jenny"]

route1 = Route([Rattata(), Pidgey(), Oddish(), Bellsprout()], [3, 4, 5], viridian_city, pallet_town, trainer_levels=[4, 5, 6], trainer_pokemon=[Rattata(), Pidgey(), Oddish(), Bellsprout()], name="Route 1")
viridian_forest = Route([Weedle(), Caterpie(), Bellsprout(), Rattata(), Pikachu()], [4, 5, 6], viridian_city, pewter_city, trainer_levels=[4, 5, 6], trainer_pokemon=[Bellsprout(), Rattata(), Pikachu(), Weedle(), Caterpie()], name="Route 2: Viridian Forest")
route3 = Route([Pidgey(), Spearow(), Mankey(), Sandshrew(), Rattata()], [6, 7, 8], mount_moon, pewter_city, trainer_levels= [6, 7, 8], trainer_pokemon=[Pikachu(), Sandshrew(), Vulpix(), Spearow(), Mankey()], name="Route 3")
mt_moon_cave = Route([Magnemite(), Cubone(), Diglett(), Rattata(), Geodude(), Zubat()], [8, 9, 10, 11], mount_moon, None, trainer_levels=[9, 10, 11, 12], trainer_pokemon=[Magnemite(), Cubone(), Diglett(), Geodude()], name="Mount Moon Cave")
route4 = Route([Ekans(), Spearow(), Sandshrew(), Mankey(), Raticate()], [10, 11, 12, 13], mount_moon, cerulean_city, trainer_levels=[11, 12, 13, 14], trainer_pokemon=[Magnemite(), Cubone(), Diglett(), Geodude()], name="Route 4")

map_object = MapLocation("Map")

map_object.map_locations = [pallet_town, viridian_city, pewter_city, mount_moon, cerulean_city]
pallet_town.initialize(route1)
viridian_city.initialize(route1, viridian_forest)
pewter_city.initialize(viridian_forest, route3)
mount_moon.initialize(route3, mt_moon_cave, route4)
cerulean_city.initialize(route4)

# intialize player location
player.initialize()

# get starter pokemon

starters = ['Charmander', 'Bulbasaur', 'Squirtle']

# starting functions
def intro():
    global player
    slow_type("Welcome to the world of Pokemon!\nWhat is your name?.")
    name = input("Enter: ").strip()
    player.name = name
    slow_type(f"Nice to meet you, {player.name}. I'm Professor Oak.\nLet's get started with you choosing your Pokemon.")
    new_line()

def get_starter():
    global oak_pokemon
    slow_type(f"Choose your starter!\n1. {starters[0]}\n2. {starters[1]}\n3. {starters[2]}")
    starter_choice = get_valid_input("Enter number: ", [1, 2, 3])
    slow_type(f"You chose {starters[starter_choice-1]}.")
    starter_nickname = input("Give it a nickname: ").strip()
    if starter_choice == 1:
        player.pokemon.append(Charmander(5, name=starter_nickname, moves=Charmander.generate_moves(5), player_owned=True))
        oak_pokemon = next(Bulbasaur.generate(5))
    elif starter_choice == 2:
        player.pokemon.append(Bulbasaur(5, name=starter_nickname, moves=Bulbasaur.generate_moves(5), player_owned=True))
        oak_pokemon = next(Squirtle.generate(5))
    elif starter_choice == 3:
        player.pokemon.append(Squirtle(5, name=starter_nickname, moves=Squirtle.generate_moves(5), player_owned=True))
        oak_pokemon = next(Charmander.generate(5))
    for pokemon1, value in player.pokedex.items():
        for pokemon2 in player.pokemon:
            if pokemon1.species == pokemon2.species:
                player.pokedex[pokemon1] = True
    starters.pop(starter_choice-1)
    backup = starters
    new_line()

def intro2():
    slow_type("Now, let's have our first battle.")
    time.sleep(0.5)
    slow_type("I challenge you!")

# game
if __name__ == "__main__":

    if not player.tutorial_beat:

        intro()
        get_starter()
        intro2()
        
        while True:
            player.local_location = player.map_location.pokemonlab
            if Battle([oak_pokemon], wild=False, trainer=True, trainer_name="Professor Oak", runnable=False).battle():
                new_line()
                slow_type("You're ready to set out.\nCatch Pokemon and train them.\nDefeat the Gym Leader in\nPewter City to win!")
                time.sleep(1)
                player.tutorial_beat = True
                break
            else:
                player.map_location.black_out()
                new_line()
                slow_type("Ah, you're back. Let's try that again.")
    try:
        player.map_location.change_location()
    except:
        print('hi')
        pass
    player.map_location.location_loop()