import pygame
from .game_state import GameState
from .fight_state import FightState
from .prize_state import PrizeState
from characters.boss_data import BossData

class FinalBattleState(GameState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.state = 'intro'  # 'intro', 'fighting', 'victory', 'defeat'
        self.intro_timer = 180  # 3 seconds at 60 FPS
        
        # Final battle opponents in order of appearance
        self.final_bosses = ['niall', 'billy', 'ciaran']
        
        # Initialize the fight state with all opponents
        self.fight_state = FightState(
            p1_char_id='player',  # Player character
            p2_char_id=self.final_bosses,  # List of boss IDs
            is_campaign=True,
            is_final_battle=True
        )
        
    def update(self):
        if self.state == 'intro':
            if self.intro_timer > 0:
                self.intro_timer -= 1
            else:
                self.state = 'fighting'
        elif self.state == 'fighting':
            result = self.fight_state.update()
            if result is not None:
                if isinstance(result, PrizeState):
                    # Player won the final battle
                    self.state = 'victory'
                    return PrizeState(level='final')  # Special final prize
                else:
                    # Player lost
                    self.state = 'defeat'
                    from .menu_state import MenuState
                    return MenuState()
        return None
        
    def handle_event(self, event):
        if self.state == 'intro':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.intro_timer = 0
        elif self.state == 'fighting':
            return self.fight_state.handle_event(event)
        return None
        
    def draw(self, screen):
        if self.state == 'intro':
            # Draw dramatic intro screen
            screen.fill((0, 0, 0))  # Black background
            
            # Draw title
            title = self.font.render("FINAL BATTLE", True, (255, 0, 0))
            title_rect = title.get_rect(center=(screen.get_width() // 2, 100))
            screen.blit(title, title_rect)
            
            # Draw boss names with dramatic spacing
            y_pos = 200
            for boss_id in self.final_bosses:
                boss_data = BossData.get_boss_data(boss_id)
                name = self.font.render(boss_data['name'], True, boss_data['color'])
                name_rect = name.get_rect(center=(screen.get_width() // 2, y_pos))
                screen.blit(name, name_rect)
                y_pos += 100
                
            # Draw prompt
            if self.intro_timer <= 0:
                prompt = self.font.render("Press ENTER to begin", True, (255, 255, 255))
                prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, 500))
                screen.blit(prompt, prompt_rect)
                
        elif self.state == 'fighting':
            self.fight_state.draw(screen) 