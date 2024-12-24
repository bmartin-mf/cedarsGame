import pygame
from .game_state import GameState
from characters.character import Character
from characters.ai_controller import AIController
from characters.boss_data import BossData
from map.map_manager import MapManager
from sound.sound_manager import SoundManager

class FightState(GameState):
    def __init__(self, p1_char_id, p2_char_id, ai_opponent=False, ai_difficulty='medium', is_campaign=False, is_final_battle=False):
        super().__init__()  # Initialize parent class
        self.font = pygame.font.Font(None, 72)  # 2x font size
        self.round_time = 99 * 60  # 99 seconds in frames
        
        # Screen dimensions (2x scale)
        self.SCREEN_WIDTH = 1600  # 2x of 800
        self.SCREEN_HEIGHT = 1200  # 2x of 600
        
        # Campaign mode attributes
        self.is_campaign = is_campaign
        self.is_final_battle = is_final_battle
        self.boss_data = None
        
        # Initialize map manager with stage ID matching character ID in campaign mode
        stage_id = 99 if is_final_battle else (p2_char_id if is_campaign else 0)
        self.map_manager = MapManager(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, stage_id)
        
        # Initialize sound manager and play stage music
        self.sound_manager = SoundManager()
        self.sound_manager.play_stage_music(stage_id)
        
        # Initialize player character (2x positions)
        self.p1 = Character(400, 1000, char_id=p1_char_id, facing_right=True)  # Start on left
        
        # Initialize opponents
        self.opponents = []
        if is_final_battle and isinstance(p2_char_id, list):
            # Multiple opponents for final battle (2x positions)
            positions = [(1000, 1000), (1200, 1000), (1400, 1000)]  # Spread out the opponents
            for i, opponent_id in enumerate(p2_char_id):
                opponent = Character(positions[i][0], positions[i][1], char_id=opponent_id, facing_right=False)
                if isinstance(opponent_id, str):  # If it's a boss
                    boss_data = BossData.get_boss_data(opponent_id)
                    if boss_data:
                        opponent.health *= boss_data['health_multiplier']
                        opponent.speed *= boss_data['speed_multiplier']
                        opponent.damage_multiplier = boss_data['damage_multiplier']
                self.opponents.append({
                    'character': opponent,
                    'ai': AIController(boss_data['difficulty'] if boss_data else 'medium')
                })
        else:
            # Single opponent (2x position)
            self.p2 = Character(1200, 1000, char_id=p2_char_id, facing_right=False)  # Start on right
            if is_campaign:
                self.boss_data = BossData.get_boss_data(p2_char_id)
                self.p2.health *= self.boss_data['health_multiplier']
                self.p2.speed *= self.boss_data['speed_multiplier']
                self.p2.damage_multiplier = self.boss_data['damage_multiplier']
            self.opponents = [{
                'character': self.p2,
                'ai': AIController(self.boss_data['difficulty'] if self.boss_data else ai_difficulty)
            }]
        
        # Round system
        self.round_number = 1
        self.p1_rounds_won = 0
        self.p2_rounds_won = 0
        self.round_state = 'fighting'  # 'fighting', 'round_over', 'match_over'
        self.round_end_timer = 180  # 3 seconds at 60 FPS
        self.winner = None
        
    def __del__(self):
        """Clean up when the state is destroyed"""
        if hasattr(self, 'sound_manager'):
            self.sound_manager.stop_music()
            
    def check_round_end(self):
        """Check if the round should end"""
        if self.round_state == 'fighting':
            if self.p1.health <= 0:
                self.round_state = 'round_over'
                self.winner = 'P2'
                self.p2_rounds_won += 1
                self.p1.state = 'loss'
                for opp in self.opponents:
                    opp['character'].state = 'win'
            elif all(opp['character'].health <= 0 for opp in self.opponents):
                self.round_state = 'round_over'
                self.winner = 'P1'
                self.p1_rounds_won += 1
                self.p1.state = 'win'
                for opp in self.opponents:
                    opp['character'].state = 'loss'
                    
                # Special case: After defeating Bren, Lee appears
                if self.is_campaign and self.boss_data and self.boss_data['name'] == 'Bren' and self.p1_rounds_won >= 2:
                    self.round_state = 'lee_intro'
                    self.round_end_timer = 180  # 3 seconds for Lee's intro
                    # Create Lee as the new opponent
                    self.p2 = Character(1200, 1000, char_id='lee', facing_right=False)
                    self.opponents = [{
                        'character': self.p2,
                        'ai': AIController('hard')  # Lee is a tough opponent
                    }]
                    self.boss_data = {
                        'name': 'Lee',
                        'color': (255, 0, 0),  # Red for Lee
                        'health_multiplier': 1.5,
                        'speed_multiplier': 1.2,
                        'damage_multiplier': 1.3,
                        'difficulty': 'hard'
                    }
                    # Reset round counters for the new fight
                    self.round_number = 1
                    self.p1_rounds_won = 0
                    self.p2_rounds_won = 0
                    self.p1.health = 200  # Reset player health
                    # Change music for Lee's fight
                    self.sound_manager.play_stage_music('lee')
                    return
                    
            elif self.round_time <= 0:
                self.round_state = 'round_over'
                # Determine winner by total health percentage
                p1_health_percent = self.p1.health / 200
                p2_health_percent = sum(opp['character'].health / 200 for opp in self.opponents) / len(self.opponents)
                if p1_health_percent > p2_health_percent:
                    self.winner = 'P1'
                    self.p1_rounds_won += 1
                    self.p1.state = 'win'
                    for opp in self.opponents:
                        opp['character'].state = 'loss'
                else:
                    self.winner = 'P2'
                    self.p2_rounds_won += 1
                    self.p1.state = 'loss'
                    for opp in self.opponents:
                        opp['character'].state = 'win'
                    
            # Check if match is over
            if self.p1_rounds_won >= 2 or self.p2_rounds_won >= 2:
                self.round_state = 'match_over'
                
    def handle_event(self, event):
        """Handle keyboard events for jumping and attacks"""
        if event.type == pygame.KEYDOWN:
            # During round end, any key press continues to next round
            if self.round_end_timer <= 0:
                if self.winner is not None:
                    if self.p1_rounds_won >= 2 or self.p2_rounds_won >= 2:
                        # Game is over, transition to appropriate state
                        if self.is_campaign and self.p1_rounds_won >= 2:
                            return PrizeState(self.current_stage)
                        else:
                            return MenuState()
                    else:
                        # Reset for next round
                        self.reset_round()
                        return None
            
            # During active gameplay, handle normal controls
            if event.key == pygame.K_LEFT:
                self.p1.move(-1)
            elif event.key == pygame.K_RIGHT:
                self.p1.move(1)
            elif event.key == pygame.K_SPACE:
                self.p1.jump()
            elif event.key == pygame.K_z:
                self.p1.attack('punch')
            elif event.key == pygame.K_x:
                self.p1.attack('kick')
            elif event.key == pygame.K_c:
                self.p1.throw_item()
        
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                # Only stop movement if the released key matches the current movement direction
                if (event.key == pygame.K_LEFT and self.p1.vel_x < 0) or \
                   (event.key == pygame.K_RIGHT and self.p1.vel_x > 0):
                    self.p1.move(0)
        
        return None

    def update(self):
        if self.round_state == 'fighting':
            # Get pressed keys for continuous movement
            keys = pygame.key.get_pressed()
            
            # Player 1 movement (only move if keys are pressed)
            dx1 = 0
            if keys[pygame.K_LEFT]: dx1 -= 1
            if keys[pygame.K_RIGHT]: dx1 += 1
            if dx1 != 0:  # Only update movement if there's input
                self.p1.move(dx1)
            
            # Update all opponents with AI
            for opp in self.opponents:
                # Get AI decision
                actions = opp['ai'].decide_action(opp['character'], self.p1)
                # Apply AI actions
                opp['ai'].apply_actions(opp['character'], actions)
            
            # Update all characters with map collision handling
            self.p1.update(self.map_manager)
            for opp in self.opponents:
                opp['character'].update(self.map_manager)
            
            # Check all collisions
            self.check_collisions()
            
            # Update timer
            if self.round_time > 0:
                self.round_time -= 1
                
            # Check for round end
            self.check_round_end()
        else:
            # Update round end timer
            if self.round_end_timer > 0:
                self.round_end_timer -= 1
            
        return None
            
    def check_collisions(self):
        # Check player collisions with all opponents
        for opp in self.opponents:
            if self.p1.rect.colliderect(opp['character'].rect):
                # Push characters apart
                if self.p1.x < opp['character'].x:
                    self.p1.x = opp['character'].x - self.p1.width
                else:
                    self.p1.x = opp['character'].x + opp['character'].width
                self.p1.rect.x = self.p1.x
                opp['character'].rect.x = opp['character'].x
            
            # Check attack collisions
            if self.p1.attack_rect and self.p1.attack_rect.colliderect(opp['character'].rect):
                opp['character'].take_damage(10 * self.p1.damage_multiplier)
                
            if opp['character'].attack_rect and opp['character'].attack_rect.colliderect(self.p1.rect):
                self.p1.take_damage(10 * opp['character'].damage_multiplier)
                
            # Check thrown item collisions
            for item in self.p1.thrown_items[:]:
                if item['active'] and item['rect'].colliderect(opp['character'].rect):
                    opp['character'].take_damage(15 * self.p1.damage_multiplier)
                    item['active'] = False
                    self.p1.thrown_items.remove(item)
                    
            for item in opp['character'].thrown_items[:]:
                if item['active'] and item['rect'].colliderect(self.p1.rect):
                    self.p1.take_damage(15 * opp['character'].damage_multiplier)
                    item['active'] = False
                    opp['character'].thrown_items.remove(item)
                    
    def draw(self, screen):
        # Draw the stage and obstacles
        self.map_manager.draw(screen)
        
        # Draw all characters
        self.p1.draw(screen)
        for opp in self.opponents:
            opp['character'].draw(screen)
        
        # Draw timer
        seconds = self.round_time // 60
        timer_text = self.font.render(str(seconds), True, (255, 255, 255))
        timer_rect = timer_text.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(timer_text, timer_rect)
        
        # Draw round indicators
        if self.round_state == 'lee_intro':
            round_text = self.font.render("LEE HAS APPEARED!", True, (255, 0, 0))
        elif self.is_final_battle:
            round_text = self.font.render("FINAL BATTLE - Round " + str(self.round_number), True, (255, 0, 0))
        elif self.is_campaign:
            round_text = self.font.render(f"VS {self.boss_data['name']} - Round {self.round_number}", True, self.boss_data['color'])
        else:
            round_text = self.font.render(f"Round {self.round_number}", True, (255, 255, 255))
        round_rect = round_text.get_rect(center=(screen.get_width() // 2, 20))
        screen.blit(round_text, round_rect)
        
        # Draw round wins
        p1_wins_text = self.font.render(f"Wins: {self.p1_rounds_won}", True, (0, 255, 0))
        p2_wins_text = self.font.render(f"Wins: {self.p2_rounds_won}", True, (0, 255, 0))
        screen.blit(p1_wins_text, (50, 50))
        screen.blit(p2_wins_text, (700, 50))
        
        # Draw health bars
        # Player health bar
        pygame.draw.rect(screen, (128, 128, 128), (50, 20, 300, 20))
        p1_health_width = 300 * (self.p1.health / 200)
        pygame.draw.rect(screen, (255, 0, 0), (50, 20, p1_health_width, 20))
        
        # Opponents' health bars
        total_width = 300
        bar_width = total_width / len(self.opponents)
        for i, opp in enumerate(self.opponents):
            x_pos = 450 + (i * bar_width)
            pygame.draw.rect(screen, (128, 128, 128), (x_pos, 20, bar_width - 5, 20))
            health_width = (bar_width - 5) * (opp['character'].health / (200 * (self.boss_data['health_multiplier'] if self.is_campaign else 1)))
            if self.is_campaign:
                health_color = self.boss_data['color']
            else:
                health_color = (255, 0, 0)
            pygame.draw.rect(screen, health_color, (x_pos, 20, health_width, 20))
            
            # Draw opponent name
            if self.is_campaign or self.is_final_battle:
                boss_data = BossData.get_boss_data(opp['character'].char_id)
                name = self.font.render(boss_data['name'], True, boss_data['color'])
                name_rect = name.get_rect(center=(x_pos + bar_width/2, 50))
                screen.blit(name, name_rect)
        
        # Draw round end message
        if self.round_state == 'round_over':
            if self.winner == 'P1':
                win_text = "You Win Round!"
            else:
                win_text = "Opponents Win Round!"
                
            if self.round_end_timer <= 0:
                win_text += " - Press ENTER to continue"
                
            text = self.font.render(win_text, True, (255, 255, 0))
            text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text, text_rect)
            
        # Draw match end message
        elif self.round_state == 'match_over':
            if self.p1_rounds_won >= 2:
                if self.is_final_battle:
                    win_text = "LEGENDARY VICTORY! You've defeated all champions!"
                elif self.is_campaign:
                    win_text = f"Victory! You've defeated {self.boss_data['name']}!"
                else:
                    win_text = "Player 1 Wins Match!"
            else:
                if self.is_final_battle:
                    win_text = "Defeat! The champions remain unbeaten!"
                elif self.is_campaign:
                    win_text = f"Defeat! {self.boss_data['name']} is victorious!"
                else:
                    win_text = "Player 2 Wins Match!"
                
            if self.round_end_timer <= 0:
                win_text += " - Press ENTER to continue"
                
            text = self.font.render(win_text, True, (255, 255, 0))
            text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text, text_rect) 