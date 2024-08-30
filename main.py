import pygame
import sys
import random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60


class Gun(pygame.sprite.Sprite):
    def __init__(self, img_path, sound_path):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(img_path), (30, 30))
        self.shot = pygame.mixer.Sound(sound_path)
        self.rect = self.image.get_rect()

    def shoot(self):
        self.shot.play()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Bullseye(pygame.sprite.Sprite):
    def __init__(self, img_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(img_path), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.speed_x = random.uniform(1, 3)
        self.speed_y = random.uniform(1, 3)

    def update(self):
        # bullseye movement
        self.rect.x += self.speed_x * self.direction_x
        self.rect.y += self.speed_y * self.direction_y

        # wrap around screen edge
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction_x *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.direction_y *= -1

        # keep the bullseye on the window
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))


class Chicken(pygame.sprite.Sprite):
    def __init__(self, img_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(img_path), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.speed_x = random.uniform(1, 3)
        self.speed_y = random.uniform(1, 3)

    def update(self):
        # bullseye movement
        self.rect.x += self.speed_x * self.direction_x
        self.rect.y += self.speed_y * self.direction_y

        # wrap around screen edge
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction_x *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.direction_y *= -1

        # keep the bullseye on the window
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))


def generate_bullseye(num_bullseye):
    for _ in range(num_bullseye):
        bullseye = Bullseye("src/bullseye.png", 0, 0)

        while True:
            halved_bulls_width = bullseye.rect.width // 2
            halved_bulls_height = bullseye.rect.height // 2

            # new bullseye x and y position
            new_bulls_x = random.randrange(halved_bulls_width, SCREEN_WIDTH - halved_bulls_width)
            new_bulls_y = random.randrange(halved_bulls_height+100, SCREEN_HEIGHT - halved_bulls_height)
            bullseye.rect.center = [new_bulls_x, new_bulls_y]

            # check collision between objects
            if not pygame.sprite.spritecollideany(bullseye, bullseye_group) and not pygame.sprite.spritecollideany(
                    bullseye, chicken_group):
                break

        bullseye_group.add(bullseye)


def generate_chicken(num_chicken):
    for c in range(num_chicken):
        chicken = Chicken("src/hen.png", 0, 0)

        while True:
            halved_chicken_width = chicken.rect.width // 2
            halved_chicken_height = chicken.rect.height // 2

            # new chicken x and y position
            new_chicken_x = random.randrange(halved_chicken_width, SCREEN_WIDTH - halved_chicken_width)
            new_chicken_y = random.randrange(halved_chicken_height+100, SCREEN_HEIGHT - halved_chicken_height)
            chicken.rect.center = [new_chicken_x, new_chicken_y]

            # check collision between objects
            if not pygame.sprite.spritecollideany(chicken, bullseye_group) and not pygame.sprite.spritecollideany(
                    chicken, chicken_group):
                break

        chicken_group.add(chicken)


pygame.init()
clock = pygame.time.Clock()

score = 0
running = True
main_menu_screen = True
main_menu_song = False
game_state_screen = False
game_over_screen = False
game_over_song = False

# window settings
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Don't Shoot Your Chicken")
pygame.display.set_icon(pygame.image.load("src/deadchicken.png"))

# backgrounds
background = pygame.transform.scale(pygame.image.load("src/background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
game_over_background = pygame.transform.scale(pygame.image.load("src/gameover.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
pygame.mouse.set_visible(False)

# main menu pic
dead_chicken = pygame.transform.scale(pygame.image.load("src/deadchicken.png"), (200, 200)).convert_alpha()
dead_chicken_rect = dead_chicken.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-30))

# gun
gun = Gun("src/gun.png", "src/gunshot.mp3")
gun_group = pygame.sprite.Group()
gun_group.add(gun)

# bullseye and chicken group
bullseye_group = pygame.sprite.Group()
chicken_group = pygame.sprite.Group()

# bullseye
generate_bullseye(10)

# chicken loop
generate_chicken(1)

# fonts
pygame.font.init()
text_font = pygame.font.SysFont('Comic Sans MS', 30)
title_font = pygame.font.SysFont('Comic Sans MS', 50)

# sounds
pygame.mixer.init()
main_menu_sound = pygame.mixer.Sound("src/gamestart.mp3")
game_over_sound = pygame.mixer.Sound("src/gameover.mp3")

# game loop
while running:
    # title text
    title_surface = title_font.render("Don't Shoot Your Chicken", False, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 50))

    # main menu text
    main_menu_surface = text_font.render('Press Enter to start', False, (255, 255, 255))
    main_menu_rect = main_menu_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+100))

    # score text
    score_surface = text_font.render(f'Score: {score}', False, (255, 255, 255))

    # game over text
    total_score = text_font.render(f'Score: {score}', False, (0, 0, 0))
    total_score_rect = total_score.get_rect(center=(SCREEN_WIDTH//2, 100))
    game_over_surface = text_font.render('YOUR CHICKEN IS DEAD!', False, (0, 0, 0))
    game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+100))
    back_menu_surface = text_font.render('Press Enter to main menu', False, (0, 0, 0))
    back_menu_rect = back_menu_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+150))

    # game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            gun.shoot()
            if pygame.sprite.spritecollide(gun, bullseye_group, True):
                score += 10
            elif pygame.sprite.spritecollide(gun, chicken_group, True):
                game_over_screen = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if main_menu_screen:
                    main_menu_screen = False
                    game_state_screen = True
                    score = 0  # reset score
                    bullseye_group.empty()  # clear previous sprites
                    chicken_group.empty()
                    generate_bullseye(10)  # regenerate game objects
                    generate_chicken(1)
                    game_over_song = False
                    main_menu_song = False
                elif game_over_screen:
                    game_over_screen = False
                    main_menu_screen = True
                    game_over_song = False
                    main_menu_song = False

    # generate new groups of bullseye after all are shot
    if len(bullseye_group) == 0:
        generate_bullseye(10)
        generate_chicken(1)

        # we have 20 chicken maximum
        if len(chicken_group) >= 20:
            generate_chicken(0)

    pygame.display.flip()

    if main_menu_screen:
        window.blit(background, (0, 0))
        window.blit(title_surface, title_rect)
        window.blit(main_menu_surface, main_menu_rect)
        window.blit(dead_chicken, dead_chicken_rect)
        if not main_menu_song:
            main_menu_sound.play()
            main_menu_song = True
    elif game_state_screen and not game_over_screen:
        game_state_screen = True
        window.blit(background, (0, 0))
        window.blit(score_surface, (0, 0))
        # bullseye
        bullseye_group.draw(window)
        bullseye_group.update()
        # chicken
        chicken_group.draw(window)
        chicken_group.update()
        # gun
        gun_group.draw(window)
        gun_group.update()
    elif game_over_screen:
        window.blit(game_over_background, (0, 0))
        window.blit(total_score, total_score_rect)
        window.blit(game_over_surface, game_over_rect)
        window.blit(back_menu_surface, back_menu_rect)
        if not game_over_song:
            game_over_sound.play()
            game_over_song = True

    clock.tick(FPS)
