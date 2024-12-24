import pygame
from .game_state import GameState
from .fight_state import FightState

class CharacterSelectState(GameState):
    def __init__(self, ai_opponent=False, ai_difficulty='medium'):
        super().__init__()  # Initialize parent class
        self.font = pygame.font.Font(None, 74)
        self.characters = ["Fighter 1", "Fighter 2"]
        self.selected_char = 0
        self.player1_selected = None
        self.player2_selected = None
        self.ai_opponent = ai_opponent
        self.ai_difficulty = ai_difficulty
        print(f"CharacterSelect initialized: AI={ai_opponent}, Difficulty={ai_difficulty}")  # Debug print
        
    def handle_event(self, event):
        next_state = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_char = (self.selected_char - 1) % len(self.characters)
            elif event.key == pygame.K_RIGHT:
                self.selected_char = (self.selected_char + 1) % len(self.characters)
            elif event.key == pygame.K_RETURN:
                if self.player1_selected is None:
                    self.player1_selected = self.selected_char
                    if self.ai_opponent:
                        # AI automatically selects its character
                        self.player2_selected = (self.selected_char + 1) % len(self.characters)
                        print(f"Starting AI fight: P1={self.player1_selected}, P2={self.player2_selected}, Difficulty={self.ai_difficulty}")  # Debug print
                        next_state = FightState(
                            p1_char_id=self.player1_selected,
                            p2_char_id=self.player2_selected,
                            ai_opponent=True,
                            ai_difficulty=self.ai_difficulty
                        )
                elif not self.ai_opponent and self.player2_selected is None:
                    self.player2_selected = self.selected_char
                    print(f"Starting PvP fight: P1={self.player1_selected}, P2={self.player2_selected}")  # Debug print
                    next_state = FightState(
                        p1_char_id=self.player1_selected,
                        p2_char_id=self.player2_selected,
                        ai_opponent=False
                    )
            elif event.key == pygame.K_ESCAPE:
                from .menu_state import MenuState  # Import here to avoid circular import
                next_state = MenuState()
                print("Returning to menu")  # Debug print
        return next_state

    def update(self):
        return None

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Black background
        
        # Draw title
        title_text = "Select Your Character"
        if self.ai_opponent and self.player1_selected is None:
            title_text += f" (VS AI - {self.ai_difficulty.title()})"
        
        title = self.font.render(title_text, True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title, title_rect)
        
        # Draw character options
        for i, char in enumerate(self.characters):
            color = (255, 255, 0) if i == self.selected_char else (255, 255, 255)
            if i == self.player1_selected:
                color = (0, 255, 0)  # Green for P1 selection
            elif i == self.player2_selected:
                color = (0, 0, 255)  # Blue for P2/AI selection
                
            text = self.font.render(char, True, color)
            text_rect = text.get_rect(center=(200 + i * 400, 300))
            screen.blit(text, text_rect)
            
        # Draw selection status
        if self.player1_selected is None:
            status = "Select Your Character"
        elif not self.ai_opponent and self.player2_selected is None:
            status = "Player 2 Select"
        else:
            status = "Press ENTER to Start"
            
        status_text = self.font.render(status, True, (255, 255, 255))
        status_rect = status_text.get_rect(center=(screen.get_width() // 2, 500))
        screen.blit(status_text, status_rect)
        
        # Draw escape instruction
        escape_text = self.font.render("Press ESC to return to menu", True, (128, 128, 128))
        escape_rect = escape_text.get_rect(center=(screen.get_width() // 2, 550))
        screen.blit(escape_text, escape_rect) 