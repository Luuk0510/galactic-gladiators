import pygame
import sys
import os
import json

class PlayerSetup:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.player_name = ""
        self.save_dir = "saves"

    def choose_game_option(self):
        title_font_path = os.path.join("fonts", "MajorMonoDisplay-Regular.ttf")  # BebasNeue-Regular
        button_font_path = os.path.join("fonts", "Roboto-Regular.ttf")

        title_font = pygame.font.Font(title_font_path, 80)
        button_font = pygame.font.Font(button_font_path, 40)
        footer_font = pygame.font.Font(button_font_path, 20)

        title_text = title_font.render("Galactic Gladiators", True, (255, 255, 255))
        new_game_text = button_font.render("Nieuw Spel", True, (0, 0, 0))
        load_game_text = button_font.render("Laad Spel", True, (0, 0, 0))
        footer_text = footer_font.render("Gemaakt door Joep en Luuk", True, (200, 200, 200))

        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
        footer_rect = footer_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 30))

        button_width = 300
        button_height = 80

        new_game_rect = pygame.Rect((self.screen.get_width() // 2 - button_width // 2, self.screen.get_height() // 2 - 50), (button_width, button_height))
        load_game_rect = pygame.Rect((self.screen.get_width() // 2 - button_width // 2, self.screen.get_height() // 2 + 100), (button_width, button_height))

        default_button_color = (255, 255, 255)
        hover_button_color = (200, 200, 200)

        while True:
            mouse_pos = pygame.mouse.get_pos()

            if new_game_rect.collidepoint(mouse_pos):
                new_game_color = hover_button_color
            else:
                new_game_color = default_button_color

            if load_game_rect.collidepoint(mouse_pos):
                load_game_color = hover_button_color
            else:
                load_game_color = default_button_color

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if new_game_rect.collidepoint(event.pos):
                        return "new_game"
                    elif load_game_rect.collidepoint(event.pos):
                        return self.load_game() 

            self.screen.fill((20, 20, 20))

            self.screen.blit(title_text, title_rect)

            self.draw_button_with_shadow(new_game_rect, new_game_color, 20)
            self.draw_button_with_shadow(load_game_rect, load_game_color, 20)

            self.screen.blit(new_game_text, 
                            new_game_text.get_rect(center=new_game_rect.center))
            self.screen.blit(load_game_text, 
                            load_game_text.get_rect(center=load_game_rect.center))

            self.screen.blit(footer_text, footer_rect)

            pygame.display.flip()
            self.clock.tick(30)

    def draw_button_with_shadow(self, rect, color, radius):
        shadow_offset = 5
        shadow_color = (50, 50, 50)

        shadow_rect = rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        pygame.draw.rect(self.screen, shadow_color, shadow_rect, border_radius=radius)

        pygame.draw.rect(self.screen, color, rect, border_radius=radius)

    def get_player_name(self):
        font_path = os.path.join("fonts", "Roboto-Regular.ttf")
        font = pygame.font.Font(font_path, 25)
        label_font = pygame.font.Font(font_path, 35)

        input_box = pygame.Rect(self.screen.get_width() // 2 - 200, self.screen.get_height() // 2, 400, 50)
        label = label_font.render("Voer je naam in:", True, (255, 255, 255))
        label_rect = label.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 60))

        active = False
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        text = ''
        submit_button_rect = pygame.Rect(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 100, 200, 50)
        submit_button_color = pygame.Color('green')

        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False

                    color = color_active if active else color_inactive
                    
                    if submit_button_rect.collidepoint(event.pos):
                        self.player_name = text
                        return self.player_name

                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            self.player_name = text
                            return self.player_name
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode 

            self.screen.fill((20, 20, 20))

            self.screen.blit(label, label_rect)

            txt_surface = font.render(text, True, color)
            input_box.w = max(400, txt_surface.get_width() + 10)
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 10))
            pygame.draw.rect(self.screen, color, input_box, 2, border_radius=10)

            pygame.draw.rect(self.screen, submit_button_color, submit_button_rect, border_radius=15)
            submit_text = font.render("Bevestigen", True, (255, 255, 255))
            submit_text_rect = submit_text.get_rect(center=submit_button_rect.center)
            self.screen.blit(submit_text, submit_text_rect)

            if submit_button_rect.collidepoint(mouse_pos):
                submit_button_color = pygame.Color('darkgreen')
            else:
                submit_button_color = pygame.Color('green')

            pygame.display.flip()
            self.clock.tick(30)
            
    def load_game(self):
        save_files = [f for f in os.listdir(self.save_dir) if f.endswith(".json")]
        if not save_files:
            return "new_game"
    
        font_path = os.path.join("fonts", "Roboto-Regular.ttf")
        font = pygame.font.Font(font_path, 30)
        title_font = pygame.font.Font(font_path, 50)
    
        title_text = title_font.render("Laad Spel", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
    
        selected_file = None
    
        file_data = []
        for file in save_files:
            file_path = os.path.join(self.save_dir, file)
            with open(file_path, 'r') as f:
                game_data = json.load(f)
                save_time = game_data.get('save_time', 'Unknown time')
                file_data.append((file, save_time))
    
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for idx, (file, _) in enumerate(file_data):
                        file_rect = pygame.Rect(self.screen.get_width() // 2 - 300, 300 + idx * 60, 600, 50)  
                        if file_rect.collidepoint(event.pos):
                            selected_file = file
                            break
                    if selected_file:
                        return self.load_game_data(selected_file)
    
            self.screen.fill((30, 30, 30)) 
    
            self.screen.blit(title_text, title_rect)
    
            for idx, (file, save_time) in enumerate(file_data):
                file_rect = pygame.Rect(self.screen.get_width() // 2 - 300, 300 + idx * 60, 600, 50)
    
                if file_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, (200, 200, 200), file_rect, border_radius=15)
                else:
                    pygame.draw.rect(self.screen, (100, 100, 100), file_rect, border_radius=15)
    
                file_text = font.render(file, True, (255, 255, 255))
                time_text = font.render(save_time, True, (200, 200, 200))
    
                self.screen.blit(file_text, file_text.get_rect(midleft=(file_rect.left + 10, file_rect.centery)))
                self.screen.blit(time_text, time_text.get_rect(midright=(file_rect.right - 10, file_rect.centery)))
    
            pygame.display.flip()
            self.clock.tick(30)


    def load_game_data(self, filename):
        file_path = os.path.join(self.save_dir, filename)
        with open(file_path, 'r') as f:
            game_data = json.load(f)

        return game_data
