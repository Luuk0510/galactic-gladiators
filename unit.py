import random
from decorator import log_special_power

class Unit:
    def __init__(self, rank, special_power=None):
        self.rank = rank
        self.special_power = special_power
        self.rank_visible = False
        self.special_power_used = False
        self.was_attacked = False
        self.invisible = False

    def use_special_power(self, *args, **kwargs):
        """Definieer het gedrag van de speciale kracht in subklassen."""
        pass
    
    def end_turn(self):
        pass

    def is_rank_visible(self, cheat_mode=False):
        """Geeft aan of de rang van de eenheid zichtbaar is."""
        return self.rank_visible or cheat_mode
    
    def become_allied(self, new_player):
        self.player = new_player  # Wissel de eigenaar van de eenheid naar de nieuwe speler
        print(f"{self.__class__.__name__} has switched sides!")


class Scout(Unit):
    def __init__(self):
        super().__init__(rank=1, special_power="Infiltration")
        self.invisible_turns = 0

    @log_special_power    
    def use_special_power(self):
        if not self.special_power_used:
            self.invisible = True
            self.invisible_turns = 3
            self.special_power_used = True
            self.rank_visible = False
            return True
        return False

    def end_turn(self):
        if self.invisible_turns > 0:
            self.invisible_turns -= 1
            if self.invisible_turns == 0:
                self.invisible = False
    
    def check_invisibility(self):
        return self.invisible_turns > 0


class Soldier(Unit):
    def __init__(self):
        super().__init__(rank=2)
        # Geen speciale krachten
    


class Sniper(Unit):
    def __init__(self):
        super().__init__(rank=3, special_power="Precision Shot")
    
    @log_special_power   
    def use_special_power(self, target):
        if not self.special_power_used:
            # Simuleer de dobbelsteenworp
            dice_roll = random.randint(1, 6)
            if dice_roll >= 5:
                target.eliminate()  # Elimineer de vijandelijke eenheid
            
            # De Sniper verdwijnt ongeacht het resultaat
            self.special_power_used = True
            self.eliminate()

    def eliminate(self):
        # Logica om de Sniper te elimineren
        print("Sniper is eliminated.")


class ShieldBearer(Unit):
    def __init__(self):
        super().__init__(rank=4, special_power="Energy Field")
        self.shield_active = False

    @log_special_power   
    def use_special_power(self):
        if not self.special_power_used:
            self.shield_active = True  # Activeer het schild
            self.special_power_used = True

    def deactivate_shield(self):
        self.shield_active = False


class BattleMaster(Unit):
    def __init__(self):
        super().__init__(rank=5, special_power="Battle Cry")

    @log_special_power 
    def use_special_power(self, allies):
        if not self.special_power_used:
            for ally in allies:
                if self.is_adjacent(ally):
                    ally.rank += 1  # Verhoog de rang van naburige eenheden
            self.special_power_used = True

    def is_adjacent(self, other_unit):
        # Bepaal of de eenheid naast de BattleMaster staat
        return True  # Dit is placeholder-logica


class Commando(Unit):
    def __init__(self):
        super().__init__(rank=6, special_power="Sabotage")

    @log_special_power 
    def use_special_power(self, target):
        target_unit = self.board.get_unit(target)
        if not self.special_power_used and self.is_adjacent(target):
            target_unit.become_allied(self.player)
            self.special_power_used = True

    def is_adjacent(self, other_unit_coord):
        dx = abs(self.coord.x - other_unit_coord.x)
        dy = abs(self.coord.y - other_unit_coord.y)

        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

class Flag(Unit):
    def __init__(self):
        super().__init__(rank=0)
