import pygame
import sys
import random

pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Collector")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Game states
HOME = 0
PLAYING = 1
GAME_OVER = 2
WIN = 3
game_state = HOME
selected_option = 0
menu_options = ["START GAME", "INSTRUCTIONS", "QUIT"]
show_instructions = False

# Maze walls (x, y, width, height)
walls = [
    (0, 0, 800, 20), (0, 0, 20, 600), (780, 0, 20, 600), (0, 580, 800, 20),  # Borders
    (100, 100, 20, 200), (200, 50, 20, 150), (300, 200, 20, 200),
    (400, 100, 200, 20), (500, 200, 20, 150), (600, 300, 150, 20),
    (150, 350, 200, 20), (450, 400, 20, 100), (100, 450, 150, 20)
]

def init_game():
    global player_x, player_y, dots, score, ghosts, lives, power_mode, power_timer, power_pellets, flash_timer
    # Player
    player_x, player_y = 50, 50
    lives = 3
    
    # Ghosts (x, y, dx, dy, color, start_x, start_y)
    ghosts = [
        [400, 300, random.choice([-2, 2]), random.choice([-2, 2]), RED, 400, 300],
        [200, 200, random.choice([-2, 2]), random.choice([-2, 2]), PINK, 200, 200],
        [600, 400, random.choice([-2, 2]), random.choice([-2, 2]), CYAN, 600, 400],
        [300, 450, random.choice([-2, 2]), random.choice([-2, 2]), ORANGE, 300, 450]
    ]
    
    # Power mode
    power_mode = False
    power_timer = 0
    flash_timer = 0
    
    # Power pellets in corners
    power_pellets = [(60, 60), (740, 60), (60, 540), (740, 540)]
    
    # Dots and scoring
    dots = []
    score = 0
    for x in range(40, WIDTH, 40):
        for y in range(40, HEIGHT, 40):
            dot_rect = pygame.Rect(x-5, y-5, 10, 10)
            collision = False
            for wall in walls:
                if dot_rect.colliderect(pygame.Rect(wall)):
                    collision = True
                    break
            # Don't place dots where power pellets are
            for pellet in power_pellets:
                if abs(x - pellet[0]) < 20 and abs(y - pellet[1]) < 20:
                    collision = True
                    break
            if not collision:
                dots.append((x, y))

def reset_player():
    global player_x, player_y
    player_x, player_y = 50, 50

player_radius = 15
player_speed = 5
ghost_size = 15
init_game()

def check_collision(x, y, size=player_radius):
    rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
    for wall in walls:
        if rect.colliderect(pygame.Rect(wall)):
            return True
    return False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_state == HOME:
                if not show_instructions:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            game_state = PLAYING
                            init_game()
                        elif selected_option == 1:
                            show_instructions = True
                        elif selected_option == 2:
                            pygame.quit()
                            sys.exit()
                else:
                    if event.key == pygame.K_ESCAPE:
                        show_instructions = False
            elif game_state in [GAME_OVER, WIN] and event.key == pygame.K_SPACE:
                game_state = HOME
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == HOME and not show_instructions:
            mouse_x, mouse_y = event.pos
            for i, option in enumerate(menu_options):
                option_y = HEIGHT//2 + i * 60
                if option_y - 20 <= mouse_y <= option_y + 20:
                    if i == 0:
                        game_state = PLAYING
                        init_game()
                    elif i == 1:
                        show_instructions = True
                    elif i == 2:
                        pygame.quit()
                        sys.exit()
    
    screen.fill(BLACK)
    
    if game_state == HOME:
        if not show_instructions:
            title = big_font.render("MAZE COLLECTOR", True, WHITE)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 150))
            
            for i, option in enumerate(menu_options):
                color = YELLOW if i == selected_option else WHITE
                option_text = font.render(option, True, color)
                screen.blit(option_text, (WIDTH//2 - option_text.get_width()//2, HEIGHT//2 + i * 60))
            
            controls = font.render("Use UP/DOWN arrows or mouse to select, ENTER to confirm", True, GRAY)
            screen.blit(controls, (WIDTH//2 - controls.get_width()//2, HEIGHT - 50))
        else:
            title = big_font.render("INSTRUCTIONS", True, WHITE)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
            
            instructions = [
                "Use arrow keys to move the yellow player",
                "Collect all dots and power pellets to win",
                "Avoid ghosts or lose a life (3 lives total)",
                "Eat flashing power pellets to turn ghosts blue",
                "Touch blue ghosts for bonus points!"
            ]
            
            for i, instruction in enumerate(instructions):
                text = font.render(instruction, True, WHITE)
                screen.blit(text, (WIDTH//2 - text.get_width()//2, 150 + i * 40))
            
            back_text = font.render("Press ESC to go back", True, GRAY)
            screen.blit(back_text, (WIDTH//2 - back_text.get_width()//2, HEIGHT - 50))
    
    elif game_state == PLAYING:
        keys = pygame.key.get_pressed()
        new_x, new_y = player_x, player_y
        
        if keys[pygame.K_LEFT]:
            new_x -= player_speed
        if keys[pygame.K_RIGHT]:
            new_x += player_speed
        if keys[pygame.K_UP]:
            new_y -= player_speed
        if keys[pygame.K_DOWN]:
            new_y += player_speed
        
        if not check_collision(new_x, new_y):
            player_x, player_y = new_x, new_y
        
        # Update power mode
        if power_mode:
            power_timer -= 1
            if power_timer <= 0:
                power_mode = False
        flash_timer += 1
        
        # Move ghosts
        ghost_speed = 1 if power_mode else 2
        for ghost in ghosts:
            new_x = ghost[0] + ghost[2] * ghost_speed
            new_y = ghost[1] + ghost[3] * ghost_speed
            if check_collision(new_x, ghost[1], ghost_size) or random.randint(1, 30) == 1:
                ghost[2] = random.choice([-1, 1]) if power_mode else random.choice([-2, 2])
            if check_collision(ghost[0], new_y, ghost_size) or random.randint(1, 30) == 1:
                ghost[3] = random.choice([-1, 1]) if power_mode else random.choice([-2, 2])
            if not check_collision(new_x, ghost[1], ghost_size):
                ghost[0] = new_x
            if not check_collision(ghost[0], new_y, ghost_size):
                ghost[1] = new_y
        
        # Check ghost collisions
        for ghost in ghosts:
            if ((player_x - ghost[0])**2 + (player_y - ghost[1])**2)**0.5 < player_radius + ghost_size:
                if power_mode:
                    # Reset ghost to start position
                    ghost[0], ghost[1] = ghost[5], ghost[6]
                    score += 200
                else:
                    lives -= 1
                    if lives <= 0:
                        game_state = GAME_OVER
                    else:
                        reset_player()
        
        # Check dot collection
        for dot in dots[:]:
            if ((player_x - dot[0])**2 + (player_y - dot[1])**2)**0.5 < player_radius + 5:
                dots.remove(dot)
                score += 10
        
        # Check power pellet collection
        for pellet in power_pellets[:]:
            if ((player_x - pellet[0])**2 + (player_y - pellet[1])**2)**0.5 < player_radius + 8:
                power_pellets.remove(pellet)
                power_mode = True
                power_timer = 300  # 5 seconds at 60 FPS
                score += 50
        
        # Check win condition
        if len(dots) == 0 and len(power_pellets) == 0:
            game_state = WIN
        
        # Draw walls
        for wall in walls:
            pygame.draw.rect(screen, BLUE, wall)
        
        # Draw dots
        for dot in dots:
            pygame.draw.circle(screen, WHITE, dot, 3)
        
        # Draw power pellets (flashing)
        if flash_timer % 20 < 10:
            for pellet in power_pellets:
                pygame.draw.circle(screen, WHITE, pellet, 8)
        
        # Draw ghosts
        for ghost in ghosts:
            color = BLUE if power_mode else ghost[4]
            pygame.draw.rect(screen, color, (ghost[0] - ghost_size, ghost[1] - ghost_size, ghost_size * 2, ghost_size * 2))
        
        # Draw player
        pygame.draw.circle(screen, YELLOW, (player_x, player_y), player_radius)
        
        # Draw score and lives
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 50))
        if power_mode:
            power_text = font.render(f"Power: {power_timer//60 + 1}s", True, YELLOW)
            screen.blit(power_text, (10, 90))
    
    elif game_state == GAME_OVER:
        game_over = big_font.render("GAME OVER", True, WHITE)
        final_score = font.render(f"Final Score: {score}", True, WHITE)
        restart = font.render("Press SPACE to return to menu", True, WHITE)
        screen.blit(game_over, (WIDTH//2 - game_over.get_width()//2, HEIGHT//2 - 50))
        screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2 + 20))
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 60))
    
    elif game_state == WIN:
        win_text = big_font.render("YOU WIN!", True, WHITE)
        final_score = font.render(f"Final Score: {score}", True, WHITE)
        restart = font.render("Press SPACE to return to menu", True, WHITE)
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2 + 20))
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 60))
    
    pygame.display.flip()
    clock.tick(60)
