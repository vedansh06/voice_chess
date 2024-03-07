'''BUGS:
1. The program cannot find moves with other pieces that can block checkmate. If a king is in check and cannot
move, the program will display checkamte even though there is a piece that can block the check, or capture the 
checking piece
2. No mechanism to show a draw
3. Reset black move to engine, make the handle_move method applicable for white'''

import pygame
from square import Square
from piece import Rook
from piece import Bishop
from piece import Knight
from piece import Queen
from piece import King
from piece import Pawn
from engine import minimax


# Game state checker
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.turn = "white"
        self.prev_move = ""
        self.config = [
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ]
        self.squares = self.generate_squares()
        self.setup_board()


    def generate_squares(self):
        output = []
        for y in range(7, -1, -1):
            for x in range(8):
                output.append(Square(x, y, self.tile_width, self.tile_height))
        return output

    def get_square_from_pos(self, pos):
        for square in self.squares:
            if square.pos == pos:
                return square
            
    def get_square_from_coord(self, coord):
        for square in self.squares:
            if square.coord == coord:
                return square
    
    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece

    def setup_board(self):
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != "":
                    square = self.get_square_from_pos((x, y))
                    # looking inside contents, what piece does it have
                    if piece[1] == "R":
                        square.occupying_piece = Rook(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )
                    # as you notice above, we put `self` as argument, or means our class Board
                    elif piece[1] == "N":
                        square.occupying_piece = Knight(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )
                    elif piece[1] == "B":
                        square.occupying_piece = Bishop(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )
                    elif piece[1] == "Q":
                        square.occupying_piece = Queen(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )
                    elif piece[1] == "K":
                        square.occupying_piece = King(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )
                    elif piece[1] == "P":
                        square.occupying_piece = Pawn(
                            (x, y), "white" if piece[0] == "w" else "black", self
                        )

    def handle_move(self, mx, my):
        if self.turn == "white" or self.turn == "black":
            try:
                x = (mx-30) // self.tile_width
                y = ((565-my)-20) // self.tile_height + 1
                clicked_square = self.get_square_from_pos((x, y))
                
                if self.selected_piece is None:
                    if clicked_square.occupying_piece is not None:
                        if clicked_square.occupying_piece.color == self.turn:
                            self.selected_piece = clicked_square.occupying_piece
                elif self.selected_piece.move(self, clicked_square):
                    self.turn = "black" if self.turn == "white" else "white"
                    self.prev_move = clicked_square.occupying_piece.this_move
                elif clicked_square.occupying_piece is not None:
                    if clicked_square.occupying_piece.color == self.turn:
                        self.selected_piece = clicked_square.occupying_piece
                
            except AttributeError:
                pass
        else:
            pass

    def engine_move(self):
            #max_player = True if self.turn == "white" else False
            best_move = minimax(self, 2, False)
            piece_square = self.get_square_from_coord(best_move[:2])
            new_square = self.get_square_from_coord(best_move[2:])
            self.selected_piece = piece_square.occupying_piece
            self.selected_piece.move(self, new_square)
            self.turn = "white" if self.turn == "black" else "black"

    def audio_move(self, move):
        piece_square = self.get_square_from_coord(move[:2])
        new_square = self.get_square_from_coord(move[2:])
        self.selected_piece = piece_square.occupying_piece
        self.selected_piece.move(self, new_square)
        self.turn = "white" if self.turn == "black" else "black"
        self.prev_move = move
        
    # check state checker
    def is_in_check(
        self, color, board_change=None
    ):  # board_change = [(x1, y1), (x2, y2)]
        output = False
        king_pos = None
        changing_piece = None   
        old_square = None
        new_square = None
        new_square_old_piece = None
        if board_change is not None:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece
        pieces = [
            i.occupying_piece for i in self.squares if i.occupying_piece is not None
        ]
        if changing_piece is not None:
            if changing_piece.notation == "K":
                king_pos = new_square.pos
        if king_pos == None:
            for piece in pieces:
                if piece.notation == "K" and piece.color == color:
                    king_pos = piece.pos
        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares(self):
                    if square.pos == king_pos:
                        output = True
        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece
        return output

    # checkmate state checker
    def is_in_checkmate(self, color):
        output = False
        for piece in [i.occupying_piece for i in self.squares]:
            if piece != None:
                if piece.notation == "K" and piece.color == color:
                    king = piece
        if king.get_valid_moves(self) == []:
            if self.is_in_check(color):
                output = True
        return output
    
    def draw(self, display):
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True
        for square in self.squares:
            square.draw(display)
