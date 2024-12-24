import pygame
import os
from .game_state import GameState
from .campaign_state import CampaignState
from sound.sound_manager import SoundManager

class PrizeState(GameState):
    def __init__(self, level):
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.level = level
        self.animation_timer = 180  # 3 seconds at 60 FPS
        self.frame_counter = 0
        
        # Stop any playing music
        self.sound_manager = SoundManager()
        self.sound_manager.stop_music()
        
        # Load stage-specific prize
        if level == 2:  # Billy's stage
            prize_path = os.path.join("fighting_game", "assets", "images", "prize", "prize_2.png")
            if not os.path.exists(prize_path):
                prize_path = os.path.join("assets", "images", "prize", "prize_2.png")
            try:
                self.prize_image = pygame.image.load(prize_path)
                self.prize_image = pygame.transform.scale(self.prize_image, (100, 100))
                self.animation_text = "You found Billy's prize!"
            except:
                self.prize_image = self.create_default_chest()
                self.animation_text = "You found a treasure chest!"
        elif level == 3:  # Niall's stage
            prize_path = os.path.join("fighting_game", "assets", "images", "prize", "prize_3.png")
            if not os.path.exists(prize_path):
                prize_path = os.path.join("assets", "images", "prize", "prize_3.png")
            try:
                self.prize_image = pygame.image.load(prize_path)
                self.prize_image = pygame.transform.scale(self.prize_image, (100, 100))
                self.animation_text = "You found Niall's prize!"
            except:
                self.prize_image = self.create_default_chest()
                self.animation_text = "You found a treasure chest!"
        elif level == 4:  # Ciaran's stage
            self.frames = self.load_whiskey_frames()
            self.current_frame = 0
            self.frame_delay = 10  # Update animation every 10 frames
            self.animation_text = "Your prize: A Triple Whiskey!"
        else:  # Default chest for other stages
            chest_path = os.path.join("fighting_game", "assets", "images", "prize", "chest.png")
            if not os.path.exists(chest_path):
                chest_path = os.path.join("assets", "images", "prize", "chest.png")
            try:
                self.chest_image = pygame.image.load(chest_path)
                self.chest_image = pygame.transform.scale(self.chest_image, (100, 100))
            except:
                self.chest_image = self.create_default_chest()
            self.animation_text = "You found a treasure chest!"
        
        self.state = 'running'  # 'running' or 'complete'
        
    def load_whiskey_frames(self):
        """Load or create whiskey pouring animation frames"""
        frames = []
        glass_height = 40
        liquid_height = 0
        glass_width = 30
        barman_width = 60
        barman_height = 100
        
        for i in range(6):  # 6 frame animation
            surface = pygame.Surface((200, 150), pygame.SRCALPHA)
            
            # Draw barman
            pygame.draw.rect(surface, (100, 100, 100), (20, 10, barman_width, barman_height))  # Body
            pygame.draw.circle(surface, (200, 150, 100), (50, 5), 15)  # Head
            
            # Draw arm holding bottle
            bottle_angle = min(i * 15, 60)  # Gradually tilt the bottle
            bottle_start = (60, 40)
            bottle_end = (100, 40 + i * 5)  # Bottle moves down slightly
            pygame.draw.line(surface, (100, 100, 100), bottle_start, bottle_end, 8)  # Arm
            
            # Draw bottle
            bottle_color = (139, 69, 19)  # Brown for whiskey bottle
            pygame.draw.rect(surface, bottle_color, (bottle_end[0] - 5, bottle_end[1] - 20, 10, 20))
            
            # Draw glass
            glass_x = 120
            glass_y = 80
            # Glass outline
            pygame.draw.polygon(surface, (200, 200, 200), [
                (glass_x, glass_y),  # Top left
                (glass_x + glass_width, glass_y),  # Top right
                (glass_x + glass_width - 5, glass_y + glass_height),  # Bottom right
                (glass_x + 5, glass_y + glass_height)  # Bottom left
            ])
            
            # Draw liquid
            if i > 0:  # Start filling after first frame
                liquid_height = min((i * 8), glass_height - 5)  # Fill gradually
                liquid_y = glass_y + glass_height - liquid_height
                liquid_width = glass_width - (10 * (glass_y + glass_height - liquid_y) / glass_height)
                liquid_x = glass_x + (glass_width - liquid_width) / 2
                pygame.draw.rect(surface, (160, 82, 45), (liquid_x, liquid_y, liquid_width, liquid_height))
                
                # Draw pouring stream
                if i < 5:  # Only show stream while pouring
                    stream_start = (bottle_end[0], bottle_end[1])
                    stream_end = (glass_x + glass_width/2, liquid_y)
                    pygame.draw.line(surface, (160, 82, 45), stream_start, stream_end, 2)
            
            frames.append(surface)
        
        return frames
        
    def create_default_chest(self):
        """Create a default chest image"""
        surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        # Draw basic chest shape
        pygame.draw.rect(surface, (139, 69, 19), (10, 40, 80, 50))  # Main body
        pygame.draw.rect(surface, (101, 67, 33), (10, 40, 80, 25))  # Top half
        pygame.draw.rect(surface, (255, 215, 0), (45, 55, 10, 10))  # Lock
        return surface
        
    def update(self):
        if self.state == 'running':
            self.frame_counter += 1
            if self.level == 4:  # Whiskey animation
                if self.frame_counter % self.frame_delay == 0:
                    self.current_frame = min(self.current_frame + 1, len(self.frames) - 1)
                if self.current_frame >= len(self.frames) - 1:
                    self.animation_timer -= 1
            else:  # Chest animation
                self.animation_timer -= 1
                
            if self.animation_timer <= 0:
                self.state = 'complete'
                
        return None
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.state == 'complete':
                return CampaignState()
        return None
        
    def draw(self, screen):
        screen.fill((0, 0, 0))  # Black background
        
        if self.level == 4:  # Whiskey animation
            # Draw current frame of whiskey animation
            frame = self.frames[self.current_frame]
            frame_rect = frame.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(frame, frame_rect)
        else:
            # Draw chest
            chest_rect = self.chest_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(self.chest_image, chest_rect)
        
        # Draw text
        text = self.font.render(self.animation_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(text, text_rect)
        
        if self.state == 'complete':
            prompt = self.font.render("Press ENTER to continue", True, (255, 255, 0))
            prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))
            screen.blit(prompt, prompt_rect) 