# TrzySwinki (Three Pigs) 🐷

A Python game implementation inspired by the "Three Little Pigs" fairy tale. This project features a strategic game where pigs with different house structures defend against a wolf.

## Overview

TrzySwinki is a tile-based strategy game where:
- **Three pigs** (Red, Blue, Pink) each have their own unique house structure
- A **wolf** antagonist threatens the pigs
- **Collision detection** determines if the wolf breaches a pig's house
- **Game mechanics** involve house orientation and positioning on a game board

## Game Concepts

### Actors
The game features two types of actors that inherit from the `Actor` base class:

- **Pig** - A defensive actor with an optional house structure
  - Position on the board
  - Associated house (can be None)
  - Collision detection with other pigs and wolves
  
- **Wolf** - An antagonist actor
  - Position on the board
  - Collision detection with pigs

### House Types

Three distinct house structures are implemented:

1. **STICK_HOUSE** - A linear 4-tile structure
   ```
   [1, 1, 1, 1]
   [0, 0, 0, 0]
   [0, 0, 0, 0]
   ```

2. **GUN_HOUSE** - An L-shaped 4-tile structure
   ```
   [1, 1, 1, 0]
   [1, 0, 0, 0]
   [0, 0, 0, 0]
   ```

3. **CORNER_HOUSE** - A corner 3-tile structure
   ```
   [1, 1, 0, 0]
   [1, 0, 0, 0]
   [0, 0, 0, 0]
   ```

### Game Board

- **Size**: 5×5 grid
- **Content**: NumPy array tracking actor positions
- **Forbidden Zones**: Certain positions are blocked to ensure valid game state
- **Update System**: Board updates based on actor positions

### Orientation System

Houses can be rotated using the `Orientation` enum:
- `RIGHT` (0°)
- `DOWN` (90°)
- `LEFT` (180°)
- `UP` (270°)

## Project Structure

```
TrzySwinki/
├── main.py          # Main game implementation
└── README.md        # This file
```

## Key Features

### 1. **Collision Detection**
- Actor-to-actor collision using the `__mul__` operator
- House-to-house collision detection using abstract board mapping
- Position validation against forbidden zones

### 2. **Data Classes**
- `Point` - Represents (x, y) coordinates
- `Board` - Manages game state
- `House` - Represents house structure and orientation

### 3. **Enums**
- `Orientation` - Defines house rotation states (IntEnum)

### 4. **Exception Handling**
- `ActorPositionNotOnBoardException` - Raised when an actor is positioned outside valid zones

## Code Architecture

```python
# Core Classes Hierarchy
Actor (abstract base)
├── Pig (with optional House)
└── Wolf

Board (game state management)
House (structure with tiles and orientation)
Point (coordinate system)
```

## Usage

### Running the Game

```bash
python main.py
```

### Creating Game Configuration

```python
from main import get_config, run

config = get_config()
run(**config)
```

### Example: Custom Game Setup

```python
from main import Pig, Wolf, STICK_HOUSE, GUN_HOUSE, Point

red_pig = Pig(Point(0, 1), STICK_HOUSE, "red_pig")
wolf = Wolf(Point(2, 3))

# Check collision
collision = red_pig * wolf
```

## Current Implementation Status

- ✅ Core game classes and data structures
- ✅ Collision detection system
- ✅ House structure definitions
- ✅ Board state management
- ✅ Actor positioning
- ⏳ Game loop (in `run()` function)
- ⏳ Win/lose conditions
- ⏳ User input handling
- ⏳ Visualization/rendering

## Technical Details

### Dependencies
- **NumPy** - Array operations for board and house collision detection
- **Python 3.7+** - Type hints and dataclasses support

### Key Algorithms
- **House Collision Detection**: Maps house tiles to an abstract 100×100 board, uses dot product to detect overlaps
- **Position Validation**: Checks against forbidden zone list
- **Orientation Tracking**: Modular arithmetic for 360° rotation

## Future Enhancements

- [ ] Implement complete game loop in `run()` function
- [ ] Add game rendering (CLI or GUI)
- [ ] Implement wolf AI/movement logic
- [ ] Add win/lose conditions
- [ ] Support player input for house rotation/pig movement
- [ ] Add difficulty levels
- [ ] Implement scoring system

## Polish Game Terms

- **TrzySwinki** - Three Pigs
- **Swinki** - Pigs
- **Wilk** - Wolf

## License

Open source - feel free to use and modify!

## Author Notes

This is a strategic game prototype implementing object-oriented design principles, collision detection algorithms, and game state management in Python.
