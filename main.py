from datetime import datetime

import make_tweet
import send_tweet
from player_history_db_handler import player_history_db_handler
from player_info_db_handler import player_info_db_handler
from scraping import scraping

# 機能のオンオフも追加するかも？
enable_config = (True, True, True, True)

# スクレイピングのデータベース準備
player_history_db = player_history_db_handler()

# oauth関連のデータベースを参照
player_info_db = player_info_db_handler()
player_info_list = player_info_db.player_info_export()

# 登録人数分繰り返し
for url, token, token_secret in player_info_list:
    scoreSaber_link = "https://scoresaber.com/u/" + url

    '''スクレイピング開始'''

    # スクレイピング・解析
    scraping = scraping(scoreSaber_link)

    # 0=name,1=pp,2=global_ranking,3=local_ranking,4=topSong,5=tpoPP,6=recent_play_UTC
    today_data = []

    # 名前のスクレイピング
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
    today_data.append(scraping.recent_play_UTC())

    print(today_data)
    print(type(today_data[0]))

    '''スクレイピング終了'''

    # 名前が一致する昨日のデータ出力
    yesterday_data = player_history_db.player_yesterday_data_export(today_data[0])

    # 最新のデータをデータベースに入力
    player_history_db.player_today_data_import(today_data)

    how_long_not_play = datetime.now().replace(microsecond=0) - today_data[6]

    # ツイート作成
    tweet_sentence = make_tweet.make_tweet(yesterday_data, today_data)

    # ツイート
    send_tweet.send_tweet(tweet_sentence, token, token_secret)
