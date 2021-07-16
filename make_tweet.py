from datetime import datetime
from decimal import *

import unicodedata

string_count = 0;
tweet_sentence = ""


def decimalCalculation(float1, float2):
    result = Decimal(str(float1)) - Decimal(str(float2))
    return result


def stringCount(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in "FWA":
            count += 2
        else:
            count += 1
    return count


def ry(count):
    if count >= 280:
        return True
    else:
        return False


def addText(text):
    # これをしないとローカル変数とみなされ関数内の変更が反映されない
    global string_count, tweet_sentence
    if string_count == 0:
        string_count += stringCount(text)
    else:
        string_count += stringCount(text) + 1
    if not ry(string_count):
        print(text)
        tweet_sentence += text + "\n"


def make_tweet(yesterday_data, today_data):
    addText(today_data[0])

    if ry(string_count):
        print("以下略")
    else:

        # yesterday_data[1] is Noneとすると'NoneType' object is not subscriptableのエラーが出る
        if yesterday_data is None:
            addText(f"pp:{today_data[1]}")
        else:
            if today_data[1] == yesterday_data[1]:
                addText(f"pp:{today_data[1]}(前日比:0pp)")
            # For nerf
            elif today_data[1] < yesterday_data[1]:
                ppDiff = decimalCalculation(today_data[1], yesterday_data[1])
                addText(f"pp:{today_data[1]}(前日比:{ppDiff}pp)")
            else:
                ppDiff = decimalCalculation(today_data[1], yesterday_data[1])
                addText(f"pp:{today_data[1]}(前日比:+{ppDiff}pp)")

        if ry(string_count):
            print("以下略")
        else:

            if yesterday_data is None:
                addText(f"GR:#{today_data[2]}")
            else:
                if today_data[2] == yesterday_data[2]:
                    addText(f"GR:#{today_data[2]}(前日比:0)")
                elif today_data[2] < yesterday_data[2]:
                    gRankingDiff = decimalCalculation(yesterday_data[2], today_data[2])
                    addText(f"GR:#{today_data[2]}(前日比:+{gRankingDiff})")
                else:
                    gRankingDiff = decimalCalculation(yesterday_data[2], today_data[2])
                    addText(f"GR:#{today_data[2]}(前日比:{gRankingDiff})")

            if ry(string_count):
                print("以下略")
            else:

                if yesterday_data is None:
                    addText(f"LR:#{today_data[3]}")
                else:
                    if today_data[3] == yesterday_data[3]:
                        addText(f"LR:#{today_data[3]}(前日比:0)")
                    elif today_data[3] < yesterday_data[3]:
                        lRankingDiff = decimalCalculation(yesterday_data[3], today_data[3])
                        addText(f"LR:#{today_data[3]}(前日比:+{lRankingDiff})")
                    else:
                        lRankingDiff = decimalCalculation(yesterday_data[3], today_data[3])
                        addText(f"LR:#{today_data[3]}(前日比:{lRankingDiff})")

                if ry(string_count):
                    print("以下略")
                else:

                    if yesterday_data is None or yesterday_data[5] is None:
                        pass
                    else:
                        if today_data[4] != yesterday_data[4]:
                            addText(f"！トップソング更新！\nMAP:{today_data[4]}\npp:{today_data[5]}")
                        elif today_data[4] == yesterday_data[4] and today_data[5] > yesterday_data[5]:
                            topPPDiff = decimalCalculation(today_data[5], yesterday_data[5])
                            addText(f"！トップスコア更新！\nMAP:{today_data[4]}\npp:{today_data[5]}(前日比:+{topPPDiff})")

                    if ry(string_count):
                        print("以下略")
                    else:

                        how_long_not_play = datetime.now().replace(microsecond=0) - today_data[6]
                        if how_long_not_play.days >= 1:
                            how_long_not_play = how_long_not_play.days
                            addText(f"\n最新のスコア送信:{how_long_not_play}日前")
                        else:
                            how_long_not_play_hour = int(how_long_not_play.total_seconds() / 3600)
                            how_long_not_play_minute = int(how_long_not_play.total_seconds() % 3600 / 60)
                            addText(f"\n最新のスコア送信:{how_long_not_play_hour}時間{how_long_not_play_minute}分前")

    return tweet_sentence
