import flask
import os
from flask_sqlalchemy import SQLAlchemy
import requests
from dotenv import find_dotenv, load_dotenv

# Local Imports
import sql_models # Required to get SQL model access.
import sql_admin_functions

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
    sql_admin_functions.sql_add_demo_data_random(db, 20)
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

app.run(
    use_reloader=True,
    debug=True
)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Runing Main.py')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
