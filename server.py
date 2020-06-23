import socket
from _thread import *
import pickle
from game import Player
import pygame as pg
from setting import *

'''
server.py
작성자: 2017038015신윤성
서버를 생성하는 파일. socket모듈을 이용해 서버를 생성하고, 클라이언트가 그 서버에 접속한다.
접속이 확인되면 스레드를 생성해 플레이어 한 명당 한 개씩 스레드를 가지고 플레이한다.
reply가 상대방을 의미한다. reply객체를 상대에게 보냄으로써 상대의 상태를 화면에 그릴 수 있다.
'''

key_set = {'right': pg.K_RIGHT, 'left': pg.K_LEFT, 'up': pg.K_UP, 'down': pg.K_DOWN, 'drop': pg.K_SPACE}
cur_player = 0
players = [Player('left', key_set, True), Player('right', key_set, True)]
port = 5555
clock = pg.time.Clock()


def thread_client(conn, player_num):
    global cur_player
    players[player_num - 1].start_game()
    conn.send(pickle.dumps(players[player_num - 1]))
    while True:
        try:
            data = pickle.loads(conn.recv(2048*3))
            players[player_num - 1] = data
            if not data:
                print("disconnected")
                break
            else:
                if player_num == 1:
                    reply = players[1]
                else:
                    reply = players[0]

            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("lost connection")
    cur_player -= 1
    if player_num == 1:
        players[player_num - 1] = Player('left', key_set, True)
    elif player_num == 2:
        players[player_num - 1] = Player('right', key_set, True)
    conn.close()


if __name__ == "__main__":
    server = str(input('서버 IP 입력 : '))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen(2)

    print("waiting for a connection....")

    connected = set()

    while True:
        while cur_player < 2:
            conn, addr = s.accept()
            print("Connected to:", addr)
            cur_player += 1
            start_new_thread(thread_client, (conn, cur_player))
