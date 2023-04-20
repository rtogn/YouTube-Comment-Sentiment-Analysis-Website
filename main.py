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
# pylint: disable=no-name-in-module
from YTSA_Core_Files import sql_admin_functions, sql_requests
from YTSA_Core_Files import sql_models as sqm
from YTSA_Core_Files.sql_models import db
from vader import sent_score, ave_sent_score, get_formatted_score, get_text_rating

load_dotenv(find_dotenv())
APIKEY = os.getenv("APIKEY")

app = flask.Flask(__name__)
app.config.update(SECRET_KEY='12345')  # Key required for flask.session
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///YT_Sentiment_App.db"
db.init_app(app)

# Create tables if empty
with app.app_context():
    db.create_all()


@app.route('/',  methods=["GET", "POST"])
def index():
    """_summary_
    Route to base page of website
    """
    # Set default username if has not logged in yet to guest for display.

    username = 'guest'
    if 'user_name' in session:
        username = session['user_name']

    # registration form
    if flask.request.method == "POST":
        form_data = flask.request.form

        if "register_submit" in flask.request.form:
            username = form_data["user_name"]
            password = form_data["password"]
            email = form_data["email"]
            message = sql_admin_functions.register_user(
                username, password, email)

            if message == "Registration successful":
                session['user_name'] = username
                # Registration successful, close popup
                return flask.redirect('/?username=' + username)

            # Registration failed, display error message in popup
            return flask.render_template(
                "index.html",
                register_error=message
            )

    # sql_admin_functions.sql_add_demo_data_random(db, 20)
    # Call get_top_five() to get the top 5 videos.
    vids = sql_requests.get_top_five()

    # Extract the video IDs from the VideoInfo objects and store them in a list.
    video_ids = [vid.video_id for vid in vids]

    video_info_list = []
    for video_id in video_ids:
        url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id=' + \
            video_id + '&key=' + APIKEY
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            video_info = response.json()['items'][0]['snippet']
            video_info['video_id'] = video_id
            video_info['sentiment_score'] = [
                vid.sentiment_score_average for vid in vids if vid.video_id == video_id][0]
            video_info_list.append(video_info)

    num_vids = len(video_info_list)
    return flask.render_template(
        "index.html",
        num_vids=num_vids,
        video_info_list=video_info_list,
        user=username
    )


@app.route('/login', methods=["GET", "POST"])
def login_page():
    """_summary_
    Route to bare login page for testing

    """
    if flask.request.method == 'POST':
        # Get the form data from the request object
        username = flask.request.form['user_name']
        password = flask.request.form['password']

        # Query the database for the user
        user = sqm.Users.query.filter_by(user_name=username).first()

        # Check if user and password are valid
        if sql_admin_functions.validate_login(user, password):
            # Store the user's ID in the session
            flask.session['user_id'] = user.id
            flask.session['user_name'] = user.user_name
            return flask.redirect('/?username=' + username)

        # Handle invalid login credentials
        error = 'Invalid username or password'
        return flask.render_template('index.html', error=error)

    # GET request, render the login page
    return flask.render_template('index.html')


# Logout route


@app.route('/logout')
def logout():
    """_summary_
    Route to bare logout page for testing

    """
    # Clear the user session and redirect to login page
    flask.session.clear()
    return flask.redirect('/')

# this function is for converting large number of likes,
# comments and subscribers to 1.4K or 2.5M


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
    vid_dict = {
        "video_id": [],
        "video_title": [],
        "video_thumbnail": [],
        "channel_id": [],
        "channel_title": [],
        "channel_thumbnail": [],
        "channel_subscriber_count": []
    }

    form_data = flask.request.args

    # search for the query term
    query = form_data.get("term", "")

    search_url = "https://www.googleapis.com/youtube/v3/search?"
    search_params = {
        "q": query,
        "part": "snippet",
        "type": "video",
        "maxResults": max_result,
        "key": APIKEY

    }
    # json response of the data
    response_search = requests.get(search_url, search_params, timeout=30)
    response_search = response_search.json()

    for i in range(max_result):

        try:
            vid_dict["channel_id"].append(
                response_search["items"][i]['snippet']['channelId'])
        except IndexError:
            print("no channelid")

        try:
            vid_dict["video_id"].append(
                response_search["items"][i]['id']['videoId'])
        except IndexError:
            print("no videoid")
        try:
            vid_dict["video_title"].append(
                response_search["items"][i]['snippet']['title'])
        except IndexError:
            print("no videotitle")
        try:
            vid_dict["video_thumbnail"].append(
                response_search["items"][i]['snippet']['thumbnails']['high']['url'])
        except IndexError:
            print("no video thumbnail")

        channel_url = "https://www.googleapis.com/youtube/v3/channels?"
        channel_params = {
            "id": (vid_dict["channel_id"][i]),
            "part": "snippet,statistics",
            "key": APIKEY
        }

        response_channel = requests.get(
            channel_url, channel_params, timeout=30)
        response_channel = response_channel.json()

        try:
            vid_dict["channel_title"].append(
                response_channel["items"][0]['snippet']['title'])
        except IndexError:
            vid_dict["channel_title"].append("no title")

        try:
            vid_dict["channel_thumbnail"].append(
                response_channel["items"][0]['snippet']['thumbnails']['default']['url'])
        except IndexError:
            vid_dict["channel_thumbnail"].append("no thumbnail")

        try:
            vid_dict["channel_subscriber_count"].append(
                number_suffix(
                    float(
                        response_channel["items"][0]['statistics']['subscriberCount'])))
        except IndexError:
            vid_dict["channel_subscriber_count"].append("no subscriber")

    return flask.render_template(
        "search_results.html",
        videoId=vid_dict["video_id"],
        videoTitle=vid_dict["video_title"],
        channelId=vid_dict["channel_id"],
        videoThumbnail=vid_dict["video_thumbnail"],
        channelTitle=vid_dict["channel_title"],
        channelThumbnail=vid_dict["channel_thumbnail"],
        channelsubscriberCount=vid_dict["channel_subscriber_count"],
        user=session.get('user_name'),

    )


@app.route('/video_view/', methods=["GET", "POST"])
def video_view():
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-locals
    """_summary_
    Route to Video view page
    """
    max_comments = 100

    vid_dict = {
        "video_title": [],
        "channel_title": [],
        "subscriber_count": [],
        "comment_count": [],
        "view_count": [],
        "like_count": "",
        "channel_thumbnail": [],
        "channelsub_scriber_count": [],
        "channel_id": [],
        "author_display_name": [],
        "author_profile_image_url": [],
        "text_display": [],
        "sent_scores": [],
        "ave_sent_scores": []
    }

    form_data = flask.request.args

    query = form_data.get("watch?v", "")

    video_url = "https://www.googleapis.com/youtube/v3/videos?"
    video_params = {
        "id": query,
        "part": 'snippet, statistics',
        "type": "video",
        "key": APIKEY,

    }
    response_video = requests.get(video_url, video_params, timeout=30)
    response_video = response_video.json()

    try:
        vid_dict["video_title"] = response_video["items"][0]['snippet']['title']
    except KeyError:
        print("no title")

    try:
        vid_dict["channel_id"] = response_video["items"][0]['snippet']['channelId']
    except KeyError:
        print("no channelid")

    try:
        vid_dict["comment_count"] = number_suffix(float(
            response_video["items"][0]['statistics']['commentCount']))
    except KeyError:
        print("")

    try:
        vid_dict["like_count"] = number_suffix(float(
            response_video["items"][0]['statistics']['likeCount']))
    except KeyError:
        print("")

    try:
        vid_dict["view_count"] = number_suffix(float(
            response_video["items"][0]['statistics']['viewCount']))
    except KeyError:
        print("")

    channel_url = "https://www.googleapis.com/youtube/v3/channels?"
    channel_params = {
        "id": vid_dict["channel_id"],
        "part": "snippet, statistics",
        "key": APIKEY,

    }
    response_channel_vid = requests.get(
        channel_url, channel_params, timeout=30)

    response_channel_vid = response_channel_vid.json()

    try:
        vid_dict["channel_title"] = response_channel_vid["items"][0]['snippet']['title']
    except KeyError:
        print("no title")

    try:
        vid_dict["channel_thumbnail"] = (response_channel_vid["items"][0]
                                         ['snippet']['thumbnails']['default']['url'])
    except KeyError:
        print("no thumbnail")

    try:
        vid_dict["channelsub_scriber_count"] = number_suffix(float(
            response_channel_vid["items"][0]['statistics']['subscriberCount']))
    except KeyError:
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
    response_comments = response_comments.json()

    for i in range(max_comments):

        try:
            vid_dict["author_profile_image_url"].append(
                response_comments["items"][i]['snippet']['topLevelComment']
                    ['snippet']['authorProfileImageUrl'])
        except IndexError:
            print("no profile")

        try:
            vid_dict["author_display_name"].append(
                response_comments["items"][i]['snippet']['topLevelComment'][
                    'snippet']['authorDisplayName'])
        except IndexError:
            print("no author")

        try:
            vid_dict["text_display"].append(
                response_comments["items"][i]['snippet']['topLevelComment']
                ['snippet']['textDisplay'])
            vid_dict["sent_scores"].append(
                get_formatted_score(sent_score(
                    response_comments["items"][i]['snippet']['topLevelComment']
                    ['snippet']['textDisplay'])))
        except IndexError:
            print("")

    raw_ave = ave_sent_score(vid_dict["text_display"])
    ave_sent_scores = get_formatted_score(raw_ave)
    score_ratings = get_text_rating(raw_ave)
    sql_requests.add_video(query, vid_dict, raw_ave)

    return flask.render_template(
        "video_view.html",
        videoId=query,
        videoTitle=vid_dict["video_title"],
        subscriberCount=vid_dict["subscriber_count"],
        commentCount=vid_dict["comment_count"],
        likeCount=vid_dict["like_count"],
        viewCount=vid_dict["view_count"],
        channelThumbnail=vid_dict["channel_thumbnail"],
        channelsubscriberCount=vid_dict["channelsub_scriber_count"],
        channelId=vid_dict["channel_id"],
        channelTitle=vid_dict["channel_title"],
        authorDisplayname=vid_dict["author_display_name"],
        authorProfileImageUrl=vid_dict["author_profile_image_url"],
        textDisplay=vid_dict["text_display"],
        sent_score=vid_dict["sent_scores"],
        ave_sent_score=ave_sent_scores,
        score_rating=score_ratings,
        max_comments=max_comments,
        len=len,
        user=session.get('user_name'),
    )


@app.route('/sql', methods=["GET", "POST"])
def sql_playground_temporary():
    """_summary_
    Route to SQL Demo Page
    """
    # sql_admin_functions.add_live_test_vids()
    sql_admin_functions.register_user("admin", "1234", "admin@ytsa.com")
    sql_requests.get_top_five()
    if flask.request.method == "POST":
        form_data = flask.request.form
        target_row = db.session.execute(db.select(sqm.VideoInfo).filter_by(
            id=form_data["video_id"])).scalar_one()
        # target_row.sentiment_score_average=form_data["new_score"]
        sql_requests.set_sent_arvrg_video(
            target_row, float(form_data["new_score"]))
        db.session.commit()

    vids = sqm.VideoInfo.query.all()

    num_vids = len(vids)
    return flask.render_template(
        "sql_playground_temporary.html",
        num_vids=num_vids,
        vids=vids
    )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(
        use_reloader=True,
        debug=True
    )
    print('Runing Main.py')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
