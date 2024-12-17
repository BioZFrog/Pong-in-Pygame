import pygame  
import random  

pygame.init()  # Initialize Pygame

# Variables
screen = pygame.display.set_mode((400, 300))  # Set screen size
pygame.display.set_caption("Pong Game")  # Set the window title
clock = pygame.time.Clock()  # Create a clock object to control frame rate

# Player positions and scores
player1_score = 0
player1_pos_x = 10
player1_pos_y = 100
player2_score = 0
player2_pos_x = 385
player2_pos_y = 100
game_scene = "menu"  # Initialize to menu scene

font = pygame.font.Font(None, 50)  # Set font for text rendering
WHITE = (255, 255, 255)  # Define white color

# Player classes for player 1 and player 2
class Player():
    def __init__(self, width, height):
        self.x = player1_pos_x  # Set player 1's x position
        self.y = player1_pos_y  # Set player 1's y position
        self.width = width  # Set player 1's width
        self.height = height  # Set player 1's height

player = Player(5, 50)  # Instantiate player 1

class Player2():
    def __init__(self, width, height):
        self.x = player2_pos_x  # Set player 2's x position
        self.y = player2_pos_y  # Set player 2's y position
        self.width = width  # Set player 2's width
        self.height = height  # Set player 2's height

player2 = Player2(5, 50)  # Instantiate player 2

# Ball setup
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)  # Center ball
ball_velocity = pygame.Vector2(-150, 150)  # Ball velocity

# Menu Scene function
def show_menu():
    screen.fill((0, 0, 0))  # Fill screen with black
    title_text = font.render("START MENU", True, WHITE)  # Title text
    start_text = font.render("Press ENTER to Play", True, WHITE)  # Start instruction
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 200))  # Center title
    screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, 300))  # Center start instruction

# GameOver Scene function
def show_gameover():
    screen.fill((0, 0, 0))  # Fill screen with black
    if player1_score == 3 > player2_score:
        game_over_text = font.render("Player 1 Won!", True, WHITE)  # Display winner
    elif player2_score == 3 > player1_score:
        game_over_text = font.render("Player 2 Won!", True, WHITE)  # Display winner
    elif player1_score == 3 == player2_score == 3:
        game_over_text = font.render("It's a Draw!", True, WHITE)  # Display draw
    screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 100))  # Center text
    # Display score and restart/quit options
    screen.blit(font.render(f"Player 1 Score: {player1_score}", True, WHITE), (100, 150))
    screen.blit(font.render(f"Player 2 Score: {player2_score}", True, WHITE), (screen.get_width() - 200, 150))

# Main game loop
running = True
while running:
    dt = clock.tick(60) / 1000  # Time delta to ensure frame-rate independent movement

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit game if the close button is pressed

    keys = pygame.key.get_pressed()  # Get all pressed keys

    if game_scene == 'menu':  # Menu scene
        show_menu()
        if keys[pygame.K_RETURN]:  # Start game if ENTER is pressed
            game_scene = "gameplay"  # Switch to gameplay scene
            player1_score = 0  # Reset scores
            player2_score = 0
            ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)  # Reset ball position
            ball_velocity = pygame.Vector2(-150, 150)  # Reset ball velocity

    elif game_scene == 'gameplay':  # Gameplay scene
        # Player 1 movement
        if keys[pygame.K_w] and player.y > 0:
            player.y -= 300 * dt  # Move up
        if keys[pygame.K_s] and player.y < screen.get_height() - player.height:
            player.y += 300 * dt  # Move down

        # Player 2 movement
        if keys[pygame.K_UP] and player2.y > 0:
            player2.y -= 300 * dt  # Move up
        if keys[pygame.K_DOWN] and player2.y < screen.get_height() - player2.height:
            player2.y += 300 * dt  # Move down

        ball_pos += ball_velocity * dt  # Update ball position

        # Ball collision with player 1
        if (ball_pos.x - 5 < player.x + player.width and
            ball_pos.x + 5 > player.x and
            ball_pos.y + 5 > player.y and
            ball_pos.y - 5 < player.y + player.height):
            ball_velocity.x = -ball_velocity.x  # Bounce off player 1
            ball_velocity.y += random.uniform(-50, 1)  # Add randomness

        # Ball collision with player 2
        if (ball_pos.x - 5 < player2.x + player2.width and
            ball_pos.x + 5 > player2.x and
            ball_pos.y + 5 > player2.y and
            ball_pos.y - 5 < player2.y + player2.height):
            ball_velocity.x = -ball_velocity.x  # Bounce off player 2
            ball_velocity.y += random.uniform(-50, 10)  # Add randomness

        if ball_pos.y < 0 or ball_pos.y > screen.get_height():  # Ball hits top or bottom
            ball_velocity.y = -ball_velocity.y
            ball_velocity.x += random.uniform(-50, 10)  # Add randomness

        if ball_pos.x < 0:  # Player 2 scores
            player2_score += 1
            ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)  # Reset ball
            ball_velocity = pygame.Vector2(-150, 150)  # Reset velocity

        if ball_pos.x > screen.get_width():  # Player 1 scores
            player1_score += 1
            ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)  # Reset ball
            ball_velocity = pygame.Vector2(-150, 150)  # Reset velocity

        # Drawing the game elements
        screen.fill((0, 0, 0))  # Clear screen
        # Draw scores, players, ball, and net
        screen.blit(font.render(f"{player1_score}", True, WHITE), (100, 10))
        screen.blit(font.render(f"{player2_score}", True, WHITE), (screen.get_width() - 100, 10))
        pygame.draw.rect(screen, WHITE, (player.x, player.y, player.width, player.height))  # Player 1
        pygame.draw.rect(screen, WHITE, (player2.x, player2.y, player2.width, player2.height))  # Player 2
        pygame.draw.rect(screen, '#b1a7a6', (200, 0, 5, 400))  # Net
        pygame.draw.circle(screen, WHITE, (int(ball_pos.x), int(ball_pos.y)), 5)  # Ball

        if player1_score >= 3 or player2_score >= 3:  # Check for game over
            game_scene = "gameover"  # Switch to game over scene

    elif game_scene == 'gameover':  # Game over scene
        show_gameover()
        if keys[pygame.K_r]:  # Restart game if R is pressed
            game_scene = "gameplay"
            player1_score = 0
            player2_score = 0
            player.x = player1_pos_x
            player.y = player1_pos_y
            player2.x = player2_pos_x
            player2.y = player2_pos_y
            ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)  # Reset ball
            ball_velocity = pygame.Vector2(-150, 150)  # Reset velocity
        if keys[pygame.K_q]:  # Quit game if Q is pressed
            running = False

    pygame.display.flip()  # Update the screen

pygame.quit()  # Quit Pygame
