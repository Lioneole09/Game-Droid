import pygame
import random
from collections import deque
from pygame.locals import *

# Inisialisasi Pygame
pygame.init()

# Membuat labirin
peta = [
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
]

# Membuat ukuran labirin
cell_size = 25
peta_width = 16
peta_height = 16
width = peta_width * cell_size
height = peta_height * cell_size

# Membuat ukuran jendela game
width = 700
height = peta_height * cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Droid")

#  Membuat Droid Pencari
pencari_image = pygame.image.load("DroidMerah.png")
pencari_image = pygame.transform.scale(pencari_image, (int(cell_size * 0.9), int(cell_size * 0.9)))
pencari_rect = pencari_image.get_rect()
pencari_rect.center = ((8 * cell_size) + (cell_size // 2), (8 * cell_size) + (cell_size // 2))
pencari_speed = 1
pencari_visited = set()

# Membuat Droid Penghindar
penghindar_image = pygame.image.load("DroidHijau.png")
penghindar_image = pygame.transform.scale(penghindar_image, (int(cell_size * 0.9), int(cell_size * 0.9)))
penghindar_rect = penghindar_image.get_rect()
penghindar_rect.center = ((4 * cell_size) + (cell_size // 2), (4 * cell_size) + (cell_size // 2))
penghindar_speed = 1
penghindar_visited = set()

# Fungsi untuk menggambar labirin
def menggambar_peta():
    for y in range(peta_height):
        for x in range(peta_width):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if peta[y][x] == 0:
                pygame.draw.rect(screen, (255, 255, 255), rect)
            else:
                pygame.draw.rect(screen, (0, 0, 00), rect)

# Fungsi untuk menggambar objek pada labirin
def menggambar_objek(image, rect):
    screen.blit(image, rect)

# Fungsi untuk memeriksa apakah suatu objek berada dalam area valid
def is_valid(pos):
    x, y = pos
    return 0 <= x < peta_width and 0 <= y < peta_height and peta[y][x] == 0

# Mendapatkan posisi awal droid merah dan droid hijau
while True:
    droid_merah_x, droid_merah_y = random.randint(1, peta_width - 2), random.randint(1, peta_height - 2)
    droid_hijau_x, droid_hijau_y = random.randint(1, peta_width - 2), random.randint(1, peta_height - 2)
    if (
        peta[droid_merah_y][droid_merah_x] == 0
        and peta[droid_hijau_y][droid_hijau_x] == 0
        and abs(droid_merah_x - droid_hijau_x) > 1
        and abs(droid_merah_y - droid_hijau_y) > 1
        and (droid_merah_x != droid_hijau_x or droid_merah_y != droid_hijau_y)
    ):
        break

# Fungsi untuk menggerakkan droid pencari
def gerak_pencari():
    x = pencari_rect.centerx // cell_size
    y = pencari_rect.centery // cell_size

    if (x, y) not in pencari_visited:
        pencari_visited.add((x, y))

    target_rect = (penghindar_rect.centerx // cell_size, penghindar_rect.centery // cell_size)

    def bfs(start, target):
        queue = deque([(start, 0)])
        visited = set([start])

        while queue:
            pos, steps = queue.popleft()

            if pos == target:
                return steps

            x, y = pos
            neighbors = [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
            valid_neighbors = [(nx, ny) for nx, ny in neighbors if is_valid((nx, ny)) and (nx, ny) not in visited]

            queue.extend([(neighbor, steps + 1) for neighbor in valid_neighbors])
            visited.update(valid_neighbors)
        return -1

    possible_moves = [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
    valid_moves = [(px, py) for px, py in possible_moves if is_valid((px, py))]

    distances = [bfs(move, target_rect) for move in valid_moves]
    min_distance = min(distances)

    valid_moves = [valid_moves[i] for i, distance in enumerate(distances) if distance == min_distance]

    if valid_moves:
        next_pos = random.choice(valid_moves)
        pencari_rect.center = ((next_pos[0] * cell_size) + (cell_size // 2), (next_pos[1] * cell_size) + (cell_size // 2))
    else:
        pencari_visited.clear()
        gerak_pencari()
            
# Fungsi untuk menggerakkan droid penghindar
def gerak_penghindar():
    x = penghindar_rect.centerx // cell_size
    y = penghindar_rect.centery // cell_size

    if (x, y) not in penghindar_visited:
        penghindar_visited.add((x, y))

        possible_moves = [(x + dx, y + dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
        valid_moves = [(px, py) for px, py in possible_moves if is_valid((px, py))]

        valid_moves = [move for move in valid_moves if move not in penghindar_visited]

    if valid_moves:
        next_pos = random.choice(valid_moves)
        penghindar_rect.center = ((next_pos[0] * cell_size) + (cell_size // 2), (next_pos[1] * cell_size) + (cell_size // 2))
    else:
        unvisited_moves = [(px, py) for px, py in possible_moves if is_valid((px, py)) and (px, py) not in penghindar_visited]
        if unvisited_moves:
            next_pos = random.choice(unvisited_moves)
            penghindar_rect.center = ((next_pos[0] * cell_size) + (cell_size // 2), (next_pos[1] * cell_size) + (cell_size // 2))
        else:
            penghindar_visited.clear()
            gerak_penghindar()

# Mendefinisikan warna tombol
BUTTON_COLOR = (200, 0, 0)
BUTTON_HOVER_COLOR = (0, 30, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)

# tombol star
class Button:
    def __init__(self, x, y, width, height, text, font_size=25):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.hovered = False

    def draw(self, screen):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        
        text_surface = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

button_width = 150
button_height = 50
button_x = peta_width * cell_size +50 # Mengatur posisi horizontal tombol
button_y = 10 # Mengatur posisi vertikal tombol
start_button = Button(button_x, button_y, button_width, button_height, "Start Game")



# Fungsi utama untuk memulai permainan
def mulai_permainan():
    global running
    game_started = False
    clock = pygame.time.Clock()
    running = True
    
    # Mendapatkan posisi awal droid merah dan droid hijau
    while True:
        droid_merah_x, droid_merah_y = random.randint(1, peta_width - 2), random.randint(1, peta_height - 2)
        droid_hijau_x, droid_hijau_y = random.randint(1, peta_width - 2), random.randint(1, peta_height - 2)
        if (
            peta[droid_merah_y][droid_merah_x] == 0
            and peta[droid_hijau_y][droid_hijau_x] == 0
            and abs(droid_merah_x - droid_hijau_x) > 1
            and abs(droid_merah_y - droid_hijau_y) > 1
        ):
            break

    pencari_rect.center = ((droid_merah_x * cell_size) + (cell_size // 2), (droid_merah_y * cell_size) + (cell_size // 2))
    penghindar_rect.center = ((droid_hijau_x * cell_size) + (cell_size // 2), (droid_hijau_y * cell_size) + (cell_size // 2))


    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if game_started:
                    pass
                elif start_button.rect.collidepoint(event.pos):
                    game_started = True
                    
        screen.fill((0, 0, 255))
        menggambar_peta()
                    
        if not game_started:     
            menggambar_objek(pencari_image, pencari_rect)
            menggambar_objek(penghindar_image, penghindar_rect)
    
            start_button.check_hover(pygame.mouse.get_pos())
            start_button.draw(screen)
        
        else:
            if game_started:
                gerak_pencari()
                gerak_penghindar()
        
                menggambar_objek(pencari_image, pencari_rect)
                menggambar_objek(penghindar_image, penghindar_rect)
                start_button.check_hover(pygame.mouse.get_pos())
                start_button.draw(screen)
        
        pygame.display.update()
        clock.tick(3)
        
        if pencari_rect == penghindar_rect:
            running = False
    pygame.quit()

# Menjalankan permainan
mulai_permainan()
