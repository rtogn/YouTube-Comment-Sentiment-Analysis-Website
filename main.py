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


# this function is for converting large number of likes, comments and subscribers to 1.4K or 2.5M
def numbersuffix(number):
    # suffixes i.e million = m or thousand = K
    suffixes = ['', 'K', 'M', 'B', 'T']
    index = 0
    while number >= 1000 and index < len(suffixes) - 1:
        number /= 1000.0
        index += 1
    return f"{number:,.1f}{suffixes[index]}"


@app.route('/search_results', methods=["GET", "POST"])
def search_results():

    max_result = 6
    videoId = []
    videoTitle = []
    videoThumbnail = []
    channelId = []
    channelTitle = []
    channelThumbnail = []
    channelsubscriberCount = []

    form_data = flask.request.args

    query = form_data.get("term", "")

    search_url = "https://www.googleapis.com/youtube/v3/search?"
    search_params = {
        "q": query,
        "part": "snippet",
        "type": "video",
        "maxResults": max_result,
        "key": APIKEY

    }
    responseSearch = requests.get(search_url, search_params)
    # print(responseSearch.text)

    responseSearch = responseSearch.json()

    for i in range(max_result):

        try:
            channelId.append(
                responseSearch["items"][i]['snippet']['channelId'])
        except:
            print("no channelid")

        try:
            videoId.append(responseSearch["items"][i]['id']['videoId'])
        except:
            print("no videoid")
        try:
            videoTitle.append(responseSearch["items"][i]['snippet']['title'])
        except:
            print("no videotitle")
        try:
            videoThumbnail.append(responseSearch["items"][i]
                                  ['snippet']['thumbnails']['high']['url'])
        except:
            print("no video thumbnail")

    print(channelId)

    channel_url = "https://www.googleapis.com/youtube/v3/channels?"
    channel_params = {
        "id": ','.join(channelId),
        "part": "snippet, statistics",
        "key": APIKEY,

    }
    responseChannel = requests.get(channel_url, channel_params)
    print(responseChannel.text)

    responseChannel = responseChannel.json()

    for x in range(len(channelId)):

        try:
            channelTitle.append(
                responseChannel["items"][x]['snippet']['title'])
        except:
            channelTitle.append("no title")

        try:
            channelThumbnail.append(responseChannel["items"][x]
                                    ['snippet']['thumbnails']['default']['url'])
        except:
            channelThumbnail.append("no thumbnail")

        try:
            channelsubscriberCount.append(numbersuffix(float(
                responseChannel["items"][x]['statistics']['subscriberCount'])))
        except:
            channelsubscriberCount.append("no subscriber")

    return flask.render_template(
        "search_results.html",

        videoId=videoId,
        videoTitle=videoTitle,
        channelId=channelId,
        videoThumbnail=videoThumbnail,
        channelTitle=channelTitle,
        channelThumbnail=channelThumbnail,
        channelsubscriberCount=channelsubscriberCount,

    )


@app.route('/video_view/', methods=["GET", "POST"])
def video_view():
    max_comments = 100

    videoTitle = []
    channelTitle = []
    subscriberCount = []
    commentCount = []
    likeCount = []
    channelThumbnail = []
    channelsubscriberCount = []
    channelId = []
    authorDisplayname = []
    authorProfileImageUrl = []
    textDisplay = []
    sent_score = []
    ave_sent_score = []

    form_data = flask.request.args
    # print("\n\n\n")
    # print(form_data)
    # print("\n\n\n")
    query = form_data.get("watch?v", "")
    # print(query)

    video_url = "https://www.googleapis.com/youtube/v3/videos?"
    video_params = {
        "id": query,
        "part": 'snippet, statistics',
        "type": "video",
        "key": APIKEY,

    }
    responseVideo = requests.get(video_url, video_params)
    # print(responseVideo.text)
    responseVideo = responseVideo.json()

    try:
        videoTitle = responseVideo["items"][0]['snippet']['title']
    except:
        print("no title")

    try:
        channelId = responseVideo["items"][0]['snippet']['channelId']
    except:
        print("no channelid")

    try:
        commentCount = numbersuffix(float(
            responseVideo["items"][0]['statistics']['commentCount']))
    except:
        print("")

    try:
        likeCount = numbersuffix(float(
            responseVideo["items"][0]['statistics']['likeCount']))
    except:
        print("")

    channel_url = "https://www.googleapis.com/youtube/v3/channels?"
    channel_params = {
        "id": channelId,
        "part": "snippet, statistics",
        "key": APIKEY,

    }
    responseChannelVid = requests.get(channel_url, channel_params)
    print(responseChannelVid.text)

    responseChannelVid = responseChannelVid.json()

    try:
        channelTitle = responseChannelVid["items"][0]['snippet']['title']
    except:
        print("no title")

    try:
        channelThumbnail = responseChannelVid["items"][0]['snippet']['thumbnails']['default']['url']
    except:
        print("no thumbnail")

    try:
        channelsubscriberCount = numbersuffix(float(
            responseChannelVid["items"][0]['statistics']['subscriberCount']))
    except:
        print("no subscriber")

    comments_url = "https://www.googleapis.com/youtube/v3/commentThreads?"
    comments_params = {
        "videoId": query,
        "part": "snippet",
        "key": APIKEY,
        "maxResults": max_comments,
        "textFormat": 'plainText',
        "order": 'relevance'

    }
    responseComments = requests.get(comments_url, comments_params)
    # print(responseComments.text)

    responseComments = responseComments.json()

    for i in range(max_comments):

        try:
            authorProfileImageUrl.append(
                responseComments["items"][i][
                    'snippet']['topLevelComment']['snippet']['authorProfileImageUrl'])
        except:
            print("no profile")

        try:
            authorDisplayname.append(
                responseComments["items"][i]['snippet']['topLevelComment'][
                    'snippet']['authorDisplayName'])
        except:
            print("no author")

        try:
            textDisplay.append(
                responseComments["items"][i]['snippet']['topLevelComment'][
                    'snippet']['textDisplay'])
            sent_score.append(sentScore(responseComments["items"][i]['snippet']['topLevelComment'][
                'snippet']['textDisplay']))
        except:
            print("")

    ave_sent_score = aveSentScore(textDisplay)

    # print(textDisplay)
    # print(authorDisplayname)

    return flask.render_template(
        "video_view.html",
        videoId=query,
        videoTitle=videoTitle,
        subscriberCount=subscriberCount,
        commentCount=commentCount,
        likeCount=likeCount,
        channelThumbnail=channelThumbnail,
        channelsubscriberCount=channelsubscriberCount,
        channelId=channelId,
        channelTitle=channelTitle,
        authorDisplayname=authorDisplayname,
        authorProfileImageUrl=authorProfileImageUrl,
        textDisplay=textDisplay,
        sent_score=sent_score,
        ave_sent_score=ave_sent_score

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
