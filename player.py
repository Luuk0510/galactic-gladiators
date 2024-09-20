from coordinate import Coordinate
import random;

class Player:
    def __init__(self, name, color):
        self.name = name
        self.units = []
        self.color = color
        self.gold = 0

    def add_unit(self, unit):
        self.units.append(unit)

class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name=name, color=(0, 0, 255))

class AIPlayer(Player):
    def __init__(self):
        super().__init__(name="AI", color=(0, 242, 255))

    def make_move(self, board):
        unit_coords = [coord for coord, tile in board.tiles.items() if tile.unit and tile.unit.player == self]
        if not unit_coords:
            return

        random.shuffle(unit_coords)
        for from_coord in unit_coords:
            possible_moves = self.get_possible_moves(from_coord, board)
            random.shuffle(possible_moves)
            for to_coord in possible_moves:
                target_unit = board.get_unit(to_coord)
                if board.is_within_bounds(to_coord) and (target_unit is None or target_unit.player != self):
                    board.move_unit(from_coord, to_coord)
                    return 

    def get_possible_moves(self, from_coord, board):
        x, y = from_coord.x, from_coord.y
        possible_moves = [
            Coordinate(x - 1, y),  # up
            Coordinate(x + 1, y),  # down
            Coordinate(x, y - 1),  # left
            Coordinate(x, y + 1)   # right
        ]
        # Filter valid moves
        return [coord for coord in possible_moves if board.is_within_bounds(coord) and (board.get_unit(coord) is None or board.get_unit(coord).player != self)]



