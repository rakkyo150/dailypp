import re
import datetime as dt

import requests
from bs4 import BeautifulSoup


class Scraping:
    def __init__(self, link):
        global soup, soup_recent
        html_doc = requests.get(link).text
        html_doc_recent = requests.get(link + "&sort=2").text
        soup = BeautifulSoup(html_doc, "html.parser")
        soup_recent = BeautifulSoup(html_doc_recent, "html.parser")

    # find_allはResultset(listという認識でok)を返すので、直接get_textやcontentsやstringやtextは使えないので、欲しい要素がなるべく近くなるように使う
    def name(self):
        name_tags = soup.find("h5", class_="title is-5")
        return name_tags.get_text(strip=True)

    def global_ranking(self):
        global_ranking_tag = soup.find("a", href="/global")
        global_ranking = global_ranking_tag.string
        return int(global_ranking.replace("#", ""))

    # CSSセレクタだと返り値はResultsetになるので注意
    def local_ranking(self):
        local_ranking_tag = soup.find("a", href=re.compile("country"))
        local_ranking = local_ranking_tag.get_text(strip=True)
        return int(local_ranking.replace("#", ""))

    def today_pp(self):
        lis = soup.find_all("li")
        for li in lis:
            if "Performance" in li.get_text():
                pp = li.get_text()
                pp = pp.replace("Performance Points: ", "")
        return float(re.sub(r"[pp|,]", "", pp))

    def topSong(self):
        topSong_tag = soup.find("span", class_="songTop pp")
        return topSong_tag.text

    def topPP(self):
        topPP_tag = soup.find("span", class_="scoreTop ppValue")
        return float(topPP_tag.string)

    def recent_play_JST(self):
        JST = dt.timezone(dt.timedelta(hours=+9), 'JST')
        UTC=dt.timezone(dt.timedelta(hours=0),'UTC')

        recent_song = soup_recent.find("span", class_="songBottom time")
        recent_play_UTC_str = recent_song.get("title")
        recent_play_UTC_str = recent_play_UTC_str.replace(" UTC", "")
        # tzinfoの付与忘れないこと
        recent_play_UTC = dt.datetime.strptime(recent_play_UTC_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)
        recent_play_JST = recent_play_UTC.astimezone(JST)
        return recent_play_JST
