from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from form_validation import validate_add_serie_form, validate_user_registration_form
from database import init_db, save_obj
from models import User
from tmdb_api import search_tv_serie_by_title
from sqlalchemy.exc import IntegrityError


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    CORS(app)
    # Set globals
    init_db()
    with app.app_context():
        # db.create_all()
        # Add some routes
        @app.route("/", methods=['GET'])
        def index():
            return jsonify("Hello, World!!!")

        @app.route("/search", methods=['GET'])
        def search():
            query = request.args.get('query')
            return search_tv_serie_by_title(query)

        @app.route("/series/<int:serie_id>", methods=['GET'])
        def get_serie_details(serie_id):
            return {"serie_id": serie_id}

        @app.route("/users", methods=['POST'])
        def add_user():
            if not validate_user_registration_form(request.form):
                abort(400)
            user = User(request.form['username'],request.form['email'], request.form['password'])
            try:
                save_obj(user)
            except IntegrityError:
                abort(403)
            return {"isSaved":True}

        @app.route("/users/<int:user_id>", methods=['GET'])
        def get_user_details(user_id):
            return {"user_id": user_id}

        @app.route("/users/<int:user_id>/series", methods=['POST'])
        def add_serie_to_favorites(user_id):
            if not validate_add_serie_form(request.form):
                abort(400)
            serie_id = request.form['serie_id']
            return {"user_id": user_id, "serie_id": serie_id}

        @app.errorhandler(500)
        def internal_server_error(error):
            app.logger.error('Server Error: %s', (error))
            return {'error_code':'500','error_message':'Internal Server Error'}

        @app.errorhandler(Exception)
        def unhandled_exception(error):
            app.logger.error('Unhandled Exception: %s', (error))
            return {'error_code':'500','error_message':'Internal Server Error'}

    return app


application = create_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
