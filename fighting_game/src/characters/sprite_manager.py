import pygame
import math
import os

class SpriteManager:
    def __init__(self, char_id=0):
        self.animation_speed = 0.2
        self.frame_counter = 0
        self.char_id = char_id
        
        # Character dimensions (1.5x scale)
        self.WIDTH = 112   # 1.5x of 75
        self.HEIGHT = 225  # 1.5x of 150
        self.FACE_SIZE = 45  # 1.5x of 30
        self.TORSO_WIDTH = 45  # 1.5x of 30
        self.TORSO_HEIGHT = 90  # 1.5x of 60
        self.LINE_THICKNESS = 9  # 1.5x of 6
        
        # Try to load full character sprite first
        self.full_character = self.load_full_character()
        
        # Only load these if we don't have a full character sprite
        if not self.full_character:
            self.face_image = self.load_face_image()
            self.win_image = self.load_special_asset('win')
            self.loss_image = self.load_special_asset('lose')
            self.prize_image = self.load_special_asset('prize')
        
        # Create and store sprites once during initialization
        self.sprites = self.create_character_sprites()
        
    def load_full_character(self):
        """Try to load a full character sprite sheet"""
        # Handle stage-specific characters
        char_path = None
        
        if isinstance(self.char_id, str):
            if self.char_id == 'bren':
                char_path = os.path.join("fighting_game", "assets", "images", "faces", "bren_char.png")
                # Adjust width for Bren
                self.WIDTH = int(self.WIDTH * 1.5)  # 50% wider
            elif self.char_id == 'lee':
                char_path = os.path.join("fighting_game", "assets", "images", "faces", "lee_char.png")
            elif self.char_id == 'billy':
                char_path = os.path.join("fighting_game", "assets", "images", "faces", "billy_char.png")
            elif self.char_id == 'niall':
                char_path = os.path.join("fighting_game", "assets", "images", "faces", "niall_char.png")
            elif self.char_id == 'ciaran':
                char_path = os.path.join("fighting_game", "assets", "images", "faces", "final_boss.png")
                
        if char_path:
            # Try without fighting_game prefix if not found
            if not os.path.exists(char_path):
                char_path = char_path.replace("fighting_game/", "")
                
            try:
                if os.path.exists(char_path):
                    print(f"Loading character sprite from: {char_path}")
                    char_surface = pygame.image.load(char_path)
                    # Scale to match our character size
                    base_sprite = pygame.transform.scale(char_surface, (self.WIDTH, self.HEIGHT))
                    
                    # Create animation frames by modifying the base sprite
                    sprites = {}
                    
                    # Idle animation - just use base sprite
                    sprites['idle'] = [base_sprite]
                    
                    # Walk animation - create slight bobbing effect
                    walk_frames = []
                    for i in range(4):
                        frame = base_sprite.copy()
                        offset = int(math.sin(i * math.pi / 2) * 4)  # Small vertical offset
                        frame_surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
                        frame_surface.blit(frame, (0, offset))
                        walk_frames.append(frame_surface)
                    sprites['walk'] = walk_frames
                    
                    # Punch animation - create arm extension effect
                    punch_frames = []
                    for i in range(3):
                        frame = base_sprite.copy()
                        if i == 1:  # Extended punch frame
                            # Draw punch effect
                            punch_width = int(60 if self.char_id == 'bren' else 40)  # Wider punch for Bren
                            pygame.draw.line(frame, (255, 255, 0), 
                                          (self.WIDTH - 20, self.HEIGHT // 2),
                                          (self.WIDTH + punch_width - 30, self.HEIGHT // 2), 8)
                        punch_frames.append(frame)
                    sprites['punch'] = punch_frames
                    
                    # Kick animation - create leg extension effect
                    kick_frames = []
                    for i in range(3):
                        frame = base_sprite.copy()
                        if i == 1:  # Extended kick frame
                            # Draw kick effect
                            kick_width = int(60 if self.char_id == 'bren' else 40)  # Wider kick for Bren
                            pygame.draw.line(frame, (255, 255, 0),
                                          (self.WIDTH - 20, self.HEIGHT * 0.7),
                                          (self.WIDTH + kick_width - 30, self.HEIGHT * 0.7), 8)
                        kick_frames.append(frame)
                    sprites['kick'] = kick_frames
                    
                    # Jump animation - just use base sprite with slight squash
                    jump_frame = base_sprite.copy()
                    jump_frame = pygame.transform.scale(jump_frame, 
                                                     (self.WIDTH, int(self.HEIGHT * 0.9)))
                    sprites['jump'] = [jump_frame]
                    
                    # Crouch animation - squash the sprite
                    crouch_frame = pygame.transform.scale(base_sprite,
                                                        (self.WIDTH, int(self.HEIGHT * 0.8)))
                    sprites['crouch'] = [crouch_frame]
                    
                    # Throw animation - similar to punch but with projectile effect
                    throw_frames = []
                    for i in range(3):
                        frame = base_sprite.copy()
                        if i == 1:  # Throwing frame
                            # Draw throw effect
                            pygame.draw.circle(frame, (255, 100, 0),
                                            (self.WIDTH - 10, self.HEIGHT // 2), 8)
                        throw_frames.append(frame)
                    sprites['throw'] = throw_frames
                    
                    # Win/Loss animations - modify base sprite
                    win_frame = base_sprite.copy()
                    pygame.draw.line(win_frame, (255, 255, 0),
                                   (self.WIDTH // 2, 10),
                                   (self.WIDTH // 2, 30), 4)  # Victory effect
                    sprites['win'] = [win_frame]
                    
                    loss_frame = pygame.transform.scale(base_sprite,
                                                      (self.WIDTH, int(self.HEIGHT * 0.9)))
                    sprites['loss'] = [loss_frame]
                    
                    return sprites
            except Exception as e:
                print(f"Error loading character sprite: {e}")
        return None
        
    def load_face_image(self):
        """Load custom face image or create a default one"""
        # Try to load custom face image
        face_path = os.path.join('assets', 'images', 'faces', f'fight_{self.char_id}.png')
        try:
            if os.path.exists(face_path):
                face_surface = pygame.image.load(face_path)
                # Scale to expected size if needed
                if face_surface.get_size() != (self.FACE_SIZE, self.FACE_SIZE):
                    face_surface = pygame.transform.scale(face_surface, (self.FACE_SIZE, self.FACE_SIZE))
                return face_surface
        except:
            pass  # Fall back to default face if loading fails
            
        return self.create_default_face()
        
    def create_default_face(self):
        """Create a default face if no image is found"""
        surface = pygame.Surface((self.FACE_SIZE, self.FACE_SIZE), pygame.SRCALPHA)
        center = self.FACE_SIZE // 2
        radius = center
        
        # Default face design
        if self.char_id == 0:  # Fighter 1
            # Simple smiling face
            pygame.draw.circle(surface, (255, 255, 255), (center, center), radius)  # Head outline
            pygame.draw.circle(surface, (0, 0, 0), (center-5, center-5), 3)   # Left eye
            pygame.draw.circle(surface, (0, 0, 0), (center+5, center-5), 3)  # Right eye
            pygame.draw.arc(surface, (0, 0, 0), (center-8, center-8, 16, 16), 0, math.pi, 3)  # Smile
        else:  # Fighter 2
            # Simple serious face
            pygame.draw.circle(surface, (255, 255, 255), (center, center), radius)  # Head outline
            pygame.draw.line(surface, (0, 0, 0), (center-8, center-5), (center-2, center-5), 3)   # Left eyebrow
            pygame.draw.line(surface, (0, 0, 0), (center+2, center-5), (center+8, center-5), 3)   # Right eyebrow
            pygame.draw.circle(surface, (0, 0, 0), (center-5, center), 3)   # Left eye
            pygame.draw.circle(surface, (0, 0, 0), (center+5, center), 3)  # Right eye
            pygame.draw.line(surface, (0, 0, 0), (center-5, center+5), (center+5, center+5), 3)  # Straight mouth
            
        return surface
        
    def load_special_asset(self, asset_type):
        """Load special assets (win, lose, prize) from their respective folders"""
        # Special case for main character loss image
        if asset_type == 'lose' and (self.char_id == 0 or self.char_id == 'player'):
            loss_path = os.path.join("fighting_game", "assets", "images", "lose", "mc_lose.png")
            if not os.path.exists(loss_path):
                # Try without fighting_game prefix
                loss_path = os.path.join("assets", "images", "lose", "mc_lose.png")
            if os.path.exists(loss_path):
                print(f"Loading main character loss image from: {loss_path}")
                try:
                    loss_surface = pygame.image.load(loss_path)
                    # Scale to match character size
                    if loss_surface.get_size() != (self.WIDTH, self.HEIGHT):
                        loss_surface = pygame.transform.scale(loss_surface, (self.WIDTH, self.HEIGHT))
                    return loss_surface
                except Exception as e:
                    print(f"Error loading main character loss image: {e}")
        
        # Regular asset loading for other cases
        asset_path = os.path.join("fighting_game", "assets", "images", asset_type, f"fight_{self.char_id}.png")
        if not os.path.exists(asset_path):
            # Try without fighting_game prefix
            asset_path = os.path.join("assets", "images", asset_type, f"fight_{self.char_id}.png")
            
        try:
            if os.path.exists(asset_path):
                print(f"Loading {asset_type} image from: {asset_path}")
                asset_surface = pygame.image.load(asset_path)
                # Scale based on asset type
                if asset_type == 'prize':
                    # Prize items should be small (20x20)
                    if asset_surface.get_size() != (20, 20):
                        asset_surface = pygame.transform.scale(asset_surface, (20, 20))
                else:
                    # Win/Loss images should match character size
                    if asset_surface.get_size() != (self.WIDTH, self.HEIGHT):
                        asset_surface = pygame.transform.scale(asset_surface, (self.WIDTH, self.HEIGHT))
                return asset_surface
        except Exception as e:
            print(f"Error loading {asset_type} image: {e}")
            
        # Return appropriate default based on asset type
        if asset_type == 'prize':
            return self.create_default_prize()
        elif asset_type == 'win':
            return self.create_victory_pose()
        elif asset_type == 'lose':
            return self.create_defeat_pose()
        return self.create_default_sprite()
        
    def create_default_prize(self):
        """Create a default prize projectile"""
        surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 100, 0), (10, 10), 10)  # Orange projectile
        return surface
        
    def create_character_sprites(self):
        """Create basic character sprites with visible limbs"""
        sprites = {
            'idle': [],
            'walk': [],
            'punch': [],
            'kick': [],
            'jump': [],
            'crouch': [],
            'throw': [],  # Add throw animation
            'win': [],    # Add win animation
            'loss': []    # Add loss animation
        }
        
        # If we have a full character sprite, use it for all states
        full_sprites = self.load_full_character()
        if full_sprites:
            return full_sprites  # Return the pre-made animation frames
            
        # Otherwise, create default animated sprites
        # Create throw animation frames
        for i in range(3):  # 3-frame throw animation
            surface = pygame.Surface((50, 100), pygame.SRCALPHA)
            # Body
            pygame.draw.rect(surface, (255, 255, 255), (15, 20, 20, 40))  # Torso
            surface.blit(self.face_image, (15, 5))  # Position face image
            
            # Arms (throwing animation)
            if i == 0:  # Wind up
                pygame.draw.line(surface, (255, 255, 255), (35, 25), (45, 35), 4)  # Right arm back
            elif i == 1:  # Throw
                pygame.draw.line(surface, (255, 255, 255), (35, 25), (55, 35), 4)  # Right arm extended
                if self.prize_image:
                    surface.blit(self.prize_image, (55, 30))  # Show projectile
            else:  # Return
                pygame.draw.line(surface, (255, 255, 255), (35, 25), (45, 45), 4)  # Right arm down
                
            pygame.draw.line(surface, (255, 255, 255), (15, 25), (5, 45), 4)  # Left arm
            pygame.draw.line(surface, (255, 255, 255), (20, 60), (15, 90), 4)  # Left leg
            pygame.draw.line(surface, (255, 255, 255), (30, 60), (35, 90), 4)  # Right leg
            
            sprites['throw'].append(surface)
            
        # Add win animation (use custom win image if available)
        if self.win_image:
            sprites['win'].append(self.win_image)
        else:
            victory_pose = self.create_victory_pose()
            sprites['win'].append(victory_pose)
            
        # Add loss animation (use custom loss image if available)
        if self.loss_image:
            sprites['loss'].append(self.loss_image)
        else:
            defeat_pose = self.create_defeat_pose()
            sprites['loss'].append(defeat_pose)
            
        # Create idle animation frames
        for i in range(2):  # Simple 2-frame idle animation
            surface = pygame.Surface((50, 100), pygame.SRCALPHA)
            # Body
            pygame.draw.rect(surface, (255, 255, 255), (15, 20, 20, 40))  # Torso
            
            # Draw face instead of simple circle
            surface.blit(self.face_image, (15, 5))  # Position face image
            
            # Arms (slightly different positions for idle animation)
            arm_offset = i * 2  # Small movement for idle animation
            pygame.draw.line(surface, (255, 255, 255), (15, 25), (5, 45 + arm_offset), 4)  # Left arm
            pygame.draw.line(surface, (255, 255, 255), (35, 25), (45, 45 + arm_offset), 4)  # Right arm
            
            # Legs
            pygame.draw.line(surface, (255, 255, 255), (20, 60), (15, 90), 4)  # Left leg
            pygame.draw.line(surface, (255, 255, 255), (30, 60), (35, 90), 4)  # Right leg
            
            sprites['idle'].append(surface)
        
        # Create punch animation frames
        for i in range(3):  # 3-frame punch animation
            surface = pygame.Surface((50, 100), pygame.SRCALPHA)
            # Body
            pygame.draw.rect(surface, (255, 255, 255), (15, 20, 20, 40))  # Torso
            surface.blit(self.face_image, (15, 5))  # Position face image
            
            # Arms (punching animation)
            if i == 0:  # Wind up
                pygame.draw.line(surface, (255, 255, 255), (35, 25), (45, 35), 4)  # Right arm back
            elif i == 1:  # Punch out
                pygame.draw.line(surface, (255, 255, 255), (35, 25), (65, 25), 4)  # Right arm extended
            else:  # Return
                pygame.draw.line(surface, (255, 255, 255), (35, 25), (45, 45), 4)  # Right arm down
                
            pygame.draw.line(surface, (255, 255, 255), (15, 25), (5, 45), 4)  # Left arm
            
            # Legs
            pygame.draw.line(surface, (255, 255, 255), (20, 60), (15, 90), 4)  # Left leg
            pygame.draw.line(surface, (255, 255, 255), (30, 60), (35, 90), 4)  # Right leg
            
            sprites['punch'].append(surface)
            
        # Create kick animation frames
        for i in range(3):  # 3-frame kick animation
            surface = pygame.Surface((50, 100), pygame.SRCALPHA)
            # Body
            pygame.draw.rect(surface, (255, 255, 255), (15, 20, 20, 40))  # Torso
            surface.blit(self.face_image, (15, 5))  # Position face image
            
            # Arms
            pygame.draw.line(surface, (255, 255, 255), (15, 25), (5, 45), 4)  # Left arm
            pygame.draw.line(surface, (255, 255, 255), (35, 25), (45, 45), 4)  # Right arm
            
            # Legs (kicking animation)
            pygame.draw.line(surface, (255, 255, 255), (20, 60), (15, 90), 4)  # Left leg
            if i == 0:  # Wind up
                pygame.draw.line(surface, (255, 255, 255), (30, 60), (35, 75), 4)  # Right leg back
                pygame.draw.circle(surface, (255, 200, 0), (35, 75), 4)  # Wind up effect
            elif i == 1:  # Kick out
                pygame.draw.line(surface, (255, 255, 255), (30, 60), (75, 60), 6)  # Right leg extended, thicker
                pygame.draw.circle(surface, (255, 100, 0), (75, 60), 8)  # Kick impact effect
            else:  # Return
                pygame.draw.line(surface, (255, 255, 255), (30, 60), (35, 90), 4)  # Right leg down
                
            sprites['kick'].append(surface)
            
        # Create walk animation frames
        for i in range(4):  # 4-frame walk animation
            surface = pygame.Surface((50, 100), pygame.SRCALPHA)
            # Body
            pygame.draw.rect(surface, (255, 255, 255), (15, 20, 20, 40))  # Torso
            surface.blit(self.face_image, (15, 5))  # Position face image
            
            # Arms (alternating swing)
            arm_offset = 10 * math.sin(i * math.pi / 2)
            pygame.draw.line(surface, (255, 255, 255), (15, 25), (5, 45 + arm_offset), 4)
            pygame.draw.line(surface, (255, 255, 255), (35, 25), (45, 45 - arm_offset), 4)
            
            # Legs (alternating swing)
            leg_offset = 10 * math.sin(i * math.pi / 2)
            pygame.draw.line(surface, (255, 255, 255), (20, 60), (15, 90 + leg_offset), 4)
            pygame.draw.line(surface, (255, 255, 255), (30, 60), (35, 90 - leg_offset), 4)
            
            sprites['walk'].append(surface)
            
        # Create jump frame
        surface = pygame.Surface((50, 100), pygame.SRCALPHA)
        # Body
        pygame.draw.rect(surface, (255, 255, 255), (15, 20, 20, 40))  # Torso
        surface.blit(self.face_image, (15, 5))  # Position face image
        
        # Arms up
        pygame.draw.line(surface, (255, 255, 255), (15, 25), (5, 15), 4)
        pygame.draw.line(surface, (255, 255, 255), (35, 25), (45, 15), 4)
        
        # Legs bent
        pygame.draw.line(surface, (255, 255, 255), (20, 60), (15, 75), 4)
        pygame.draw.line(surface, (255, 255, 255), (30, 60), (35, 75), 4)
        
        sprites['jump'].append(surface)
        
        # Create crouch frame
        surface = pygame.Surface((50, 100), pygame.SRCALPHA)
        # Crouched body
        pygame.draw.rect(surface, (255, 255, 255), (15, 40, 20, 30))  # Shorter torso
        surface.blit(self.face_image, (15, 25))  # Position face image lower for crouch
        
        # Crouched arms
        pygame.draw.line(surface, (255, 255, 255), (15, 45), (5, 55), 4)
        pygame.draw.line(surface, (255, 255, 255), (35, 45), (45, 55), 4)
        
        # Crouched legs
        pygame.draw.line(surface, (255, 255, 255), (20, 70), (15, 90), 4)
        pygame.draw.line(surface, (255, 255, 255), (30, 70), (35, 90), 4)
        
        sprites['crouch'].append(surface)
        
        return sprites
        
    def create_victory_pose(self):
        """Create default victory pose"""
        surface = pygame.Surface((50, 100), pygame.SRCALPHA)
        # Triumphant pose
        pygame.draw.rect(surface, (255, 255, 255), (15, 20, 20, 40))  # Torso
        surface.blit(self.face_image, (15, 5))  # Face
        # Arms raised in victory
        pygame.draw.line(surface, (255, 255, 255), (15, 25), (5, 15), 4)
        pygame.draw.line(surface, (255, 255, 255), (35, 25), (45, 15), 4)
        # Legs in stable stance
        pygame.draw.line(surface, (255, 255, 255), (20, 60), (15, 90), 4)
        pygame.draw.line(surface, (255, 255, 255), (30, 60), (35, 90), 4)
        return surface
        
    def create_defeat_pose(self):
        """Create default defeat pose"""
        surface = pygame.Surface((50, 100), pygame.SRCALPHA)
        # Slumped pose
        pygame.draw.rect(surface, (255, 255, 255), (15, 30, 20, 30))  # Shorter torso
        surface.blit(self.face_image, (15, 15))  # Face
        # Arms hanging down
        pygame.draw.line(surface, (255, 255, 255), (15, 35), (10, 55), 4)
        pygame.draw.line(surface, (255, 255, 255), (35, 35), (40, 55), 4)
        # Legs bent
        pygame.draw.line(surface, (255, 255, 255), (20, 60), (15, 85), 4)
        pygame.draw.line(surface, (255, 255, 255), (30, 60), (35, 85), 4)
        return surface
        
    def get_animation_frame(self, state, facing_right, frame_counter):
        """Get the current animation frame for the given state"""
        if state not in self.sprites:
            state = 'idle'
            
        animation = self.sprites[state]
        frame_index = int(frame_counter * self.animation_speed) % len(animation)
        frame = animation[frame_index]
        
        # Create a copy of the frame before flipping
        frame = frame.copy()
        
        # Flip the sprite if facing left
        if not facing_right:
            frame = pygame.transform.flip(frame, True, False)
            
        return frame 