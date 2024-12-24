import pygame
import sys
from states.game_state import GameState
from states.menu_state import MenuState
from ui.touch_controls import TouchControls

class Game:
    def __init__(self):
        pygame.init()
        
        # Get the current display info
        info = pygame.display.Info()
        self.SCREEN_WIDTH = info.current_w
        self.SCREEN_HEIGHT = info.current_h
        
        # Set up fullscreen display with scaling
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            pygame.FULLSCREEN | pygame.SCALED
        )
        
        # Calculate scaling factors
        self.scale_x = self.SCREEN_WIDTH / 1500  # Original width
        self.scale_y = self.SCREEN_HEIGHT / 750  # Original height
        
        # Initialize touch controls
        self.touch_controls = TouchControls(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        pygame.display.set_caption("2D Fighter")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = MenuState()
        print(f"Game initialized in fullscreen mode: {self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Allow escape to exit fullscreen
                    self.running = False
            
            # Handle touch events
            elif event.type in (pygame.FINGERDOWN, pygame.FINGERUP, pygame.FINGERMOTION):
                touch_state = self.touch_controls.handle_touch(event)
                # Convert touch states to keyboard events
                events = []
                
                # For FINGERDOWN events, also send a generic KEYDOWN event for round transitions
                if event.type == pygame.FINGERDOWN:
                    events.append(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}))
                
                # Movement
                if touch_state['move'] != 0:
                    key = pygame.K_RIGHT if touch_state['move'] > 0 else pygame.K_LEFT
                    events.append(pygame.event.Event(pygame.KEYDOWN, {'key': key}))
                
                # Jump (either up button or jump button)
                if touch_state['up'] or touch_state['jump']:
                    events.append(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE}))
                
                # Attack buttons
                if touch_state['punch']:
                    events.append(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_z}))
                if touch_state['kick']:
                    events.append(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_x}))
                
                # Send all generated events to the current state
                for touch_event in events:
                    next_state = self.current_state.handle_event(touch_event)
                    if next_state is not None:
                        print(f"State transition: {self.current_state.__class__.__name__} -> {next_state.__class__.__name__}")
                        self.current_state = next_state
                        break
                continue
            
            # Let the current state handle other events
            next_state = self.current_state.handle_event(event)
            if next_state is not None:
                print(f"State transition: {self.current_state.__class__.__name__} -> {next_state.__class__.__name__}")
                self.current_state = next_state

    def update(self):
        # Update current state and check for state transition
        next_state = self.current_state.update()
        if next_state is not None:
            print(f"State transition from update: {self.current_state.__class__.__name__} -> {next_state.__class__.__name__}")
            self.current_state = next_state

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        self.current_state.draw(self.screen)
        
        # Draw touch controls on top
        self.touch_controls.draw(self.screen)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)  # Target 60 FPS
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 