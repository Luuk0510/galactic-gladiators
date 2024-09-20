import os
import pygame
import sys
from coordinate import Coordinate
from tile import Tile

class GameView:
    def __init__(self, screen, board, human_player, ai_player, selected_unit=None):
        self.screen = screen
        self.board = board
        self.tile_size = 80
        self.human_player = human_player
        self.ai_player = ai_player
        self.selected_unit = selected_unit

        self.sidebar_width = 400
        self.sidebar_height = screen.get_height()
        font_path = os.path.join("fonts", "Roboto-Regular.ttf")
        self.font_size = 25 
        self.font_path = font_path
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.button_text = "Strijdkreet"
        self.button_padding = 20
        self.player = human_player

        self.paused = False

    def draw_board(self):
        if not self.paused:
            for row in range(10):
                for col in range(10):
                    coord = Coordinate(row, col)
                    tile = self.board.tiles.get(coord, Tile())
                    color = tile.color

                    pygame.draw.rect(self.screen, color,
                                    (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                    (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size), 1)

                    if tile.unit:
                        unit = tile.unit
                        selected = coord == self.selected_unit
                        if unit.player == self.human_player:
                            self.draw_unit(unit, col * self.tile_size, row * self.tile_size, str(unit.rank), selected)
                        elif unit.player == self.ai_player:
                            if unit.rank_visible or self.cheat_mode:
                                self.draw_unit(unit, col * self.tile_size, row * self.tile_size, str(unit.rank), selected)
                            else:
                                self.draw_unit(unit, col * self.tile_size, row * self.tile_size, "?", selected)

            self.draw_sidebar(self.selected_unit)
        else:
            self.draw_pause_menu()


    def draw_unit(self, unit, x, y, text, selected=False):
        color = unit.player.color
        highlight_color = (255, 255, 0)
        
        if not unit.invisible:
            if selected:
                pygame.draw.circle(self.screen, highlight_color, (x + self.tile_size // 2, y + self.tile_size // 2), 35)
            pygame.draw.circle(self.screen, color, (x + self.tile_size // 2, y + self.tile_size // 2), 30)
            font = pygame.font.Font(None, 36)
            text_surface = font.render(text if unit.is_rank_visible(self.cheat_mode) or unit.player == self.human_player else "?", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
            self.screen.blit(text_surface, text_rect)

    def draw_sidebar(self, selected_unit=None):
        sidebar_rect = pygame.Rect(self.screen.get_width() - self.sidebar_width, 0, self.sidebar_width, self.sidebar_height)
        pygame.draw.rect(self.screen, (255, 255, 200), sidebar_rect)

        self.draw_legend()

        unit = None
        if selected_unit:
            unit = self.board.get_unit(selected_unit)

        self.show_selected_unit(unit)

        self.show_gold()

        if unit and unit.special_power and not unit.special_power_used:
            self.draw_special_power_button(unit)

        self.draw_cheat_mode_button()

    def draw_special_power_button(self, unit):
        button_text = f"Use {unit.special_power}"
        button_size = self.font.size(button_text)

        button_padding_x = 10
        button_padding_y = 5 
        button_width = button_size[0] + 2 * button_padding_x
        button_height = button_size[1] + 2 * button_padding_y

        button_x = self.screen.get_width() - self.sidebar_width + 20
        button_y = 650 

        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, (0, 200, 0), button_rect, border_radius=20)

        button_text_surface = self.font.render(button_text, True, (255, 255, 255))
        button_text_rect = button_text_surface.get_rect(center=button_rect.center)
        self.screen.blit(button_text_surface, button_text_rect)

        self.special_power_button_rect = button_rect

    def draw_rounded_rect(self, surface, color, rect, corner_radius):
        pygame.draw.rect(surface, color, (rect.x + corner_radius, rect.y, rect.width - 2 * corner_radius, rect.height))
        pygame.draw.rect(surface, color, (rect.x, rect.y + corner_radius, rect.width, rect.height - 2 * corner_radius))
        pygame.draw.circle(surface, color, (rect.x + corner_radius, rect.y + corner_radius), corner_radius)
        pygame.draw.circle(surface, color, (rect.x + rect.width - corner_radius, rect.y + corner_radius), corner_radius)
        pygame.draw.circle(surface, color, (rect.x + corner_radius, rect.y + rect.height - corner_radius), corner_radius)
        pygame.draw.circle(surface, color, (rect.x + rect.width - corner_radius, rect.y + rect.height - corner_radius), corner_radius)

    def draw_legend(self):
        legends = [
            ("Verhoogd", (0, 128, 0)),
            ("Dekking", (128, 0, 128)),
            ("Sensor", (255, 0, 0)),
            ("Goudmijn", (255, 215, 0))
        ]

        y_offset = 50
        for name, color in legends:
            pygame.draw.rect(self.screen, color, (self.screen.get_width() - self.sidebar_width + 20, y_offset, 60, 60))
            legend_text = self.font.render(name, True, (0, 0, 0))
            self.screen.blit(legend_text, (self.screen.get_width() - self.sidebar_width + 90, y_offset + 20))
            y_offset += 80

    def show_selected_unit(self, unit):
        unit_name = unit.__class__.__name__ if unit else ""
        text = f"Geselecteerd: {unit_name}"

        y_offset = 700 - 120
        rendered_text = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(rendered_text, (self.screen.get_width() - self.sidebar_width + 20, y_offset))

    def show_gold(self):
        gold_text = f"Goud: {self.player.gold}"
        y_offset = 700 - 80
        rendered_gold_text = self.font.render(gold_text, True, (0, 0, 0))
        self.screen.blit(rendered_gold_text, (self.screen.get_width() - self.sidebar_width + 20, y_offset))    

    def draw_pause_menu(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((20, 20, 20, 150))
        self.screen.blit(overlay, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        corner_radius = 20
        button_spacing = 40
        button_width = 300
        button_height = 100

        center_x = self.screen.get_width() // 2 - 150  

        resume_color = (255, 255, 255) if not pygame.Rect(center_x, 300, button_width, button_height).collidepoint(mouse_pos) else (200, 200, 200)
        save_color = (255, 255, 255) if not pygame.Rect(center_x, 300 + button_height + button_spacing, button_width, button_height).collidepoint(mouse_pos) else (200, 200, 200)
        quit_color = (255, 0, 0) if not pygame.Rect(center_x, 300 + 2 * (button_height + button_spacing), button_width, button_height).collidepoint(mouse_pos) else (255, 100, 100)


        pause_font = pygame.font.Font(self.font_path, 50)

        resume_text = pause_font.render("Hervatten", True, (0, 0, 0))
        save_text = pause_font.render("Opslaan", True, (0, 0, 0))
        quit_text = pause_font.render("Afsluiten", True, (0, 0, 0))

        resume_rect = pygame.Rect(center_x, 300, button_width, button_height)
        save_rect = pygame.Rect(center_x, 300 + button_height + button_spacing, button_width, button_height)
        quit_rect = pygame.Rect(center_x, 300 + 2 * (button_height + button_spacing), button_width, button_height)

        self.draw_rounded_rect(self.screen, resume_color, resume_rect, corner_radius)
        self.draw_rounded_rect(self.screen, save_color, save_rect, corner_radius)
        self.draw_rounded_rect(self.screen, quit_color, quit_rect, corner_radius)

        self.screen.blit(resume_text, resume_text.get_rect(center=resume_rect.center))
        self.screen.blit(save_text, save_text.get_rect(center=save_rect.center))
        self.screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    self.paused = False 
                elif save_rect.collidepoint(event.pos):
                    self.controller.save_game()
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    def draw_rounded_rect(self, surface, color, rect, corner_radius):
        pygame.draw.rect(surface, color, (rect.x + corner_radius, rect.y, rect.width - 2 * corner_radius, rect.height))
        pygame.draw.rect(surface, color, (rect.x, rect.y + corner_radius, rect.width, rect.height - 2 * corner_radius))
        pygame.draw.circle(surface, color, (rect.x + corner_radius, rect.y + corner_radius), corner_radius)
        pygame.draw.circle(surface, color, (rect.x + rect.width - corner_radius, rect.y + corner_radius), corner_radius)
        pygame.draw.circle(surface, color, (rect.x + corner_radius, rect.y + rect.height - corner_radius), corner_radius)
        pygame.draw.circle(surface, color, (rect.x + rect.width - corner_radius, rect.y + rect.height - corner_radius), corner_radius)

    def draw_cheat_mode_button(self):
        cheat_button_text = "Toggle Cheat Mode"

        button_width = 250
        button_height = 40

        button_x = self.screen.get_width() - self.sidebar_width + self.button_padding
        button_y = self.sidebar_height - 50

        cheat_button = pygame.Rect(button_x, button_y, button_width, button_height)

        self.draw_rounded_rect(self.screen, (0, 128, 128), cheat_button, corner_radius=15)

        text_surface = self.font.render(cheat_button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=cheat_button.center)
        self.screen.blit(text_surface, text_rect)

        self.button_rect = cheat_button


    def check_button_click(self, pos):
        if hasattr(self, 'special_power_button_rect') and self.special_power_button_rect.collidepoint(pos):
            return 'use_special_power'
        elif hasattr(self, 'button_rect') and self.button_rect.collidepoint(pos):
            return 'toggle_cheat_mode'
        return None
    
    def show_winner_screen(self, human_player_gold, return_to_start_callback):
        winner_font = pygame.font.Font(os.path.join("fonts", "Roboto-Regular.ttf"), 60)
        button_font = pygame.font.Font(os.path.join("fonts", "Roboto-Regular.ttf"), 40)

        winner_text = winner_font.render("Je hebt gewonnen!", True, (255, 255, 255))
        gold_text = button_font.render(f"Totaal Goud: {human_player_gold}", True, (255, 255, 255))
        back_to_menu_text = button_font.render("Terug naar Startscherm", True, (0, 0, 0))

        winner_text_rect = winner_text.get_rect(center=(self.screen.get_width() // 2, 200))
        gold_text_rect = gold_text.get_rect(center=(self.screen.get_width() // 2, 300))

        back_button_rect = pygame.Rect(self.screen.get_width() // 2 - 250, 500, 500, 80)

        while True:
            mouse_pos = pygame.mouse.get_pos()

            self.screen.fill((20, 20, 20))

            self.screen.blit(winner_text, winner_text_rect)
            self.screen.blit(gold_text, gold_text_rect)

            if back_button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (180, 180, 180), back_button_rect, border_radius=15)
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), back_button_rect, border_radius=15)

            back_text_rect = back_to_menu_text.get_rect(center=back_button_rect.center)
            self.screen.blit(back_to_menu_text, back_text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        return_to_start_callback()

            pygame.display.flip()
