"""THINGS LEFT TO DO:
Issue 1: App or webiste or neither. Have to make this program into a proper flowing program.

Issue 2: Make a move recording table

Issue 3: Develop a game end screen which does not automatically terminate the program after checkmate.
It displays a window that shows the winner and the when you close the window , it terminates the program.

Issue 4: When the audio move function or the chess engine is running the program freezes, so maybe fix that

Issue 5: Refer to bugs section in files

Issue 6: Actually implement your neural network to recognize moves instead of using google like you are doing
right now. 

Issue 7: UI creation, but that is probably related to Issue 3

Issue 8: Print row and columns on the screen for each, also maybe player names

Issue 9: Exception handling for voice input, what to do if move is not valid or input is incomprehensible

Issue 10: The pieces cannot be dragged, but  they can be moved by clicking on them and then releasing the mouse button
(can still be allowed as does not pose a big problem)

Issue 11: For blindfold chess, make the engine speak its moves out aloud

Issue 12: Add functioanlity to change whether engine is black or white"""

# Initialises the game and contains the game loop
import pygame
from side_panel import SpeakButton
from board1 import Board
from PyQt5.QtWidgets import *

pygame.init()

BOARD_SIZE = (600, 600)
PANEL_SIZE = (300, 500)
SCREEN_SIZE = (1050, 660)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Chess Game")

board = Board(BOARD_SIZE[0], BOARD_SIZE[1])
moves_panel = pygame.Surface((PANEL_SIZE[0], PANEL_SIZE[1]))
mic_button = SpeakButton(700, 545, 75, 75)


def draw(display):
    display.fill("white")
    board.draw(display)
    mic_button.draw(display)
    moves_panel.fill((20, 20, 20))
    screen.blit(moves_panel, (700, 30))
    pygame.display.update()


if __name__ == "__main__":
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        #if board.turn == "black":
         #   board.engine_move()
        for event in pygame.event.get():
            # Quit the game if the user presses the close button
            if event.type == pygame.QUIT:
                running = False
            elif  mx > 650 or mx < 30:
                move = mic_button.handle_event(event)
                if type(move) == str:
                    board.audio_move(move)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the mouse is clicked
                if event.button == 1 and mx <= 650:
                    board.handle_move(mx, my)
                    
        if board.is_in_checkmate("black"):  # If black is in checkmate
            print("White wins!")
            running = False
        elif board.is_in_checkmate("white"):  # If white is in checkmate
            print("Black wins!")

            running = False
        # Draw the board
        draw(screen)
