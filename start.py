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

'''
함수명 : game_over
작성자 : 오기탁
게임 오버를 구현하는 함수입니다
텍스트를 출력하고 메인으로 돌아가거나 게임을 재시작합니다.
'''
def game_over(value, is_multi=False):
    font1 = pg.font.SysFont("arial", 64, True, False)
    font2 = pg.font.SysFont("arial", 32, True, False)
    txt_surface1 = font1.render("Game Over", True, colors[1])
    if not is_multi:
        txt_surface2 = font2.render("deleted line : " + str(value), True, colors[5])
    else:
        if value == 3:
            txt_surface2 = font1.render("Computer Win!", True, colors[5])
        else:
            txt_surface2 = font1.render("Player" + str(value) + " Win", True, colors[5])
    txt_surface3 = font2.render("Press Enter key to return", True, colors[4])
    screen.blit(txt_surface1, (size[0] / 2 - txt_surface1.get_width() / 2, size[1] / 4))
    screen.blit(txt_surface2, (size[0] / 2 - txt_surface2.get_width() / 2, size[1] * 3 / 8))
    screen.blit(txt_surface3, (size[0] / 2 - txt_surface3.get_width() / 2, size[1] / 2))
    pg.display.flip()

    run = True
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                    run = False

'''
함수명 : solo_play
작성자 : 김근호
하이파이 테트리스의 1인 플레이 기능을 구현하였습니다.
게임 오버시 게임오버 함수를 호출하고 메인메뉴로 돌아갑니다.
'''
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
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if pause_game() == 1:
                        run = False
            player.key_input(event)

        player.move_piece()
        player.fall_time_check()
        player.draw_board(screen)
        clock.tick(FPS)
        pg.display.flip()
        if player.is_game_over():
            run = False
            game_over(player.get_score())

'''
함수명 : multi_play
작성자 : 오기탁
start파일에 포함되는 로컬 플레이 함수
객체 두 개를 가지고 게임을 플레이하는 함수입니다
'''
def multi_play():
    run = True
    key_set1 = {'right': pg.K_d, 'left': pg.K_a, 'up': pg.K_w, 'down': pg.K_s, 'drop': pg.K_SPACE}
    key_set2 = {'right': pg.K_RIGHT, 'left': pg.K_LEFT, 'up': pg.K_UP, 'down': pg.K_DOWN, 'drop': pg.K_RETURN}
    player1 = Player('left', key_set1)
    player2 = Player('right', key_set2)
    Player.make_multi(player1, player2)
    screen.fill(WHITE)
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if pause_game() == 1:
                        run = False
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
            if player1.is_game_over():
                game_over(2, True)
            elif player2.is_game_over():
                game_over(1, True)

'''
함수명 : ai_menu
작성자 : 김근호
vs Computer 메뉴를 골랐을 때 실행되며, ai_view 와 vs_ai 메뉴를 선택할 수 있는 화면을 출력합니다.
'''
def ai_menu():
    run = True
    menu_list = ['View AI', 'vs AI', 'Main Menu']
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
                if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                    if cur_menu == 0:
                        run = False
                        ai_view()
                    if cur_menu == 1:
                        run = False
                        ai_play()
                    elif cur_menu == 2:
                        run = False

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

'''
함수명 : ai_play
작성자 : 김근호
ai와 대전하는 게임모드를 구현한 함수입니다. tetris_gym.py로 부터 ai 플레이를 가져옵니다.
'''
def ai_play():
    run = True
    key_set = {'right': pg.K_RIGHT, 'left': pg.K_LEFT, 'up': pg.K_UP, 'down': pg.K_DOWN, 'drop': pg.K_SPACE}
    player = Player('left', key_set)
    ai_player = AI_Player('right')
    screen.fill(WHITE)
    Player.make_multi(player, ai_player)
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if pause_game() == 1:
                        run = False
            player.key_input(event)

        player.move_piece()
        player.fall_time_check()
        ai_player.fall_time_check()
        player.draw_board(screen)
        ai_player.draw_board(screen)

        clock.tick(FPS)
        pg.display.flip()
        if ai_player.is_game_over() or player.is_game_over():
            run = False
            if player.is_game_over():
                game_over(3, True)
            elif ai_player.is_game_over():
                game_over(1, True)

'''
함수명 : ai_view
작성자 : 김근호
ai 혼자 플레이하는 모습을 확인할 수 있습니다. ai 플레이를 tetris_gym.py로 부터 가져옵니다.
'''
def ai_view():
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
                if event.key == pg.K_ESCAPE:
                    if pause_game() == 1:
                        run = False
        ai_player.env.ai_step()
        ai_player.draw_board(screen)
        clock.tick(FPS)
        pg.display.flip()
        if ai_player.is_game_over():
            run = False
            game_over(ai_player.get_score())

'''
함수명 : online_room
작성자 : 김근호
Online Play 메뉴를 선택했을 때에 호출되는 함수 입니다.
서버 접속을 위한 아이피 입력 화면을 출력합니다.
ip를 입력받았을 때 해당 서버에 접속하여 online_play()함수를 호출합니다.
'''
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

    try:
        network = Network(address_txt)
        online_play(network)
    except:
        print("Network Error!")


'''
함수명 : online_play()
작성자: 2017038015신윤성
start파일에 포함되는 온라인 플레이 함수.
p는 플레이어 한 명의 객체를 받아온다. 이를 움직이고 조작한 뒤 상대에게 그 정보를 보낸다.
상대는 그 정보를 받고 자신이 조작한 정보를 다시 서버로 보내 계속 주고 받는다.
'''
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

'''
함수명 : pause_game
작성자 : 김영현
Play 도중 esc키를 누르면 일시정지가 되고 main menu로 되돌아가거나 Play를 이어서 할 수 있게 해준다.
'''
def pause_game():
    run = True
    menu_list = ['Main Menu', 'Resume']
    cur_menu = 0
    ret_value = 0
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                if event.key == pg.K_DOWN:
                    cur_menu = (cur_menu + 1) % len(menu_list)
                if event.key == pg.K_UP:
                    cur_menu = (cur_menu + len(menu_list) - 1) % len(menu_list)
                if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                    if cur_menu == 0:
                        run = False
                        ret_value = 1
                    if cur_menu == 1:
                        run = False

        menu_font = pg.font.SysFont("arial", 30, True, True)
        menu_text = []
        for text in menu_list:
            if menu_list[cur_menu] == text:
                menu_text.append(menu_font.render(text, True, colors[1]))
            else:
                menu_text.append(menu_font.render(text, True, WHITE))

        i = 0
        for text in menu_text:
            screen.blit(text, [size[0] / 2 - text.get_width() / 2, size[1] / 4 + i * text.get_height()])
            i += 1

        pg.display.flip()
        clock.tick(FPS)
    screen.fill(WHITE)
    return ret_value

'''
함수명 : main_menu
작성자 : 김영현
cur_menu로 현재메뉴 값을 저장후 엔터키 입력시 해당 메뉴의 메서드 실행
'''
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
                if event.key == pg.K_SPACE or event.key == pg.K_RETURN:
                    if cur_menu == 0:
                        solo_play()
                    if cur_menu == 1:
                        multi_play()
                    if cur_menu == 2:
                        ai_menu()
                    if cur_menu == 3:
                        online_room()
                    elif cur_menu == 4:
                        run = False
                        pg.display.quit()
                        quit()

        screen.fill(WHITE)
        logo_font = pg.font.SysFont("arial", 80, True, False)
        logo_txt = logo_font.render("HiPy Tetris", True, colors[0])
        screen.blit(logo_txt, [size[0] / 4, size[1] / 8])
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
