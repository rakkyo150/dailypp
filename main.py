from datetime import datetime
import time

from make_tweet import make_tweet
from twitter_handler import Twitter_handler
from player_db_handler import Player_db_handler
from scraping import Scraping

# 機能のオンオフも追加するかも？
enable_config = (True, True, True, True)

# スクレイピングのデータベース準備
player_db = Player_db_handler()

# oauth関連のデータベースを参照
player_info_list = player_db.player_info_export()

# 登録人数分繰り返し
for url, oauth_token, oauth_token_secret in player_info_list:
    scoreSaber_link = "https://scoresaber.com/u/" + url
    print(oauth_token,oauth_token_secret)

    # 連携が切れたならデータベースのデータを削除
    twitter_handler_api=Twitter_handler(oauth_token,oauth_token_secret)
    if twitter_handler_api.verify_credentials() is False:
        player_db.player_info_delete(oauth_token)
        player_db.player_history_delete(oauth_token)
    else:

        '''スクレイピング開始'''

        # スクレイピング・解析
        scraping = Scraping(scoreSaber_link)

        # 0=name,1=pp,2=global_ranking,3=local_ranking,4=topSong,5=tpoPP,6=recent_play_UTC
        today_data = []

        # スコアセイバーの名前(player)のスクレイピング
        today_data.append(scraping.name())

        # PPのスクレイピング
        today_data.append(scraping.today_pp())

        # グローバルランキングのスクレイピング
        today_data.append(scraping.global_ranking())

        # ローカルランキングのスクレイピング
        today_data.append(scraping.local_ranking())

        # トップソングのスクレイピング
        today_data.append(scraping.topSong())

        # トップソングのPPのスクレイピング
        today_data.append(scraping.topPP())

        # 最新のスコア送信のスクレイピング
        today_data.append(scraping.recent_play_JST())

        print("スクレイピング終了。1秒待つ。")
        time.sleep(1)

        '''スクレイピング終了'''

        # スコアセイバーの名前が一致する昨日のデータ出力してから削除
        yesterday_data = player_db.player_yesterday_data_export(oauth_token, today_data[0])

        # 現在時刻は日本標準時を使う
        JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
        now_JST = datetime.now(JST)

        # 最新のデータをデータベースに入力
        player_db.player_today_data_import(oauth_token, now_JST, today_data)

        how_long_not_play = now_JST.replace(microsecond=0) - today_data[6]

        # ツイート作成
        tweet_sentence = make_tweet(yesterday_data, today_data, now_JST)

        # ツイート
        twitter_handler_api.send_tweet(tweet_sentence)

player_db.player_db_connection_close()
