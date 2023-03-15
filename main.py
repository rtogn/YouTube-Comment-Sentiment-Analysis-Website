"""_summary_
Main file of YTSA flask app
Routes for each page are defined as well as boilerplate setup. 
"""
import os
import requests
import flask
from flask import redirect, session
from dotenv import find_dotenv, load_dotenv
# Local Imports
from YTSA_Core_Files import sql_admin_functions, sql_requests, sql_models
from YTSA_Core_Files.sql_models import db
from vader import sent_score, ave_sent_score

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
    """_summary_
    Route to base page of website
    """
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
    """_summary_
    Route to bare login page for testing (will remove later in favor of popup)
    """
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
        except AttributeError:
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
def number_suffix(number):
    """_summary_
    # suffixes i.e million = m or thousand = K
    Args:
        number (_type_): _description_

    Returns:
        _type_: _description_
    """
    suffixes = ['', 'K', 'M', 'B', 'T']
    index_suffix = 0
    while number >= 1000 and index_suffix < len(suffixes) - 1:
        number /= 1000.0
        index_suffix += 1
    return f"{number:,.1f}{suffixes[index_suffix]}"


@app.route('/search_results', methods=["GET", "POST"])
def search_results():
    """_summary_
    Route to search results page
    """
    max_result = 6
    video_id = []
    video_title = []
    video_thumbnail = []
    channel_id = []
    channel_title = []
    channel_thumbnail = []
    channel_subscriber_count = []

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
    response_search = requests.get(search_url, search_params, timeout=30)
    # print(responseSearch.text)

    response_search = response_search.json()

    for i in range(max_result):

        try:
            channel_id.append(
                response_search["items"][i]['snippet']['channelId'])
        except AttributeError:
            print("no channelid")

        try:
            video_id.append(response_search["items"][i]['id']['videoId'])
        except AttributeError:
            print("no videoid")
        try:
            video_title.append(response_search["items"][i]['snippet']['title'])
        except AttributeError:
            print("no videotitle")
        try:
            video_thumbnail.append(response_search["items"][i]
                                  ['snippet']['thumbnails']['high']['url'])
        except AttributeError:
            print("no video thumbnail")

    print(channel_id)

    channel_url = "https://www.googleapis.com/youtube/v3/channels?"
    channel_params = {
        "id": ','.join(channel_id),
        "part": "snippet, statistics",
        "key": APIKEY,

    }
    response_channel = requests.get(channel_url, channel_params, timeout=30)
    print(response_channel.text)

    response_channel = response_channel.json()

    for x in range(len(channel_id)):

        try:
            channel_title.append(
                response_channel["items"][x]['snippet']['title'])
        except AttributeError:
            channel_title.append("no title")

        try:
            channel_thumbnail.append(response_channel["items"][x]
                                    ['snippet']['thumbnails']['default']['url'])
        except AttributeError:
            channel_thumbnail.append("no thumbnail")

        try:
            channel_subscriber_count.append(number_suffix(float(
                response_channel["items"][x]['statistics']['subscriberCount'])))
        except AttributeError:
            channel_subscriber_count.append("no subscriber")

    return flask.render_template(
        "search_results.html",

        videoId=video_id,
        videoTitle=video_title,
        channelId=channel_id,
        videoThumbnail=video_thumbnail,
        channelTitle=channel_title,
        channelThumbnail=channel_thumbnail,
        channelsubscriberCount=channel_subscriber_count,

    )


@app.route('/video_view/', methods=["GET", "POST"])
def video_view():
    """_summary_
    Route to Video view page
    """
    max_comments = 100

    video_title = []
    channel_title = []
    subscriber_count = []
    comment_count = []
    like_count = []
    channel_thumbnail = []
    channelsub_scriber_count = []
    channel_id = []
    author_display_name = []
    author_profile_image_url = []
    text_display = []
    sent_scores = []
    ave_sent_scores = []

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
    response_video = requests.get(video_url, video_params, timeout=30)
    # print(responseVideo.text)
    response_video = response_video.json()

    try:
        video_title = response_video["items"][0]['snippet']['title']
    except AttributeError:
        print("no title")

    try:
        channel_id = response_video["items"][0]['snippet']['channelId']
    except AttributeError:
        print("no channelid")

    try:
        comment_count = number_suffix(float(
            response_video["items"][0]['statistics']['commentCount']))
    except AttributeError:
        print("")

    try:
        like_count = number_suffix(float(
            response_video["items"][0]['statistics']['likeCount']))
    except AttributeError:
        print("")

    channel_url = "https://www.googleapis.com/youtube/v3/channels?"
    channel_params = {
        "id": channel_id,
        "part": "snippet, statistics",
        "key": APIKEY,

    }
    response_channel_vid = requests.get(channel_url, channel_params, timeout=30)
    print(response_channel_vid.text)

    response_channel_vid = response_channel_vid.json()

    try:
        channel_title = response_channel_vid["items"][0]['snippet']['title']
    except AttributeError:
        print("no title")

    try:
        channel_thumbnail = response_channel_vid["items"][0]['snippet']['thumbnails']['default']['url']
    except AttributeError:
        print("no thumbnail")

    try:
        channelsub_scriber_count = number_suffix(float(
            response_channel_vid["items"][0]['statistics']['subscriberCount']))
    except AttributeError:
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
    response_comments = requests.get(comments_url, comments_params, timeout=30)
    # print(responseComments.text)

    response_comments = response_comments.json()

    for i in range(max_comments):

        try:
            author_profile_image_url.append(
                response_comments["items"][i][
                    'snippet']['topLevelComment']['snippet']['authorProfileImageUrl'])
        except AttributeError:
            print("no profile")

        try:
            author_display_name.append(
                response_comments["items"][i]['snippet']['topLevelComment'][
                    'snippet']['authorDisplayName'])
        except AttributeError:
            print("no author")

        try:
            text_display.append(
                response_comments["items"][i]['snippet']['topLevelComment'][
                    'snippet']['textDisplay'])
            sent_scores.append(sent_score(response_comments["items"][i]['snippet']['topLevelComment'][
                'snippet']['textDisplay']))
        except AttributeError:
            print("")

    ave_sent_scores = ave_sent_score(text_display)

    # print(textDisplay)
    # print(authorDisplayname)

    return flask.render_template(
        "video_view.html",
        videoId=query,
        videoTitle=video_title,
        subscriberCount=subscriber_count,
        commentCount=comment_count,
        likeCount=like_count,
        channelThumbnail=channel_thumbnail,
        channelsubscriberCount=channelsub_scriber_count,
        channelId=channel_id,
        channelTitle=channel_title,
        authorDisplayname=author_display_name,
        authorProfileImageUrl=author_profile_image_url,
        textDisplay=text_display,
        sent_score=sent_scores,
        ave_sent_score=ave_sent_scores

    )


@app.route('/sql', methods=["GET", "POST"])
def sql_playground_temporary():
    """_summary_
    Route to SQL Demo Page
    """
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
