import pygame
import os

class MapManager:
    def __init__(self, width, height, stage_id):
        self.width = width
        self.height = height
        self.stage_id = stage_id
        
        # Load background image based on stage
        try:
            if self.stage_id == 'niall':  # Stage 3 has a specific background
                bg_path = os.path.join("fighting_game", "assets", "images", "stage", "fight_niall.png")
                if not os.path.exists(bg_path):
                    bg_path = os.path.join("assets", "images", "stage", "fight_niall.png")
                if os.path.exists(bg_path):
                    print(f"Loading Niall's stage background from: {bg_path}")
                    self.background = pygame.image.load(bg_path)
                    self.background = pygame.transform.scale(self.background, (width, height))
                else:
                    raise FileNotFoundError("Niall's stage background not found")
            else:  # Other stages use default background
                print("Creating default background")
                self.background = pygame.Surface((width, height))
                
                # Fill with a gradient sky
                for y in range(height):
                    # Create a gradient from light blue to darker blue
                    color = (
                        max(100, 135 - int(y * 0.2)),  # Red
                        max(100, 206 - int(y * 0.2)),  # Green
                        max(100, 235 - int(y * 0.2))   # Blue
                    )
                    pygame.draw.line(self.background, color, (0, y), (width, y))
                
                # Add some simple clouds
                cloud_color = (255, 255, 255)
                cloud_positions = [(100, 50), (300, 100), (500, 75), (700, 150)]
                for x, y in cloud_positions:
                    pygame.draw.ellipse(self.background, cloud_color, (x, y, 80, 40))
                    pygame.draw.ellipse(self.background, cloud_color, (x+20, y-10, 60, 40))
                    pygame.draw.ellipse(self.background, cloud_color, (x+40, y+5, 50, 30))
                
                # Add a simple sun
                pygame.draw.circle(self.background, (255, 255, 150), (50, 50), 30)
                
                # Add some mountains in the background
                mountain_color = (100, 100, 100)
                mountain_positions = [(200, 400), (400, 350), (600, 380)]
                for x, y in mountain_positions:
                    points = [(x, height), (x + 100, y), (x + 200, height)]
                    pygame.draw.polygon(self.background, mountain_color, points)
                
        except Exception as e:
            print(f"Error loading background: {e}")
            print("Using black background.")
            self.background = pygame.Surface((width, height))
            self.background.fill((0, 0, 0))
        
        # Initialize obstacles
        self.obstacles = []
        self.init_obstacles()
        
    def init_obstacles(self):
        """Initialize stage obstacles"""
        # Add some platforms/obstacles
        platform_height = 40  # Platform height for better visibility
        
        # Ground platform (always present)
        self.obstacles.append(pygame.Rect(0, self.height - platform_height, self.width, platform_height))
        
        # No additional platforms - just the ground for better character movement
            
    def draw(self, screen):
        # Draw background (scaled to fit screen)
        scaled_bg = pygame.transform.scale(self.background, (self.width, self.height))
        screen.blit(scaled_bg, (0, 0))
        
        # Draw ground platform
        ground = self.obstacles[0]
        pygame.draw.rect(screen, (100, 100, 100), ground)  # Gray platform
        # Add ground edge highlight
        pygame.draw.line(screen, (150, 150, 150), ground.topleft, ground.topright, 4)  # Thicker line for better visibility
            
    def check_collision(self, rect):
        """Check if a rectangle collides with any obstacles"""
        return any(obstacle.colliderect(rect) for obstacle in self.obstacles)
        
    def get_ground_height(self, x):
        """Get the height of the ground/platform at a given x coordinate"""
        return self.height - 40  # Match platform height 