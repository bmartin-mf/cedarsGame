import pygame
from .game_state import GameState
from .character_select_state import CharacterSelectState
from .campaign_state import CampaignState

class MenuState(GameState):
    def __init__(self):
        super().__init__()  # Initialize parent class
        self.font = pygame.font.Font(None, 74)
        self.menu_items = ["VS Player", "Campaign", "Quit"]
        self.selected_item = 0
        print("Menu State initialized")  # Debug print
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                if self.selected_item == 0:  # VS Player
                    print("Starting VS Player mode")  # Debug print
                    return CharacterSelectState(ai_opponent=False)
                elif self.selected_item == 1:  # Campaign
                    print("Starting Campaign mode")  # Debug print
                    return CampaignState()
                elif self.selected_item == 2:  # Quit
                    pygame.quit()
                    exit()
        return None

    def update(self):
        return None

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Black background
        
        # Draw title
        title = self.font.render("2D Fighter", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title, title_rect)
        
        # Draw menu items
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 0) if i == self.selected_item else (255, 255, 255)
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 300 + i * 100))
            screen.blit(text, text_rect) 