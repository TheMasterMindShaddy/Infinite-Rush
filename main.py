import pygame
import random
import os
import sys

pygame.init()

def resource_path(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.abspath("."), path)

# Music
pygame.mixer.init()
pygame.mixer.music.load(resource_path("sounds/bgm.mp3"))
game_over_sound = pygame.mixer.Sound(resource_path("sounds/gameover.mp3"))

screen_width = 700
screen_height = 900

gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Infinite Rush - By Lucky / The Master Mind Shaddy")

pygame_icon = pygame.image.load(resource_path("assets/icon.png")).convert_alpha()
pygame.display.set_icon(pygame_icon)

main_menu = pygame.image.load(resource_path("assets/mainmenu.png")).convert_alpha()
main_menu = pygame.transform.scale(main_menu, (screen_width, screen_height))

bgimg = pygame.image.load(resource_path("assets/bg.png")).convert()
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height))

car = pygame.image.load(resource_path("assets/car.png")).convert_alpha()
car = pygame.transform.scale(car, (70, 130))

obs = pygame.image.load(resource_path("assets/obs.png")).convert_alpha()
obs = pygame.transform.scale(obs, (90,140))

obs2 = pygame.image.load(resource_path("assets/obs2.png")).convert_alpha()
obs2 = pygame.transform.scale(obs2, (180,220))


# Colors
white = (255, 255, 255)
red = (255, 0, 0)
aqua = (0,255,255)

# Font
font = pygame.font.SysFont(None, 55)


def playButton(x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()

    if button_rect.collidepoint(mouse_pos):
        if mouse_clicked[0]:
            return True

    text = font.render("Play", True, aqua)
    text_rect = text.get_rect(center=button_rect.center)
    gameWindow.blit(text, text_rect)
    return False

def mainMenu():
    save_folder = "saves"
    save_file = os.path.join(save_folder, "save.txt")

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    if not os.path.exists(save_file):
        with open(save_file, 'w') as f:
            f.write("High-Score: 0")

    with open(save_file, 'r') as f:
        global highscore
        highscore = int(f.read().split(":")[1].strip())

    game_exit = False
    pygame.mixer.music.play(-1)

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
        gameWindow.blit(main_menu, (0,0))
        if playButton(300, 450, 100, 60):
            gameLoop()
        pygame.display.update()
    pygame.quit()
    sys.exit()

def displayScore(score):
    box = pygame.Surface((70, 75), pygame.SRCALPHA)
    box.fill((0, 0, 0, 100))
    gameWindow.blit(box, (15, 15))

    small_font = pygame.font.SysFont(None, 25)
    score_font = pygame.font.SysFont(None, 45)

    label = small_font.render("SCORE", True, (200, 200, 200))
    number = score_font.render(str(score), True, (255, 255, 255))

    gameWindow.blit(label, (25, 20))
    gameWindow.blit(number, (25, 40))

def displayHighScore(highscore):
    box = pygame.Surface((85,75), pygame.SRCALPHA)
    box.fill((0, 0, 0, 100))
    gameWindow.blit(box, (600, 15))

    small_font = pygame.font.SysFont(None, 25)
    large_font = pygame.font.SysFont(None, 45)

    label = small_font.render("Highscore", True, white)
    number = large_font.render(str(highscore), True, white)

    gameWindow.blit(label, (600, 20))
    gameWindow.blit(number, (600, 40))

def GameOver(score):
    box = pygame.Surface((530, 80), pygame.SRCALPHA)
    box.fill((0, 0, 0, 100))
    box_rect = box.get_rect(topleft = (100, 400))
    gameWindow.blit(box, box_rect)

    text = font.render(f"Game Over!! Your Score is: {str(score)}", True, aqua)
    text_rect = text.get_rect(center = box_rect.center)
    gameWindow.blit(text, text_rect)

    retry_rect = pygame.Rect(275, 510, 150, 60)
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()

    if retry_rect.collidepoint(mouse_pos):
        pygame.draw.rect(gameWindow, red, retry_rect)
        if mouse_clicked[0]:
            mainMenu()
    retry = font.render("Retry", True, white)
    retry_rect = retry.get_rect(center = retry_rect.center)
    gameWindow.blit(retry, retry_rect)

# Game Loop
def gameLoop():
    global highscore
    game_exit = False
    game_over = False
    score_increase = True

    # Background position
    bg_y = 0
    bg_speed = 5
    bg_speed_increae = 0
    should_increase = True

    # Car
    car_x = 200
    car_y = 650
    car_velo = 15

    # Obstacles
    obs_x = random.randint(130,500)
    obs_y = random.randint(-200, 0)
    obs_speed = 15

    # Obstacle Truck
    obs2_x = 0
    obs2_y = 0
    obs2_speed = 15
    truck_spawn = False
    truck_spawn_clock = 0

    # Score
    score = 0
    score_timer = 0

    clock = pygame.time.Clock()  

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                car_y -= car_velo

            if keys[pygame.K_DOWN]:
                car_y += car_velo

            if keys[pygame.K_LEFT]:
                car_x -= car_velo

            if keys[pygame.K_RIGHT]:
                car_x += car_velo
            
        # Move background down
        bg_y += bg_speed
        
        if should_increase:
            bg_speed_increae += clock.get_time()
            if bg_speed_increae > 5000:
                bg_speed += 1
                obs_speed += 1
                obs2_speed += 1
                bg_speed_increae = 0
            if score == 350:
                should_increase = False
                obs_speed = 25
                obs2_speed = 25


        # Moving The Obstacle
        obs_y += obs_speed
        if obs_y > 1000:
            obs_x = random.randint(130,500)
            obs_y = random.randint(-200, -100)

        # Moving The Truck
        truck_spawn_clock += clock.get_time()
        if not truck_spawn and truck_spawn_clock > 5000:
            obs2_x = random.randint(80,450)
            obs2_y = random.randint(-350,-250)
            truck_spawn = True
            truck_spawn_clock = 0

        if truck_spawn:
            obs2_y += obs2_speed

            if obs2_y > 1000:
                truck_spawn = False

        # Reset Background Position
        if bg_y >= screen_height:
            bg_y = 0

        # Calculating The Score
        if score_increase:
            score_timer += clock.get_time()
            if score_timer >= 100:
                score+=1
                score_timer = 0


        # If the Car exceeds the road
        if car_x < 130 or car_x > 500 or car_y < 0 or car_y > 770:
            if car_x < 130:
                car_x = 130
            if car_x > 500:
                car_x = 500
            if car_y < 0:
                car_y = 0
            if car_y > 770:
                car_y = 770

        # Car and Obstacle Collition
        car_rect = pygame.Rect(car_x + 5, car_y + 5, 60, 120)
        obs_rect = pygame.Rect(obs_x + 15, obs_y+ 10, 60, 120)
        obs2_rect = pygame.Rect(obs2_x + 50, obs2_y, 80, 210)

        if obs_rect.colliderect(obs2_rect):
            obs2_x = random.randint(80,450)
            obs2_y = random.randint(-350, -250)

        if not game_over and (car_rect.colliderect(obs_rect) or car_rect.colliderect(obs2_rect)):
            if keys[pygame.K_LSHIFT]:
                pass
            else:
                pygame.mixer.music.stop()
                game_over_sound.play()
                obs_speed = 0
                bg_speed = 0
                obs2_speed = 0
                should_increase = False
                score_increase = False
                if score > highscore:
                    highscore = score
                    with open("saves/save.txt", 'w') as f:
                        f.write(f"High-Score: " + str(highscore))
                game_over = True

        # Draw two backgrounds
        gameWindow.blit(bgimg, (0, bg_y))
        gameWindow.blit(bgimg, (0, bg_y - screen_height))

        # Plotting The Game's Obstacle Car
        gameWindow.blit(obs, (obs_x, obs_y))

        # Plotting The Game's Obstacle Truck
        if truck_spawn:
            gameWindow.blit(obs2, (obs2_x, obs2_y))

        # Plotting and Control Of The Car
        gameWindow.blit(car,(car_x,car_y))

        # Displaying Of The Score and The HighScore
        displayScore(score)
        displayHighScore(highscore)

        # Displaying the Game_Over Text
        if game_over:
            GameOver(score)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()
    sys.exit()

mainMenu()