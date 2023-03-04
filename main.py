import os
import requests
import flask
from flask import redirect, request, session
from dotenv import find_dotenv, load_dotenv
# Local Imports
from YTSA_Core_Files import sql_admin_functions, sql_requests, sql_models
from YTSA_Core_Files.sql_models import db
from vader import sentScore, aveSentScore

load_dotenv(find_dotenv())
APIKEY = os.getenv("APIKEY")

app = flask.Flask(__name__)
app.config.update(SECRET_KEY='12345')  # Key required for flask.session
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///YT_Sentiment_App.db"
db.init_app(app)

# Create tabels if empty
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Set default username if has not logged in yet to guest for display.
    if not session:
        session['user'] = 'Guest'

    # sql_admin_functions.sql_add_demo_data_random(db, 20)
    return flask.render_template(
        "index.html",
    )

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
            db_user = db.session.execute(db.select(sql_models.Users).filter_by(
                user_name=form_data["user_name"])).scalar_one()
            # If user is found in DB compare entered password to what is stored to validate (after decrypting)
            success = sql_admin_functions.validate_login(
                db_user, password_entered)
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

    channelTitle = []
    videoId = []
    vid_title = []
    vid_thumbnail = []

    form_data = flask.request.args

    print("\n\n\n")
    print(form_data)
    print("\n\n\n")

    query = form_data.get("term", "")

    response = requests.get(
        "https://www.googleapis.com/youtube/v3/search?",
        params={"q": query, "part": "snippet", "type": "video",
                "maxResults": 12, "key": APIKEY},
    )

    response = response.json()
    for i in range(12):

        try:
            channelTitle.append(
                response["items"][i]['snippet']['channelTitle'])
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
            vid_thumbnail.append(response["items"][i]
                                 ['snippet']['thumbnails']['high']['url'])
        except:
            print("no thumbnail")

    return flask.render_template(
        "search_results.html",

        channelTitle=channelTitle,
        videoId=videoId,
        vid_title=vid_title,
        vid_thumbnail=vid_thumbnail,

    )


@app.route('/video_view/', methods=["GET", "POST"])
def video_view():
    max_comments = 100

    vid_title = []
    channelTitle = []
    channelId = []
    authorDisplayname = []
    authorProfileImageUrl = []
    textDisplay = []
    sent_score = []
    
    form_data = flask.request.args

    videoId = form_data.get("watch?v", "")

    video_url = "https://www.googleapis.com/youtube/v3/videos?"
    video_params = {
        "id": videoId,
        "part": 'snippet',
        "type": "video",
        "key": APIKEY,

    }
    response = requests.get(video_url, video_params)
    response = response.json()

    vid_title = response["items"][0]['snippet']['title']
    channelTitle = response["items"][0]['snippet']['channelTitle']
    channelId = response["items"][0]['snippet']['channelId']

    comments_url = "https://www.googleapis.com/youtube/v3/commentThreads?"
    comments_params = {
        "videoId": videoId,
        "part": "snippet",
        "key": APIKEY,
        "maxResults": max_comments,
        "textFormat": 'plainText',
        "order": 'relevance'


    }
    r_comments = requests.get(comments_url, comments_params)
    r_comments = r_comments.json()

    for i in range(max_comments):

        try:
            authorProfileImageUrl.append(
                r_comments["items"][i][
                    'snippet']['topLevelComment']['snippet']['authorProfileImageUrl'])
        except:
            print("no profile")

        try:
            authorDisplayname.append(
                r_comments["items"][i]['snippet']['topLevelComment'][
                    'snippet']['authorDisplayName'])
        except:
            print("no author")

        try:
            textDisplay.append(
                r_comments["items"][i]['snippet']['topLevelComment'][
                    'snippet']['textDisplay'])
            sent_score.append(sentScore(r_comments["items"][i]['snippet']['topLevelComment'][
                    'snippet']['textDisplay']))
        except:
            print("")

    ave_sent_score = aveSentScore(textDisplay)
    
    return flask.render_template(
        "video_view.html",
        videoId=videoId,
        vid_title=vid_title,
        channelId=channelId,
        channelTitle=channelTitle,
        authorDisplayname=authorDisplayname,
        authorProfileImageUrl=authorProfileImageUrl,
        textDisplay=textDisplay,
        sent_score = sent_score,
        ave_sent_score = ave_sent_score
        

    )


@app.route('/sql', methods=["GET", "POST"])
def sql_playground_temporary():
    if flask.request.method == "POST":
        form_data = flask.request.form
        target_row = db.session.execute(db.select(sql_models.Video_Info).filter_by(
            id=form_data["video_id"])).scalar_one()
        # target_row.sentiment_score_average=form_data["new_score"]
        sql_requests.update_sentiment_average_video(
            target_row, float(form_data["new_score"]))
        db.session.commit()

    vids = sql_models.Video_Info.query.all()
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
