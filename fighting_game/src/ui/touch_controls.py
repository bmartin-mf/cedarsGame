import pygame

class TouchControls:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Calculate UI element sizes based on screen dimensions
        self.button_size = min(screen_width, screen_height) // 8
        self.dpad_size = min(screen_width, screen_height) // 3  # Larger D-pad
        
        # D-pad position (bottom left)
        dpad_margin = 40
        self.dpad_center = (
            dpad_margin + self.dpad_size // 2,
            screen_height - self.dpad_size // 2 - dpad_margin
        )
        
        # D-pad rectangles
        dpad_button_size = self.dpad_size // 3
        
        # Center pad
        self.dpad_center_rect = pygame.Rect(
            self.dpad_center[0] - dpad_button_size // 2,
            self.dpad_center[1] - dpad_button_size // 2,
            dpad_button_size,
            dpad_button_size
        )
        
        # Left button
        self.dpad_left = pygame.Rect(
            self.dpad_center[0] - dpad_button_size * 3 // 2,
            self.dpad_center[1] - dpad_button_size // 2,
            dpad_button_size,
            dpad_button_size
        )
        
        # Right button
        self.dpad_right = pygame.Rect(
            self.dpad_center[0] + dpad_button_size // 2,
            self.dpad_center[1] - dpad_button_size // 2,
            dpad_button_size,
            dpad_button_size
        )
        
        # Up button
        self.dpad_up = pygame.Rect(
            self.dpad_center[0] - dpad_button_size // 2,
            self.dpad_center[1] - dpad_button_size * 3 // 2,
            dpad_button_size,
            dpad_button_size
        )
        
        # Down button
        self.dpad_down = pygame.Rect(
            self.dpad_center[0] - dpad_button_size // 2,
            self.dpad_center[1] + dpad_button_size // 2,
            dpad_button_size,
            dpad_button_size
        )
        
        # Action buttons position (bottom right)
        button_margin = 40
        button_spacing = self.button_size // 4
        
        # Create a triangular button layout
        # Jump button (top)
        self.jump_rect = pygame.Rect(
            screen_width - (1.5 * self.button_size) - button_margin,
            screen_height - (2.5 * self.button_size) - button_margin,
            self.button_size,
            self.button_size
        )
        
        # Punch button (bottom left)
        self.punch_rect = pygame.Rect(
            screen_width - (2 * self.button_size) - button_margin - button_spacing,
            screen_height - self.button_size - button_margin,
            self.button_size,
            self.button_size
        )
        
        # Kick button (bottom right)
        self.kick_rect = pygame.Rect(
            screen_width - self.button_size - button_margin + button_spacing,
            screen_height - self.button_size - button_margin,
            self.button_size,
            self.button_size
        )
        
        # Colors
        self.colors = {
            'dpad': (80, 80, 80),
            'dpad_pressed': (120, 120, 120),
            'dpad_arrows': (200, 200, 200),
            'punch': (200, 50, 50),
            'punch_pressed': (255, 100, 100),
            'kick': (50, 50, 200),
            'kick_pressed': (100, 100, 255),
            'jump': (50, 200, 50),
            'jump_pressed': (100, 255, 100)
        }
        
        # Touch state
        self.touch_state = {
            'move': 0,  # -1 for left, 0 for none, 1 for right
            'up': False,
            'down': False,
            'punch': False,
            'kick': False,
            'jump': False
        }
        
        # Store active touches
        self.active_touches = {}
        
    def handle_touch(self, event):
        """Handle touch events and return the current touch state"""
        if event.type == pygame.FINGERDOWN:
            x = event.x * self.screen_width
            y = event.y * self.screen_height
            touch_pos = (x, y)
            self.active_touches[event.finger_id] = touch_pos
            self._update_touch_state(touch_pos, True)
            
        elif event.type == pygame.FINGERUP:
            if event.finger_id in self.active_touches:
                touch_pos = self.active_touches[event.finger_id]
                self._update_touch_state(touch_pos, False)
                del self.active_touches[event.finger_id]
                
        elif event.type == pygame.FINGERMOTION:
            x = event.x * self.screen_width
            y = event.y * self.screen_height
            touch_pos = (x, y)
            self.active_touches[event.finger_id] = touch_pos
            self._reset_touch_state()
            for pos in self.active_touches.values():
                self._update_touch_state(pos, True)
        
        return self.touch_state
    
    def _update_touch_state(self, pos, is_pressed):
        """Update touch state based on touch position"""
        x, y = pos
        
        # D-pad movement
        if self.dpad_left.collidepoint(x, y):
            self.touch_state['move'] = -1 if is_pressed else 0
        elif self.dpad_right.collidepoint(x, y):
            self.touch_state['move'] = 1 if is_pressed else 0
        elif self.dpad_up.collidepoint(x, y):
            self.touch_state['up'] = is_pressed
        elif self.dpad_down.collidepoint(x, y):
            self.touch_state['down'] = is_pressed
        
        # Action buttons
        if self.punch_rect.collidepoint(x, y):
            self.touch_state['punch'] = is_pressed
        elif self.kick_rect.collidepoint(x, y):
            self.touch_state['kick'] = is_pressed
        elif self.jump_rect.collidepoint(x, y):
            self.touch_state['jump'] = is_pressed
    
    def _reset_touch_state(self):
        """Reset all touch states to default"""
        self.touch_state = {
            'move': 0,
            'up': False,
            'down': False,
            'punch': False,
            'kick': False,
            'jump': False
        }
    
    def draw(self, screen):
        """Draw the touch controls"""
        # Draw D-pad base
        pygame.draw.rect(screen, self.colors['dpad'], self.dpad_center_rect)
        
        # Draw D-pad directional buttons
        for dpad_button, is_pressed in [
            (self.dpad_left, self.touch_state['move'] == -1),
            (self.dpad_right, self.touch_state['move'] == 1),
            (self.dpad_up, self.touch_state['up']),
            (self.dpad_down, self.touch_state['down'])
        ]:
            color = self.colors['dpad_pressed'] if is_pressed else self.colors['dpad']
            pygame.draw.rect(screen, color, dpad_button)
        
        # Draw D-pad arrows
        arrow_color = self.colors['dpad_arrows']
        arrow_size = self.dpad_size // 8
        
        # Left arrow
        pygame.draw.polygon(screen, arrow_color, [
            (self.dpad_left.centerx + arrow_size, self.dpad_left.centery),
            (self.dpad_left.centerx - arrow_size, self.dpad_left.centery),
            (self.dpad_left.centerx, self.dpad_left.centery - arrow_size),
            (self.dpad_left.centerx, self.dpad_left.centery + arrow_size)
        ])
        
        # Right arrow
        pygame.draw.polygon(screen, arrow_color, [
            (self.dpad_right.centerx - arrow_size, self.dpad_right.centery),
            (self.dpad_right.centerx + arrow_size, self.dpad_right.centery),
            (self.dpad_right.centerx, self.dpad_right.centery - arrow_size),
            (self.dpad_right.centerx, self.dpad_right.centery + arrow_size)
        ])
        
        # Up arrow
        pygame.draw.polygon(screen, arrow_color, [
            (self.dpad_up.centerx, self.dpad_up.centery + arrow_size),
            (self.dpad_up.centerx, self.dpad_up.centery - arrow_size),
            (self.dpad_up.centerx - arrow_size, self.dpad_up.centery),
            (self.dpad_up.centerx + arrow_size, self.dpad_up.centery)
        ])
        
        # Down arrow
        pygame.draw.polygon(screen, arrow_color, [
            (self.dpad_down.centerx, self.dpad_down.centery - arrow_size),
            (self.dpad_down.centerx, self.dpad_down.centery + arrow_size),
            (self.dpad_down.centerx - arrow_size, self.dpad_down.centery),
            (self.dpad_down.centerx + arrow_size, self.dpad_down.centery)
        ])
        
        # Draw action buttons with a more 3D look
        for button, color, pressed, label in [
            (self.punch_rect, self.colors['punch'], self.touch_state['punch'], 'PUNCH'),
            (self.kick_rect, self.colors['kick'], self.touch_state['kick'], 'KICK'),
            (self.jump_rect, self.colors['jump'], self.touch_state['jump'], 'JUMP')
        ]:
            # Draw button shadow
            shadow_offset = 0 if pressed else 4
            shadow_rect = button.copy()
            shadow_rect.y += shadow_offset
            pygame.draw.rect(screen, (30, 30, 30), shadow_rect)
            
            # Draw button face
            button_rect = button.copy()
            button_rect.y -= 4 if not pressed else 0
            pygame.draw.rect(screen, color, button_rect)
            
            # Draw button label
            font = pygame.font.Font(None, 36)
            text = font.render(label, True, (255, 255, 255))
            screen.blit(text, (button_rect.centerx - text.get_width()//2,
                             button_rect.centery - text.get_height()//2)) 