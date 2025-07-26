# Tetris

This repository contains a simple terminal-based Tetris game implemented in Python using the `curses` module.

## Running the game

Run the following command from the repository root:

```bash
python3 tetris.py
```

Controls:

- **Left/Right arrows**: move piece
- **Down arrow**: drop piece one row
- **Space**: rotate piece
- **q**: quit the game


## Motocross RL Demo

This repository also includes a minimal motocross environment with a tabular Q-learning agent. The environment uses `pygame` for rendering. Install dependencies and run training with:

```bash
pip install pygame
python3 train_agent.py
```

After training, a short demonstration will render the agent riding across the track.
