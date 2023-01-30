import flask
import os
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

APIKEY = os.getenv("APIKEY")

app = flask.Flask(__name__)


@app.route('/')
def index():

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
        params={"q": query, type: "video", "key": APIKEY},


    )

    response = response.json()
    for i in range(10):
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
                                 ['snippet']['thumbnail']['high']['url'])
        except:
            print("no thumbnail")

    return flask.render_template(
        "search_results.html",
        channelId=channelId,
        videoId=videoId,
        vid_title=vid_title,
        vid_thumbnail=vid_thumbnail,
        vid_description=vid_description
    )


@app.route('/video_view')
def video_view():
    return flask.render_template(
        "video_view.html"
    )


app.run(
    use_reloader=True,
    debug=True
)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Runing Main.py')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
