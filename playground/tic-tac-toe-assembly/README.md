# Tic Tac Toe in MIPS

### Source Code documentation is available in `Tic-Tac-Toe.asm`

## Program Description

1. The Tic Tac Toe program starts by printing a set of instructions for the player
2. Placement validation function prevents both computer and player to only place moves on an empty slot.
3. After both player and computer makes a move, an updated board will be printed.
4. Game will continue running until either the player, or the computer wins by placing 3 marks in a row, or when the board is filled.
5. When the game is over, it prompts the winner of the game and ends the program.

#

## Execution

### Setup

1. Open the [MARS MIPS Simulator](http://courses.missouristate.edu/kenvollmar/mars/)
2. Compile (F3) `Tic-Tac-Toe.asm` from the simulator
3. Start (F5) The program

### Play the Game

1. You will be player X and go first.
2. When prompted, type a number (0-8) and hit enter.
3. Get 3 in a row to win the game
4. When there is a winner or the board is full, execution ends

#

## Solved Challenges

### Where do I start?

As a beginner in assembly, the language is very intimidating. Because I had no prior experiences using assembly, it was a challenge to figure out which component of the code I had to start first; even a simple game is hard to code in assembly.

### Collision Handling

To make sure the user or the computer doesn't place any moves in a pre-occupied slot of the game board, I created a function that checks if the place is pre-occupied with 'O' or 'X'. If there is a collision, I simply re-ran the place procedures.

### Check for Winner

Tic-Tac-Toe is a game that offers 8 three-in-a-row winning positions. To accomodate for all 8 winning rows, I created 18 separate procedures that checks for each winning three-in-a-row sets.
