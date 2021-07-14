import sqlite3


class player_history_db_handler:
    def __init__(self):
        global conn, cur
        conn = sqlite3.connect('playerHistory.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS history('
                    'date TEXT,'
                    'user TEXT,'
                    'pp REAL,'
                    'gRanking INTEGER,'
                    'lRanking INTEGER,'
                    'topSong TEXT,topPP INTEGER)'
                    )

    def player_yesterday_data_export(self, name):
        cur.execute('SELECT max(date),pp,gRanking,lRanking,topSong,topPP from history where user=?', (name,))
        yesterday_data = cur.fetchone()
        return yesterday_data

    def player_today_data_import(self, today_data):
        cur.execute('INSERT INTO history VALUES (datetime("now","localtime"),?,?,?,?,?,?)', (
            today_data[0],
            today_data[1],
            today_data[2],
            today_data[3],
            today_data[4],
            today_data[5]
        )
                    )

        conn.commit()
        conn.close()
