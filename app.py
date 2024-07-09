import colours
import pygame

from random import randint

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 900
WINDOW_DIMENSIONS = WINDOW_WIDTH, WINDOW_HEIGHT

SEGMENT_SIZE  =  20

KEY_MAP = {
    119: "Up",
    115: "Down",
    100: "Right",
    97: "Left"
}

pygame.init()
pygame.display.set_caption("🐍   Snake   🐍")

font = pygame.font.Font(None, 28)
titleFont = pygame.font.Font(None, 42)

clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_DIMENSIONS)


def draw_start_menu():
    screen.fill(colours.BACKGROUND_STARTMENU)
    info = font.render("Drücke 'SPACE', um das Spiel zu starten!", True, colours.TEXT)
    with open('datafile.yml','r') as f:
        data = f.read()
    highscore = font.render(f"Highscore: {data}", True, colours.TEXT)
    help = font.render("Bewegen:   [W - Oben]  [S - Unten]  [A - Links]  [D - Rechts]", True, colours.TEXT)
    screen.blit(info, (WINDOW_WIDTH/2 - info.get_width()/2, WINDOW_HEIGHT/2 + info.get_height()/2))
    screen.blit(highscore, (WINDOW_WIDTH/2 - highscore.get_width()/2, WINDOW_HEIGHT/2 + info.get_height()*2 + highscore.get_height()/2))
    screen.blit(help, (WINDOW_WIDTH/4 - info.get_width()/2, WINDOW_HEIGHT/1.1 + info.get_height()/2))
    pygame.display.update()

def draw_pause_menu(score):
    screen.fill(colours.BACKGROUND_PAUSE)
    title = titleFont.render("Pausiert", True, colours.TEXT)
    scoreText = font.render(f"Deine Punkte: {score}", True, colours.TEXT)
    restart_button = font.render("R - Neustart", True, colours.TEXT)
    quit_button = font.render("Q - Verlassen", True, colours.TEXT)
    startmenu_button = font.render("E - Startmenu", True, colours.TEXT)
    continue_button = font.render("SPACE - Weiter", True, colours.TEXT)
    screen.blit(title, (WINDOW_WIDTH/2 - title.get_width()/2, WINDOW_HEIGHT/2 - title.get_height()*6))
    screen.blit(scoreText, (WINDOW_WIDTH/2 - scoreText.get_width()/2, WINDOW_HEIGHT/2 - scoreText.get_height()*2.25))
    screen.blit(restart_button, (WINDOW_WIDTH/2 - restart_button.get_width()/2, WINDOW_HEIGHT/1.9 + restart_button.get_height()))
    screen.blit(quit_button, (WINDOW_WIDTH/2 - quit_button.get_width()/2, WINDOW_HEIGHT/2 + quit_button.get_height()/2))
    screen.blit(startmenu_button, (WINDOW_WIDTH/2 - startmenu_button.get_width()/2, WINDOW_HEIGHT/2 + startmenu_button.get_height()*3))
    screen.blit(continue_button, (WINDOW_WIDTH/2 - continue_button.get_width()/2, WINDOW_HEIGHT/2 + continue_button.get_height()*5))
    pygame.display.update()

def draw_game_over_screen(score):
    screen.fill(colours.BACKGROUND_GAMEOVER)
    title = titleFont.render("Verloren", True, colours.TEXT)
    scoreText = font.render(f"Deine Punkte: {score}", True, colours.TEXT)
    restart_button = font.render("R - Neustart", True, colours.TEXT)
    quit_button = font.render("Q - Verlassen", True, colours.TEXT)
    screen.blit(title, (WINDOW_WIDTH/2 - title.get_width()/2, WINDOW_HEIGHT/2 - title.get_height()*6))
    screen.blit(scoreText, (WINDOW_WIDTH/2 - scoreText.get_width()/2, WINDOW_HEIGHT/2 - scoreText.get_height()*2.25))
    screen.blit(restart_button, (WINDOW_WIDTH/2 - restart_button.get_width()/2, WINDOW_HEIGHT/1.9 + restart_button.get_height()))
    screen.blit(quit_button, (WINDOW_WIDTH/2 - quit_button.get_width()/2, WINDOW_HEIGHT/2 + quit_button.get_height()/2))
    with open('datafile.yml','r') as f:
        data = f.read()
    score = int(score)
    if int(data) < score:
        highscore = font.render("Neuer Highscore!", True, colours.TEXT)
        screen.blit(highscore, (WINDOW_WIDTH/2 - highscore.get_width()/2, WINDOW_HEIGHT/2 - highscore.get_height()*3.5))
    pygame.display.update()


def check_collisions(snake_positions):
    head_x_position, head_y_position = snake_positions[0]

    return (
        head_x_position in (-20, WINDOW_WIDTH )
        or head_y_position in (-20, WINDOW_HEIGHT)
        or (head_x_position, head_y_position) in snake_positions[1:]
    )

def check_food_collision(snake_positions, food_position):
    if snake_positions[0] == food_position:
        snake_positions.append(snake_positions[-1])

        return True


def draw_objects(snake_positions, food_position_1, food_position_2):
    pygame.draw.rect(screen, colours.FOOD, [food_position_1, (SEGMENT_SIZE, SEGMENT_SIZE)])
    pygame.draw.rect(screen, colours.FOOD, [food_position_2, (SEGMENT_SIZE, SEGMENT_SIZE)])

    for x, y in snake_positions:
        pygame.draw.rect(screen, colours.SNAKE, [x, y, SEGMENT_SIZE, SEGMENT_SIZE])


def move_snake(snake_positions, direction):
    head_x_position, head_y_position = snake_positions[0]

    if direction == "Left":
        new_head_position = (head_x_position - SEGMENT_SIZE, head_y_position)
    elif direction == "Right":
        new_head_position = (head_x_position + SEGMENT_SIZE, head_y_position)
    elif direction == "Down":
        new_head_position = (head_x_position, head_y_position + SEGMENT_SIZE)
    elif direction == "Up":
        new_head_position = (head_x_position, head_y_position - SEGMENT_SIZE)

    snake_positions.insert(0, new_head_position)
    del snake_positions[-1]


def on_key_press(event, current_direction):
    key = event.__dict__["key"]
    new_direction = KEY_MAP.get(key)

    all_directions = ("Up", "Down", "Left", "Right")
    opposites = ({"Up", "Down"}, {"Left", "Right"})

    if (new_direction in all_directions
    and {new_direction, current_direction} not in opposites):
        return new_direction

    return current_direction


def set_new_food_position(snake_positions):
    while True:
        x_position = randint(0, 40) * SEGMENT_SIZE
        y_position = randint(2, 28) * SEGMENT_SIZE
        food_position = (x_position, y_position)

        if food_position not in snake_positions:
            return food_position


def save_highscore(score):
    with open('datafile.yml','r') as f:
        data = f.read()
    score = int(score)
    if int(data) < score:
        new_data = score
        with open('datafile.yml','w') as f:
            f.write(str(new_data))

def play_game(state):
    game_state = state
    score = 0

    current_direction = "Down"
    snake_positions = [(100, 100), (80, 100), (60, 100), (40, 100)]
    food_position_1 = set_new_food_position(snake_positions)
    food_position_2 = set_new_food_position(snake_positions)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_highscore(score)
                print("🐍 > Spiel abgebrochen!")
                print()
                pygame.quit()
                quit()
                return
            if event.type == pygame.KEYDOWN:
                    current_direction = on_key_press(event, current_direction)

        if game_state == "start_menu":
            draw_start_menu()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game_state = "game"

        if game_state == "pause_menu":
            draw_pause_menu(score)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                save_highscore(score)
                play_game("game")
            if keys[pygame.K_q]:
                save_highscore(score)
                print()
                print("🐍 > Spiel wird geschlossen!")
                print()
                pygame.quit()
                quit()
            if keys[pygame.K_e]:
                save_highscore(score)
                play_game("start_menu")
            if keys[pygame.K_SPACE]:
                game_state = "game"

        if game_state == "game_over":
            draw_game_over_screen(score)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                save_highscore(score)
                play_game("game")
            if keys[pygame.K_q]:
                save_highscore(score)
                print()
                print("🐍 > Spiel wird geschlossen!")
                print()
                pygame.quit()
                quit()
  
        if game_state == "game":
            screen.fill(colours.BACKGROUND)
            draw_objects(snake_positions, food_position_1, food_position_2)
        
            scoreText = font.render(f"Punkte: {score}", True, colours.TEXT)
            screen.blit(scoreText, (20, 20))

            pygame.display.update()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                game_state = "pause_menu"

            move_snake(snake_positions, current_direction)

            if check_collisions(snake_positions):
                game_state = "game_over"

            if check_food_collision(snake_positions, food_position_1):
                food_position_1 = set_new_food_position(snake_positions)
                score += 1
            if check_food_collision(snake_positions, food_position_2):
                food_position_2 = set_new_food_position(snake_positions)
                score += 1

            clock.tick(11)

print()
print("🐍 > Spiel wird startet ...")
print()

play_game("start_menu")
