import pygame


def help():

    pygame.init()
    size = [288, 612]
    window = pygame.display.set_mode(size)
    pygame.display.set_caption('помощь')
    background = pygame.image.load('background.png')
    font = pygame.font.SysFont('Times New Roman', 20)
    text = font.render('Прыжок - Space', True, [0, 100, 0])
    text1 = font.render('Вернуться в меню - Escape', True, [0, 100, 0])

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    import menu
                    menu.menu()
        window.blit(background, (0, 0))
        window.blit(text, (30, 200))
        window.blit(text1, (30, 100))
        pygame.display.flip()
    pygame.quit()
