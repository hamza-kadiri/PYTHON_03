from flask import Flask, request, jsonify

from omdb_api import search_tv_serie_by_title

application = Flask(__name__)


@application.route("/")
def index():
    return "Hello, World!"


@application.route("/search")
def search():
    query = request.args.get('query')
    return jsonify(dict(search_tv_serie_by_title(query)))


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
