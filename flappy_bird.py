import pygame
import random


def game():

    def reset_game():
        nonlocal bird_rect, obstacles, obstacle_timer, game_over, score
        bird_rect = bird.get_rect(center=(100, 300))
        obstacles.clear()
        obstacle_timer = pygame.time.get_ticks()
        game_over = False
        score = 0

    pygame.init()
    size = [288, 612]
    window = pygame.display.set_mode(size)
    pygame.display.set_caption('flappy bird')

    cursor_image = pygame.transform.scale(pygame.image.load('cursor.png'), [30, 30])
    pygame.mouse.set_visible(False)

    background = pygame.image.load('background.png')
    background_x = 0
    background_speed = 2

    bird_images = [pygame.image.load(f'redbird{i}.png') for i in range(1, 4)]
    bird_index = 0
    bird_rect = bird_images[bird_index].get_rect(center=(100, 300))

    gravity = 3
    jump_speed = 60

    obstacle = pygame.image.load('pipe-green.png')
    inverted_obstacle = pygame.transform.rotate(obstacle, 180)
    obstacles = []
    obstacle_timer = 0
    obstacle_frequency = 1500
    distance = 30

    font = pygame.font.SysFont('Times New Roman', 30)

    game_over_image = pygame.image.load('gameover.png')
    game_over_rect = game_over_image.get_rect(center=(size[0] // 2, size[1] // 2))

    numbers_images = [pygame.image.load(f'{i}.png') for i in range(10)]
    score = 0

    text = font.render('Play Again', True, [0, 100, 0])
    play_again_rect = text.get_rect(center=(size[0] // 2, size[1] // 2 + 100))

    run = True
    game_over = False

    FPS = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    import menu
                    menu.menu()
                elif event.key == pygame.K_SPACE:
                    bird_rect.y -= jump_speed

            elif event.type == pygame.MOUSEBUTTONDOWN and play_again_rect.collidepoint(event.pos):
                reset_game()

        if not game_over:

            current_time = pygame.time.get_ticks()
            if current_time - obstacle_timer > obstacle_frequency:
                obstacle_timer = current_time
                new_obstacle_top = inverted_obstacle.get_rect(center=(size[0], random.randint(0, 150)))
                new_obstacle_lower = obstacle.get_rect(center=(size[0], new_obstacle_top.y + distance + 612))
                obstacles.append((new_obstacle_top, new_obstacle_lower))

            background_x -= background_speed
            window.blit(background, (background_x, 0))
            window.blit(background, (background_x + size[0], 0))

            if background_x <= -size[0]:
                background_x = 0

            bird_rect.y += gravity

            bird = bird_images[bird_index]
            bird_rect = bird.get_rect(center=bird_rect.center)
            bird_index = (bird_index + 1) % len(bird_images)

            for obstacle_pair in obstacles:
                if bird_rect.colliderect(obstacle_pair[0]) or bird_rect.colliderect(obstacle_pair[1]):
                    game_over = True

            if bird_rect.y >= size[1]:
                game_over = True

            if bird_rect.y <= 0:
                game_over = True

            window.blit(bird, bird_rect)

            for obstacle_pair in obstacles:
                obstacle_pair[0].x -= background_speed
                obstacle_pair[1].x -= background_speed
                window.blit(inverted_obstacle, obstacle_pair[0])
                window.blit(obstacle, obstacle_pair[1])

            obstacles = [(top, lower) for top, lower in obstacles if top.x + top.width > 0 and lower.x + lower.width > 0]

            for obstacle_pair in obstacles:
                if obstacle_pair[0].x < bird_rect.x < obstacle_pair[0].x + background_speed:
                    score += 1

            numbers_width = numbers_images[0].get_width()
            score_numbers = [int(numbers) for numbers in str(score)]
            x_position = (size[0] - len(score_numbers) * numbers_width) // 2

            for number in score_numbers:
                window.blit(numbers_images[number], (x_position, 10))
                x_position += numbers_width

        else:

            with open('maxscore.txt', 'r') as file:
                max_score = int(file.read())

            if max_score < score:
                max_score = score
                with open('maxscore.txt', 'w') as file:
                    file.write(f'{max_score}')

            window.blit(background, (0, 0))
            with open("maxscore.txt", "r") as file:

                text1 = font.render("Max Score:", True, [0, 100, 0])
                window.blit(text1, (10, 40))

                numbers_width = numbers_images[0].get_width()
                score_numbers = [int(numbers) for numbers in file.read()]
                x_position = (size[0] - len(score_numbers) * numbers_width) // 1.5

                for number in score_numbers:
                    window.blit(numbers_images[number], (x_position, 40))
                    x_position += numbers_width

            window.blit(game_over_image, game_over_rect)
            window.blit(text, play_again_rect)

            if pygame.mouse.get_focused():
                pos = pygame.mouse.get_pos()
                window.blit(cursor_image, pos)

        pygame.display.flip()
        FPS.tick(60)
