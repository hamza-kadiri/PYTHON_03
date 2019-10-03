from flask import Flask, request, jsonify
from flask_cors import CORS

from omdb_api import search_tv_serie_by_title, get_tv_serie


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    CORS(app)
    # Set globals
    #db = SQLAlchemy()
    with app.app_context():
        # db.init_app(app)
        # Add some routes
        @app.route("/")
        def index():
            return jsonify("Hello, World!!!")

        @app.route("/search")
        def search():
            query = request.args.get('query')
            return jsonify(search_tv_serie_by_title(query))

        @app.route("/serie/<serie_id>")
        def get_serie(serie_id):
            serie_id = int(serie_id)
            return jsonify(get_tv_serie(serie_id))

    return app


application = create_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
