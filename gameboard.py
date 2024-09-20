import random
from coordinate import Coordinate
from tile import Tile, Sensor, Goldmine, Cover, Highground
from unit import Flag, Scout

class GameBoard:
    BOARD_SIZE = 10
    MIDDLE_ROW_COUNT = 4
    SPECIAL_TILES = {
        Highground: 3,
        Cover: 2,
        Sensor: 4,
        Goldmine: 3
    }

    def __init__(self, initialize_board=True): 
        self.tiles = {}
        if initialize_board:
            self.setup_board()

    def update(self, turn_counter):
        for coord, tile in self.tiles.items():
            if isinstance(tile, Goldmine) and tile.unit_on_mine is not None:
                tile.increment_turn_counter()  
                tile.apply_effect(tile.unit_on_mine) 
    
    def setup_board(self):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                coord = Coordinate(row, col)
                self.tiles[coord] = Tile()

        middle_start = (self.BOARD_SIZE - self.MIDDLE_ROW_COUNT) // 2
        middle_end = middle_start + self.MIDDLE_ROW_COUNT
        middle_rows = list(range(middle_start, middle_end))

        placed_tiles = set()

        for tile_class, count in self.SPECIAL_TILES.items():
            while count > 0:
                row = random.choice(middle_rows)
                col = random.randint(0, 9)
                coord = Coordinate(row, col)
                if coord not in placed_tiles:
                    self.tiles[coord] = tile_class()
                    placed_tiles.add(coord)
                    count -= 1

   
    def place_unit(self, coord, unit):
        tile = self.tiles.get(coord)
        if tile:
            return tile.place_unit(unit)
        return False

    def remove_unit(self, coord):
        tile = self.tiles.get(coord)
        if tile:
            return tile.remove_unit()
        return False

    def get_unit(self, coord):
        tile = self.tiles.get(coord)
        if tile:
            return tile.unit
        return None
    
    def move_unit(self, from_coord, to_coord):
        if from_coord in self.tiles and self.tiles[from_coord].unit:
            unit = self.tiles[from_coord].unit
            
            if isinstance(unit, Flag):
                print("De vlag mag niet bewegen!")
                return False

            self.remove_tile_effect(from_coord, unit)

            if self.is_adjacent(from_coord, to_coord) and self.tiles[to_coord].unit is None:
                self.tiles[to_coord].unit = unit
                self.tiles[from_coord].unit = None

                self.apply_tile_effect(to_coord, unit)
                
                if isinstance(unit, Scout) and unit.check_invisibility():
                    enemy_unit = self.tiles[to_coord].unit
                    if enemy_unit and enemy_unit.player != unit.player:
                        print(f"Scout at {to_coord} detected enemy unit and eliminates it.")
                        self.remove_unit(to_coord)
                        unit.rank_visible = True
                        
                return True

    def apply_tile_effect(self, coord, unit):
        tile = self.tiles.get(coord)
        if tile:
            tile.apply_effect(unit)

    def remove_tile_effect(self, coord, unit):
        tile = self.tiles.get(coord)
        if tile:
            tile.remove_effect(unit)

    def is_adjacent(self, from_coord, to_coord):
        return (abs(from_coord.x - to_coord.x) == 1 and from_coord.y == to_coord.y) or \
               (abs(from_coord.y - to_coord.y) == 1 and from_coord.x == to_coord.x)

    def attack_unit(self, from_coord, to_coord):
        from_tile = self.tiles.get(from_coord)
        to_tile = self.tiles.get(to_coord)
        attacker = from_tile.unit
        defender = to_tile.unit

        if attacker.rank > defender.rank:
            to_tile.remove_unit()
            attacker.rank_visible = True
            attacker.was_attacked = True
            
        elif attacker.rank < defender.rank:
            from_tile.remove_unit()
            
            defender.rank_visible = True
            defender.was_attacked = True
        else:
            from_tile.remove_unit()
            to_tile.remove_unit()
            
    def use_special_power(self, coord):
        unit = self.board.get(coord)
        if unit:
            print(f"Using special power: {unit.special_power}")

    def is_within_bounds(self, coord):
        return 0 <= coord.x < self.BOARD_SIZE and 0 <= coord.y < self.BOARD_SIZE

    def restore_board(self, tiles_data):
        for tile_data in tiles_data:
            coord = Coordinate(tile_data["position"]["x"], tile_data["position"]["y"])
            tile_type = tile_data["tile_type"]

            if tile_type == "highground":
                tile = Highground()
            elif tile_type == "cover":
                tile = Cover()
            elif tile_type == "sensor":
                tile = Sensor()
            elif tile_type == "goldmine":
                tile = Goldmine()
            else:
                tile = Tile()

            self.tiles[coord] = tile
            
    def all_units(self):
        units = []
        for tile in self.tiles.values():
            if tile.unit:
                units.append(tile.unit)
        return units