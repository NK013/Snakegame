import time
import colours
import pygame

from random import randint

WINDOW_HEIGHT = 600 #840
WINDOW_WIDTH = 900 #800
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

clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_DIMENSIONS)


def draw_start_menu():
    screen.fill((0, 0, 0))
    info = font.render("Drücke 'SPACE', um das Spiel zu starten!", True, (255, 255, 255))
    with open('datafile.yml','r') as f:
        data = f.read()
    highscore = font.render(f"Highscore: {data}", True, (255, 255, 255))
    screen.blit(info, (WINDOW_WIDTH/2 - info.get_width()/2, WINDOW_HEIGHT/2 + info.get_height()/2))
    screen.blit(highscore, (WINDOW_WIDTH/2 - highscore.get_width()/2, WINDOW_HEIGHT/2 + info.get_height()*2 + highscore.get_height()/2))
    pygame.display.update()


def check_collisions(snake_positions):
    head_x_position, head_y_position = snake_positions[0]

    return (
        head_x_position in (-20, WINDOW_WIDTH )
        or head_y_position in (-20, WINDOW_HEIGHT) #20
        or (head_x_position, head_y_position) in snake_positions[1:]
    )


def check_food_collision(snake_positions, food_position):
    if snake_positions[0] == food_position:
        snake_positions.append(snake_positions[-1])

        return True


def draw_objects(snake_positions, food_position):
    pygame.draw.rect(screen, colours.FOOD, [food_position, (SEGMENT_SIZE, SEGMENT_SIZE)])

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
    #print(f"Key num: {key}")
    new_direction = KEY_MAP.get(key)

    all_directions = ("Up", "Down", "Left", "Right")
    opposites = ({"Up", "Down"}, {"Left", "Right"})

    if (new_direction in all_directions
    and {new_direction, current_direction} not in opposites):
        return new_direction

    return current_direction


def set_new_food_position(snake_positions):
    while True:
        x_position = randint(0, 40) * SEGMENT_SIZE #x_position = randint(0, 39) * SEGMENT_SIZE
        y_position = randint(2, 28) * SEGMENT_SIZE #y_position = randint(2, 41) * SEGMENT_SIZE
        food_position = (x_position, y_position)

        if food_position not in snake_positions:
            return food_position


def gameover(score):
    print()
    print("🐍 > Du hast verloren!")
    print("🐍 > Deine Punkte: " + str(score))
    print()

    with open('datafile.yml','r') as f:
        data = f.read()

    if int(data) < score:
        new_data = score

        with open('datafile.yml','w') as f:
            f.write(str(new_data))

        print("🐍 > Du hast einen neuen Highscore aufgestellt!")
        print("🐍 > Ehemaliger Highscore: " + data)
        print("🐍 > Neuer Highscore: " + str(new_data))
        print()

        
def play_game():
    game_state = "start_menu"
    score = 0

    current_direction = "Down"
    snake_positions = [(100, 100), (80, 100), (60, 100), (40, 100)]
    food_position = set_new_food_position(snake_positions)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("🐍 > Spiel abgebrochen!")
                print()
                return
            if event.type == pygame.KEYDOWN:
                    current_direction = on_key_press(event, current_direction)
                    #print(f"Key pressed: '{pygame.key.name(event.key)}'")  

        keys = pygame.key.get_pressed()

        if game_state == "start_menu":
            draw_start_menu()
            if keys[pygame.K_SPACE]:
                game_state = "game"
  
        if game_state == "game":

            if keys[pygame.K_ESCAPE]:
                gameover(score)
                game_state = "start_menu"

            screen.fill(colours.BACKGROUND)
            draw_objects(snake_positions, food_position)

        
            scoreText = font.render(f"Punkte: {score}", True, colours.TEXT)
            screen.blit(scoreText, (20, 20))

            pygame.display.update()

            move_snake(snake_positions, current_direction)

            if check_collisions(snake_positions):
                gameover(score)
                return

            if check_food_collision(snake_positions, food_position):
                food_position = set_new_food_position(snake_positions)
                score += 1

            clock.tick(11) #speed

print()
print("🐍 > Spiel startet ...")

play_game()