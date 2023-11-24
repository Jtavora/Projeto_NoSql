import flask
from routes import configure_routes

app = flask.Flask(__name__)

if __name__ == '__main__':
    configure_routes(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
