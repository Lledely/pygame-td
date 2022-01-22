# Main game file
import pygame
import enemies
import towers
import os
import sys


class SpriteGroup(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

    def get_event(self, event: pygame.event):
        for sprite in self:
            sprite.get_event(event)


class Grass(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y) -> None:
        super().__init__(grass_group, all_sprites)
        self.image = images['grass']
        self.rect = self.image.get_rect().move(
            CELL_WIDTH * pos_x, CELL_HEIGHT * pos_y)


class Road(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y) -> None:
        super().__init__(road_group, all_sprites)
        self.image = images['road']
        self.rect = self.image.get_rect().move(CELL_WIDTH * pos_x,
                                               CELL_HEIGHT * pos_y)


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


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '0':
                Grass(x, y)
            elif level[y][x] == '1':
                Road(x, y)
                board.board[x][y] = 1
    return x, y


def load_level(filename):
    filename = "level/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def load_image(name, color_key=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def start_screen() -> None:
    pass


def main() -> None:
    global board
    pygame.init()
    size = (800, 800)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("TD")
    clock = pygame.time.Clock()
    FPS = 60
    level_name = '1'
    running = True
    board = Board(16, 16, 40)
    level = load_level(level_name)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        board.render(screen)
        generate_level(level)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


images = {
    # 'tower': load_image('tower.png'),
    'grass': load_image('grass.png'),
    'road': load_image('road.png')
}
# enemy_image = load_image('enemy.png')

all_sprites = pygame.sprite.Group()
grass_group = pygame.sprite.Group()
road_group = pygame.sprite.Group()


CELL_WIDTH = CELL_HEIGHT = 40


if __name__ == "__main__":
    main()