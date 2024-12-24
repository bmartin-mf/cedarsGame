import pygame
from .sprite_manager import SpriteManager

class Character:
    def __init__(self, x, y, char_id=0, facing_right=True):
        # Initialize sprite manager first to get dimensions
        self.sprite_manager = SpriteManager(char_id)
        
        self.x = x
        self.y = y
        # Adjust width for Bren's character
        if isinstance(char_id, str) and char_id == 'bren':
            self.width = int(self.sprite_manager.WIDTH * 1.5)  # 50% wider for Bren
        else:
            self.width = self.sprite_manager.WIDTH
        self.height = self.sprite_manager.HEIGHT
        self.vel_x = 0
        self.vel_y = 0
        self.health = 200
        self.facing_right = facing_right
        self.state = 'idle'
        self.is_jumping = False
        self.is_attacking = False
        self.is_throwing = False
        self.attack_cooldown = 0
        self.throw_cooldown = 0
        self.frame_counter = 0
        self.char_id = char_id
        self.damage_multiplier = 1.0
        self.speed = 1.0  # Base speed multiplier
        self.thrown_items = []  # List to track thrown items
        
        # Movement constants (adjusted for better control)
        self.BASE_MOVE_SPEED = 3  # Reduced base speed for better control
        self.JUMP_SPEED = -12  # Reduced jump velocity
        self.GRAVITY = 0.4  # Reduced gravity
        
        # Get screen info for fullscreen
        screen_info = pygame.display.Info()
        self.SCREEN_WIDTH = screen_info.current_w
        self.SCREEN_HEIGHT = screen_info.current_h
        self.GROUND_Y = self.SCREEN_HEIGHT - 150  # Ground position adjusted for screen height
        
        # Collision buffer
        self.collision_buffer = 5  # Small buffer for smoother collision response
        
        # Projectile constants
        self.THROW_SPEED = 8  # Reduced throw speed
        self.THROW_COOLDOWN = 45
        
        # Collision rectangles
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.attack_rect = None
        
    def move(self, dx):
        """Move the character horizontally"""
        # Direct movement without momentum
        if dx != 0:
            self.vel_x = dx * self.BASE_MOVE_SPEED * self.speed
            self.facing_right = dx > 0
            self.state = 'walk'
        else:
            # Immediately stop when no input
            self.vel_x = 0
            if not self.is_attacking and not self.is_jumping and not self.is_throwing:
                self.state = 'idle'
            
    def jump(self):
        # Only allow jumping when on the ground
        if not self.is_jumping and self.y >= self.GROUND_Y:
            self.vel_y = self.JUMP_SPEED
            self.is_jumping = True
            self.state = 'jump'
            
    def attack(self, attack_type='punch'):
        if not self.is_attacking and self.attack_cooldown <= 0:
            self.is_attacking = True
            self.state = attack_type
            self.attack_cooldown = 20  # 20 frames cooldown
            
            # Create attack hitbox with adjusted width for Bren
            attack_width = 60 if isinstance(self.char_id, str) and self.char_id == 'bren' else 40
            if self.facing_right:
                self.attack_rect = pygame.Rect(self.rect.right, self.rect.centery - 10, attack_width, 20)
            else:
                self.attack_rect = pygame.Rect(self.rect.left - attack_width, self.rect.centery - 10, attack_width, 20)
                
    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        
    def throw_item(self):
        if not self.is_throwing and self.throw_cooldown <= 0:
            self.is_throwing = True
            self.state = 'throw'
            self.throw_cooldown = self.THROW_COOLDOWN
            
            # Create thrown item
            item_x = self.rect.right if self.facing_right else self.rect.left
            item_speed = self.THROW_SPEED if self.facing_right else -self.THROW_SPEED
            thrown_item = {
                'rect': pygame.Rect(item_x, self.rect.centery, 15, 15),
                'vel_x': item_speed,
                'active': True
            }
            self.thrown_items.append(thrown_item)
            
    def update(self, map_manager=None):
        # Update frame counter for animations
        self.frame_counter += 1
        
        # Apply gravity
        self.vel_y += self.GRAVITY
        
        # Store previous position for collision resolution
        prev_x = self.x
        prev_y = self.y
        
        # Update position with collision buffer
        new_x = self.x + self.vel_x
        new_y = self.y + self.vel_y
        
        # Screen boundary checks with buffer
        if new_x < self.collision_buffer:
            new_x = self.collision_buffer
            self.vel_x = 0
        elif new_x > self.SCREEN_WIDTH - self.width - self.collision_buffer:
            new_x = self.SCREEN_WIDTH - self.width - self.collision_buffer
            self.vel_x = 0
            
        # Update position
        self.x = new_x
        self.y = new_y
        
        # Update rectangle position
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Update thrown items
        for item in self.thrown_items[:]:
            if item['active']:
                item['rect'].x += item['vel_x']
                if item['rect'].right < 0 or item['rect'].left > self.SCREEN_WIDTH:
                    self.thrown_items.remove(item)
        
        # Handle map collisions if map manager is provided
        if map_manager:
            if map_manager.check_collision(self.rect):
                # Get the ground height at current x position
                ground_y = map_manager.get_ground_height(self.rect.centerx)
                
                # If we're falling onto a platform
                if self.vel_y > 0 and self.rect.bottom > ground_y:
                    # Gentle landing
                    self.y = ground_y - self.rect.height
                    self.vel_y = 0
                    self.is_jumping = False
                    if not self.is_attacking and not self.is_throwing:
                        self.state = 'idle' if self.vel_x == 0 else 'walk'
                # If we hit a wall, stop immediately
                elif self.vel_x != 0:
                    self.x = prev_x
                    self.vel_x = 0
                
                self.rect.x = self.x
                self.rect.y = self.y
        
        # Ground collision (if not on platform)
        if self.y > self.GROUND_Y:
            self.y = self.GROUND_Y
            self.vel_y = 0
            self.is_jumping = False
            if not self.is_attacking and not self.is_throwing:
                self.state = 'idle' if abs(self.vel_x) < 0.1 else 'walk'
            
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1
            
        # Reset attack/throw states after animation
        if self.is_attacking:
            if self.attack_cooldown <= 15:  # Attack animation finished
                self.is_attacking = False
                self.attack_rect = None
                if not self.is_jumping:
                    self.state = 'idle'
        if self.is_throwing:
            if self.throw_cooldown <= 40:  # Throw animation finished
                self.is_throwing = False
                if not self.is_jumping:
                    self.state = 'idle'
            
    def draw(self, screen):
        # Get current animation frame
        current_frame = self.sprite_manager.get_animation_frame(
            self.state, 
            self.facing_right,
            self.frame_counter
        )
        
        # Draw the character
        screen.blit(current_frame, (self.x, self.y))
        
        # Draw attack hitbox for debugging
        if self.attack_rect:
            pygame.draw.rect(screen, (255, 255, 0), self.attack_rect, 1)
            
        # Draw thrown items
        for item in self.thrown_items:
            if item['active']:
                pygame.draw.rect(screen, (255, 100, 0), item['rect'])  # Orange projectile
            
        # Draw health bar
        health_width = 50 * (self.health / 200)
        health_rect = pygame.Rect(self.rect.x, self.rect.y - 20, health_width, 5)
        pygame.draw.rect(screen, (0, 255, 0), health_rect) 