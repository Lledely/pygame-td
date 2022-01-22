# Main game file
import pygame
import enemies
import towers


class SpriteGroup(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

    def get_event(self, event: pygame.event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.rect = None

    def get_event(self, event: pygame.event):
        pass


class Board(object):

    def __init__(self, width: int=16, height: int=16, cell_size: int=40):
        self.width = width
        self.height = height
        self.top = 155
        self.side = 155
        self.cell_size = cell_size
        self.board = [[0] * width for _ in range(height)]

    def render(self, screen: pygame.display):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.side, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    def get_cell(self, mouse_pos: tuple) -> tuple:
        if not (self.side <= mouse_pos[0] <= self.side + self.width * self.cell_size and
                self.top <= mouse_pos[1] <= self.top + self.height * self.cell_size):
            return
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        return (x, y)

    def get_click(self, mouse_pos: tuple) -> None:
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


def start_screen() -> None:
    pass

def main() -> None:
    pygame.init()
    size = (800, 800)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("TD")
    clock = pygame.time.Clock()
    FPS = 60
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