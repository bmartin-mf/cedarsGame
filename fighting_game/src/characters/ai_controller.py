import random
import math

class AIController:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.reaction_time = {
            'easy': 30,      # Slower reactions
            'medium': 20,    # Medium reactions
            'hard': 10,      # Quick reactions
            'extreme': 5     # Lightning fast reactions
        }[difficulty]
        
        self.aggression = {
            'easy': 0.3,     # Less aggressive
            'medium': 0.6,   # Moderately aggressive
            'hard': 0.8,     # Very aggressive
            'extreme': 0.9   # Extremely aggressive
        }[difficulty]
        
        self.frame_counter = 0
        self.decision_cooldown = 0
        self.current_action = None
        
    def decide_action(self, ai_char, player_char):
        """Decide AI character's next action based on game state"""
        # Reset current action
        self.current_action = {
            'move': 0,  # -1 for left, 0 for none, 1 for right
            'jump': False,
            'attack': None
        }
        
        # Calculate distance to player
        distance = abs(ai_char.rect.centerx - player_char.rect.centerx)
        
        # Defensive behavior
        if ai_char.health < 30 and self.difficulty != 'easy':
            # Try to maintain some distance when low on health
            if distance < 80:
                self.current_action['move'] = -1 if ai_char.x < player_char.x else 1
                if random.random() < 0.3:
                    self.current_action['jump'] = True
            return self.current_action
        
        # Offensive behavior
        if distance > 100:
            # Move towards player with pauses
            if random.random() < (0.8 if self.difficulty == 'extreme' else 0.6):
                self.current_action['move'] = -1 if ai_char.x > player_char.x else 1
            
            # Jump occasionally to be unpredictable
            if random.random() < (0.15 if self.difficulty == 'extreme' else 0.08):
                self.current_action['jump'] = True
                
        elif distance <= 60:  # In attack range
            # Stop moving when in attack range
            self.current_action['move'] = 0
            
            # Choose attack type
            if self.difficulty == 'extreme':
                if random.random() < 0.6:
                    self.current_action['attack'] = random.choice(['punch', 'kick', 'throw'])
            else:
                if random.random() < 0.5:
                    self.current_action['attack'] = 'punch'
                elif random.random() < 0.3:
                    self.current_action['attack'] = 'kick'
            
            # Only move during attack in extreme difficulty
            if self.difficulty == 'extreme' and random.random() < 0.3:
                self.current_action['move'] = random.choice([-1, 1])
        
        return self.current_action
        
    def apply_actions(self, character, actions):
        """Apply the decided actions to the character"""
        if actions['move']:
            character.move(actions['move'])
        if actions['jump']:
            character.jump()
        if actions['attack']:
            character.attack(actions['attack']) 