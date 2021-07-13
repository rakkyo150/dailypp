from datetime import datetime

import unicodedata
from pytz import timezone
from bs4 import BeautifulSoup
import requests
import re
import sqlite3
from decimal import *

from player_info_db_handler import player_info_db_handler
import secret
import twitter


string_count=0;
tweet_sentence=""

def decimalCalculation(float1,float2):
    result=Decimal(str(float1))-Decimal(str(float2))
    return result

def stringCount(text):
    count=0
    for c in text:
        if unicodedata.east_asian_width(c) in "FWA":
            count+=2
        else:
            count+=1
    return count

def ry(count):
    if count>=280:
        return True
    else:
        return False

def addText(text):
    # これをしないとローカル変数とみなされ関数内の変更が反映されない
    global string_count,tweet_sentence
    if string_count==0:
        string_count+=stringCount(text)
    else:
        string_count+=stringCount(text)+1
    if not ry(string_count):
        print(text)
        tweet_sentence+=text+"\n"

#機能のオンオフも追加するかも？
enable_config=(True,True,True,True)

#スクレイピングのデータベース準備
conn=sqlite3.connect('playerHistory.db')
cur=conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS history('
            'date TEXT,'
            'user TEXT,'
            'pp REAL,'
            'gRanking INTEGER,'
            'lRanking INTEGER,'
            'topSong TEXT,topPP INTEGER)'
            )

#oauth関連のデータベースを参照
player_info_db=player_info_db_handler()
player_info_list=player_info_db.player_info_export()

#登録人数分繰り返し
for url,token,token_secret in player_info_list:


    # ツイート権限付与
    auth = twitter.OAuth(consumer_key=secret.consumer_key,
                         consumer_secret=secret.consumer_secret,
                         token=token,
                         token_secret=token_secret)
    tweet = twitter.Twitter(auth=auth)

    scoreSaber_link=url

    '''スクレイピング開始'''

    #スクレイピング・解析
    html_doc = requests.get(scoreSaber_link).text
    html_doc_recent = requests.get(scoreSaber_link + "&sort=2").text
    soup = BeautifulSoup(html_doc, "html.parser")
    soup_recent = BeautifulSoup(html_doc_recent, "html.parser")

    # find_allはResultset(listという認識でok)を返すので、直接get_textやcontentsやstringやtextは使えないので、欲しい要素がなるべく近くなるように使う
    #名前のスクレイピング
    name_tags = soup.find("h5", class_="title is-5")
    name = name_tags.get_text(strip=True)


    #グローバルランキングのスクレイピング
    global_ranking_tag=soup.find("a",href="/global")
    global_ranking=global_ranking_tag.string
    today_gRanking=int(global_ranking.replace("#",""))

    #CSSセレクタだと返り値はResultsetになるので注意
    #ローカルランキングのスクレイピング
    local_ranking_tag=soup.find("a",href=re.compile("country"))
    local_ranking=local_ranking_tag.get_text(strip=True)
    today_lRanking=int(local_ranking.replace("#",""))

    #PPのスクレイピング
    lis=soup.find_all("li")
    for li in lis:
        if "Performance" in li.get_text():
            pp=li.get_text()
            pp=pp.replace("Performance Points: ","")
    today_pp=float(re.sub(r"[pp|,]","",pp))

    #トップソングのスクレイピング
    topSong_tag=soup.find("span",class_="songTop pp")
    topSong=topSong_tag.text

    #トップソングのPPのスクレイピング
    topPP_tag=soup.find("span",class_="scoreTop ppValue")
    topPP=float(topPP_tag.string)

    #最新のスコア送信のスクレイピング
    recent_song=soup_recent.find("span",class_="songBottom time")
    recent_play_UTC_str=recent_song.get("title")
    recent_play_UTC_str=recent_play_UTC_str.replace(" UTC","")
    recent_play_UTC=datetime.strptime(recent_play_UTC_str,"%Y-%m-%d %H:%M:%S")

    '''スクレイピング終了'''

    # 名前が一致するひとつ前のデータを選択・出力
    cur.execute('SELECT max(date),pp,gRanking,lRanking,topSong,topPP from history where user=?', name)
    yesterday_data = cur.fetchone()

    #最新のデータをデータベースに入力
    cur.execute('INSERT INTO history VALUES (datetime("now","localtime"),?,?,?,?,?,?)',(
        name,
        today_pp,
        today_gRanking,
        today_lRanking,
        topSong,
        topPP
    )
                )

    how_long_not_play = datetime.now().replace(microsecond=0) - recent_play_UTC


    '''ツイート作成'''

    addText(name)

    if ry(string_count):
        print("以下略")
    else:

        if yesterday_data[1]==None:
            addText(f"pp:{pp}")
        else:
            if today_pp==yesterday_data[1]:
                addText(f"pp:{pp}(前日比:0pp)")
            #For nerf
            elif today_pp<yesterday_data[1]:
                ppDiff=decimalCalculation(today_pp, yesterday_data[1])
                addText(f"pp:{pp}(前日比:{ppDiff}pp)")
            else:
                ppDiff=decimalCalculation(today_pp, yesterday_data[1])
                addText(f"pp:{pp}(前日比:+{ppDiff}pp)")

        if ry(string_count):
            print("以下略")
        else:

            if yesterday_data[2]==None:
                addText(f"GR:#{today_gRanking}")
            else:
                if today_gRanking==yesterday_data[2]:
                    addText(f"GR:#{today_gRanking}(前日比:0)")
                elif today_gRanking<yesterday_data[2]:
                    gRankingDiff=decimalCalculation(yesterday_data[2],today_gRanking)
                    addText(f"GR:#{today_gRanking}(前日比:+{gRankingDiff})")
                else:
                    gRankingDiff=decimalCalculation(yesterday_data[2],today_gRanking)
                    addText(f"GR:#{today_gRanking}(前日比:{gRankingDiff})")

            if ry(string_count):
                print("以下略")
            else:

                if yesterday_data[3]==None:
                    addText(f"LR:#{today_lRanking}")
                else:
                    if today_lRanking==yesterday_data[3]:
                        addText(f"LR:#{today_lRanking}(前日比:0)")
                    elif today_lRanking<yesterday_data[3]:
                        lRankingDiff=decimalCalculation(yesterday_data[3],today_lRanking)
                        addText(f"LR:#{today_lRanking}(前日比:+{lRankingDiff})")
                    else:
                        lRankingDiff = decimalCalculation(yesterday_data[3], today_lRanking)
                        addText(f"LR:#{today_lRanking}(前日比:{lRankingDiff})")

                if ry(string_count):
                    print("以下略")
                else:

                    if yesterday_data[4]==None or yesterday_data[5]==None:
                        pass
                    else:
                        if topSong!=yesterday_data[4]:
                            addText(f"！トップソング更新！\nMAP:{topSong}\npp:{topPP}")
                        elif topSong==yesterday_data[4] and topPP>yesterday_data[5]:
                            topPPDiff=decimalCalculation(topPP,yesterday_data[5])
                            addText(f"！トップスコア更新！\nMAP:{topSong}\npp:{topPP}(前日比:+{topPPDiff})")

                    if ry(string_count):
                        print("以下略")
                    else:

                        if how_long_not_play.days>=1:
                            how_long_not_play=how_long_not_play.days
                            addText(f"\n最新のスコア送信:{how_long_not_play}日前")
                        else:
                            how_long_not_play_hour=int(how_long_not_play.total_seconds()/3600)
                            how_long_not_play_minute=int(how_long_not_play.total_seconds()%3600/60)
                            addText(f"\n最新のスコア送信:{how_long_not_play_hour}時間{how_long_not_play_minute}分前")

    print(string_count)

    '''ツイート作成終了'''

    cur.execute('SELECT * FROM history')
    print(cur.fetchall())

    #ツイート
    tweet.status.update(status=tweet_sentence)

conn.commit()
conn.close()