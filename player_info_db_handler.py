import sqlite3


# scoresaberのURLもここで格納されます。
class player_info_db_handler:
    def __init__(self):
        global conn, cur
        conn = sqlite3.connect("player_info.db")
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS playerInfo(score_saber_url TEXT,oauth_token TEXT,oauth_token_secret TEXT)')

    def player_info_insert(self, url, oauth_token, oauth_token_secret):
        cur.execute('INSERT INTO playerInfo VALUES(?,?,?)', (url, oauth_token, oauth_token_secret))

        conn.commit()
        conn.close()

    def player_info_export(self):
        cur.execute('SELECT * from playerInfo')
        return cur.fetchall()

    def player_info_delete(self,oauth_token):
        cur.execute('DELETE FROM playerInfo WHERE oauth_token=?',(oauth_token,))

    def player_info_db_connection_close(self):
        conn.commit()
        conn.close()
