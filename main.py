import sql_requests
import flask
import os
from flask_sqlalchemy import SQLAlchemy
import requests
from dotenv import find_dotenv, load_dotenv


# Local Imports

import sql_models 
#import vader.py

import sql_models

#19dec91db46812de3b6c78d6df156f35fb56aa47

# Required to get SQL model access.
import sql_admin_functions
import sql_models

load_dotenv(find_dotenv())

APIKEY = os.getenv("APIKEY")

app = flask.Flask(__name__)

db = SQLAlchemy()
db_name = "YT_Sentiment_App"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name + ".db"
db.init_app(app)


@app.route('/')
def index():

    # Set up DB with random entries (not for final code)
    # sql_admin_functions.sql_add_demo_data_random(db, 20)
    return flask.render_template(
        "index.html",

    )


@app.route('/search_results', methods=["GET", "POST"])
def search_results():

    channelId = []
    videoId = []
    vid_title = []
    vid_thumbnail = []
    vid_description = []

    form_data = flask.request.args

    print("\n\n\n")
    print(form_data)
    print("\n\n\n")

    query = form_data.get("term", "")

    response = requests.get(
        "https://www.googleapis.com/youtube/v3/search?",
        params={"q": query, "part": "snippet", type: "video",
                "maxResults": 12, "key": APIKEY},
    )

    response = response.json()
    for i in range(12):
        try:
            channelId.append(response["items"][i]['snippet']['channelId'])
        except:
            print("")
        try:
            videoId.append(response["items"][i]['id']['videoId'])
        except:
            print("no video")
        try:
            vid_title.append(response["items"][i]['snippet']['title'])
        except:
            print("no title")
        try:
            vid_description.append(
                response["items"][i]['snippet']['description'])
        except:
            print("no description")
        try:
            vid_thumbnail.append(response["items"][i]
                                 ['snippet']['thumbnails']['high']['url'])
        except:
            print("no thumbnail")

    return flask.render_template(
        "search_results.html",
        channelId=channelId,
        videoId=videoId,
        vid_title=vid_title,
        vid_description=vid_description,
        vid_thumbnail=vid_thumbnail,

    )


@app.route('/video_view')
def video_view():
    return flask.render_template(
        "video_view.html"
    )


class Video_Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Video ID string, comes after "watch?v=". So for https://www.youtube.com/watch?v=jfKfPfyJRdk the ID is 'jfKfPfyJRdk'
    video_id = db.Column(db.String, nullable=False, unique=True)
    video_tite = db.Column(db.String, nullable=False)
    channel = db.Column(db.String)
    # Raw sentiment score as floating pt value
    sentiment_score_average = db.Column(db.Float)
    entry_count = db.Column(db.Integer, nullable=False)
    date_updated = db.Column(db.String, nullable=False)


@app.route('/sql', methods=["GET", "POST"])
def sql_playground_temporary():
    if flask.request.method == "POST":
        form_data = flask.request.form
        target_row = db.session.execute(db.select(Video_Info).filter_by(
            id=form_data["video_id"])).scalar_one()
        # target_row.sentiment_score_average=form_data["new_score"]
        sql_requests.update_sentiment_average(
            target_row, float(form_data["new_score"]))
        db.session.commit()

    vids = Video_Info.query.all()
    num_vids = len(vids)
    return flask.render_template(
        "sql_playground_temporary.html",
        num_vids=num_vids,
        vids=vids
    )


app.run(
    use_reloader=True,
    debug=True
)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Runing Main.py')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
