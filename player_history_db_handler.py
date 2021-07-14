import sqlite3


class player_history_db_handler:
    def __init__(self):
        global conn, cur
        conn = sqlite3.connect('player_history.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS history('
                    'oauth_token TEXT,'
                    'date TEXT,'               
                    'user TEXT,'
                    'pp REAL,'
                    'gRanking INTEGER,'
                    'lRanking INTEGER,'
                    'topSong TEXT,'
                    'topPP INTEGER,'
                    'recent_play TEXT'
                    ')'
                    )

    def player_yesterday_data_export(self, oauth_token,name):
        cur.execute('SELECT max(date),pp,gRanking,lRanking,topSong,topPP from history where oauth_token=? AND user=?', (oauth_token,name))
        yesterday_data = cur.fetchone()
        return yesterday_data

    def player_today_data_import(self, oauth_token,today_data):
        cur.execute('INSERT INTO history VALUES (?,datetime("now","localtime"),?,?,?,?,?,?,?)', (
            oauth_token,
            today_data[0],
            today_data[1],
            today_data[2],
            today_data[3],
            today_data[4],
            today_data[5],
            today_data[6]
        )
                    )

    def player_history_delete(self,oauth_token):
        cur.execute('DELETE FROM history WHERE oauth_token=?',(oauth_token,))

    def player_history_db_connection_close(self):
        conn.commit()
        conn.close()
