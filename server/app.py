from flask import Flask, request, jsonify

from omdb_api import search_tv_serie_by_title


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
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
            return (jsonify(search_tv_serie_by_title(query)))

    return app


application = create_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
