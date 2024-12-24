class GameState:
    def handle_event(self, event):
        """Handle pygame events"""
        pass

    def update(self):
        """Update game state logic
        Returns:
            GameState or None: The next state to transition to, or None to stay in current state
        """
        return None

    def draw(self, screen):
        """Draw the current state
        Args:
            screen: pygame surface to draw on
        """
        pass 