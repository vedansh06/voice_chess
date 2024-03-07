import pygame

# Class for creating each square of the board
class Square:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
#removed abs_x, abs_y and abs_pos attributes. If bugs arise just undo changes.
        self.pos = (x, y)
        self.color = 'dark' if (x + y) % 2 == 0 else 'light'
        self.draw_color = (240, 217, 181) if self.color == 'light' else (181, 136, 99)
        self.highlight_color = (255, 255, 143) if self.color == 'light' else (255, 234, 0)
        self.occupying_piece = None
        self.coord = self.get_coord()
        self.highlight = False
        self.rect = pygame.Rect(
            (x * width) + 30,
            565 - ((y * height) + 20),
            self.width,
            self.height
        )

    # get the formal notation of the tile
    def get_coord(self):
        columns = 'abcdefgh'
        return columns[self.x] + str(self.y + 1)

    def draw(self, display):
        # configures if tile should be light or dark or highlighted tile
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)
        # adds the chess piece icons
        if self.occupying_piece != None:
            centering_rect = self.occupying_piece.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.occupying_piece.img, centering_rect.topleft)