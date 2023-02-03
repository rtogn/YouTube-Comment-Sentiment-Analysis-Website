import flask
import os
from flask_sqlalchemy import SQLAlchemy
import requests
#from dotenv import find_dotenv, load_dotenv

# Local Imports
import sql_models # Required to get SQL model access.
import sql_admin_functions
import sql_models

#load_dotenv(find_dotenv())

APIKEY = os.getenv("APIKEY")

app = flask.Flask(__name__)

db = SQLAlchemy()
db_name = "YT_Sentiment_App"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name + ".db"
db.init_app(app)

@app.route('/')
def index():
    # Set up DB with random entries (not for final code)
    #sql_admin_functions.sql_add_demo_data_random(db, 20)
    return flask.render_template(
        "index.html"
    )
@app.route('/search_results')
def search_results():
    return flask.render_template(
        "search_results.html"
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

import sql_requests
@app.route('/sql', methods=["GET", "POST"])
def sql_playground_temporary():
    if flask.request.method == "POST":
        form_data = flask.request.form
        target_row = db.session.execute(db.select(Video_Info).filter_by(id=form_data["video_id"])).scalar_one()
        #target_row.sentiment_score_average=form_data["new_score"]
        sql_requests.update_sentiment_average(target_row, float(form_data["new_score"]))
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
