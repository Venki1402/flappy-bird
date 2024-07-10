import pygame, sys, random
from pygame.locals import *

class Player:
    def __init__(self, x, y):
        self.sprite = pygame.image.load('bird.png')
        self.rect = pygame.Rect(x, y, self.sprite.get_width(), self.sprite.get_height())
        self.velocity = 5

class Pipe:
    def __init__(self, y, height, isUpperPipe):
        temp = pygame.image.load('pipe.png')
        if isUpperPipe:
            temp = pygame.transform.flip(temp, False, True)
        self.sprite = pygame.transform.scale(temp, (temp.get_width(), height))
        self.rect = pygame.Rect(screen_width, y, self.sprite.get_width(), height)
        self.velocity = -5

class ScorePipe:
    def __init__(self, x):
        self.rect = pygame.Rect(x, 0, 1, screen_height)
        self.velocity = -5
        self.passed = False

pygame.init()

screen_width = 1280
screen_height = 720
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (screen_width, screen_height)) 

screen = pygame.display.set_mode((screen_width, screen_height), SCALED, vsync=True)

clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

player = Player(100, 100)

gravity = 0.5

pipes = []

def create_pipes():
    height1 = random.randint(0, screen_height - (int(screen_height/2)))
    height2 = screen_height - (height1 + 250)
    pipe1 = Pipe(0, height1, True)
    pipe2 = Pipe(height1 + 250, height2, False)
    score_pipe = ScorePipe(screen_width + pipe1.sprite.get_width())
    pipes.append(pipe1)
    pipes.append(pipe2)
    pipes.append(score_pipe)
    

ADD_PIPE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_PIPE_EVENT, 1200)

game_over = False
score = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    # Restart the game
                    player.rect.y = 100
                    player.velocity = 0
                    pipes = []
                    game_over = False
                    score = 0
                else:
                    player.velocity = -10
        if event.type == ADD_PIPE_EVENT and not game_over:
            create_pipes()

    if not game_over:
        player.velocity += gravity

        if player.rect.y + player.rect.height < screen_height:
            player.rect.y += player.velocity

        for pipe in pipes:
            pipe.rect.x += pipe.velocity
            if isinstance(pipe, ScorePipe) and not pipe.passed and player.rect.left > pipe.rect.right:
                score += 1
                pipe.passed = True

        # Collision detection
        for pipe in pipes:
            if not isinstance(pipe, ScorePipe) and player.rect.colliderect(pipe.rect):
                game_over = True

        if player.rect.y + player.rect.height >= screen_height:
            game_over = True

        # Remove pipes that are off-screen
        pipes = [pipe for pipe in pipes if pipe.rect.right > 0]

    screen.fill(white)
    screen.blit(background, (0, 0))

    # Always draw pipes and player
    for pipe in pipes:
        if not isinstance(pipe, ScorePipe):
            screen.blit(pipe.sprite, pipe.rect)
    screen.blit(player.sprite, player.rect)

    if game_over:
        # Display "Game Over" in red color
        font = pygame.font.Font(None, 102)
        text = font.render("Game Over!!", True, red)
        text_rect = text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(text, text_rect)

        # Display "Press space to restart" in blue color and small size below
        font = pygame.font.Font(None, 24)
        restart_text = font.render("Press space to restart", True, blue)
        restart_text_rect = restart_text.get_rect(center=(screen_width/2, screen_height/2 + 50))
        screen.blit(restart_text, restart_text_rect)

    # Display the score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)