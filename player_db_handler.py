import os
import psycopg2


# スコアセイバーのURLもここで格納されます。
class Player_db_handler:
    def __init__(self):
        global conn, cur
        # データベースのURLは環境変数に設定している
        link=os.environ.get('DATABASE_URL')
        conn = psycopg2.connect(link)
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS player_info('
            'score_saber_url TEXT,'
            'oauth_token TEXT,'
            'oauth_token_secret TEXT'
            ')'
        )
        cur.execute(
            'CREATE TABLE IF NOT EXISTS player_history('
            'oauth_token TEXT,'
            'date TEXT,'
            'player TEXT,'
            'pp REAL,'
            'gRanking INTEGER,'
            'lRanking INTEGER,'
            'topSong TEXT,'
            'topPP REAL,'
            'recent_play TEXT'
            ')'
        )

    # oauth_tokenに被りがあったらupdate
    def player_info_upsert(self, url, oauth_token, oauth_token_secret):
        cur.execute('DELETE FROM player_info WHERE oauth_token=%s',(oauth_token,))
        cur.execute(
            'INSERT INTO player_info VALUES (%s,%s,%s)',
            (url, oauth_token, oauth_token_secret)
        )


    def player_today_data_import(self, oauth_token, now_JST ,today_data):
        cur.execute(
            'INSERT INTO player_history ('
            'oauth_token,'
            'date,'
            'player,'
            'pp,'
            'gRanking,'
            'lRanking,'
            'topSong,'
            'topPP,'
            'recent_play'
            ') VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (
                oauth_token,
                now_JST,
                today_data[0],
                today_data[1],
                today_data[2],
                today_data[3],
                today_data[4],
                today_data[5],
                today_data[6]
            )
        )


    def player_info_export(self):
        cur.execute('SELECT * from player_info')
        return cur.fetchall()


    # yesterday_dataを取得してからoauth_tokenが一致するデータを全削除
    # スコアセイバーのアカウントの名前を変えた日は前日比は反映されない
    def player_yesterday_data_export(self, oauth_token, player):
        cur.execute(
            'SELECT player,pp,gRanking,lRanking,topSong,topPP '
            'FROM player_history '
            'WHERE oauth_token=%s AND player=%s', (oauth_token, player)
        )
        # oauth_tokenとnow_JSTはセレクトしていないのでyesterday_dataはtoday_dataと同じ構成
        yesterday_data = cur.fetchone()
        cur.execute('DELETE FROM player_history WHERE oauth_token=%s', (oauth_token,))
        return yesterday_data

    # Twitterの連携が切れたら
    def player_info_delete(self, oauth_token):
        cur.execute('DELETE FROM player_info WHERE oauth_token=%s', (oauth_token,))

    # Twitterの連携が切れたら
    def player_history_delete(self, oauth_token):
        cur.execute('DELETE FROM player_history WHERE oauth_token=%s', (oauth_token,))

    def player_db_connection_close(self):
        conn.commit()
        conn.close()