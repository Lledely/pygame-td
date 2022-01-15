# Main game file
import pygame


pygame.init()
size = (800, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("TD")
clock = pygame.time.Clock()
FPS = 60


class SpriteGroup(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = None

    def get_event(self, event):
        pass


class Board():

    def __init__(self, width=16, height=16, cell_size=40):
        self.width = width
        self.height = height
        self.top = 155
        self.side = 155
        self.cell_size = cell_size
        self.board = [[0] * width for _ in range(height)]

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.side, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    def get_cell(self, mouse_pos) -> tuple:
        if not (self.side <= mouse_pos[0] <= self.side + self.width * self.cell_size and
                self.top <= mouse_pos[1] <= self.top + self.height * self.cell_size):
            return None
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        return (x, y)

    def get_click(self, mouse_pos) -> None:
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


def start_screen() -> None:
    pass

def main() -> None:
    running = True
    board = Board(16, 16, 40)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()