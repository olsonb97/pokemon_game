import random
import time
import copy

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
    
    def __init__(self, name, mtype, power, accuracy, special=False, status=None):
        self.name = name
        self.mtype = mtype
        self.power = power
        self.accuracy = accuracy
        self.special = special
        self.status = status

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
ember = Move("Ember", 'fire', 9, 80)
bubble = Move("Bubble", 'water', 9, 80)
vine_whip = Move("Vine Whip", 'grass', 9, 80)
tackle = Move("Tackle", 'normal', 6, 100)
yawn = Move("Yawn", 'normal', 0, 50, special=True, status='asleep')
confuse_ray = Move("Confuse Ray", 'normal', 0, 40, special=True, status='confused')
splash = Move("Spash", 'normal', 0, 50)
wing_attack = Move("Wing Attack", 'normal', 8, 90)
scratch = Move("Scratch", 'normal', 7, 95)
spark = Move("Spark", 'normal', 10, 85)
bulldoze = Move("Bulldoze", 'ground', 10, 80)
toxic = Move("Toxic", 'poison', 0, 80, special=True, status='poisoned')
paralyze = Move("Paralyze", 'electric', 0, 60, special=True, status='paralyzed')
bug_bite = Move("Bug Bite", 'bug', 7, 85)
psychic = Move("Psychic", 'psychic', 8, 90)
shadow_ball = Move("Shadow Ball", 'ghost', 8, 90)
rock_throw = Move("Rock Throw", 'rock', 8, 90)
low_kick = Move("Low Kick", 'fighting', 8, 90)


# move sets
fire_moves = [ember, tackle, yawn, confuse_ray]
grass_moves = [vine_whip, tackle, toxic, confuse_ray]
water_moves = [bubble, tackle, yawn, confuse_ray]
god_moves = [bubble, ember, paralyze, toxic]

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
        self.paralyzed_counter = 0
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
                for key, val in self.learnable_moves.items():
                    self.learn_move(key, val)
                self.xp -= 100
            time.sleep(0.5)


    def learn_move(self, level, move):
        if self.level == level:
            time.sleep(0.5)
            new_line()
            if len(self.move_set) < 4:
                slow_type(f"{self.name} learned {move}!")
                self.move_set.append(move)
            else:
                slow_type(f"{self.name} is trying to learn {move}.\nDelete a move to make room?\n1. Yes\n2. No")
                choice = get_valid_input("Enter number: ", [1, 2])
                if choice == 1:
                    for index, value in enumerate(self.move_set):
                        slow_type(f"{index + 1}. {value}")
                    move_index = get_valid_input("Enter number: ", [1, 2, 3, 4])-1
                    slow_type(f"{self.name} forgot {self.move_set[move_index]}...")
                    time.sleep(1)
                    slow_type(f"...and learned {move}!")
                    self.move_set[move_index] = move
                elif choice == 2:
                    return

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
            player.pokedex[self.evolve_pokemon1] = True
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
            player.pokedex[self.evolve_pokemon2] = True
            slow_type(f"{self.evolve_pokemon2} was registered in the Pokedex.")
            time.sleep(1)
            self.evolved2 = True

    @classmethod
    def generate(cls, level):
        yield cls(level)

# pokemon subclasses
class Charmander(Pokemon):
    
    def __init__(self, level=5, name='', player_owned=False):
        super().__init__('Charmander', 35, 'fire', 1.1, 1.1, level, fire_moves, name, player_owned)
        self.evolve_level1 = 16
        self.evolve_pokemon1 = Charmeleon()
        self.evolve_level2 = 36
        self.evolve_pokemon2 = Charizard()
        self.learnable_moves = {6: scratch}

class Charmeleon(Pokemon):
    
    def __init__(self, level=8, name='', player_owned=False):
        super().__init__('Charmeleon', 40, 'fire', 1.15, 1.1, level, fire_moves, name, player_owned)
        self.evolve_level1 = 36
        self.evolve_pokemon1 = Charizard()

class Charizard(Pokemon):
    
    def __init__(self, level=12, name='', player_owned=False):
        super().__init__('Charizard', 45, 'fire', 1.19, 1.12, level, fire_moves, name, player_owned)

class Bulbasaur(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Bulbasaur', 40, 'grass', 1, 1, level, grass_moves, name, player_owned)
        self.evolve_level1 = 16
        self.evolve_pokemon1 = Ivysaur()
        self.evolve_level2 = 32
        self.evolve_pokemon2 = Venusaur()

class Ivysaur(Pokemon):

    def __init__(self, level=8, name="", player_owned=False):
        super().__init__('Ivysaur', 45, 'grass', 1.1, 1, level, grass_moves, name, player_owned)
        self.evolve_level1 = 32
        self.evolve_pokemon1 = Venusaur()

class Venusaur(Pokemon):

    def __init__(self, level=12, name="", player_owned=False):
        super().__init__('Venusaur', 45, 'grass', 1.2, 1, level, grass_moves, name, player_owned)
    
class Squirtle(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Squirtle', 38, 'water', 1.05, 1.05, level, water_moves, name, player_owned)
        self.evolve_level1 = 16
        self.evolve_pokemon1 = Wartortle()
        self.evolve_level2 = 32
        self.evolve_pokemon2 = Blastoise()

class Wartortle(Pokemon):

    def __init__(self, level=8, name="", player_owned=False):
        super().__init__('Wartortle', 42, 'water', 1.1, 1.05, level, water_moves, name, player_owned)
        self.evolve_level1 = 32
        self.evolve_pokemon1 = Blastoise()

class Blastoise(Pokemon):

    def __init__(self, level=12, name="", player_owned=False):
        super().__init__('Blastoise', 42, 'water', 1.15, 1.03, level, water_moves, name, player_owned)

class Rattata(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Rattata', 40, 'normal', 1.1, 1.05, level, [tackle, scratch, confuse_ray], name, player_owned)
        self.evolve_pokemon1 = Raticate()
        self.evolve_level1 = 20
        
class Staryu(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Staryu', 36, 'water', 1.05, 1.05, level, [tackle, bubble, paralyze, confuse_ray], name, player_owned)
        self.evolve_pokemon1 = Starmie()
        self.evolve_level1 = 36
        
class Starmie(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Starmie', 41, 'water', 1.15, 1.05, level, [tackle, bubble, paralyze, confuse_ray], name, player_owned)
        
class Goldeen(Pokemon):
    
    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Goldeen', 36, 'water', 1.05, 1.05, level, [tackle, bubble, confuse_ray], name, player_owned)
        self.evolve_level1 = 33
        self.evolve_pokemon1 = Seaking()
        
class Seaking(Pokemon):
    
    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Seaking', 42, 'water', 1.1, 1.05, level, [tackle, bubble, confuse_ray], name, player_owned)

class Raticate(Pokemon):

    def __init__(self, level=8, name="", player_owned=False):
        super().__init__('Raticate', 42, 'normal', 1.12, 1.05, level, [tackle, scratch, confuse_ray], name, player_owned)

class Magikarp(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Magikarp', 38, 'water', 1, 1.15, level, [splash], name, player_owned)
        self.evolve_level1 = 20
        self.evolve_pokemon1 = Gyarados()
        self.learnable_moves = {20: bubble, 20: tackle}

class Gyarados(Pokemon):

    def __init__(self, level=12, name="", player_owned=False):
        super().__init__('Gyarados', 43, 'water', 1.2, 1.1, level, [water_moves], name, player_owned)

class Caterpie(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Caterpie', 36, 'bug', 1.05, 1.05, level, [confuse_ray, vine_whip, toxic], name, player_owned)
        self.evolve_level1 = 7
        self.evolve_pokemon1 = Metapod()
        self.evolve_level2 = 10
        self.evolve_pokemon2 = Butterfree()

class Metapod(Pokemon):

    def __init__(self, level=8, name="", player_owned=False):
        super().__init__('Metapod', 42, 'bug', 1.05, 1, level, [confuse_ray, vine_whip, toxic], name, player_owned)
        self.evolve_level1 = 10
        self.evolve_pokemon1 = Butterfree()

class Butterfree(Pokemon):

    def __init__(self, level=12, name="", player_owned=False):
        super().__init__('Butterfree', 42, 'bug', 1.1, 1.05, level, [confuse_ray, vine_whip, toxic], name, player_owned)

class Vulpix(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Vulpix', 37, 'fire', 1.1, 1.05, level, [ember, tackle, confuse_ray], name, player_owned)

class Pidgey(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Pidgey', 35, 'flying', 1.15, 1.15, level, [wing_attack, scratch], name, player_owned)
        self.evolve_pokemon1 = Pidgeotto()
        self.evolve_level1 = 18
        self.evolve_pokemon2 = Pidgeot()
        self.evolve_level2 = 36

class Pidgeotto(Pokemon):

    def __init__(self, level=8, name="", player_owned=False):
        super().__init__('Pidgeotto', 38, 'flying', 1.17, 1.1, level, [wing_attack, scratch], name, player_owned)
        self.evolve_level1 = 36
        self.evolve_pokemon1 = Pidgeot()

class Pidgeot(Pokemon):

    def __init__(self, level=12, name="", player_owned=False):
        super().__init__('Pidgeot', 41, 'flying', 1.19, 1.1, level, [wing_attack, scratch], name, player_owned)

class Weedle(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Weedle', 34, 'bug', 1.05, 1.15, level, [confuse_ray, tackle, toxic], name, player_owned)
        self.evolve_level1 = 7
        self.evolve_pokemon1 = Kakuna()
        self.evolve_level2 = 10
        self.evolve_pokemon2 = Beedrill()

class Kakuna(Pokemon):

    def __init__(self, level=8, name="", player_owned=False):
        super().__init__('Kakuna', 42, 'bug', 1.05, 1, level, [confuse_ray, vine_whip, yawn, toxic], name, player_owned)
        self.evolve_level1 = 10
        self.evolve_pokemon1 = Beedrill()

class Beedrill(Pokemon):

    def __init__(self, level=12, name="", player_owned=False):
        super().__init__('Beedrill', 42, 'bug', 1.1, 1.05, level, [confuse_ray, vine_whip, yawn, toxic], name, player_owned)

class Pikachu(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Pikachu', 40, 'electric', 1.15, 1.05, level, [scratch, tackle, confuse_ray, spark], name, player_owned)

class Diglett(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Diglett', 40, 'ground', 1.1, 1.15, level, [bulldoze, tackle, confuse_ray], name, player_owned)
        self.evolve_level1 = 26
        self.evolve_pokemon1 = Dugtrio()

class Dugtrio(Pokemon):

    def __init__(self, level=8, name="", player_owned=False):
        super().__init__('Dugtrio', 43, 'ground', 1.13, 1.12, level, [bulldoze, tackle, confuse_ray], name, player_owned)

class Cubone(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Cubone', 40, 'ground', 1.15, 1.05, level, [scratch, rock_throw, confuse_ray, bulldoze], name, player_owned)
        self.evolve_level1 = 28
        self.evolve_pokemon1 = Marowak()

class Marowak(Pokemon):

    def __init__(self, level=8, name="", player_owned=False):
        super().__init__('Marowak', 42, 'ground', 1.15, 1.1, level, [scratch, rock_throw, confuse_ray, bulldoze], name, player_owned)

class Magnemite(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Magnemite', 40, 'electric', 1.05, 1.05, level, [confuse_ray, spark, paralyze], name, player_owned)
        self.evolve_level1 = 30
        self.evolve_pokemon1 = Magneton()

class Magneton(Pokemon):

    def __init__(self, level=8, name="", player_owned=False):
        super().__init__('Magneton', 41, 'electric', 1.1, 1.05, level, [confuse_ray, spark, paralyze], name, player_owned)

class Geodude(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Geodude', 40, 'normal', 1.1, 1.05, level, [rock_throw, confuse_ray, bulldoze], name, player_owned)
        self.evolve_pokemon1 = Graveler()
        self.evolve_level1 = 25

class Graveler(Pokemon):

    def __init__(self, level=8, name="", player_owned=False):
        super().__init__('Graveler', 44, 'normal', 1.1, 1.05, level, [rock_throw, confuse_ray, bulldoze], name, player_owned)
        
class Onix(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Onix', 40, 'rock', 1.1, 1.05, level, [rock_throw, confuse_ray, bulldoze, tackle], name, player_owned)
        
class Bellsprout(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Bellsprout', 34, 'grass', 1.05, 1.1, level, [tackle, vine_whip, confuse_ray, yawn], name, player_owned)
        self.evolve_level1 = 21
        self.evolve_pokemon1 = Weepinbell()
        
class Weepinbell(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Weepinbell', 38, 'grass', 1.1, 1.1, level, [tackle, vine_whip, confuse_ray, yawn], name, player_owned)
        
class Oddish(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Oddish', 35, 'grass', 1.1, 1.15, level, [tackle, vine_whip, confuse_ray, toxic], name, player_owned)
        self.evolve_level1 = 21
        self.evolve_pokemon1 = Gloom()
        
class Gloom(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Gloom', 38, 'grass', 1.1, 1.1, level, [tackle, vine_whip, confuse_ray, toxic], name, player_owned)

class Spearow(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Spearow', 37, 'flying', 1.1, 1.1, level, [scratch, wing_attack, confuse_ray], name, player_owned)
        self.evolve_level1 = 21
        self.evolve_pokemon1 = Fearow()
        
class Fearow(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Fearow', 39, 'flying', 1.15, 1.1, level, [scratch, wing_attack, confuse_ray], name, player_owned)
        
class Ekans(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Ekans', 37, 'poison', 1.15, 1.1, level, [toxic, tackle, paralyze], name, player_owned)
        self.evolve_level1 = 22
        self.evolve_pokemon1 = Arbok()
        
class Arbok(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Arbok', 39, 'poison', 1.17, 1.1, level, [toxic, tackle, paralyze], name, player_owned)
        
class Sandshrew(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Sandshrew', 36, 'ground', 1.13, 1.1, level, [scratch, bulldoze, paralyze], name, player_owned)
        self.evolve_level1 = 22
        self.evolve_pokemon1 = Sandslash()
        
class Sandslash(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Sandslash', 39, 'ground', 1.17, 1.1, level, [scratch, bulldoze, paralyze], name, player_owned)
        
class Mankey(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Mankey', 36, 'fighting', 1.12, 1.16, level, [tackle, paralyze, rock_throw, low_kick], name, player_owned)
        self.evolve_level1 = 28
        self.evolve_pokemon1 = Primeape()
        
class Primeape(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Primeape', 40, 'fighting', 1.16, 1.12, level, [tackle, paralyze, rock_throw, low_kick], name, player_owned)
        
class Zubat(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Zubat', 35, 'flying', 1.08, 1.12, level, [paralyze, tackle, wing_attack], name, player_owned)
        self.evolve_level1 = 22
        self.evolve_pokemon1 = Golbat()
        
class Golbat(Pokemon):

    def __init__(self, level=5, name="", player_owned=False):
        super().__init__('Golbat', 40, 'flying', 1.1, 1.11, level, [paralyze, tackle, wing_attack], name, player_owned)

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
            if pokemon.hp > 0:
                self.active_pokemon = pokemon
                break

    def opening_statement(self):
        if self.wild:
            return slow_type(f"Wild {self.active_enemy_pokemon.name} appeared!")
        return slow_type(f"{self.trainer_name} challenges you to a battle!\n{self.trainer_name} sent out {self.active_enemy_pokemon.name}!")

    def get_damage(self, attacker, move):
        damage = round(attacker.attack * move.power)
        return damage
    
    def take_damage(self, attacker, defender, move, damage):
        accuracy_roll = random.randint(1, 101)
        if accuracy_roll in range(1, move.accuracy):
            damage = round(defender.defense * damage)
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
            if not i.special:
                slow_type(f"{self.active_pokemon.move_set.index(i)+1}. {i.name} | Power: {i.power} | Type: {i.mtype.capitalize()} | Accuracy: {i.accuracy}")
            elif i.special:
                slow_type(f"{self.active_pokemon.move_set.index(i)+1}. {i.name} | Status Effect: {i.status.capitalize()} | Accuracy: {i.accuracy}")

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
                paralyzee.paralyzed_counter = 0
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
                    checkee.confused = False
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
        pokemon.asleep_counter = 0
        pokemon.confused_counter = 0
        pokemon.poisoned_counter = 1
        pokemon.paralyzed_counter = 0
        pokemon.paralyzed = False
        pokemon.poisoned = False
        pokemon.asleep = False
        pokemon.confused = False
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
        if not move.special:
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

    def catch_sequence(self, pokeball):
        counter = 0
        while counter < 5:
            slow_type("...")
            time.sleep(0.5)
            if random.randint(1, 100) in range(1, pokeball.power*round(self.active_enemy_pokemon.maxhp/self.active_enemy_pokemon.hp)):
                counter += 1
                if counter >= 5:
                    slow_type(f"{self.active_enemy_pokemon} was caught!")
                    time.sleep(0.5)
                    return True
            else:
                slow_type(f"{self.active_enemy_pokemon} escaped the {pokeball}...")
                time.sleep(0.5)
                return False

    def use_item(self, item):
        if item.name == "Potion":
            slow_type("Use on which Pokemon?")
            self.print_user_pokemon()
            pokemon_index = get_valid_input("Enter number: ", list(range(1, len(self.user_pokemon)+1)))-1
            pokemon_choice = self.user_pokemon[pokemon_index]
            if pokemon_choice.hp >= pokemon_choice.maxhp:
                slow_type(f"{pokemon_choice} is already at full health.")
                return False
            pokemon_choice.hp += 20
            if pokemon_choice.hp > pokemon_choice.maxhp:
                pokemon_choice.hp = pokemon_choice.maxhp
            slow_type(f"{pokemon_choice} healed for 20 HP.")
            self.print_health(pokemon_choice, user=True)
            self.user_items.remove(item)
            return True
        elif item.name == "Attack Boost":
            new_attack = round(self.active_pokemon.attack + item.power, 2)
            slow_type(f"{self.active_pokemon}'s attack raised from {self.active_pokemon.attack} to {new_attack}!")
            self.active_pokemon.attack = new_attack
            self.user_items.remove(item)
            return True
        elif item.name == "Defense Boost":
            new_defense = round(self.active_pokemon.defense - item.power, 2)
            slow_type(f"{self.active_pokemon}'s defense raised from {self.active_pokemon.defense} to {new_defense}!")
            self.active_pokemon.defense = new_defense
            self.user_items.remove(item)
            return True
        elif item.itype == 'catch':
            if self.wild:
                if self.catch_sequence(item):
                    self.active_enemy_pokemon.player_owned=True
                    if len(self.user_pokemon) < 6:
                        nickname = input("Give it a name: ")
                        self.active_enemy_pokemon.name = nickname
                        player.pokemon.append(self.active_enemy_pokemon)
                        slow_type(f"{self.active_enemy_pokemon} was added to your party")
                    else:
                        slow_type(f"Party is full. {self.active_enemy_pokemon} was released.")
                    self.user_items.remove(item)
                    return True
                else:
                    self.user_items.remove(item)
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
            for pokemon, value in player.pokedex.items():
                if pokemon.species == self.active_enemy_pokemon.species:
                    player.pokedex[pokemon] = True
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

class Attack_Boost(Item):

    id = 1
    def __init__(self):
        super().__init__("Attack Boost", "attack", 0.15)
        self.cost = 100
        self.id = Attack_Boost.id
        Attack_Boost.id += 1

class Defense_Boost(Item):

    id = 1
    def __init__(self):
        super().__init__("Defense Boost", "defense", 0.15)
        self.cost = 100
        self.id = Defense_Boost.id
        Defense_Boost.id += 1

class Pokeball(Item):

    id = 1
    def __init__(self):
        super().__init__("Pokeball", "catch", 25)
        self.cost = 50
        self.id = Pokeball.id
        Pokeball.id += 1

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
        self.name = name
        self.money = money
        self.gym_badges= []

    def initialize(self):
        self.map_location = pallet_town
        self.local_location = pallet_town.pokemonlab

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
            for pokemon in player.map_location.pokemon_gym.leader_pokemon:
                pokemon.hp = pokemon.maxhp
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
            pokemon.confused = False
            pokemon.asleep = False
            pokemon.paralyzed = False
            pokemon.poisoned = False
            pokemon.confused_counter = 0
            pokemon.asleep_counter = 0
            pokemon.paralyzed_counter = 0
            pokemon.poisoned_counter = 1
        slow_type("......", 0.5)
        slow_type(self.string)

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

    def __init__(self, trainer_pokemon = [], trainer_levels = [], leader_pokemon=[], leader_name="Gym Leader", gym_name=""):
        super().__init__(gym_name)
        self.trainer_pokemon = trainer_pokemon
        self.trainer_levels = trainer_levels
        self.leader_pokemon = leader_pokemon
        self.leader_name = leader_name

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
    
    def inventory_display(self):
        while True:
            slow_type("------------ Inventory ------------")
            slow_type(f"You have ${player.money}.\n1. Check Pokemon\n2. Check Bag\n3. Check Map\n4. Check Pokedex\n5. Back")
            choice = get_valid_input("Enter number: ", [1, 2, 3, 4, 5])
            if choice == 1:
                slow_type("------------ Party ------------")
                for pokemon in player.pokemon:
                    slow_type(f"{pokemon} | {pokemon.species} | HP: {pokemon.hp}/{pokemon.maxhp}" + (" (Paralyzed)" if pokemon.paralyzed else "") + (" (Poisoned)" if pokemon.poisoned else ""))
                while True:
                    if get_valid_input("1. Switch Lead Pokemon\n2. Back\nEnter number: ", [1, 2]) == 1:
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

            if choice == 2:
                slow_type("------------ Bag ------------")
                if player.items == []:
                    slow_type("No items left.")
                for item in player.items:
                    slow_type(f"{item}")
            if choice == 3:
                slow_type(player.map)
            if choice == 4:
                slow_type("------------ Pokedex ------------")
                for pokemon, value in player.pokedex.items():
                    if value:
                        slow_type(f"{pokemon.species} | Type: {pokemon.ptype.capitalize()} | Weakness: {', '.join([weakness.capitalize() for weakness in pokemon.weakness])}")
            if choice == 5:
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
            self.visited = False
            self.string = "Your Pokemon have been healed.\nTake care, honey. And have fun!"
            self.name = "Mom's House"

        def choose(self):
            slow_type(f"1. Heal Pokemon\n2. Talk to Mom\n3. Return to {player.map_location}")
            choice = get_valid_input("Enter number: ", [1, 2, 3])
            if choice == 1:
                self.heal()
            if choice == 2:
                if not self.visited:
                    new_line()
                    slow_type("Welcome home! I hope you enjoy your adventure.\nI got these items for you!")
                    time.sleep(0.5)
                    slow_type(f"{player.name} obtained Mom's Gifts!")
                    player.items += [next(Potion().generate()), next(Attack_Boost().generate()), next(Defense_Boost().generate())] + [next(Pokeball().generate()) for i in range(3)]
                    player.money += 100
                    time.sleep(1)
                    slow_type("Take care now!")
                    self.visited = True
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
        self.pokemart = Pokemart([Potion(), Attack_Boost(), Defense_Boost(), Pokeball()])

    def initialize(self, *routes):
        self.local_locations = [self.pokemon_center, self.pokemart]
        for route in routes:
            self.local_locations.insert(0, route)

# pewter city
class PewterCity(MapLocation):

    def __init__(self):
        super().__init__("Pewter City")
        self.pokemon_center = PokemonCenter()
        self.pokemart = Pokemart([Potion(), Attack_Boost(), Defense_Boost(), Pokeball()])
        self.pokemon_gym = PokemonGym([Geodude(), Mankey(), Sandshrew()], [8, 9, 10], [Geodude(8), Onix(12)], "Brock", "Pewter City Gym")
        self.badge = "Rock Badge"
        self.victory_message = f"Congratulations, {player.name}. You hit like a rock!\nBest of luck on your journey."

    def initialize(self, *routes):
        self.local_locations = [self.pokemon_gym, self.pokemon_center, self.pokemart]
        for route in routes:
            self.local_locations.insert(0, route)

# mount moon
class MountMoon(MapLocation):

    def __init__(self):
        super().__init__("Mount Moon")
        self.pokemart = Pokemart([Potion(), Attack_Boost(), Defense_Boost(), Pokeball()])

    def initialize(self, *routes):
        self.local_locations = [self.pokemart]
        for route in routes:
            self.local_locations.insert(0, route)
            
class CeruleanCity(MapLocation):

    def __init__(self):
        super().__init__("Cerulean City")
        self.pokemon_center = PokemonCenter()
        self.pokemart = Pokemart([Potion(), Attack_Boost(), Defense_Boost(), Pokeball(), Greatball()])
        self.pokemon_gym = PokemonGym([Goldeen(), Staryu()], [15, 16, 17, 18], [Staryu(18), Starmie(21)], "Misty", "Cerulean City Gym")
        self.badge = "Water Badge"
        self.victory_message = f"Congrats, {player.name}! It's a rainy day for me...\nWell, have fun on the rest of your journey!"

    def initialize(self, *routes):
        self.local_locations = [self.pokemart]
        for route in routes:
            self.local_locations.insert(0, route)

# create plaayer
player = Player(money=0)

# create locations
pallet_town = PalletTown()
viridian_city = ViridianCity()
pewter_city = PewterCity()
mount_moon = MountMoon()
cerulean_city = CeruleanCity()

# initializing
route1 = Route([Magikarp(), Rattata(), Pidgey(), Oddish(), Bellsprout()], [3, 4, 5], viridian_city, pallet_town, trainer_levels=[4, 5, 6], trainer_pokemon=[Rattata(), Pidgey(), Oddish(), Bellsprout()], name="Route 1")
viridian_forest = Route([Weedle(), Caterpie(), Bellsprout(), Rattata(), Pikachu()], [4, 5, 6], viridian_city, pewter_city, trainer_levels=[4, 5, 6], trainer_pokemon=[Bellsprout(), Rattata(), Pikachu(), Weedle(), Caterpie()], name="Route 2: Viridian Forest")
route3 = Route([Pidgey(), Spearow(), Mankey(), Sandshrew(), Rattata()], [6, 7, 8], mount_moon, pewter_city, trainer_levels= [6, 7, 8], trainer_pokemon=[Pikachu(), Sandshrew(), Vulpix(), Spearow(), Mankey()], name="Route 3")
mt_moon_cave = Route([Magnemite(), Cubone(), Diglett(), Rattata(), Geodude(), Zubat()], [8, 9, 10, 11], mount_moon, None, trainer_levels=[9, 10, 11, 12], trainer_pokemon=[Magnemite(), Cubone(), Diglett(), Geodude()], name="Mount Moon Cave")
route4 = Route([Ekans(), Spearow(), Sandshrew(), Mankey(), Raticate()], [10, 11, 12, 13], mount_moon, cerulean_city, trainer_levels=[11, 12, 13, 14], trainer_pokemon=[Magnemite(), Cubone(), Diglett(), Geodude()], name="Route 4")
map_object = MapLocation("Map")
map_object.map_locations = [pallet_town, viridian_city, pewter_city, mount_moon, cerulean_city]
player.initialize()
pallet_town.initialize(route1)
viridian_city.initialize(route1, viridian_forest)
pewter_city.initialize(viridian_forest, route3)
mount_moon.initialize(route3, mt_moon_cave)
trainer_names = ["Janet", "Alissa", "Jim", "Gary", "Kaleb", "Lucas", "Vivian", "Marco", "Jake", "Harry", "Dawn", "May", "Brendan", "Alex", "Shauna", "Liko", "Goh", "Terry", "Jenny"]

# beginning pokemon party

player.pokemon = []
player.items = []
player.map ="""
   Pallet Town
        V
     Route 1
        V
   Viridian City
        V
Route 2: Viridian Forest
        V
   Pewter City
        V
     Route 3
        V
     Mt Moon -----> Mt Moon Cave
        V
     Route 4
        V
  Cerulean City
"""
player.pokedex = {
Charmander(): False,
Bulbasaur(): False,
Squirtle(): False
}
player.pokedex = {pokemon: player.pokedex[pokemon] for pokemon in sorted(player.pokedex, key=lambda x: x.name)}

player.inventory = {'pokemon': player.pokemon, 'items': player.items}

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
        player.pokemon.append(Charmander(5, name=starter_nickname, player_owned=True))
        oak_pokemon = next(Bulbasaur.generate(5))
    elif starter_choice == 2:
        player.pokemon.append(Bulbasaur(5, name=starter_nickname, player_owned=True))
        oak_pokemon = next(Squirtle.generate(5))
    elif starter_choice == 3:
        player.pokemon.append(Squirtle(5, starter_nickname, player_owned=True))
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

    intro()
    get_starter()
    intro2()
    
    while True:
        player.local_location = player.map_location.pokemonlab
        if Battle([oak_pokemon], wild=False, trainer=True, trainer_name="Professor Oak", runnable=False).battle():
            new_line()
            slow_type("You're ready to set out.\nCatch Pokemon and train them.\nDefeat the Gym Leader in\nPewter City to win!")
            time.sleep(1)
            break
        else:
            player.map_location.black_out()
            oak_pokemon.hp = oak_pokemon.maxhp
            new_line()
            slow_type("Ah, you're back. Let's try that again.")

    player.map_location.location_loop()
