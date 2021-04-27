import socket
import datetime
import sqlite3

SERVER_ADDRESS = '127.0.0.1', 54321
BUFFER_SIZE = 1024
last_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
print(last_date)


with sqlite3.connect('data.sqlite3') as conn:
    conn.execute('''
    CREATE TABLE IF NOT EXISTS station_status (
    station_id INT,
    last_date TEXT,
    alarm1 INT,
    alarm2 INT,
    PRIMARY KEY(station_id) );
    ''')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(SERVER_ADDRESS)
        print(f'Server is running on: {s.getsockname()[0]} {s.getsockname()[1]}')

        while True:
            get_data, new_client = s.recvfrom(BUFFER_SIZE)
            station_id, alarm_1, alarm_2 = get_data.decode().split()
            print(f'received data from client:'
                  f'\nstation_id:{station_id}'
                  f'\nalarm_1:{alarm_1}'
                  f'\nalarm_2:{alarm_2}')

            conn.execute('''
            INSERT OR REPLACE INTO
            station_status
            VALUES(?, ?, ?, ?)
            ''', (station_id, last_date, alarm_1, alarm_2))
            conn.commit()

            data_to_client = 'station data has been received '.encode()
            print('sending back to client...')
            s.sendto(data_to_client, new_client)
