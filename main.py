# Main game file
import pygame
import enemies
import towers
import os
import sys


pygame.init()
size = (800, 800)
SCREEN = pygame.display.set_mode(size)
pygame.display.set_caption("TD")
TEXT_SIZE = 30
TEXT_COLOR = (255, 255, 255)

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
            board.side + CELL_WIDTH * pos_x, board.top + CELL_HEIGHT * pos_y)


class Road(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y) -> None:
        super().__init__(road_group, all_sprites)
        self.image = images['road']
        self.rect = self.image.get_rect().move(board.side + CELL_WIDTH * pos_x,
                                               board.top + CELL_HEIGHT * pos_y)


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


def load_level(name):
    filename = os.path.join('levels', name)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip().split() for line in mapFile]
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
         if color_key == -1:
             color_key = image.get_at((0, 0))
         image.set_colorkey(color_key)
    return image


def start_screen() -> None:
    pass


def show_info(screen: pygame.Surface, wallet: int = 69420, current_round: int = 69, max_round: int = 420) -> None:
    font = pygame.font.Font(None, TEXT_SIZE)
    wallet_info = font.render("Money: {}".format(wallet), True, pygame.Color(TEXT_COLOR))
    round_info = font.render("Round: {}/{}".format(current_round, max_round), True, pygame.Color(TEXT_COLOR))
    wallet_info_coords = (10, 15)
    round_info_coords = (410, 15)
    screen.blit(wallet_info, wallet_info_coords)
    screen.blit(round_info, round_info_coords)


def main() -> None:
    global board
    MAX_ROUND = 40
    CURRENT_ROUND = 1
    WALLET = 0
    clock = pygame.time.Clock()
    FPS = 60
    level_name = 'level1.txt'
    running = True
    board = Board(16, 16, 40)
    level = load_level(level_name)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(FPS)
        SCREEN.fill((0, 0, 0))
        show_info(SCREEN, WALLET, CURRENT_ROUND, MAX_ROUND)
        board.render(SCREEN)
        generate_level(level)
        all_sprites.draw(SCREEN)
        pygame.display.flip()
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