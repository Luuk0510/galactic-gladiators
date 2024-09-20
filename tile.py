class Tile:
    def __init__(self, tile_type='normal', unit=None, color=(255, 255, 255)): # white
        self.tile_type = tile_type
        self.unit = unit
        self.color = color

    def place_unit(self, unit):
        if self.unit is None:
            self.unit = unit
            return True
        return False  

    def remove_unit(self):
        if self.unit is not None:
            self.unit = None
            return True
        return False 

    def apply_effect(self, unit):
        pass
    
    def remove_effect(self, unit):
        pass

    def __repr__(self):
        return f"Tile(type={self.tile_type}, unit={self.unit})"
    
    
class Highground(Tile):
    def __init__(self):
        super().__init__('highground', color=(0, 128, 0)) # green

    def apply_effect(self, unit):
        unit.rank += 1
    
    def remove_effect(self, unit):
        unit.rank -= 1

class Cover(Tile):
    def __init__(self):
        super().__init__('cover', color=(128, 0, 128)) # purple

    def apply_effect(self, unit):
        unit.is_vulnerable_to_special_powers = False
        
    def remove_effect(self, unit):
        unit.is_vulnerable_to_special_powers = True 

class Sensor(Tile):
    def __init__(self):
        super().__init__('sensor', color=(255, 0, 0)) # red

    def apply_effect(self, unit):
        unit.rank_visible = True

    def remove_effect(self, unit):
        unit.rank_visible = False

class Goldmine(Tile):
    def __init__(self):
        super().__init__('goldmine', color=(255, 215, 0))  # goud
        self.turn_counter = 0
        self.unit_on_mine = None

    def apply_effect(self, unit):
        if self.unit_on_mine == unit:
            if self.turn_counter >= 3:
                unit.player.gold += 1
                self.turn_counter = 0  
        else:
            self.turn_counter = 0  
            self.unit_on_mine = unit
            
    def remove_effect(self, unit):
        if self.unit_on_mine == unit:
            self.unit_on_mine = None
            self.turn_counter = 0

    def increment_turn_counter(self):
        if self.unit_on_mine is not None:
            self.turn_counter += 1
        

        


