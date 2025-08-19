import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 7

# Ball settings
BALL_SIZE = 20
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Score variables
score_left = 0
score_right = 0
font = pygame.font.SysFont('Arial', 36)

# Create paddles as rectangles
left_paddle = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create ball as a rectangle
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y

# Function to draw all game elements
def draw():
    SCREEN.fill(BLACK)  # Fill background
    pygame.draw.rect(SCREEN, WHITE, left_paddle)  # Draw left paddle
    pygame.draw.rect(SCREEN, WHITE, right_paddle)  # Draw right paddle
    pygame.draw.ellipse(SCREEN, WHITE, ball)  # Draw ball
    pygame.draw.aaline(SCREEN, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))  # Draw center line
    score_text = font.render(f"{score_left}   {score_right}", True, WHITE)
    SCREEN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))  # Display score
    pygame.display.flip()  # Update display

# Function to reset ball position and direction after a score
def reset_ball():
    global ball_dx, ball_dy
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_dx *= -1  # Change direction
    ball_dy = BALL_SPEED_Y if ball_dy > 0 else -BALL_SPEED_Y

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Paddle movement controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED  # Move left paddle up
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED  # Move left paddle down
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED  # Move right paddle up
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED  # Move right paddle down

    # Ball movement
    ball.x += ball_dx
    ball.y += ball_dy

    # Ball collision with top/bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1  # Reverse vertical direction

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_dx *= -1  # Reverse horizontal direction

    # Score update and ball reset
    if ball.left <= 0:
        score_right += 1
        reset_ball()
    if ball.right >= WIDTH:
        score_left += 1
        reset_ball()

    draw()  # Draw everything
    clock.tick(60)  # Limit to 60 FPS
