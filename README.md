# AI Project: Connect 4 with MCTS and ID3

This project offers a text-based Connect 4 game (no graphical interface), using simple characters to represent the board. Players take turns dropping discs into a 7×6 grid, aiming to connect four in a row. It includes human vs human, human vs AI, and AI vs AI modes,.

Developed for the AI course at the University of Porto, the AI combines **Monte Carlo Tree Search (MCTS)** with UCT and an **ID3 decision tree** to evaluate and select moves.

## Features
- **MCTS (Monte Carlo Tree Search)** for move selection
- **ID3 algorithm** for building a decision tree to predict moves

## Requirements
- pandas
- matplotlib

## Setup & Usage

1. Navigate to the project directory:
   ```bash
   cd path/to_project
   ```
2. Install dependencies:
    ``` bash
    pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```