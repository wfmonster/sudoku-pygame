# 🧩 Sudoku

A classic Sudoku puzzle game built with Python and Pygame — a personal learning project for [Boot.dev](https://boot.dev).

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?logo=pygame)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

## 📖 About

This project is an implementation of the classic Sudoku number puzzle using Pygame. It's designed as a hands-on learning experience to explore game development concepts including rendering, user input handling, and game state management.

## ✨ Planned Features

- 🎮 Standard 9×9 Sudoku grid
- 📚 Multiple puzzles organized by difficulty level
- 🖱️ Click-to-input number entry
- 🏆 Win/lose state detection
- 🪵 Wooden texture background aesthetic
- 🎯 Start screen with puzzle selection

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- [UV](https://github.com/astral-sh/uv) package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sudoku.git
   cd sudoku
   ```

2. Install dependencies with UV:
   ```bash
   uv sync
   ```

### Running the Game

```bash
uv run main.py
```

## 🎮 How to Play

Sudoku is a logic-based number puzzle. The objective is to fill a 9×9 grid so that:
- Each **row** contains the digits 1-9 with no repetition
- Each **column** contains the digits 1-9 with no repetition  
- Each of the nine 3×3 **sub-boxes** contains the digits 1-9 with no repetition

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.13 | Core language |
| Pygame 2.6.1 | Game framework & rendering |
| UV | Package management |

## 📁 Project Structure

```
sudoku/
├── main.py          # Game entry point and main loop
├── constants.py     # Color definitions and screen dimensions
├── pyproject.toml   # Project configuration and dependencies
└── README.md        # You are here!
```

## 🗺️ Roadmap

- [x] Basic grid rendering
- [ ] Puzzle loading system
- [ ] User input handling
- [ ] Number validation
- [ ] Win/lose conditions
- [ ] Difficulty selection screen
- [ ] Visual polish & textures

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built as a learning project for [Boot.dev](https://boot.dev)
- Powered by [Pygame](https://www.pygame.org/)

---

*Last Updated: January 15, 2026*
