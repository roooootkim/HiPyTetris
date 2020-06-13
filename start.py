import pygame as pg
from network import *
from game import Player
from game import AI_Player
from setting import *
successes, failures = pg.init()
print("{0} successes and {1} failures in start.py".format(successes, failures))

screen = pg.display.set_mode(size)
pg.display.set_caption("HiPy Tetris")
clock = pg.time.Clock()


def solo_play():
    run = True
    key_set = {'right': pg.K_RIGHT, 'left': pg.K_LEFT, 'up': pg.K_UP, 'down': pg.K_DOWN, 'drop': pg.K_SPACE}
    player = Player('center', key_set)

    screen.fill(WHITE)
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
                quit()
            player.key_input(event)

        player.move_piece()
        player.fall_time_check()
        player.draw_board(screen)
        clock.tick(FPS)
        pg.display.flip()
        if player.is_game_over():
            run = False
            print("게임 오버 구현하기.")


def multi_play():
    run = True
    key_set1 = {'right': pg.K_RIGHT, 'left': pg.K_LEFT, 'up': pg.K_UP, 'down': pg.K_DOWN, 'drop': pg.K_RETURN}
    key_set2 = {'right': pg.K_d, 'left': pg.K_a, 'up': pg.K_w, 'down': pg.K_s, 'drop': pg.K_SPACE}
    player1 = Player('right', key_set1)
    player2 = Player('left', key_set2)
    Player.make_multi(player1, player2)
    screen.fill(WHITE)
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
                quit()
            player1.key_input(event)
            player2.key_input(event)

        player1.move_piece()
        player2.move_piece()
        player1.fall_time_check()
        player2.fall_time_check()
        player1.draw_board(screen)
        player2.draw_board(screen)
        clock.tick(FPS)
        pg.display.flip()
        if player1.is_game_over() or player2.is_game_over():
            run = False
            print("게임 오버 구현하기")


def computer_play():
    run = True
    ai_player = AI_Player('center')
    screen.fill(WHITE)
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    ai_player.env.ai_step()
        ai_player.env.ai_step()  # 이 line 주석처리 하면 엔터 누를때 마다 한번씩 행동함.
        ai_player.draw_board(screen)
        clock.tick(FPS)
        pg.display.flip()
        if ai_player.is_game_over():
            run = False
            print("게임 오버 구현하기")


def online_room():
    run = True
    input_box = pg.Rect(size[0] / 2 - 200, size[1] / 2 - 16, 400, 32)
    font1 = pg.font.SysFont("arial", 30, True, False)
    font2 = pg.font.Font(None, 32)
    address_txt = ''
    backspace = False
    delay_count = 0
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    run = False
                elif event.key == pg.K_BACKSPACE:
                    backspace = True
                    delay_count = 0
                else:
                    address_txt += event.unicode
            if event.type == pg.KEYUP:
                if event.key == pg.K_BACKSPACE:
                    backspace = False
                    delay_count = 0

        if backspace:
            if delay_count == 0 or delay_count >= 10:
                address_txt = address_txt[:-1]
            delay_count += 1

        screen.fill(WHITE)
        txt_surface1 = font1.render("Enter the server address", True, BLACK)
        txt_surface2 = font2.render(address_txt, True, BLACK)
        input_box.w = max(input_box.w, txt_surface2.get_width() + 10)
        screen.blit(txt_surface1, (input_box.x + 5, input_box.y - 50))
        screen.blit(txt_surface2, (input_box.x + 5, input_box.y + 5))
        pg.draw.rect(screen, BLACK, input_box, 2)

        pg.display.flip()
        clock.tick(FPS)

    network = Network(address_txt)
    online_play(network)


def online_play(network):
    run = True
    p1 = network.getp()
    screen.fill(WHITE)
    while run:
        p2 = network.send(p1)

        p1.init_attack_count()

        if p2.attack_count != 0:
            print(p2.attack_count)
            p1.online_attacked(p2.attack_count)
            p2.init_attack_count()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
                quit()
            if not p2.is_waiting():
                p1.key_input(event)

        if not p2.is_waiting():
            p1.move_piece()
            p1.fall_time_check()
            p1.cal_attack_count()

        p1.draw_board(screen)
        p2.draw_board(screen)
        pg.display.update()

        clock.tick(FPS)
        pg.display.flip()

        if p1.is_game_over() or p2.is_game_over():
            network.send(p1)
            run = False
            print("게임 오버 구현하기")


def main_menu():
    run = True
    menu_list = ['Play Game', 'Multi Play', 'vs Computer', 'Online Play', 'Exit']
    cur_menu = 0
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    cur_menu = (cur_menu + 1) % len(menu_list)
                if event.key == pg.K_UP:
                    cur_menu = (cur_menu + len(menu_list) - 1) % len(menu_list)
                if event.key == pg.K_RETURN:
                    if cur_menu == 0:
                        solo_play()
                    if cur_menu == 1:
                        multi_play()
                    if cur_menu == 2:
                        computer_play()
                    if cur_menu == 3:
                        online_room()
                    elif cur_menu == 4:
                        run = False
                        pg.display.quit()
                        quit()

        screen.fill(WHITE)
        menu_font = pg.font.SysFont("arial", 30, True, False)
        menu_text = []
        for text in menu_list:
            if menu_list[cur_menu] == text:
                menu_text.append(menu_font.render(text, True, colors[1]))
            else:
                menu_text.append(menu_font.render(text, True, colors[0]))

        i = 0
        for text in menu_text:
            screen.blit(text, [size[0] / 4, size[1] / 2 - 125 + i * 50])
            i += 1

        pg.display.flip()
        clock.tick(FPS)
    pg.quit()


if __name__ == "__main__":
    main_menu()
