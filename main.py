import flask, os, requests

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template(
        "index.html"
    )

app.run(
        use_reloader = True,
        debug=True
)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Runing Main.py')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
