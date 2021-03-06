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
towers_locations = [[0] * 16 for i in range(16)]
enemy_list = {}

class SpriteGroup(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

    def get_event(self, event: pygame.event):
        for sprite in self:
            sprite.get_event(event)


class Tower_image(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, tower_type) -> None:
        super().__init__(all_sprites)
        self.image = images['tower']
        self.rect = self.image.get_rect().move(
            board.side + CELL_WIDTH * pos_x, board.top + CELL_HEIGHT * pos_y)


class Enemy_image(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y) -> None:
        super().__init__(all_sprites)
        self.image = images['enemy']
        self.rect = self.image.get_rect().move(
            board.side + CELL_WIDTH * pos_x, board.top + CELL_HEIGHT * pos_y)
        self.x_pos = pos_x
        self.y_pos = pos_y

    def update(self, obj):
        x_new = 0
        y_new = 0
        direction = enemy_list[obj][0]
        if pygame.sprite.spritecollideany(self, grass_borders):
            if direction % 2 == 0:
                y_new = self.y_pos
                if board[x_new - 1][y_new] == 0:
                    direction = 3
                else:
                    direction = 1
            else:
                x_new = self.x_pos
                if board[x_new][y_new - 1] == 0:
                    direction = 0
                else:
                    direction = 2
        t = clock.tick()
        if direction == 0:
            enemy_list[obj] = (direction, enemy_list[obj][1] - t * obj.speed, enemy_list[obj][2], enemy_list[obj][-1])
        elif direction == 1:
            enemy_list[obj] = (direction, enemy_list[obj][1], enemy_list[obj][2] + t * obj.speed, enemy_list[obj][-1])
        elif direction == 2:
            enemy_list[obj] = (direction, enemy_list[obj][1] + t * obj.speed, enemy_list[obj][2], enemy_list[obj][-1])
        else:
            enemy_list[obj] = (direction, enemy_list[obj][1], enemy_list[obj][2] - t * obj.speed, enemy_list[obj][-1])


class Grass(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y) -> None:
        super().__init__(all_sprites, grass_borders)
        self.image = images['grass']
        self.rect = self.image.get_rect().move(
            board.side + CELL_WIDTH * pos_x, board.top + CELL_HEIGHT * pos_y)


class Road(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y) -> None:
        super().__init__(all_sprites)
        self.image = images['road']
        self.rect = self.image.get_rect().move(board.side + CELL_WIDTH * pos_x,
                                               board.top + CELL_HEIGHT * pos_y)


class Selection_of_Towers(object):

    def __init__(self, width: int=1, height: int=4, cell_size: int=135):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.image_height = 100
        self.image_width = 135
        self.top = 160
        self.side = 10
        self.screen = SCREEN

    def render(self, screen: pygame.display):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.side, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)
                image = load_image("tower.png")
                image1 = pygame.transform.scale(image, (135, 100))
                self.screen.blit(image1, (self.side + self.image_width * x, 30 * y + self.top + self.image_height * y))

    def pick_tower(self, pos):
        y = (pos[1] - self.top) // 135
        x = (pos[0] - self.side) // 100
        if y == 0:
            obj = towers.ShortRangeTower()
        if y == 1:
            obj = towers.MiddleRangeTower()
        if y == 2:
            obj = towers.LongRangeTower()
        if y == 3:
            obj = towers.DGTower()
        return obj


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
        x = (mouse_pos[0] - self.side) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        return (x, y)

    def get_click(self, mouse_pos: tuple) -> None:
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if towers_locations[y][x] != 0:
                Tower_image(x, y, towers_locations[y][x])
            elif level[y][x] == '0':
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
        print('???? ?????????????? ??????????????????:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
         if color_key == -1:
             color_key = image.get_at((0, 0))
         image.set_colorkey(color_key)
    return image


def show_info(screen: pygame.Surface, wallet: int = 69420, current_round: int = 69, max_round: int = 420) -> None:
    font = pygame.font.Font(None, TEXT_SIZE)
    wallet_info = font.render("Money: {}".format(wallet), True, pygame.Color(TEXT_COLOR))
    round_info = font.render("Round: {}/{}".format(current_round, max_round), True, pygame.Color(TEXT_COLOR))
    wallet_info_coords = (10, 15)
    round_info_coords = (410, 15)
    screen.blit(wallet_info, wallet_info_coords)
    screen.blit(round_info, round_info_coords)


def start_screen() -> None:
    pass


def main() -> None:
    global board, screen, wallet, enemy_list, clock
    MAX_ROUND = 40
    CURRENT_ROUND = 1
    ENEMIES_AMOUNT = 10
    ENTRY = 14
    count_enemies = 0
    clock = pygame.time.Clock()
    wallet = 1000
    FPS = 60
    level_name = 'level1.txt'
    running = True
    board = Board(16, 16, 40)
    towers_table = Selection_of_Towers(1, 4, 135)
    level = load_level(level_name)
    tower_picked = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not tower_picked:
                        tower_type = towers_table.pick_tower(event.pos)
                        tower_picked = True
                        wallet -= tower_type.cost
                        print(wallet)
                        continue
                    if not(155 <= event.pos[0] <= 800 and 155 <= event.pos[1] <= 800):
                        continue
                    x, y = board.get_cell(event.pos)
                    if level[y][x] == 1 or towers_locations[y][x] != 0:
                        continue
                    towers_locations[y][x] = tower_type
                    tower_picked = False
        clock.tick(FPS)
        if count_enemies <= ENEMIES_AMOUNT:
            enemy_sprite = Enemy_image(0, 14)
            enemy = enemies._Enemy()
            enemy_list[enemy] = (2, 0, 155 + 13 * 40, enemy_sprite)
        SCREEN.fill((0, 0, 0))
        show_info(SCREEN, wallet, CURRENT_ROUND, MAX_ROUND)
        board.render(SCREEN)
        towers_table.render(SCREEN)
        generate_level(level)
        for key in enemy_list:
            key[3].update(key)
        all_sprites.draw(SCREEN)
        pygame.display.flip()
    pygame.quit()


images = {
    'tower': load_image('tower.png'),
    'grass': load_image('grass.png'),
    'road': load_image('road.png'),
    'enemy': load_image('enemy.png')
}

all_sprites = pygame.sprite.Group()
grass_borders = pygame.sprite.Group()

CELL_WIDTH = CELL_HEIGHT = 40


if __name__ == "__main__":
    main()