import pygame
import sys
import random
import os
import json
import datetime
from coordinate import Coordinate
from gameboard import GameBoard
from view import GameView
from playersetup import PlayerSetup 
from player import HumanPlayer, AIPlayer
from unit import Scout, Soldier, Sniper, ShieldBearer, BattleMaster, Commando, Flag

class GameController:
    def __init__(self):
        pygame.display.set_caption("Galactic Gladiators")
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.board = GameBoard(initialize_board=False)

        setup = PlayerSetup(self.screen)
        game_option = setup.choose_game_option()

        self.setup_mode = True 

        if game_option == "new_game":
            player_name = setup.get_player_name()
            self.human_player = HumanPlayer(player_name)
            self.ai_player = AIPlayer()
            self.board.setup_board()

        elif isinstance(game_option, dict): 
            game_data = game_option
            self.human_player = HumanPlayer(game_data['human_player']['nickname'])
            self.human_player.gold = game_data['human_player']['gold']
            self.ai_player = AIPlayer()
            self.ai_player.gold = game_data['ai_player']['gold']
            self.restore_tiles(game_data['tiles'])
            self.restore_units(self.human_player, game_data['human_player']['units'])
            self.restore_units(self.ai_player, game_data['ai_player']['units'])
            self.setup_mode = False

        self.view = GameView(self.screen, self.board, self.human_player, self.ai_player)
        self.view.controller = self
        self.save_dir = "saves"
        self.selected_unit = None
        self.current_player = self.human_player
        self.turn_counter = 0

        self.paused = False

        self.cheat_mode = False

        # Eenheden
        self.units_to_place = (
            [Scout() for _ in range(3)] +
            [Soldier() for _ in range(7)] +
            [Sniper() for _ in range(3)] +
            [ShieldBearer() for _ in range(2)] +
            [BattleMaster() for _ in range(2)] +
            [Commando() for _ in range(2)] +
            [Flag() for _ in range(1)]
        )
        self.units_to_place_index = 0

        self.ai_units_to_place = (
            [Scout() for _ in range(3)] +
            [Soldier() for _ in range(7)] +
            [Sniper() for _ in range(3)] +
            [ShieldBearer() for _ in range(2)] +
            [BattleMaster() for _ in range(2)] +
            [Commando() for _ in range(2)] +
            [Flag() for _ in range(1)]
        )

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
                elif event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_ESCAPE: 
                        self.view.paused = not self.view.paused

            self.screen.fill((0, 0, 0))
            self.view.selected_unit = self.selected_unit
            self.view.cheat_mode = self.cheat_mode
            self.view.draw_board()
            pygame.display.flip()
            self.clock.tick(60)

    def restore_tiles(self, tiles_data):
        self.board.restore_board(tiles_data)

    def handle_mouse_click(self, pos):
        action = self.view.check_button_click(pos)
        if action == 'toggle_cheat_mode':
            self.cheat_mode = not self.cheat_mode
            print(f"Cheat Mode {'Enabled' if self.cheat_mode else 'Disabled'}")
        elif action == 'use_special_power':
            if self.selected_unit:
                unit = self.board.tiles[self.selected_unit].unit
                if unit.special_power and not unit.special_power_used:
                    if isinstance(unit, BattleMaster):
                        allies = self.get_adjacent_allies(self.selected_unit)
                        unit.use_special_power(allies)
                    elif isinstance(unit, Commando):
                        enemy = self.get_adjacent_enemy(self.selected_unit)
                        if enemy:
                            unit.use_special_power(enemy)
                    elif isinstance(unit, Scout):
                        unit.use_special_power()
                    else:
                        unit.use_special_power()

                    unit.special_power_used = True
                    print(f"Used special power: {unit.special_power}")
                    self.switch_player()
        else:
            x, y = pos
            if x < self.screen.get_width() - self.view.sidebar_width: 
                row = y // self.view.tile_size
                col = x // self.view.tile_size
                coord = Coordinate(row, col)

                if self.setup_mode:
                    self.handle_setup_click(coord)
                else:
                    self.handle_game_click(coord)          

    def handle_setup_click(self, coord):
        if 8 <= coord.x <= 9:
            unit = self.units_to_place[self.units_to_place_index]
            if self.board.place_unit(coord, unit):
                unit.player = self.current_player
                self.units_to_place_index += 1

            if self.units_to_place_index >= len(self.units_to_place):
                self.setup_mode = False
                self.place_ai_units()
                self.switch_player()

    def place_ai_units(self):
        ai_start_row = 0
        ai_end_row = 1

        ai_coords = [Coordinate(row, col) for row in range(ai_start_row, ai_end_row + 1) for col in range(self.board.BOARD_SIZE)]
        random.shuffle(ai_coords)
        random.shuffle(self.ai_units_to_place)
        
        for unit in self.ai_units_to_place:
            if not ai_coords:
                break
            coord = ai_coords.pop()
            if self.board.place_unit(coord, unit):
                unit.player = self.ai_player
                            
    def handle_game_click(self, coord):
        if self.selected_unit is None:
            if coord in self.board.tiles and self.board.tiles[coord].unit:
                unit = self.board.tiles[coord].unit
                if unit.player == self.current_player:
                    self.selected_unit = coord
        else:
            if coord == self.selected_unit:
                self.selected_unit = None
            else:
                if self.board.move_unit(self.selected_unit, coord):
                    self.selected_unit = None
                    self.switch_player()
                elif coord in self.board.tiles and self.board.tiles[coord].unit:
                    if self.board.tiles[coord].unit.player != self.current_player:
                        if self.is_adjacent(self.selected_unit, coord):
                            self.board.attack_unit(self.selected_unit, coord)
                            self.selected_unit = None
                            self.switch_player()
                        else:
                            print("Attack must be on an adjacent tile.")
                    else:
                        self.selected_unit = None
              
    def is_adjacent(self, from_coord, to_coord):
        return (abs(from_coord.x - to_coord.x) == 1 and from_coord.y == to_coord.y) or \
            (abs(from_coord.y - to_coord.y) == 1 and from_coord.x == to_coord.x)

    def switch_player(self):
        self.turn_counter += 1
        
        self.check_winner()
        
        if self.current_player == self.human_player:
            self.current_player = self.ai_player
            self.ai_player.make_move(self.board)  
            self.current_player = self.human_player  
        else:
            self.current_player = self.human_player

        self.board.update(self.turn_counter)
        
        for unit in self.board.all_units():
            unit.end_turn()
                
        print(f"It's now {self.current_player.name}'s turn.")
        print(f"Turn counter: {self.turn_counter}")
        print(f"Human player gold: {self.human_player.gold}")
        
        if not self.cheat_mode:
            for coord, tile in self.board.tiles.items():
                if tile.unit:
                    if hasattr(tile.unit, 'was_attacked') and tile.unit.was_attacked:
                        tile.unit.rank_visible = True
                        tile.unit.was_attacked = False
                        print(f"Unit at {coord} was attacked!")
                    else:
                        tile.unit.rank_visible = False        
        
        self.save_game()                  
                    

    def save_game(self):
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        game_data = {
            "human_player": {
                "nickname": self.human_player.name,
                "gold": self.human_player.gold,
                "units": self.serialize_units(self.human_player)
            },
            "ai_player": {
                "nickname": self.ai_player.name,
                "gold": self.ai_player.gold,
                "units": self.serialize_units(self.ai_player)
            },
            "tiles": self.serialize_tiles(),
            "save_time": current_time
        }

        save_file = os.path.join(self.save_dir, f"{self.human_player.name}.json")
        with open(save_file, 'w') as f:
            json.dump(game_data, f, indent=4)
        
        print(f"Game saved to {save_file}")

    def serialize_units(self, player):
        units_data = []
        for coord, tile in self.board.tiles.items():
            if tile.unit and tile.unit.player == player:
                units_data.append({
                    "unit_type": tile.unit.__class__.__name__,
                    "position": {"x": coord.x, "y": coord.y},
                    "rank": tile.unit.rank,
                    "player": "human" if player == self.human_player else "ai"
                })
        return units_data

    
    def serialize_tiles(self):
        tiles_data = []
        for coord, tile in self.board.tiles.items():
            tile_data = {
                "position": {"x": coord.x, "y": coord.y},
                "tile_type": tile.tile_type,
                "unit": None
            }

            if tile.unit:
                tile_data["unit"] = {
                    "unit_type": tile.unit.__class__.__name__,
                    "rank": tile.unit.rank
                }

            tiles_data.append(tile_data)

        return tiles_data

    
    def restore_units(self, player, units_data):
        for unit_data in units_data:
            coord = Coordinate(unit_data["position"]["x"], unit_data["position"]["y"])
            unit = self.create_unit_from_data(unit_data)
            self.board.place_unit(coord, unit)
            unit.player = player

    def create_unit_from_data(self, unit_data):
        unit_type = unit_data["unit_type"]
        if unit_type == "Scout":
            return Scout()
        elif unit_type == "Soldier":
            return Soldier()
        elif unit_type == "Sniper":
            return Sniper()
        elif unit_type == "ShieldBearer":
            return ShieldBearer()
        elif unit_type == "BattleMaster":
            return BattleMaster()
        elif unit_type == "Commando":
            return Commando()
        elif unit_type == "Flag":
            return Flag()
        else:
            raise ValueError(f"Unknown unit type: {unit_type}")

    def load_game(self):
        self.nickname = input("Voer je nickname in om het spel te laden: ")
        save_file = os.path.join(self.save_dir, f"{self.nickname}_save.json")

        if not os.path.exists(save_file):
            print("Geen opgeslagen spel gevonden met deze nickname!")
            sys.exit()

        with open(save_file, 'r') as f:
            game_data = json.load(f)

        self.human_player = HumanPlayer(name=game_data['human_player']['nickname'])
        self.human_player.gold = game_data['human_player']['gold']

        self.ai_player = AIPlayer(name=game_data['ai_player']['nickname'])
        self.ai_player.gold = game_data['ai_player']['gold']

        self.board = GameBoard()

        self.deserialize_units(game_data['human_player']['units'], self.human_player)
        self.deserialize_units(game_data['ai_player']['units'], self.ai_player)

        print(f"Spel geladen voor {self.human_player.name} met {self.human_player.gold} goudstukken.")

    def deserialize_units(self, units_data, player):
        for unit_data in units_data:
            unit_type = unit_data['unit_type']
            position = unit_data['position']
            coord = Coordinate(position['x'], position['y'])

            if unit_type == "Scout":
                unit = Scout()
            elif unit_type == "Soldier":
                unit = Soldier()
            elif unit_type == "Sniper":
                unit = Sniper()
            elif unit_type == "ShieldBearer":
                unit = ShieldBearer()
            elif unit_type == "BattleMaster":
                unit = BattleMaster()
            elif unit_type == "Commando":
                unit = Commando()
            elif unit_type == "Flag":
                unit = Flag()

            unit.player = player
            self.board.place_unit(coord, unit)

    def check_winner(self):
        if not any(unit.player == self.ai_player for unit in self.board.all_units()):
            self.view.show_winner_screen(self.human_player.gold, self.return_to_start_screen)

    def return_to_start_screen(self):
        self.__init__() 
        self.main_loop()


if __name__ == "__main__":
    pygame.init()
    game_controller = GameController()
    game_controller.main_loop()
