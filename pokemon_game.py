import random
import time
import copy
import pickle
import os
from extra_classes import *

def slow_type(text, delay=0.008):

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

def check_pokedex(pokemon, player_obj):
    while True:
        found = False
        for pokedex_entry in player_obj.pokedex.keys():
            if pokedex_entry.species == pokemon.species:
                found = True
        if found == True:
            break
        else:
            player_obj.pokedex[pokemon] = True
            break

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
        for pokemon in self.user_pokemon:
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

    def get_damage(self, attacker, defender, move):
        damage = round(attacker.attack * move.power * (attacker.level/5))
        if move.mtype == attacker.ptype:
            damage *= 1.2
        return damage
    
    def take_damage(self, attacker, defender, move, damage):
        accuracy_roll = random.randint(1, 100)
        if accuracy_roll <= move.accuracy:
            damage = round(damage / defender.defense)
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
                slow_type(f"{self.active_pokemon.move_set.index(i)+1}. {i.name} | Power: {i.power} | Type: {i.mtype.capitalize()} | Accuracy: {i.accuracy}", 0.001)
            elif i.special:
                slow_type(f"{self.active_pokemon.move_set.index(i)+1}. {i.name} | Status: {i.status.capitalize()} | Accuracy: {i.accuracy}", 0.001)
            elif i.stat is not None:
                slow_type(f"{self.active_pokemon.move_set.index(i)+1}. {i.name} | Stat Change: {i.stat_target.capitalize()}'s {i.stat.capitalize()} | Accuracy: {i.accuracy}", 0.001)

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
                if attacker.attack_counter <= 2:
                    attacker.attack /= move.stat_change
                    attacker.attack_counter += 1
                    slow_type(f"{attacker}'s attack was raised.")
                else:
                    slow_type(f"{attacker}'s attack won't go any higher.")
            elif move.stat_target == 'enemy':
                if defender.attack_counter >= -2 and defender.attack != 1:
                    defender.attack *= move.stat_change
                    defender.attack_counter -= 1
                    if defender.attack <= 1:
                        defender.attack = 1
                    slow_type(f"{defender}'s attack was lowered.")
                else:
                    slow_type(f"{defender}'s attack won't go any lower.")
        elif move.stat == 'defense':
            if move.stat_target == 'user':
                if attacker.defense_counter <= 2 and attacker.defense >= 1:
                    attacker.defense /= move.stat_change
                    attacker.defense_counter += 1
                    if attacker.defense <= 1:
                        attacker.defense = 1
                    slow_type(f"{attacker}'s defense was raised.")
                else:
                    slow_type(f"{attacker}'s defense won't go any higher.")
            elif move.stat_target == 'enemy':
                if defender.defense_counter >= -2:
                    defender.defense *= move.stat_change
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
            self.active_pokemon.xp_boost(self.calculate_xp())

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
                    slow_type(f"{self.active_enemy_pokemon} was knocked out!\nYou won the battle!")
                self.battle_victory = True
                
                # money
                if not self.trainer_name == "":
                    money_won = round(100 * ((sum([pokemon.level for pokemon in self.trainer_pokemon])*len(self.trainer_pokemon))/(sum([pokemon.level for pokemon in self.user_pokemon])*len(self.user_pokemon))))
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
                            evolved_pokemon, value = main_pokemon.evolve()
                            if value:
                                check_pokedex(evolved_pokemon, player)
                        except:
                            pass
                    
        player.items = self.user_items
    
    def attack_turn(self, attacker, defender, move):
        damage = self.get_damage(attacker, defender, move)
        if move.power > 0:
            self.take_damage(attacker, defender, move, damage)
            if attacker == self.active_pokemon:
                self.print_health(self.active_enemy_pokemon, enemy=True)
            elif attacker == self.active_enemy_pokemon:
                self.print_health(self.active_pokemon, user=True)
        if move.special:
            if move.status == 'asleep':
                self.make_asleep(defender, move)
            if move.status == 'confused':
                self.make_confused(defender, move)
            if move.status == 'paralyzed':
                self.make_paralyzed(defender, move)
            if move.status == 'poisoned':
                self.make_poisoned(defender, move)
        if move.stat is not None:
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
                move_choice = get_valid_input("Enter number: ", list(range(1, len(self.active_pokemon.move_set)+1)))-1
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
            check_pokedex(self.active_enemy_pokemon, player)
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

class KeyItem:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

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
        super().__init__("Attack Boost", "attack", 1.1)
        self.cost = 100
        self.id = Attack_Boost.id
        Attack_Boost.id += 1

    def use(self, pokemon, item_list):
        new_attack = round(pokemon.attack * self.power, 2)
        slow_type(f"{pokemon}'s attack was raised!")
        pokemon.attack = new_attack
        item_list.remove(self)
        return True

class Defense_Boost(Item):

    id = 1
    def __init__(self):
        super().__init__("Defense Boost", "defense", 1.1)
        self.cost = 100
        self.id = Defense_Boost.id
        Defense_Boost.id += 1

    def use(self, pokemon, item_list):
        new_defense = round(pokemon.defense * self.power, 2)
        slow_type(f"{pokemon}'s defense was raised!")
        pokemon.defense = new_defense
        item_list.remove(self)
        return True

class Pokeball(Item):

    id = 1
    def __init__(self):
        super().__init__("Pokeball", "catch", 15)
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
        super().__init__("Great Ball", "catch", 20)
        self.cost = 100
        self.id = Pokeball.id
        Greatball.id += 1
    
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

class Ultraball(Item):

    id = 1
    def __init__(self):
        super().__init__("Ultra Ball", "catch", 25)
        self.cost = 150
        self.id = Pokeball.id
        Ultraball.id += 1

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

class TM(Item):

    id = 1
    def __init__(self, move):
        super().__init__("TM", "tmhm", move)
        self.name = f"TM: {move.name}"
        self.move = move

    def use(self, party, item_list):
        counter = 1
        for index, pokemon in enumerate(party):
            slow_type(f"{index+1}. {pokemon}")
            counter += 1
        slow_type(f"{counter}. Back")
        pokemon_choice = get_valid_input("Enter number: ", list(range(1, len(party)+2)))-1
        if pokemon_choice in range(0, len(party)):
            party[pokemon_choice].learn_move(party[pokemon_choice].level, moves=[self.move], tm=self)
            item_list.remove(self)
            return True
        return True

    @classmethod
    def generate(cls, move):
        yield cls(move)

class HM(Item):

    id = 1
    def __init__(self, move):
        super().__init__("HM", "tmhm", move)
        self.name = f"HM: {move.name}"
        self.move = move

    def use(self, party, item_list=None):
        counter = 1
        for index, pokemon in enumerate(party):
            slow_type(f"{index+1}. {pokemon}")
            counter += 1
        slow_type(f"{counter}. Back")
        pokemon_choice = get_valid_input("Enter number: ", list(range(1, len(party)+2)))-1
        if pokemon_choice in range(0, len(party)):
            party[pokemon_choice].learn_move(party[pokemon_choice].level, moves=[self.move], tm=self)
            return True
        return True

    @classmethod
    def generate(cls, move):
        yield cls(move)

class Player:

    def __init__(self, name='Player', money=0):
        self.visited_mom = False
        self.tutorial_beat = False
        self.name = name
        self.money = money
        self.gym_badges= []
        self.pokemon = []
        self.items = []
        self.tms_hms = []
        self.key_items = []
        self.local_location=""
        self.map_location=""
        self.museum_tree_cut = False
        self.received_parcel = False
        self.received_amber = False
        self.received_ticket = False
        self.received_aerodactyl = False
        self.received_zapdos = False
        self.received_cut = False
        self.received_pokeflute = False
        self.delivered_parcel = False
        self.map = ""
        self.pokedex = {}
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
            #TESTINGTESTINGTESTING
            self.map_location = vermillion_city
            self.local_location = vermillion_city.pokemon_center
            self.tms_hms.append(hm_fly)
            self.tms_hms.append(next(TM.generate(flamethrower)))
            self.pokemon.append(Pidgeot(49, moves=Pidgeot.generate_moves(49), player_owned=True))
            self.money = 500

    def update_map(self):
        slow_type(f"""
                                                      Bill's
                                                        ^
                                                    Rt. 24/25
                                                        ^                  
 Pewter ----> Rt. 3 ----> Mt. Moon ---> Rt. 4 ----> Cerulean ---> Rt. 9 ---> Power Plant
   ^                                                    V                        V
 Rt. 2                                                Rt. 6                 Rock Tunnel
   ^                                                    V                        V
Viridian                     Celadon <--- Rt. 8 <--- Saffron ---> Rt. 7 ---> Lavender
   ^                                                    V                        V
 Rt. 1                                                Rt. 7                   Rt. 12
   ^                                                    V                        V
 Pallet                                             Vermillion ---> Rt. 11 --> Docks
   ^                                                    V                        V
   ^                                                 SS Anne                     V
   ^                                                                             V
   ^                                                 Fuschia <------------- Rt.13/14/15
   ^                                                    V
Cinnabar <---- Rt. 20 ---- Seafoam <------ Rt. 19 ------V
""", 0.001
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
        if not badge in player.gym_badges:
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
        else:
            slow_type("You've already defeated this gym!")
            time.sleep(0.5)
            return

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

    def __init__(self, route_pokemon, route_levels, *links, trainer_pokemon = [], trainer_levels = [], name="Route 1", pokeflute_required=False, surf_required=False, step_count=3):
        super().__init__(name)
        self.trainer_pokemon = trainer_pokemon
        self.trainer_levels = trainer_levels
        self.route_pokemon = route_pokemon
        self.route_levels = route_levels
        self.links = links
        self.pokeflute_required = pokeflute_required
        self.surf_required = surf_required
        self.step_count = step_count

    def choose(self):
        for link in self.links:
            if link == player.map_location or link == player.local_location:
                self.source = link
            else:
                self.destination = link

        def go():
            slow_type(f"1. Return to {self.source}\n2. Wild Battle" + (f"\n3. Go to {self.destination} ({self.step_count} Trainer Battles)" if self.destination is not None else ""))
            if self.destination is not None:
                choice = get_valid_input("Enter number: ", [1, 2, 3])
            else:
                choice = get_valid_input("Enter number: ", [1, 2])
            if choice == 1:
                return True
            elif choice == 2:
                self.wild_battle()
            elif choice == 3:
                step_count = self.step_count
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
            
        if self.surf_required:
            surf_found = False
            for pokemon in player.pokemon:
                for move in pokemon.move_set:
                    if move.name == "Surf":
                        surf_found = True
            if surf_found:
                slow_type("The water is too deep.")
                time.sleep(0.5)
                slow_type(f"{player.name} used Surf!")
                time.sleep(0.5)
                if go():
                    return True
            else:
                slow_type("The water is too deep.")
                time.sleep(0.5)
                return True
            
        if self.pokeflute_required:
            if pokeflute in player.key_items:
                slow_type(f"{player.name} used the PokeFlute!")
                time.sleep(0.5)
                slow_type("Snorlax moved for you!")
                time.sleep(0.5)
                if go():
                    return True
            else:
                slow_type("There is a sleeping Snorlax in the way.\nMaybe something could wake it up...")

        if not self.surf_required and not self.pokeflute_required:
            if go():
                return True

# pokemon lab
class PokemonLab(Location):

    def __init__(self, name="Pokemon Lab"):
        super().__init__(name)

    def choose(self):
        slow_type(f"1. Talk to Professor Oak\n2. Return to {player.map_location}")
        choice = get_valid_input("Enter number: ", [1, 2])
        if choice == 1:
            if parcel in player.key_items:
                slow_type("Thank you for delivering this parcel to me!")
                time.sleep(0.5)
                slow_type("Take these as a thank you.")
                slow_type(f"{player.name} received a gift bag of items!")
                player.items += [next(Pokeball.generate()), next(Potion.generate()), next(FullHeal.generate())]
                player.key_items.remove(parcel)
                player.delivered_parcel = True
                time.sleep(1)
                return True
            else:
                if player.delivered_parcel:
                    slow_type(f"Having a good journey, {player.name}?")
                else:
                    slow_type("Would you mind grabbing my parcel from Viridian City?")
                time.sleep(0.5)
                return True
        if choice == 2:
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

    def __init__(self, trainer_pokemon = [], trainer_levels = [], leader_pokemon=[], leader_name="Gym Leader", gym_name="", victory_message="", gym_badge="", prize=None):
        super().__init__(gym_name)
        self.trainer_pokemon = trainer_pokemon
        self.trainer_levels = trainer_levels
        self.leader_pokemon = leader_pokemon
        self.leader_name = leader_name
        self.victory_message = victory_message
        self.gym_badge = gym_badge
        self.prize = prize

    def choose(self):
        slow_type(f"1. Trainer Battle\n2. Challenge Gym Leader\n3. Return to {player.map_location}")
        choice = get_valid_input("Enter number: ", [1, 2, 3])
        if choice == 1:
            self.trainer_battle(self.trainer_pokemon, self.trainer_levels)
        if choice == 2:
            if self.gym_battle(self.leader_pokemon, self.leader_name, badge=self.gym_badge, victory_message=self.victory_message):
                self.receive_prize()
        if choice == 3:
            return True
        
    def receive_prize(self):
        if not self.prize is None:
            new_line()
            slow_type(f"You received {self.prize} as a prize!")
            player.tms_hms.append(self.prize)
            time.sleep(1)

# map location 
class MapLocation:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
    
    # menu methods

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
            slow_type(f"{pokemon} | LVL: {pokemon.level} | HP: {pokemon.hp}/{pokemon.maxhp}" + (" (Paralyzed)" if pokemon.paralyzed else "") + (" (Poisoned)" if pokemon.poisoned else ""))
        while True:
            slow_type("1. Switch Lead Pokemon\n2. Back")
            if get_valid_input("Enter number: ", [1, 2]) == 1:
                new_line()
                for index, value in enumerate(player.pokemon):
                    slow_type(f"{index+1}. {value} | LVL: {value.level} | HP: {value.hp}/{value.maxhp}" + (" (Paralyzed)" if pokemon.paralyzed else "") + (" (Poisoned)" if pokemon.poisoned else ""))
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
            fly_found = False
            for pokemon in player.pokemon:
                for move in pokemon.move_set:
                    if move.name == "Fly":
                        fly_found = True
            if fly_found:
                slow_type(f"You have ${player.money}.\n1. Check Pokemon\n2. Check Bag\n3. Check Map\n4. Check Pokedex\n5. Save Data\n6. Back\n7. Fly")
                choice = get_valid_input("Enter number: ", [1, 2, 3, 4, 5, 6, 7])
            if not fly_found:
                slow_type(f"You have ${player.money}.\n1. Check Pokemon\n2. Check Bag\n3. Check Map\n4. Check Pokedex\n5. Save Data\n6. Back")
                choice = get_valid_input("Enter number: ", [1, 2, 3, 4, 5, 6])
            if choice == 1:
                self.display_party()
                return True
            elif choice == 2:
                slow_type("------------ Bag ------------")
                slow_type(f"Badges: {'None' if len(player.gym_badges) == 0 else ', '.join(player.gym_badges)}")
                slow_type("1. Items\n2. TM's & HM's\n3. Key Items\n4. Back")
                bag_choice = get_valid_input("Enter number: ", [1, 2, 3, 4])
                if bag_choice == 1:
                    new_line()
                    if player.items == []:
                        slow_type("No items left.")
                    else:
                        for index, item in enumerate(player.items):
                            slow_type(f"{index+1}. {item}")
                        slow_type(f"{len(player.items)+1}. Back")
                        choice = get_valid_input("Enter number: ", list(range(1, len(player.items)+2)))
                        if choice <= len(player.items):
                            if player.items[choice-1].itype == 'heal' or player.items[choice-1].itype == 'status_heal':
                                player.items[choice-1].use(player.pokemon, player.items)
                            else:
                                slow_type(f"{player.items[choice-1]} can't be used right now.")
                        else:
                            return True
                elif bag_choice == 2:
                    new_line()
                    if player.tms_hms == []:
                        slow_type("No TM's or HM's.")
                    else:
                        for index, item in enumerate(player.tms_hms):
                            slow_type(f"{index+1}. {item}")
                        slow_type(f"{len(player.tms_hms)+1}. Back")
                        tm_choice = get_valid_input("Enter number: ", list(range(1, len(player.tms_hms)+2)))
                        if tm_choice <= len(player.tms_hms):
                            if player.tms_hms[tm_choice-1].itype == 'tmhm':
                                player.tms_hms[tm_choice-1].use(player.pokemon, player.tms_hms)
                            else:
                                slow_type(f"{player.tms_hms[tm_choice-1]} can't be used right now.")
                        else:
                            return True
                elif bag_choice == 3:
                    new_line()
                    if len(player.key_items) > 0:
                        for index, item in enumerate(player.key_items):
                            slow_type(f"{index+1}. {item}")
                    else:
                        slow_type("No key items!")
                    return True
                elif bag_choice == 4:
                    return True
                        
            elif choice == 3:
                player.update_map()
            elif choice == 4:
                slow_type("------------ Pokedex ------------")
                player.pokedex = {k: player.pokedex[k] for k in sorted(player.pokedex, key=lambda x: x.species)}
                for pokemon, value in player.pokedex.items():
                    if value:
                        slow_type(f"{pokemon.species} | Type: {pokemon.ptype.capitalize()} | Weakness: {', '.join([weakness.capitalize() for weakness in pokemon.weakness])}", 0.001)
            elif choice == 5:
                player.save('./savefile')
            elif choice == 6:
                return
            elif choice == 7:
                if self.fly():
                    return True

    def fly(self):
        slow_type(f"-------- You are in {player.map_location} --------")
        slow_type("1. Pallet Town\n2. Viridian City\n3. Pewter City\n4. Cerulean City\n5. Saffron City\n6. Vermillion City\n7. Celadon City\n8. Lavender Town\n9. Fuschia City\n10. Back")
        choice = get_valid_input("Enter number: ", [1,2,3,4,5,6,7,8,9,10])-1
        if choice == 9:
            return True
        cities = [pallet_town, viridian_city, pewter_city, cerulean_city, saffron_city, vermillion_city, celadon_city, lavender_town, fuschia_city]
        slow_type(f"Flying to {cities[choice]}...")
        time.sleep(2)
        player.map_location = cities[choice]
        player.local_location = cities[choice].pokemon_center
        slow_type(f"{player.name} arrived in {cities[choice]}!")
        time.sleep(1)
        return True

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
        time.sleep(1)
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
        self.mailman = ViridianCity.Mailman()

    def initialize(self, *routes):
        self.local_locations = [self.pokemon_center, self.pokemart, self.mailman]
        for route in routes:
            self.local_locations.insert(0, route)

    class Mailman(Location):

        def __init__(self):
            super().__init__("Mailman")

        def choose(self):
            if player.received_parcel is False:
                slow_type(f"1. Talk to mailman\n2. Go back")
                choice = get_valid_input("Enter number: ", [1, 2])
                if choice == 1:
                    new_line()
                    slow_type(f"Hello! You must be {player.name}.\nCould you please deliver this parcel to Professor Oak?")
                    time.sleep(0.5)
                    player.key_items.append(parcel)
                    slow_type(f"{player.name} received the parcel!")
                    player.received_parcel = True
                    time.sleep(1)
                    return True
                if choice == 2:
                    return True
            else:
                if player.delivered_parcel:
                    slow_type("Thanks for delivering that!")
                else:
                    slow_type("Please deliver that parcel to Professor Oak.")
                time.sleep(0.5)
                return True

# pewter city
class PewterCity(MapLocation):

    def __init__(self):
        super().__init__("Pewter City")
        self.pokemon_center = PokemonCenter()
        self.pokemart = Pokemart([Potion, Attack_Boost, Defense_Boost, Pokeball])
        self.pokemon_gym = PokemonGym([Geodude(), Mankey(), Sandshrew()], [8, 9, 10], [next(Geodude.generate(8)), next(Onix.generate(12))], "Brock", "Pewter City Gym", (f"Congratulations, {player.name}. You hit like a rock!\nBest of luck on your journey."), "Rock Badge", next(TM.generate(rock_blast)))
        self.museum = PewterCity.Museum()

    def initialize(self, *routes):
        self.local_locations = [self.pokemon_gym, self.pokemon_center, self.pokemart, self.museum]
        for route in routes:
            self.local_locations.insert(0, route)

    class Museum(Location):

        def __init__(self):
            super().__init__("Pewter City Museum")

        def choose(self):
            if amber in player.key_items:
                slow_type(f"1. Enter Museum ($20)\n2. Examine Tiny Tree\n3. Return to {player.map_location}\n4. Give Amber to Scientist")
                museum_choice = get_valid_input("Enter number: ", [1, 2, 3, 4])
            else:
                slow_type(f"1. Enter Museum ($20)\n2. Examine Tiny Tree\n3. Return to {player.map_location}")
                museum_choice = get_valid_input("Enter number: ", [1, 2, 3])
            if museum_choice == 1:
                player.money -= 20
                new_line()
                time.sleep(0.5)
                slow_type("\nAerodactyl: A Pokémon from the age of dinosaurs. It was regenerated from\ngenetic material extracted from amber. It is imagined to\nhave been the king of the skies in ancient times.", 0.001)
                time.sleep(1)
                slow_type("\nKabutops: They swam underwater to hunt for its prey in ancient times.\nThe Pokémon was apparently evolving from being a water-dweller to living\non land as evident from the beginnings of change in its gills and legs.", 0.001)
                time.sleep(1)
                slow_type("\nOmastar: This is one of the ancient and long-since-extinct Pokémon\nthat have been regenerated from fossils by people.\nIf attacked by an enemy, it withdraws itself inside its hard shell.", 0.001)
                time.sleep(1)
                slow_type("\nThanks for visiting!")
                time.sleep(0.5)
            elif museum_choice == 2:
                for pokemon in player.pokemon:
                    if cut in pokemon.move_set:
                        if player.museum_tree_cut is False:
                            slow_type("1. Cut Tree\n2. Back")
                            cut_choice = get_valid_input("Enter number: ", [1, 2])
                            if cut_choice == 1:
                                slow_type("You used cut on the tree!")
                                time.sleep(0.5)
                                slow_type("You found an Amber!\nAmber added to Key Items")
                                player.key_items.append(amber)
                                player.museum_tree_cut = True
                                return True
                            elif cut_choice == 2:
                                return True
                else:
                    slow_type("Nothing to do here...")
                    time.sleep(0.5)
            elif museum_choice == 3:
                return True
            elif museum_choice == 4:
                slow_type("Wow! An amber!")
                time.sleep(0.5)
                slow_type("Give me just a minute...\nI think I can do something with this...")
                time.sleep(1)
                if len(player.pokemon) < 6:
                    player.key_items.remove(amber)
                    player.pokemon.append(next(Aerodactyl.generate(30)))
                    player.received_aerodactyl = True
                    slow_type("We reformed it into an Aerodactyl!\nPlease take good care of it.")
                    slow_type("Aerodactyl was added to your party!")
                    time.sleep(1)
                else:
                    slow_type("We can defintely restore this, but your party is full!")
            return True

# mount moon
class MountMoon(MapLocation):

    def __init__(self):
        super().__init__("Mount Moon")
        self.pokemart = Pokemart([Potion, Attack_Boost, Defense_Boost, Pokeball])
        self.pokemon_center = PokemonCenter(name="Hiker's House", string="Your Pokemon should be all rested up now...\nTake care. I hear there's some cool Pokemon in the cave...")

    def initialize(self, *routes):
        self.local_locations = [self.pokemart, self.pokemon_center]
        for route in routes:
            self.local_locations.insert(0, route)
            
class CeruleanCity(MapLocation):

    def __init__(self):
        super().__init__("Cerulean City")
        self.pokemon_center = PokemonCenter()
        self.pokemart = Pokemart([Potion, Attack_Boost, Defense_Boost, Pokeball, FullHeal, Greatball])
        self.pokemon_gym = PokemonGym([Goldeen(), Staryu()], [15, 16, 17, 18], [next(Staryu.generate(18)), next(Starmie.generate(21))], "Misty", "Cerulean City Gym", (f"Congrats, {player.name}! It's a rainy day for me...\nWell, have fun on the rest of your journey!"), "Water Badge", next(TM.generate(water_pulse)))

    def initialize(self, *routes):
        self.local_locations = [self.pokemart, self.pokemon_center, self.pokemon_gym]
        for route in routes:
            self.local_locations.insert(0, route)

class SaffronCity(MapLocation):

    def __init__(self):
        super().__init__("Saffron City")
        self.pokemon_center = PokemonCenter()
        self.pokemart = Pokemart([Potion, Attack_Boost, Defense_Boost, Pokeball, FullHeal, Greatball])
        self.pokemon_gym = SaffronCity.SaffronPokemonGym([Psyduck(), MrMime(), Kadabra()], [31,32,33,34,35,36], [next(Kadabra.generate(38)), next(MrMime.generate(37)), next(Venomoth.generate(38)), next(Alakazam.generate(43))], "Sabrina", "Saffron City Gym", (f"Congratulations, {player.name}. You really psyched me out there.\nEnjoy your journey."), "Psychic Badge", next(TM.generate(psycho_cut)))

    def initialize(self, *routes):
        self.local_locations = [self.pokemart, self.pokemon_center, self.pokemon_gym]
        for route in routes:
            self.local_locations.insert(0, route)
    
    class SaffronPokemonGym(PokemonGym):

        def __init__(self, trainer_pokemon = [], trainer_levels = [], leader_pokemon=[], leader_name="Gym Leader", gym_name="", victory_message="", gym_badge="", prize=None):
            super().__init__(trainer_pokemon, trainer_levels, leader_pokemon, leader_name, gym_name, victory_message, gym_badge, prize=None)

        def choose(self):
            if "Electric Badge" in player.gym_badges:
                slow_type(f"1. Trainer Battle\n2. Challenge Gym Leader\n3. Return to {player.map_location}")
                choice = get_valid_input("Enter number: ", [1, 2, 3])
                if choice == 1:
                    self.trainer_battle(self.trainer_pokemon, self.trainer_levels)
                if choice == 2:
                    if self.gym_battle(self.leader_pokemon, self.leader_name, badge=self.gym_badge, victory_message=self.victory_message):
                        self.receive_prize()
                if choice == 3:
                    return True
            else:
                slow_type("Hey buddy! The gym is closed right now.\nI think Vermillion City's is open, though.\nYou can get there by taking Route 6.")
                time.sleep(0.5)
                return True
            
class VermillionCity(MapLocation):

    def __init__(self):
        super().__init__("Vermillion City")
        self.pokemon_center = PokemonCenter()
        self.pokemart = Pokemart([Potion, FullHeal, Attack_Boost, Defense_Boost, Pokeball, Greatball, Ultraball])
        self.pokemon_gym = PokemonGym([Voltorb(), Pikachu(), Magnemite()], [18,19,20,21,22], [next(Voltorb.generate(21)), next(Pikachu.generate(18)), next(Raichu.generate(24))], "Lt. Surge", "Vermillion City Gym", (f"Wow, {player.name}! Well, that was shocking!\nEnjoy the rest of your electrifying journey!"), "Electric Badge", next(TM.generate(thunderbolt)))

    def initialize(self, *routes):
        self.local_locations = [self.pokemart, self.pokemon_center, self.pokemon_gym]
        for route in routes:
            self.local_locations.insert(0, route)

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
            if temp_dict[choice] == ss_anne_route:
                if player.received_ticket:
                    pass
                else:
                    slow_type("You do not have a ticket...")
                    time.sleep(1)
                    return False
            new_location = temp_dict[choice]
            player.local_location = new_location
            return True

class FuschiaCity(MapLocation):

    def __init__(self):
        super().__init__("Fuschia City")
        self.pokemon_center = PokemonCenter()
        self.pokemart = Pokemart([Potion, FullHeal, Attack_Boost, Defense_Boost, Pokeball, Greatball, Ultraball])
        self.pokemon_gym = PokemonGym([Kadabra(), Arbok(), Drowzee(), Koffing()], [18,19,20,21,22], [next(Koffing.generate(37)), next(Koffing.generate(37)), next(Venomoth.generate(39)), next(Weezing.generate(40))], "Koga", "Fuschia City Gym", (f"Wow, {player.name}, that really stings!\nHave a good rest of your journey!"), "Poison Badge", (hm_surf))

    def initialize(self, *routes):
        self.local_locations = [self.pokemart, self.pokemon_center, self.pokemon_gym]
        for route in routes:
            self.local_locations.insert(0, route)

class CeladonCity(MapLocation):

    def __init__(self):
        super().__init__("Celadon City")
        self.pokemon_center = PokemonCenter()
        self.pokemart = Pokemart([Potion, FullHeal, Attack_Boost, Defense_Boost, Pokeball, Greatball, Ultraball])
        self.arcade = CeladonCity.Arcade()
        self.pokemon_gym = PokemonGym([Bellsprout(), Weepinbell(), Ivysaur(), Gloom()], [21, 22, 23, 24, 25, 26], [next(Tangela.generate(24)), next(Victreebel.generate(29)), next(Vileplume.generate(29))], "Erika", "Celadon City Gym", "You really had me in a bind\nTake care now.", "Grass Badge", next(TM.generate(giga_drain)))

    def initialize(self, *routes):
        self.local_locations = [self.pokemart, self.pokemon_center, self.arcade, self.pokemon_gym]
        for route in routes:
            self.local_locations.insert(0, route)

    class Arcade(Location):
        def __init__(self):
            self.name = "Celadon Arcade"

        def play_slots(self):

            new_line()
            slow_type("You put $25 in the machine...")
            time.sleep(0.5)

            row1, row2, row3 = [], [], []
            grid = [row1, row2, row3]

            for row in grid:
                for x in range(3):
                    row.append(random.randint(1, 3))

            for row in grid:
                for y in range(len(row)):
                    if row[y] == 1:
                        row[y] = "X"
                    if row[y] == 2:
                        row[y] = "O"
                    if row[y] == 3:
                        row[y] = "+"

            money = 0

            if row1[0] == row2[0] and row2[0] == row3[0]:
                money += 50
            if row1[1] == row2[1] and row2[1] == row3[1]:
                money += 50
            if row1[2] == row2[2] and row2[2] == row3[2]:
                money += 50
            if row1[0] == row1[1] and row1[1] == row1[2]:
                money += 50
            if row2[0] == row2[1] and row2[1] == row2[2]:
                money += 50
            if row3[0] == row3[1] and row3[1] == row3[2]:
                money += 50
            if row1[0] == row2[1] and row2[1] == row3[2]:
                money += 50
            if row3[0] == row2[1] and row2[1] == row1[2]:
                money += 50

            for row in grid:
                for y in range(len(row)):
                    row[y] += "  "
                slow_type(row, 0.5)

            if money > 0:
                slow_type(f"${money} won!")
            else:
                slow_type("No money won...")
            return money
        
        def choose(self):
            slow_type(f"------------ You have ${player.money} ------------")
            slow_type(f"1. Play Slots ($25)\n2. Return to {player.map_location}")
            choice = get_valid_input("Enter number: ", [1, 2])
            if choice == 1:
                if player.money >= 50:
                    player.money -= 25
                    player.money += self.play_slots()
                else:
                    slow_type("You don't have enough money!")
                    time.sleep(1)
            if choice == 2:
                return True
            
class BillsHome(MapLocation):

    def __init__(self):
        super().__init__("Bill's")
        self.pokemon_center = BillsHome.BillsHouse()

    def initialize(self, *routes):
        self.local_locations = [self.pokemon_center]
        for route in routes:
            self.local_locations.insert(0, route)

    class BillsHouse(PokemonCenter):

        def __init__(self):
            self.string = "Thanks for visiting! Your Pokemon have been healed!"
            self.name = "Bill's House"

        def choose(self):
            slow_type(f"1. Heal Pokemon\n2. Talk to Bill\n3. Return to {player.map_location}")
            choice = get_valid_input("Enter number: ", [1, 2, 3])
            if choice == 1:
                self.heal()
            if choice == 2:
                if not player.received_ticket:
                    new_line()
                    slow_type(f"Hey, I've got this extra ticket to the SS Anne...\nUnfortunately, I can't go. You can have it!")
                    time.sleep(0.5)
                    slow_type(f"{player.name} obtained SS Anne Ticket!")
                    player.key_items.append(ss_anne_ticket)
                    player.received_ticket = True
                    time.sleep(1)
                    slow_type("The SS Anne is docked in Vermillion City.")
                    time.sleep(0.5)
                else:
                    new_line()
                    slow_type("Welcome back. Hope you enjoy that ticket.\nRemember, the SS Anne is docked in Vermillion City.")
                    time.sleep(0.5)
            if choice == 3:
                return True
            
class SSAnne(MapLocation):

    def __init__(self):
        super().__init__("SS Anne Captain's Quarters")
        self.pokemon_center = SSAnne.Captain()

    def initialize(self, *routes):
        self.local_locations = [self.pokemon_center]
        for route in routes:
            self.local_locations.insert(0, route)

    class Captain(PokemonCenter):

        def __init__(self):
            self.string = "Aye, lad. You should be well rested now."
            self.name = "Captain"

        def choose(self):
            slow_type(f"1. Heal Pokemon\n2. Talk to Captain\n3. Return to {player.map_location}")
            choice = get_valid_input("Enter number: ", [1, 2, 3])
            if choice == 1:
                self.heal()
            if choice == 2:
                if not player.received_cut:
                    new_line()
                    slow_type(f"Hey kid, I've got this HM I dont really need.\nYou can have it!")
                    time.sleep(0.5)
                    slow_type(f"{player.name} obtained HM: Cut!")
                    player.key_items.append(hm_cut)
                    player.received_cut = True
                    time.sleep(1)
                    time.sleep(0.5)
                else:
                    new_line()
                    slow_type("Enjoying the ship? Don't get too sea sick...")
                    time.sleep(0.5)
            if choice == 3:
                return True
            
class LavenderTown(MapLocation):

    def __init__(self):
        super().__init__("Lavender Town")
        self.pokemon_center = PokemonCenter()
        self.pokemart = Pokemart([Potion, FullHeal, Attack_Boost, Defense_Boost, Pokeball, Greatball, Ultraball])
        

    def initialize(self, *routes):
        self.local_locations = [self.pokemon_center, self.pokemart]
        for route in routes:
            self.local_locations.insert(0, route)

class TopOfPokemonTower(MapLocation):

    def __init__(self):
        super().__init__("Top of Pokemon Tower")
        self.mrfuji = TopOfPokemonTower.MrFuji()

    def initialize(self, *routes):
        self.local_locations = [self.mrfuji]
        for route in routes:
            self.local_locations.insert(0, route)

    class MrFuji(PokemonCenter):

        def __init__(self):
            self.string = "Take care."
            self.name = "Mr. Fuji"

        def choose(self):
            slow_type(f"1. Heal Pokemon\n2. Talk to Mr. Fuji\n3. Return to {player.map_location}")
            choice = get_valid_input("Enter number: ", [1, 2, 3])
            if choice == 1:
                self.heal()
            if choice == 2:
                if not player.received_pokeflute:
                    new_line()
                    slow_type(f"Thank you for visiting...\nPlease take this Pokeflute as my thanks.")
                    time.sleep(0.5)
                    slow_type(f"{player.name} obtained the PokeFlute!")
                    player.key_items.append(pokeflute)
                    player.received_pokeflute = True
                    time.sleep(1)
                    time.sleep(0.5)
                else:
                    new_line()
                    slow_type("Take all the time you need.")
                    time.sleep(0.5)
            if choice == 3:
                return True
            
class PowerPlant(MapLocation):

    def __init__(self):
        super().__init__("Power Plant")
        self.zapdos = PowerPlant.Zapdos()

    def initialize(self, *routes):
        self.local_locations = [self.zapdos]
        for route in routes:
            self.local_locations.insert(0, route)

    class Zapdos(Location):

        def __init__(self):
            self.name = "Zapdos"

        def choose(self):
            slow_type(f"1. Challenge Zapdos\n2. Return to {player.map_location}")
            choice = get_valid_input("Enter number: ", [1, 2])
            if choice == 1:
                if not player.received_zapdos:
                    slow_type(f"{player.name} steps up to the mysterious beast...")
                    slow_type("......", 0.5)
                    slow_type("It attacks!")
                    time.sleep(1)
                    if Battle([next(Zapdos.generate(50))], wild=True, runnable=False):
                        player.received_zapdos = True
                        slow_type("Zapdos is no longer here...")
                        time.sleep(1)
                else:
                    slow_type("Zapdos is no longer here...")
                    time.sleep(0.5)
            elif choice == 2:
                return True

class Docks(MapLocation):

    def __init__(self):
        super().__init__("Docks")
        self.pokemon_center = PokemonCenter("Fisher's Home", "What a good night's rest!")

    def initialize(self, *routes):
        self.local_locations = [self.pokemon_center]
        for route in routes:
            self.local_locations.insert(0, route)

class SeafoamIslands(MapLocation):

    def __init__(self):
        super().__init__("Seafoam Islands")
        self.articuno = SeafoamIslands.Articuno()

    def initialize(self, *routes):
        self.local_locations = [self.articuno]
        for route in routes:
            self.local_locations.insert(0, route)

    class Articuno(Location):

        def __init__(self):
            self.name = "Articuno"

        def choose(self):
            slow_type(f"1. Challenge Articuno\n2. Return to {player.map_location}")
            choice = get_valid_input("Enter number: ", [1, 2])
            if choice == 1:
                if not player.received_articuno:
                    slow_type(f"{player.name} steps up to the mysterious beast...")
                    slow_type("......", 0.5)
                    slow_type("It attacks!")
                    time.sleep(1)
                    if Battle([next(Articuno.generate(50))], wild=True, runnable=False):
                        player.received_articuno = True
                        slow_type("Articuno is no longer here...")
                        time.sleep(1)
                else:
                    slow_type("Articuno is no longer here...")
                    time.sleep(0.5)
            elif choice == 2:
                return True

# create player
player = Player(name="Player", money=0)
try:
    player = Player.load('./savefile')
    slow_type(f"Loading game...")
    time.sleep(1)
except:
    player = Player(money=0)

# key items
#PLACEHOLDER
amber = KeyItem("amber")
parcel = KeyItem("Parcel")
ss_anne_ticket = KeyItem("SS Anne Ticket")
pokeflute = KeyItem("PokeFlute")

# HMs
hm_cut = HM(cut)
hm_fly = HM(fly)
hm_surf = HM(surf)

# create locations
pallet_town = PalletTown()
viridian_city = ViridianCity()
pewter_city = PewterCity()
mount_moon = MountMoon()
cerulean_city = CeruleanCity()
saffron_city = SaffronCity()
vermillion_city = VermillionCity()
celadon_city = CeladonCity()
bills_home = BillsHome()
ss_anne = SSAnne()
lavender_town = LavenderTown()
top_of_pokemon_tower = TopOfPokemonTower()
power_plant = PowerPlant()
docks = Docks()
fuschia_city = FuschiaCity()
seafoam_islands = SeafoamIslands()

# initializing
trainer_names = ["Janet", "Alissa", "Jim", "Gary", "Kaleb", "Lucas", "Vivian", "Marco", "Jake", "Harry", "Dawn", "May", "Brendan", "Alex", "Shauna", "Liko", "Goh", "Terry", "Jenny"]

route1 = Route([Rattata(), Pidgey(), Oddish(), Bellsprout()], [3, 4, 5], viridian_city, pallet_town, trainer_levels=[4, 5, 6], trainer_pokemon=[Rattata(), Pidgey(), Oddish(), Bellsprout()], name="Route 1")
viridian_forest = Route([Weedle(), Caterpie(), Bellsprout(), Rattata(), Pikachu()], [4, 5, 6], viridian_city, pewter_city, trainer_levels=[4, 5, 6], trainer_pokemon=[Bellsprout(), Rattata(), Pikachu(), Weedle(), Caterpie()], name="Route 2: Viridian Forest")
viridian_pond = Route([Magikarp(), Goldeen()], [4, 5, 6], viridian_city, None, trainer_levels=[4, 5, 6], trainer_pokemon=[Magikarp(), Goldeen(), Poliwag()], name="Viridian Pond")
route3 = Route([Pidgey(), Spearow(), Mankey(), Sandshrew(), Rattata()], [6, 7, 8], mount_moon, pewter_city, trainer_levels= [6, 7, 8], trainer_pokemon=[Pikachu(), Sandshrew(), Vulpix(), Spearow(), Mankey()], name="Route 3")
route4 = Route([Ekans(), Spearow(), Sandshrew(), Mankey(), Raticate()], [10, 11, 12, 13], mount_moon, cerulean_city, trainer_levels=[11, 12, 13, 14], trainer_pokemon=[Magnemite(), Cubone(), Diglett(), Geodude()], name="Route 4")
mt_moon_cave = Route([Magnemite(), Cubone(), Diglett(), Rattata(), Geodude(), Zubat()], [8, 9, 10, 11], mount_moon, None, trainer_levels=[9, 10, 11, 12], trainer_pokemon=[Magnemite(), Cubone(), Diglett(), Geodude()], name="Mount Moon Cave")
cerulean_river = Route([Magikarp(), Goldeen(), Psyduck(), Poliwag()], [9, 10, 11], cerulean_city, None, trainer_levels=[9, 10, 11], trainer_pokemon=[Magikarp(), Goldeen(), Poliwag()], name="Cerulean River")
route5 = Route([Oddish(), Pidgey(), Abra(), Jigglypuff(), Meowth(), Psyduck(), Ekans(), Mankey()], [10, 11, 12, 13], saffron_city, cerulean_city, trainer_levels=[11, 12, 13, 14], trainer_pokemon=[Pidgeotto(), Meowth(), Pidgey(), Ekans()], name="Route 5")
route6 = Route([Pidgey(), Psyduck(), Mankey(), Pikachu(), Meowth(), Abra(), Jigglypuff(), Pidgeotto()], [13, 14, 15, 16], saffron_city, vermillion_city, trainer_levels=[14, 15, 16, 17], trainer_pokemon=[Pidgeotto(), Meowth(), Pidgey(), Ekans(), Kadabra()], name="Route 6")
route8 = Route([Pidgey(), Pidgeotto(), Rattata(), Vulpix(), Jigglypuff(), Oddish(), Meowth(), Abra(), Mankey(), Growlithe()], [17, 18, 19, 20], saffron_city, celadon_city, trainer_levels=[17, 18, 19, 20, 21], trainer_pokemon=[Pidgeotto(), Jigglypuff(), Vulpix(), Meowth(), Growlithe(), Kadabra()], name="Route 8")
route2425 = Route([Venonat(), Pidgey(), Oddish(), Abra(), Kakuna(), Metapod()], [12, 13, 14, 15], cerulean_city, bills_home, trainer_levels=[12, 13, 14, 15], trainer_pokemon=[Kakuna(), Metapod(), Pidgeotto(), Abra(), Venonat()], name="Route 24/25")
ss_anne_route = Route([Psyduck(), Seaking(), Tentacool(), Shellder(), Staryu(), Krabby()], [18, 19, 20, 21], ss_anne, vermillion_city, trainer_levels=[18, 19, 20, 21], trainer_pokemon=[Golduck(), Seaking(), Tentacool(), Shellder(), Voltorb(), Magnemite(), Pikachu(), Staryu(), Krabby()], name="SS Anne")
pokemon_tower = Route([Ghastly(), Haunter(), Cubone()], [18, 19, 20, 21, 22, 23, 24], lavender_town, top_of_pokemon_tower, trainer_levels=[19, 20, 21, 22], trainer_pokemon=[Ghastly(), Haunter(), Cubone()], name="Pokemon Tower")
route7 = Route([Jigglypuff(), Pidgey(), Vulpix(), Rattata(), Meowth(), Mankey(), Growlithe(), Abra(), Bellsprout()], [18, 19, 20, 21, 22], saffron_city, lavender_town, trainer_levels=[19, 20, 21, 22, 23], trainer_pokemon=[Abra(), Jigglypuff(), Mankey(), Growlithe(), Meowth(), Vulpix()], name="Route 7")
route9 = Route([Sandshrew(), Rattata(), Spearow(), Fearow(), Ekans(), Mankey(), Cubone(), Venonat()], [14,15,16,17,18,19], power_plant, cerulean_city, trainer_levels=[14,15,16,17,18,19], trainer_pokemon=[Sandshrew(), Rattata(), Spearow(), Fearow(), Ekans(), Mankey(), Cubone(), Venonat()], name="Route 9")
rock_tunnel = Route([Geodude(), Zubat(), Onix()], [15,116,17,18,19], power_plant, lavender_town, trainer_levels=[15,16,17,18], trainer_pokemon=[Geodude(), Graveler(), Onix(), Zubat()], name="Rock Tunnel")
route12 = Route([Poliwag(), Slowbro(), Tentacool(), Goldeen(), Magikarp()], [24,25,26,27,28], docks, lavender_town, trainer_levels=[24,25,26,27,28], trainer_pokemon=[Poliwag(), Slowbro(), Tentacool(), Goldeen(), Magikarp()], name="Route 12")
route11 = Route([Drowzee(), Sandshrew(), Pidgeotto(), Ekans(), Shellder(), Krabby()], [12,13,14,15,16], docks, vermillion_city, trainer_levels=[12,13,14,15,16], trainer_pokemon=[Drowzee(), Sandshrew(), Pidgeotto(), Ekans(), Shellder(), Krabby()], name="Route 11")
route131415 = Route([Weepinbell(), Venomoth(), Pidgeotto(), Gloom(), Krabby(), Poliwag()], [12,13,14,15,16], docks, fuschia_city, trainer_levels=[12,13,14,15,16], trainer_pokemon=[Weepinbell(), Venomoth(), Pidgeotto(), Gloom(), Krabby(), Poliwag()], name="Route 13/14/15", step_count=5)
route19 = Route([Tentacruel(), Kingler(), Poliwhirl(), Seaking()], [35,36,37,38,39], seafoam_islands, fuschia_city, trainer_levels=[35,36,37,38,39], trainer_pokemon=[Tentacruel(), Kingler(), Poliwhirl(), Seaking()], name="Route 19", step_count=5, surf_required=True)

map_object = MapLocation("Map")

map_object.map_locations = [pallet_town, viridian_city, pewter_city, mount_moon, cerulean_city, saffron_city, vermillion_city, celadon_city, bills_home, ss_anne, lavender_town, top_of_pokemon_tower, power_plant, docks, fuschia_city, seafoam_islands]
pallet_town.initialize(route1)
viridian_city.initialize(route1, viridian_forest, viridian_pond)
pewter_city.initialize(viridian_forest, route3)
mount_moon.initialize(route3, mt_moon_cave, route4)
cerulean_city.initialize(route4, route5, route2425, cerulean_river)
saffron_city.initialize(route5, route6, route7, route8)
vermillion_city.initialize(route6, ss_anne_route)
celadon_city.initialize(route8)
bills_home.initialize(route2425)
ss_anne.initialize(ss_anne_route)
lavender_town.initialize(route7, pokemon_tower, rock_tunnel)
top_of_pokemon_tower.initialize(pokemon_tower)
power_plant.initialize(route9, rock_tunnel)
docks.initialize(route12, route11, route131415)
fuschia_city.initialize(route131415, route19)
seafoam_islands.initialize(route19)

# intialize player location
player.initialize()

# get starter pokemon

starters = ['Charmander', 'Bulbasaur', 'Squirtle']

# starting functions
def intro():
    global player
    slow_type("Welcome to the world of Pokemon!\nI'm Professor Oak.\nAnd, what is your name?.")
    time.sleep(1)
    name = input("Enter: ").strip()
    new_line()
    player.name = name
    slow_type(f"Nice to meet you, {player.name}. In the world of Pokemon,\nwe train our Pokemon companions for battle.\nLet's get started with you choosing your Pokemon!")
    time.sleep(0.5)
    new_line()

def get_starter():
    global oak_pokemon
    slow_type(f"Choose your starter!\n1. {starters[0]}\n2. {starters[1]}\n3. {starters[2]}")
    starter_choice = get_valid_input("Enter number: ", [1, 2, 3])
    slow_type(f"You chose {starters[starter_choice-1]}.")
    starter_nickname = input("Give it a nickname: ").strip()
    if starter_choice == 1:
        starter = Charmander(5, name=starter_nickname, moves=[ember, growl, scratch], player_owned=True)
        oak_pokemon = next(Bulbasaur.generate(5))
    elif starter_choice == 2:
        starter = Bulbasaur(5, name=starter_nickname, moves=[vine_whip, growl, tackle], player_owned=True)
        oak_pokemon = next(Squirtle.generate(5))
    elif starter_choice == 3:
        starter = Squirtle(5, name=starter_nickname, moves=[water_gun, tackle, tail_whip], player_owned=True)
        oak_pokemon = next(Charmander.generate(5))
    player.pokemon.append(starter)
    check_pokedex(next(starter.__class__.generate(5)), player)
    starters.pop(starter_choice-1)
    backup = starters
    new_line()

def intro2():
    slow_type("Now, allow me to show you what it's all about.\nLet's have our first battle.")
    time.sleep(1)
    slow_type("I challenge you!")

# game
if __name__ == "__main__":

    #if not player.tutorial_beat:

        #intro()
        #get_starter()
        #intro2()
        
        #while True:
       #     if Battle([oak_pokemon], wild=False, trainer=True, trainer_name="Professor Oak", runnable=False).battle():
         #       new_line()
       #         slow_type("You're ready to set out.\nCatch Pokemon and train them.")
       #         time.sleep(0.5)
         #        slow_type(f"{player.name} received a map from Professor Oak!")
        #         time.sleep(1)
        #         slow_type(f"{player.name} received a Pokedex from Professor Oak!")
        #         time.sleep(1)
        #         slow_type("Head out towards Viridian City, if you wouldn't mind.\nI have someone at the Pokemon Center there waiting for you.")
        #         time.sleep(0.5)
        #         slow_type("Take care!")
        #         time.sleep(0.5)
        #        player.tutorial_beat = True
        #        break
        #    else:
         #       player.map_location.black_out()
         #       new_line()
         #       slow_type("Ah, you're back. Let's try that again.")
    try:
        player.map_location.change_location()
    except:
        pass
    player.map_location.location_loop()