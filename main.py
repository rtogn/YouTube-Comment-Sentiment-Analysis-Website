import os
import requests
import flask
from flask import redirect, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv
# Local Imports
import sql_admin_functions
import sql_requests
import sql_models

load_dotenv(find_dotenv())
APIKEY = os.getenv("APIKEY")

app = flask.Flask(__name__)
app.config.update(SECRET_KEY='12345') # Key required for flask.session
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///YT_Sentiment_Ap.db"
db.init_app(app)

@app.route('/')
def index():
    # Set default username if has not logged in yet to guest for display.
    if not session:
        session['user'] = 'Guest'

    # sql_admin_functions.sql_add_demo_data_random(db, 20)
    return flask.render_template(
        "index.html",
    )

# Users DB class. Will move to sql_models.py ASAP
class Users(db.Model):
    # Easy reference for top videos by sentiment
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)

# Login page with basic functions (there is a link on the sidebar from index)
@app.route('/login', methods=["GET", "POST"])
def login_page():
    message = "Welcome to the YTSA!"

    if flask.request.method == "POST":
        form_data = flask.request.form
        # Get pass string entered into form
        db_user = None
        password_entered = form_data["password"]
        try:
            # Attempt to get user name from table, if not result in failure and display message
            db_user = db.session.execute(db.select(Users).filter_by(
                user_name=form_data["user_name"])).scalar_one()
            # If user is found in DB compare entered password to what is stored to validate (after decrypting)
            success = sql_admin_functions.validate_login(db_user, password_entered)
            # Add retreived username to sessoin
            session['user'] = db_user.user_name
            # Manually set modified to true https://flask.palletsprojects.com/en/2.2.x/api/?highlight=session#flask.session
            session.modified = True
        except:
            print("User not found in table")
            success = False

        # Send update with username for message or redirect back to main page
        # Else update message to reflect bad login.
        if success:
            return redirect("/", code=302)
        else:
            message = "Invalid login credentials"

    return flask.render_template(
        "login.html",
        login_message=message
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
