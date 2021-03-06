import pygame
import sys
from class_1 import DialogueCharacter


def draw_text(screen, pos, dialog_text, size):  # отрисовка текста
    f = pygame.font.SysFont('arial', size)
    screen.blit(f.render(dialog_text, 1, (255, 255, 255)), pos)
    pygame.display.update()


def draw_surface(screen):
    surface1 = screen.convert_alpha()
    surface1.fill([0, 0, 0, 0])
    return surface1


def baba_ege_run(dialog_text, screen=0, rt=0):
    baba_ega_group = pygame.sprite.Group()
    pygame.init()
    size = 750, 536
    if screen == 0:
        screen = pygame.display.set_mode(size)
        pygame.display.set_icon(pygame.image.load('data/icon.jpg').convert())
        pygame.display.set_caption('Тридевятое царство')
    running = True
    fps = 20
    clock = pygame.time.Clock()
    bg_surf = pygame.image.load("data/home_baba_ega_1.bmp")
    pygame.transform.scale(bg_surf, (750, 536))
    number_baba_ega = 0
    col = 0  # переменная для отслеживания сколько раз игрок нажал ентер
    pos = [(0, 445), (100, 400), (600, 400), (750, 445), (749, 445), (749, 535), (0, 535)]  # это поле отрисовки диолога
    surface1 = draw_surface(screen)
    pygame.draw.polygon(surface1, (0, 0, 0, 170), pos)
    animation = [pygame.image.load("data/baba_ega_1.bmp"), pygame.image.load("data/baba_ega_2.bmp"),
                 pygame.image.load("data/baba_ega_4.bmp"), pygame.image.load("data/baba_ega_6.bmp"),
                 pygame.image.load("data/baba_ega_1.bmp")]  # анимация бабы Еги
    bg_baba_ega = DialogueCharacter(500, -50, animation, baba_ega_group)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_exit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # если игрок кликает мышкой или наживает энтер то следуйщая фраза
                col += 1
                surface1 = draw_surface(screen)  # отрисовка диолога
                pygame.draw.polygon(surface1, (0, 0, 0, 170), pos)
            if event.type == pygame.KEYDOWN:
                if event.key == 13:  # энтер
                    col += 1
                    surface1 = draw_surface(screen)
                    pygame.draw.polygon(surface1, (0, 0, 0, 170), pos)
        bg_surf = pygame.image.load("data/home_baba_ega_1.bmp")
        bg_surf = pygame.transform.scale(bg_surf, (750, 536))
        number_baba_ega = (number_baba_ega + 1) % 35
        pygame.draw.lines(surface1, (255, 215, 0), True, pos, 2)
        bg_baba_ega.character_draw(number_baba_ega % 35 // 7, 3, 2.5)
        baba_ega_group.draw(bg_surf)
        screen.blit(bg_surf, (0, 0))  # bg_surf это задний фон
        screen.blit(surface1, (0, 0))  # Отрисовка диолога на основном окне
        clock.tick(fps)
        pygame.display.flip()
        if col == 3:
            running = False
            screen.fill((0, 0, 0))
            if rt == 0:
                baba_ege_house(screen, baba_ega_group, bg_baba_ega)
            else:
                return True
        else:
            lst = dialog_text[col].split('\n')
            y = 430
            for i in lst:
                draw_text(surface1, (100, y), i, 30)  # заного рисуем диолог с новым текстом
                y += 31
            draw_text(surface1, (690, 500), 'ENTER', 15)  # заного рисуем диолог с новым текстом
            pygame.display.flip()
    pygame.quit()


def baba_ege_house(screen, baba_ega_group, bg_baba_ega):
    running = True
    fps = 20
    col_mouse = 7
    clock = pygame.time.Clock()
    bg_surf = pygame.image.load("data/home_baba_ega_2.bmp").convert_alpha()  # задний фон с мышаами
    number_baba_ega = 0
    pos_mouse = [((204, 370), (250, 438), (224, 399)), ((120, 423), (150, 468), (136, 447)),
                 ((452, 430), (486, 474), (458, 454)), ((483, 58), (548, 94), (516, 74)),
                 ((294, 178), (325, 208), (310, 190)), ((190, 57), (238, 89), (211, 71)),
                 ((628, 65), (671, 100), (651, 83))]
    # в этих кортеджах 1 и 2 элемент это позиции квдрата с мышами а 3 позиция для отрисовки круга
    time = 30  # время
    print_message = pygame.USEREVENT  # это эвент который срабатывает каждую секунду
    pygame.time.set_timer(print_message, 1000)  # сам таймер которых срабатывает каждую секунду
    bg_baba_ega.rect = (540, 115)
    while running:
        for event in pygame.event.get():
            if event.type == print_message:
                if time == 0:
                    end_death(screen)
                    running = False
                elif col_mouse == 0:
                    end_vin(screen)
                    running = False
                else:
                    time -= 1
            if event.type == pygame.QUIT:
                run_exit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for i in pos_mouse:
                    if i[0][0] <= pos[0] and i[0][1] <= pos[1]:
                        if i[1][0] >= pos[0] and i[1][1] >= pos[1]:
                            col_mouse -= 1
                            pygame.draw.circle(bg_surf, (255, 255, 255, 255), i[2], 31, 4)
                            pos_mouse.remove(i)
        number_baba_ega = (number_baba_ega + 1) % 35
        bg_baba_ega.character_draw(number_baba_ega % 35 // 7, 4, 3.5)
        screen.blit(bg_surf, (0, 0))
        baba_ega_group.draw(screen)
        draw_text(screen, (650, 10), f'{time // 60}:{time - (60 * (time // 60))}', 50)  # отрисовка текста
        if col_mouse == 7 or col_mouse == 5 or col_mouse == 6:  # это склонение
            text_mouse = f'Найдите {col_mouse} мышей.'
        elif col_mouse != 1 and col_mouse != 0:
            text_mouse = f'Найдите {col_mouse} мыши.'
        elif col_mouse == 1:
            text_mouse = f'Найдите {col_mouse} мышь.'
        else:
            text_mouse = 'Вы нашли всех мышей'
        draw_text(screen, (0, 490), text_mouse, 30)  # отрисовка текста с количеством мышей
        clock.tick(fps)
    pygame.quit()


def end_death(screen):  # завершение игры (смерть) и выход в главное меню
    running = True
    fps = 20
    clock = pygame.time.Clock()
    animation = [pygame.image.load("data/death_baba_ega_1.bmp"), pygame.image.load("data/death_baba_ega_2.bmp"),
                 pygame.image.load("data/death_baba_ega_3.bmp"), pygame.image.load("data/death_baba_ega_4.bmp"),
                 pygame.image.load("data/death_baba_ega_5.bmp"), pygame.image.load("data/death_baba_ega_6.bmp"),
                 pygame.image.load("data/death_baba_ega_7.bmp"), pygame.image.load("data/death_baba_ega_8.bmp"),
                 pygame.image.load("data/death_baba_ega_9.bmp"), pygame.image.load("data/death_baba_ega_10.bmp")]
    bg_surf = animation[0]
    pygame.transform.scale(bg_surf, (750, 536))
    surface1 = draw_surface(screen)
    pygame.draw.polygon(surface1, (0, 0, 0, 200), ((0, 0), (750, 0), (750, 536), (0, 536)))
    draw_text(surface1, (100, 140), 'Ты мертв!', 150)
    number_background = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_exit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos() >= (255, 350):
                    if pygame.mouse.get_pos() <= (525, 418):
                        # выход в главное меню
                        print('Выход в главное меню, строка 157')
                        exit()
        number_background = (number_background + 1) % 40
        bg_surf = animation[number_background // 4]
        bg_surf = pygame.transform.scale(bg_surf, (750, 536))
        screen.blit(bg_surf, (0, 0))
        screen.blit(surface1, (0, 0))
        pygame.draw.rect(surface1, (255, 0, 0), ((255, 350), (270, 68)))
        draw_text(surface1, (265, 360), 'начать с начала', 40)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


def end_vin(screen):
    txt = ['Спасибо тебе добрый молодец,', 'За это тебе я отдам\n свой меч кладинец.', 'Идти дальше.']
    with open('level_pos.txt', 'a', encoding='utf-8') as file:
        print(' 3', file=file)
    baba_ege_run(txt, screen, 1)


def run_exit():
    sys.exit('main.py')


if __name__ == '__main__':
    text = ['Что то русским духом по пахивает.\n Знаю нужны тебе доспехи,\n Помощь нужна мне, мыши одолели.',
            'Сможешь отловить, получишь, что хочешь.\n Не успеешь справиться,\nсуп у меня вкусный будет на ужин.',
            'Начать.']
    baba_ege_run(text)
