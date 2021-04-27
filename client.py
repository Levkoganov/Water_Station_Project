import socket
import time

SERVER_ADDRESS = '127.0.0.1', 54321

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    print(f'connecting to server at: {SERVER_ADDRESS[0]} {SERVER_ADDRESS[1]}...')

    while True:
        print('loading... ')
        time.sleep(3)
        message = input("enter one of the following stations ID: (123, 456, 789):")

        if message == '123':
            with open('status01.txt') as f:
                station_id = str(f.readline())
                alarm_1 = str(f.readline())
                alarm_2 = str(f.readline())

        elif message == '456':
            with open('status02.txt') as f:
                station_id = str(f.readline())
                alarm_1 = str(f.readline())
                alarm_2 = str(f.readline())

        elif message == '789':
            with open('status03.txt') as f:
                station_id = str(f.readline())
                alarm_1 = str(f.readline())
                alarm_2 = str(f.readline())
        else:
            print('wrong input.\n'
                  'please enter one of the following stations:[123 or 456 or 789]')
            continue

        data = station_id.encode()
        data += alarm_1.encode()
        data += alarm_2.encode()
        s.sendto(data, SERVER_ADDRESS)

        data, address = s.recvfrom(1024)
        print(data.decode())
