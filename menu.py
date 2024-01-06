import pygame


def menu():
    pygame.init()
    size = [288, 612]
    window = pygame.display.set_mode(size)
    pygame.display.set_caption('меню')
    bird = pygame.image.load('redbird2.png')
    pygame.display.set_icon(bird)
    cursor = pygame.transform.scale(pygame.image.load('cursor.png'), [30, 30])
    background = pygame.image.load('background.png')
    font = pygame.font.SysFont('Times New Roman', 30)
    pygame.mouse.set_visible(False)
    menu_items = ['Play', 'Help', 'Exit']
    menu_rect = []

    run = True
    while run:
        window.blit(background, (0, 0))
        menu_rect.clear()
        for i in range(len(menu_items)):
            menu_rect.append(pygame.Rect(50, 100 + i * 130, 200, 80))
            pygame.draw.rect(window, [0, 100, 0], menu_rect[i], 3)
            text = font.render(menu_items[i], True, [0, 100, 0])
            text_rect = text.get_rect(center=menu_rect[i].center)
            window.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for (i, item) in enumerate(menu_rect):
                        if item.collidepoint(pos):

                            if i == 0:
                                import flappy_bird
                                flappy_bird.game()
                            elif i == 1:
                                import help
                                help.help()
                            elif i == 2:
                                run = False

        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            window.blit(cursor, pos)
        pygame.display.flip()
    pygame.quit()
    quit()


menu()

