import pygame
import random
import sys
import time

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Константы размеров окна
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20

# Цвета (RGB)
COLOR_BACKGROUND = (30, 30, 30)
COLOR_SNAKE = (46, 196, 182)
COLOR_FOOD = (231, 76, 60)
COLOR_TEXT = (255, 255, 255)
COLOR_LEVEL_UP = (241, 196, 15)
COLOR_MENU_BTN = (52, 152, 219)
COLOR_ACTIVE = (46, 204, 113)

# Настройка окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# Исправление для Windows буфера
screen.fill(COLOR_BACKGROUND)
time.sleep(0.1)
pygame.display.flip()

clock = pygame.time.Clock()

# --- СИСТЕМА УПРАВЛЕНИЯ (БИНДЫ) ---
CONTROLS_PRESETS = {
    "ARROWS": {
        "UP": pygame.K_UP,
        "DOWN": pygame.K_DOWN,
        "LEFT": pygame.K_LEFT,
        "RIGHT": pygame.K_RIGHT,
        "NAME": "ARROWS"
    },
    "WASD": {
        "UP": pygame.K_w,
        "DOWN": pygame.K_s,
        "LEFT": pygame.K_a,
        "RIGHT": pygame.K_d,
        "NAME": "WASD"
    },
    "IJKL": {
        "UP": pygame.K_i,
        "DOWN": pygame.K_k,
        "LEFT": pygame.K_j,
        "RIGHT": pygame.K_l,
        "NAME": "IJKL"
    }
}

current_control_type = "ARROWS"

def show_interface(score, level, current_speed, mode):
    font = pygame.font.Font(None, 26)
    score_txt = font.render(f"Score: {score}", True, COLOR_TEXT)
    speed_txt = font.render(f"Speed: {current_speed}", True, COLOR_TEXT)
    
    if mode == "LEVELS":
        level_txt = font.render(f"Mode: Levels (Lvl. {level})", True, COLOR_LEVEL_UP)
    else:
        level_txt = font.render("Mode: Classic", True, COLOR_MENU_BTN)
        
    screen.blit(score_txt, (10, 10))
    screen.blit(level_txt, (200, 10))
    screen.blit(speed_txt, (450, 10))

def main_menu():
    font_title = pygame.font.Font(None, 56)
    font_options = pygame.font.Font(None, 28)
    font_footer = pygame.font.Font(None, 18)

    while True:
        screen.fill(COLOR_BACKGROUND)
        bind_name = CONTROLS_PRESETS[current_control_type]["NAME"]
        
        title_txt = font_title.render("SNAKE GAME", True, COLOR_SNAKE)
        opt1_txt = font_options.render("1. Classic Mode (Fixed Speed)", True, COLOR_TEXT)
        opt2_txt = font_options.render("2. Levels Mode (Speed Increases)", True, COLOR_TEXT)
        opt3_txt = font_options.render(f"3. Controls Settings (Current: {bind_name})", True, COLOR_LEVEL_UP)
        footer_txt = font_footer.render("Press 1, 2 or 3 to choose. ESC - Exit", True, (120, 120, 120))
        
        screen.blit(title_txt, (WINDOW_WIDTH // 2 - title_txt.get_width() // 2, 120))
        screen.blit(opt1_txt, (WINDOW_WIDTH // 2 - opt1_txt.get_width() // 2, 250))
        screen.blit(opt2_txt, (WINDOW_WIDTH // 2 - opt2_txt.get_width() // 2, 310))
        screen.blit(opt3_txt, (WINDOW_WIDTH // 2 - opt3_txt.get_width() // 2, 370))
        screen.blit(footer_txt, (WINDOW_WIDTH // 2 - footer_txt.get_width() // 2, 520))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_KP1]:
                    game_loop("CLASSIC")
                if event.key in [pygame.K_2, pygame.K_KP2]:
                    game_loop("LEVELS")
                if event.key in [pygame.K_3, pygame.K_KP3]:
                    settings_menu()
                if event.key == pygame.K_ESCAPE:
                    return
        clock.tick(30)

def settings_menu():
    global current_control_type
    font_title = pygame.font.Font(None, 42)
    font_options = pygame.font.Font(None, 26)
    font_footer = pygame.font.Font(None, 18)

    while True:
        screen.fill(COLOR_BACKGROUND)
        title_txt = font_title.render("CONTROLS SETTINGS", True, COLOR_MENU_BTN)
        
        c_arrows = COLOR_ACTIVE if current_control_type == "ARROWS" else COLOR_TEXT
        c_wasd = COLOR_ACTIVE if current_control_type == "WASD" else COLOR_TEXT
        c_ijkl = COLOR_ACTIVE if current_control_type == "IJKL" else COLOR_TEXT
        
        opt_arrows = font_options.render("1. Keyboard Arrows [ Up, Down, Left, Right ]", True, c_arrows)
        opt_wasd = font_options.render("2. WASD Layout [ W, S, A, D ]", True, c_wasd)
        opt_ijkl = font_options.render("3. IJKL Layout [ I, K, J, L ]", True, c_ijkl)
        footer_txt = font_footer.render("Press 1, 2 or 3 to change. ESC - Go Back.", True, (120, 120, 120))
        
        screen.blit(title_txt, (WINDOW_WIDTH // 2 - title_txt.get_width() // 2, 120))
        screen.blit(opt_arrows, (WINDOW_WIDTH // 2 - opt_arrows.get_width() // 2, 250))
        screen.blit(opt_wasd, (WINDOW_WIDTH // 2 - opt_wasd.get_width() // 2, 310))
        screen.blit(opt_ijkl, (WINDOW_WIDTH // 2 - opt_ijkl.get_width() // 2, 370))
        screen.blit(footer_txt, (WINDOW_WIDTH // 2 - footer_txt.get_width() // 2, 520))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_KP1]:
                    current_control_type = "ARROWS"
                if event.key in [pygame.K_2, pygame.K_KP2]:
                    current_control_type = "WASD"
                if event.key in [pygame.K_3, pygame.K_KP3]:
                    current_control_type = "IJKL"
                if event.key == pygame.K_ESCAPE:
                    return
        clock.tick(30)

def game_loop(mode):
    snake_pos = [[100, 100], [80, 100], [60, 100]]
    direction = "RIGHT"
    change_to = direction

    food_pos = [
        random.randrange(1, (WINDOW_WIDTH // CELL_SIZE)) * CELL_SIZE,
        random.randrange(2, (WINDOW_HEIGHT // CELL_SIZE)) * CELL_SIZE
    ]
    food_spawn = True
    score = 0
    food_eaten = 0
    binds = CONTROLS_PRESETS[current_control_type]

    while True:
        if mode == "LEVELS":
            level = 1 + (food_eaten // 3)
            current_speed = 9 + (level * 2)
        else:
            level = 1
            current_speed = 12

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == binds["UP"]: change_to = "UP"
                if event.key == binds["DOWN"]: change_to = "DOWN"
                if event.key == binds["LEFT"]: change_to = "LEFT"
                if event.key == binds["RIGHT"]: change_to = "RIGHT"

        if change_to == "UP" and direction != "DOWN": direction = "UP"
        if change_to == "DOWN" and direction != "UP": direction = "DOWN"
        if change_to == "LEFT" and direction != "RIGHT": direction = "LEFT"
        if change_to == "RIGHT" and direction != "LEFT": direction = "RIGHT"

        head_x, head_y = snake_pos[0][0], snake_pos[0][1]
        if direction == "UP": head_y -= CELL_SIZE
        if direction == "DOWN": head_y += CELL_SIZE
        if direction == "LEFT": head_x -= CELL_SIZE
        if direction == "RIGHT": head_x += CELL_SIZE

        new_head = [head_x, head_y]
        snake_pos.insert(0, new_head)

        if head_x == food_pos[0] and head_y == food_pos[1]:
            score += 10
            food_eaten += 1
            food_spawn = False
        else:
            snake_pos.pop()

        if not food_spawn:
            food_pos = [
                random.randrange(1, (WINDOW_WIDTH // CELL_SIZE)) * CELL_SIZE,
                random.randrange(2, (WINDOW_HEIGHT // CELL_SIZE)) * CELL_SIZE
            ]
            food_spawn = True

        if head_x < 0 or head_x >= WINDOW_WIDTH or head_y < 40 or head_y >= WINDOW_HEIGHT:
            break
        if new_head in snake_pos[1:]:
            break

        screen.fill(COLOR_BACKGROUND)
        pygame.draw.line(screen, (60, 60, 60), (0, 40), (WINDOW_WIDTH, 40), 2)
        pygame.draw.rect(screen, COLOR_FOOD, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

        for pos in snake_pos:
            pygame.draw.rect(screen, COLOR_SNAKE, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

        show_interface(score, level, current_speed, mode)
        pygame.display.flip()
        clock.tick(current_speed)

    # После выхода из игрового цикла вызываем окно Game Over
    game_over_screen(score, level, mode)

def game_over_screen(final_score, final_level, mode):
    """
    Новая упрощенная логика: функция только рисует экран смерти один раз 
    и мгновенно засыпает на 3 секунды, после чего автоматически возвращает игрока в меню.
    """
    font_large = pygame.font.Font(None, 56)
    font_small = pygame.font.Font(None, 24)
    
    screen.fill(COLOR_BACKGROUND)
    text_game_over = font_large.render("GAME OVER", True, COLOR_FOOD)
    
    if mode == "LEVELS":
        text_score = font_small.render(f"Final Score: {final_score} (Reached Level {final_level})", True, COLOR_TEXT)
    else:
        text_score = font_small.render(f"Final Score: {final_score}", True, COLOR_TEXT)
        
    text_restart = font_small.render("Returning to Main Menu in 3 seconds...", True, COLOR_TEXT)
    
    screen.blit(text_game_over, (WINDOW_WIDTH // 2 - text_game_over.get_width() // 2, 200))
    screen.blit(text_score, (WINDOW_WIDTH // 2 - text_score.get_width() // 2, 280))
    screen.blit(text_restart, (WINDOW_WIDTH // 2 - text_restart.get_width() // 2, 350))
    
    pygame.display.flip()
    
    # Принудительная задержка экрана смерти, никаких кнопок нажимать не нужно
    time.sleep(3)

# Точка входа в программу — ровный линейный блок без вложений
if __name__ == "__main__":
    main_menu()
    pygame.quit()
    sys.exit()
