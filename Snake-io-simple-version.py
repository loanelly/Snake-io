import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы размеров игры
WINDOW_WIDTH = 600
PLAY_HEIGHT = 600  # Чистая высота игрового поля
HEADER_HEIGHT = 40  # Высота выделенной зоны для счета
WINDOW_HEIGHT = PLAY_HEIGHT + HEADER_HEIGHT  # Общая высота окна
CELL_SIZE = 20  # Размер одной ячейки

# Цвета (RGB)
COLOR_BACKGROUND = (30, 30, 30)  # Темно-серый фон поля
COLOR_HEADER = (20, 20, 20)      # Более темный фон для панели счета
COLOR_SNAKE = (46, 196, 182)     # Бирюзовая змейка
COLOR_FOOD = (231, 76, 60)       # Красная еда
COLOR_TEXT = (255, 255, 255)     # Белый текст
COLOR_LINE = (60, 60, 60)        # Серый цвет разделительной линии

# Настройка игрового окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Классическая Змейка на Python")

clock = pygame.time.Clock()
SNAKE_SPEED = 10  # Скорость змейки

def show_score(score):
    """Вывод счета в выделенную верхнюю панель"""
    font = pygame.font.SysFont("Arial", 20, bold=True)
    score_surface = font.render(f"Счет: {score}", True, COLOR_TEXT)
    # Центрируем текст по вертикали внутри панели HEADER_HEIGHT
    screen.blit(score_surface, (15, (HEADER_HEIGHT // 2) - (score_surface.get_height() // 2)))

def game_loop():
    """Главный игровой цикл"""
    # Смещаем начальные координаты змейки ниже верхней панели счета
    snake_pos = [[300, 300], [280, 300], [260, 300]]
    
    direction = "RIGHT"
    change_to = direction

    # Спавним еду строго в пределах игрового поля (начиная со 2-й ячейки по вертикали)
    food_pos = [
        random.randrange(0, (WINDOW_WIDTH // CELL_SIZE)) * CELL_SIZE,
        random.randrange(HEADER_HEIGHT // CELL_SIZE, (WINDOW_HEIGHT // CELL_SIZE)) * CELL_SIZE
    ]
    food_spawn = True
    score = 0

    while True:
        # 1. Обработка событий (Стрелочки + WASD)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    change_to = "UP"
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    change_to = "DOWN"
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    change_to = "LEFT"
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    change_to = "RIGHT"

        # Защита от разворота на 180 градусов
        if change_to == "UP" and direction != "DOWN": direction = "UP"
        if change_to == "DOWN" and direction != "UP": direction = "DOWN"
        if change_to == "LEFT" and direction != "RIGHT": direction = "LEFT"
        if change_to == "RIGHT" and direction != "LEFT": direction = "RIGHT"

        # 2. Движение змейки
        head_x, head_y = snake_pos[0][0], snake_pos[0][1]
        
        if direction == "UP": head_y -= CELL_SIZE
        if direction == "DOWN": head_y += CELL_SIZE
        if direction == "LEFT": head_x -= CELL_SIZE
        if direction == "RIGHT": head_x += CELL_SIZE

        new_head = [head_x, head_y]
        snake_pos.insert(0, new_head)

        # 3. Проверка поедания еды
        if head_x == food_pos[0] and head_y == food_pos[1]:
            score += 10
            food_spawn = False
        else:
            snake_pos.pop()

        if not food_spawn:
            food_pos = [
                random.randrange(0, (WINDOW_WIDTH // CELL_SIZE)) * CELL_SIZE,
                random.randrange(HEADER_HEIGHT // CELL_SIZE, (WINDOW_HEIGHT // CELL_SIZE)) * CELL_SIZE
            ]
            food_spawn = True

        # 4. Проверка условий проигрыша (Мгновенный перезапуск)
        # Столкновение со стенами (верхняя граница теперь HEADER_HEIGHT)
        if head_x < 0 or head_x >= WINDOW_WIDTH or head_y < HEADER_HEIGHT or head_y >= WINDOW_HEIGHT:
            return
        
        # Столкновение со своим хвостом
        if new_head in snake_pos[1:]:
            return

        # 5. Отрисовка графики
        screen.fill(COLOR_BACKGROUND)  # Фон игрового поля

        # Отрисовка верхней отдельной панели для счета
        pygame.draw.rect(screen, COLOR_HEADER, pygame.Rect(0, 0, WINDOW_WIDTH, HEADER_HEIGHT))
        pygame.draw.line(screen, COLOR_LINE, (0, HEADER_HEIGHT), (WINDOW_WIDTH, HEADER_HEIGHT), 2)

        # Рисуем еду и змейку
        pygame.draw.rect(screen, COLOR_FOOD, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))
        for pos in snake_pos:
            pygame.draw.rect(screen, COLOR_SNAKE, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

        # Отрисовка счета за пределами поля
        show_score(score)

        pygame.display.flip()
        clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    while True:
        game_loop()
