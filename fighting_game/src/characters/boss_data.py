import pygame

class BossData:
    BOSSES = {
        'bren': {
            'name': 'Bren',
            'level': 1,
            'difficulty': 'easy',
            'color': (150, 200, 255),  # Light blue
            'quote': "Let's keep it simple!",
            'win_quote': "Good job! You're getting better!",
            'lose_quote': "Don't worry, keep practicing!",
            'special_moves': ['quick_punch'],
            'health_multiplier': 1.0,
            'speed_multiplier': 0.8,
            'damage_multiplier': 0.8
        },
        'billy': {
            'name': 'Billy',
            'level': 2,
            'difficulty': 'medium',
            'color': (200, 255, 150),  # Light green
            'quote': "Ready for some fun?",
            'win_quote': "Well played! Moving up!",
            'lose_quote': "Almost had it! Try again!",
            'special_moves': ['double_kick'],
            'health_multiplier': 1.2,
            'speed_multiplier': 1.0,
            'damage_multiplier': 1.0
        },
        'gav': {
            'name': 'Gav',
            'level': 3,
            'difficulty': 'medium',
            'color': (255, 200, 150),  # Orange
            'quote': "Show me what you've got!",
            'win_quote': "Impressive progress!",
            'lose_quote': "Getting closer! Keep going!",
            'special_moves': ['combo_punch'],
            'health_multiplier': 1.2,
            'speed_multiplier': 1.0,
            'damage_multiplier': 1.0
        },
        'andy': {
            'name': 'Andy',
            'level': 4,
            'difficulty': 'medium',
            'color': (255, 150, 150),  # Red
            'quote': "Time to step it up!",
            'win_quote': "You're becoming a master!",
            'lose_quote': "So close! Don't give up!",
            'special_moves': ['jump_kick', 'quick_punch'],
            'health_multiplier': 1.3,
            'speed_multiplier': 1.1,
            'damage_multiplier': 1.1
        },
        'craig': {
            'name': 'Craig',
            'level': 5,
            'difficulty': 'hard',
            'color': (200, 150, 255),  # Purple
            'quote': "Let's see if you're ready!",
            'win_quote': "Outstanding! The final test awaits!",
            'lose_quote': "You've got the skill, try again!",
            'special_moves': ['combo_punch', 'double_kick'],
            'health_multiplier': 1.4,
            'speed_multiplier': 1.2,
            'damage_multiplier': 1.2
        },
        'niall': {
            'name': 'Niall',
            'level': 3,
            'difficulty': 'hard',
            'color': (150, 150, 255),  # Blue
            'quote': "Prepare for a real challenge!",
            'win_quote': "Incredible! One more to go!",
            'lose_quote': "So close to the end! Keep pushing!",
            'special_moves': ['jump_kick', 'combo_punch', 'double_kick'],
            'health_multiplier': 1.5,
            'speed_multiplier': 1.3,
            'damage_multiplier': 1.3
        },
        'ciaran': {
            'name': 'Ciaran',
            'level': 4,
            'difficulty': 'extreme',
            'color': (255, 255, 150),  # Gold
            'quote': "Face the final challenge!",
            'win_quote': "Congratulations! You are the champion!",
            'lose_quote': "So close to glory! Try once more!",
            'special_moves': ['ultimate_combo'],
            'health_multiplier': 2.0,
            'speed_multiplier': 1.5,
            'damage_multiplier': 1.5
        }
    }
    
    @staticmethod
    def get_boss_face(boss_id):
        """Create a custom face for the boss"""
        surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        boss = BossData.BOSSES[boss_id]
        color = boss['color']
        
        # Base face
        pygame.draw.circle(surface, color, (10, 10), 10)  # Head outline
        
        # Custom features based on boss
        if boss['difficulty'] == 'easy':
            # Friendly face
            pygame.draw.circle(surface, (0, 0, 0), (7, 7), 2)   # Left eye
            pygame.draw.circle(surface, (0, 0, 0), (13, 7), 2)  # Right eye
            pygame.draw.arc(surface, (0, 0, 0), (5, 5, 10, 10), 0, 3.14, 2)  # Smile
        elif boss['difficulty'] == 'medium':
            # Serious face
            pygame.draw.line(surface, (0, 0, 0), (5, 6), (9, 6), 2)   # Left eyebrow
            pygame.draw.line(surface, (0, 0, 0), (11, 6), (15, 6), 2) # Right eyebrow
            pygame.draw.circle(surface, (0, 0, 0), (7, 8), 2)   # Left eye
            pygame.draw.circle(surface, (0, 0, 0), (13, 8), 2)  # Right eye
            pygame.draw.line(surface, (0, 0, 0), (7, 13), (13, 13), 2)  # Straight mouth
        elif boss['difficulty'] == 'hard':
            # Intense face
            pygame.draw.line(surface, (0, 0, 0), (5, 5), (9, 7), 2)   # Angled left eyebrow
            pygame.draw.line(surface, (0, 0, 0), (11, 7), (15, 5), 2) # Angled right eyebrow
            pygame.draw.circle(surface, (255, 0, 0), (7, 8), 2)   # Red left eye
            pygame.draw.circle(surface, (255, 0, 0), (13, 8), 2)  # Red right eye
            pygame.draw.line(surface, (0, 0, 0), (7, 14), (13, 12), 2)  # Slight frown
        else:  # extreme
            # Final boss face
            pygame.draw.line(surface, (255, 0, 0), (5, 5), (9, 7), 3)   # Thick angled left eyebrow
            pygame.draw.line(surface, (255, 0, 0), (11, 7), (15, 5), 3) # Thick angled right eyebrow
            pygame.draw.circle(surface, (255, 0, 0), (7, 8), 3)   # Large red left eye
            pygame.draw.circle(surface, (255, 0, 0), (13, 8), 3)  # Large red right eye
            pygame.draw.line(surface, (0, 0, 0), (7, 15), (13, 11), 3)  # Intense frown
            
        return surface
        
    @staticmethod
    def get_boss_data(boss_id):
        """Get boss configuration data"""
        return BossData.BOSSES.get(boss_id, None)
        
    @staticmethod
    def get_next_boss(current_boss_id):
        """Get the next boss in sequence"""
        bosses = list(BossData.BOSSES.keys())
        try:
            current_index = bosses.index(current_boss_id)
            if current_index < len(bosses) - 1:
                return bosses[current_index + 1]
        except ValueError:
            pass
        return None 