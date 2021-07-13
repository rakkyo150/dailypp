from urllib.parse import parse_qsl
from flask import Flask,jsonify,request,render_template,redirect,session
from requests_oauthlib import OAuth1Session
import secret
from player_info_db_handler import player_info_db_handler

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX Rnaxaixaixai~XHH!jmN]LWX/,?RT'

base_url="https://api.twitter.com/"

request_token_url=base_url+"oauth/request_token"
authenticate_url=base_url+"oauth/authenticate"
access_token_url=base_url+"oauth/access_token"

@app.route('/',methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/scoresaber_register',methods=['GET'])
def register_scoresaber():
    return render_template("index2.html")
    session["url"]=function()

@app.route('/twitter/request_token',methods=['GET'])
def get_twitter_request_token():

    #Twitter Application Managementで設定したURLを使う
    oauth_callback=request.args.get('http://127.0.0.1:50000/callback/twitter.html')

    twitter=OAuth1Session(secret.consumer_key,secret.consumer_secret)

    response=twitter.post(
        request_token_url,
        params={"oauth_callback":oauth_callback}
    )

    request_token=dict(parse_qsl((response.content.decode("utf-8"))))

    authenticate_endpoint="%s?oauth_token=%s"\
        %(authenticate_url,request_token["oauth_token"])

    request_token.update({"authenticate_endpoint":authenticate_endpoint})

    print(request_token)

    return redirect(request_token["authenticate_endpoint"])

@app.route('/callback/twitter.html',methods=['GET'])
def get_twitter_access_token():
     oauth_token=request.args.get("oauth_token")
     oauth_verifier=request.args.get("oauth_verifier")

     twitter=OAuth1Session(
         secret.consumer_key,
         secret.consumer_secret,
         oauth_token,
         oauth_verifier,
     )

     response=twitter.post(
         access_token_url,
         params={"oauth_verifier":oauth_verifier}
     )

     access_token=dict(parse_qsl(response.content.decode("utf-8")))

     session["oauth_token"]=access_token["oauth_token"]
     session["oauth_token_secret"]=access_token["oauth_token_secret"]

     player_info_db=player_info_db_handler()
     player_info_db.player_info_insert(session["url"],access_token["oauth_token"],access_token["oauth_token_secret"])

     return render_template("index3.html")


if __name__=="__main__":
    app.run(port=50000)