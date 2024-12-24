import pygame
from .game_state import GameState
from .fight_state import FightState
from characters.boss_data import BossData

class CampaignState(GameState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.state = 'select'  # 'select', 'win', 'lose'
        self.current_boss = 'bren'  # Start with first boss
        self.boss_order = ['bren', 'billy', 'niall', 'ciaran']  # Updated boss order
        self.completed_bosses = []
        
    def get_next_boss(self):
        """Get the next boss in the progression"""
        current_index = self.boss_order.index(self.current_boss)
        if current_index < len(self.boss_order) - 1:
            return self.boss_order[current_index + 1]
        return None
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == 'select' and event.key == pygame.K_RETURN:
                # Start fight with current boss
                return FightState('player', self.current_boss, is_campaign=True)
            elif self.state == 'win' and event.key == pygame.K_RETURN:
                # Add current boss to completed list
                if self.current_boss not in self.completed_bosses:
                    self.completed_bosses.append(self.current_boss)
                
                # Check if all regular bosses are defeated
                if len(self.completed_bosses) >= len(self.boss_order):
                    # Start final battle
                    from .final_battle_state import FinalBattleState
                    return FinalBattleState()
                    
                # Get next boss
                next_boss = self.get_next_boss()
                if next_boss:
                    self.current_boss = next_boss
                    self.state = 'select'
                else:
                    # This shouldn't happen now that we have the final battle
                    from .menu_state import MenuState
                    return MenuState()
            elif self.state == 'lose' and event.key == pygame.K_RETURN:
                # Return to menu on loss
                from .menu_state import MenuState
                return MenuState()
        return None
        
    def draw(self, screen):
        screen.fill((0, 0, 0))  # Black background
        
        if self.state == 'select':
            # Draw current stage info
            boss_data = BossData.get_boss_data(self.current_boss)
            
            # Draw boss preview
            preview_surf = pygame.transform.scale(BossData.get_boss_face(self.current_boss), (200, 200))
            preview_rect = preview_surf.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(preview_surf, preview_rect)
            
            # Draw boss name
            name = self.font.render(f"VS {boss_data['name']}", True, boss_data['color'])
            name_rect = name.get_rect(center=(screen.get_width() // 2, 350))
            screen.blit(name, name_rect)
            
            # Draw boss stats
            stats = [
                f"Health: {boss_data['health_multiplier']}x",
                f"Speed: {boss_data['speed_multiplier']}x",
                f"Damage: {boss_data['damage_multiplier']}x"
            ]
            
            for i, stat in enumerate(stats):
                text = self.font.render(stat, True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen.get_width() // 2, 400 + i * 30))
                screen.blit(text, text_rect)
                
            # Draw prompt
            prompt = self.font.render("Press ENTER to fight", True, (255, 255, 0))
            prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, 500))
            screen.blit(prompt, prompt_rect)
            
            # Draw progress
            progress = self.font.render(f"Bosses Defeated: {len(self.completed_bosses)}/{len(self.boss_order)}", True, (255, 255, 255))
            progress_rect = progress.get_rect(topleft=(20, 20))
            screen.blit(progress, progress_rect)
            
        elif self.state == 'win':
            # Draw victory text
            text = self.font.render(f"You defeated {BossData.get_boss_data(self.current_boss)['name']}!", True, (0, 255, 0))
            text_rect = text.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(text, text_rect)
            
            if len(self.completed_bosses) >= len(self.boss_order) - 1:
                # About to start final battle
                prompt = self.font.render("Press ENTER to face your final challenge!", True, (255, 0, 0))
            else:
                # More regular bosses to fight
                prompt = self.font.render("Press ENTER to continue", True, (255, 255, 0))
            prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, 300))
            screen.blit(prompt, prompt_rect)
            
        elif self.state == 'lose':
            # Draw defeat text
            text = self.font.render(f"{BossData.get_boss_data(self.current_boss)['name']} defeated you!", True, (255, 0, 0))
            text_rect = text.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(text, text_rect)
            
            prompt = self.font.render("Press ENTER to return to menu", True, (255, 255, 0))
            prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, 300))
            screen.blit(prompt, prompt_rect) 