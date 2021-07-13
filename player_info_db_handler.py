import sqlite3

#scoresaberのURLもここで格納されます。
class player_info_db_handler:
    def __init__(self):
        global conn,cur
        conn = sqlite3.connect("player_info.db")
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS playerInfo(score_saber_url TEXT,oauth_token TEXT,oauth_token_secret TEXT)')

    def scoresaber_info_insert(self,url):
        cur.execute('INSERT INTO playerInfo VALUES(score_saber_url)',url)

    def tokens_info_insert(self,oauth_token,oauth_token_secret):
        cur.execute('INSERT INTO playerInfo VALUES(oauth_token,oauth_token_secret)',(oauth_token,oauth_token_secret))

        conn.commit()
        conn.close()

    def player_info_export(self):
        cur.execute('SELECT * from tokenSets')
        return cur.fetchall()