from urllib.parse import parse_qsl
import os

from flask import Flask, request, render_template, redirect, session
from requests_oauthlib import OAuth1Session

from player_db_handler import Player_db_handler

app = Flask(__name__)
# ちゃんと変更しました
app.secret_key = os.environ["session_key"]

base_url = "https://api.twitter.com/"

request_token_url = base_url + "oauth/request_token"
authenticate_url = base_url + "oauth/authenticate"
access_token_url = base_url + "oauth/access_token"


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/scoresaber_register_form', methods=['GET'])
def register_form():
    return render_template("index2.html")


@app.route('/scoresaber_register_execute', methods=['POST'])
def register_execute():
    session["url"] = request.form["url"]
    return render_template("index3.html", verification=session["url"])


# twitterの連携確認画面作成
@app.route('/twitter/request_token', methods=['GET'])
def get_twitter_request_token():
    # Twitter Application Managementで設定したURLを使う
    oauth_callback = request.args.get('http://127.0.0.1:50000/callback/twitter.html')

    twitter = OAuth1Session(os.environ["consumer_key"], os.environ["consumer_secret"])

    response = twitter.post(
        request_token_url,
        params={"oauth_callback": oauth_callback}
    )

    request_token = dict(parse_qsl((response.content.decode("utf-8"))))

    authenticate_endpoint = "%s?oauth_token=%s" \
                            % (authenticate_url, request_token["oauth_token"])

    request_token.update({"authenticate_endpoint": authenticate_endpoint})

    print(request_token)

    return redirect(request_token["authenticate_endpoint"])


# 連携後
@app.route('/callback/twitter.html', methods=['GET'])
def get_twitter_access_token():
    oauth_token = request.args.get("oauth_token")
    oauth_verifier = request.args.get("oauth_verifier")

    twitter = OAuth1Session(
        os.environ["consumer_key"],
        os.environ["consumer_secret"],
        oauth_token,
        oauth_verifier,
    )

    response = twitter.post(
        access_token_url,
        params={"oauth_verifier": oauth_verifier}
    )

    access_token = dict(parse_qsl(response.content.decode("utf-8")))

    session["oauth_token"] = access_token["oauth_token"]
    session["oauth_token_secret"] = access_token["oauth_token_secret"]

    player_info_db = Player_db_handler()
    player_info_db.player_info_insert(
        session["url"],
        session["oauth_token"],
        session["oauth_token_secret"]
    )
    player_info_db.player_db_connection_close()

    return render_template("index4.html")


if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0',port=port)
