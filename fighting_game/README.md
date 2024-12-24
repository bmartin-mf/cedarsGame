# 2D Fighter Game

A simple 2D fighting game built with Python and Pygame.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fighting_game
   ```

2. Create and activate a virtual environment:

   **On macOS/Linux:**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate
   ```

   **On Windows:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Development Tools

The project includes several development tools:

- **Black**: Code formatter
  ```bash
  black src/
  ```

- **Pylint**: Code linter
  ```bash
  pylint src/
  ```

- **Pytest**: Testing framework
  ```bash
  pytest
  ```

## Running the Game

With the virtual environment activated:
```bash
python src/main.py
```

## Game Controls

### Player 1 (Left)
- A/D: Move left/right
- W: Jump
- J: Punch
- K: Kick

### Player 2 (Right)
- Left/Right Arrow: Move left/right
- Up Arrow: Jump
- Numpad 1: Punch
- Numpad 2: Kick

## Game Features

- Main menu with VS Player and VS AI modes
- Three AI difficulty levels (Easy, Medium, Hard)
- Character selection screen
- Basic fighting mechanics (movement, jumping, attacks)
- Health bars and round timer
- Simple collision detection and damage system

## Project Structure

```
fighting_game/
  ├─ assets/            # Game assets
  │   ├─ images/       # Character sprites and backgrounds
  │   └─ sounds/       # Sound effects and music
  ├─ src/              # Source code
  │   ├─ main.py       # Game entry point
  │   ├─ states/       # Game state management
  │   │   ├─ game_state.py
  │   │   ├─ menu_state.py
  │   │   ├─ character_select_state.py
  │   │   └─ fight_state.py
  │   ├─ characters/   # Character-related code
  │   │   ├─ character.py
  │   │   └─ ai_controller.py
  │   └─ utils/        # Utility functions
  ├─ tests/            # Test files
  ├─ requirements.txt  # Project dependencies
  ├─ .gitignore       # Git ignore file
  └─ README.md        # Project documentation
```

## Contributing

1. Create a new virtual environment (see Environment Setup)
2. Install development dependencies
3. Make your changes
4. Run formatting and linting:
   ```bash
   black src/
   pylint src/
   ```
5. Run tests:
   ```bash
   pytest
   ```
6. Submit a pull request

## Troubleshooting

### Common Issues

1. **Pygame installation fails**
   - On Linux: Install SDL dependencies
     ```bash
     sudo apt-get install python3-pygame
     ```
   - On macOS: Use Homebrew
     ```bash
     brew install sdl sdl_image sdl_mixer sdl_ttf portmidi
     ```

2. **Virtual environment not activating**
   - Make sure you're in the project directory
   - Check Python version: `python --version`
   - Try recreating the virtual environment

3. **Game performance issues**
   - Check Python version (3.8+ recommended)
   - Verify Pygame version matches requirements.txt
   - Close other resource-intensive applications 