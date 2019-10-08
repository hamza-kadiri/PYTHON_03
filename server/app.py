from flask import Flask, request, jsonify, abort, g
from flask_cors import CORS
from form_validation import validate_add_serie_form, validate_user_registration_form
from database import init_db, save_obj
from models import User, Serie, Subscription
from tmdb_api import search_tv_serie_by_title, get_tv_serie
from sqlalchemy.exc import IntegrityError
from flask_httpauth import HTTPBasicAuth
from psycopg2.errors import UniqueViolation


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    CORS(app)
    # Set globals
    init_db()
    auth = HTTPBasicAuth()
    with app.app_context():

        @auth.verify_password
        def verify_password(username_or_token, password):
            # first try to authenticate by token
            user = User.verify_auth_token(username_or_token)
            if not user:
                # try to authenticate with username/password
                user = User.get_user_by_username(username_or_token)
                if not user or not user.verify_password(password):
                    return False
            g.user = user
            return True

        @app.route('/token')
        #@auth.login_required
        def get_auth_token():
            token = g.user.generate_auth_token()
            return jsonify({'token': token.decode('ascii')})

        # Add some routes
        @app.route("/", methods=['GET'])
        def index():
            return jsonify("Welcome to our API")

        # TODO Handle multiple pages results
        @app.route("/search", methods=['GET'])
        #@auth.login_required
        def search():
            query = request.args.get('query')
            return search_tv_serie_by_title(query)

        @app.route("/series/<int:serie_id>", methods=['GET'])
        #@auth.login_required
        def get_serie_details(serie_id):
            return get_tv_serie(serie_id)

        @app.route("/users", methods=['POST'])
        def add_user():
            if not validate_user_registration_form(request.form):
                abort(400)
            user = User(request.form['username'], request.form['email'], request.form['password'])
            try:
                save_obj(user)
            except IntegrityError:
                abort(403)
            except IntegrityError:
                abort(403)
            return user.as_dict()

        # TODO Add auth
        @app.route("/users/<int:user_id>", methods=['GET'])
        @auth.login_required
        def get_user_details(user_id):
            if user_id != g.user.id:
                abort(403)
            user = User.get_user_by_id(user_id)
            if user is None:
                abort(404)
            return user.as_dict()

        # TODO Add auth
        @app.route("/users/<int:user_id>/series", methods=['POST'])
        @auth.login_required
        def add_serie_to_favorites(user_id):
            if user_id != g.user.id:
                abort(403)
            if not validate_add_serie_form(request.form):
                abort(400)
            serie_id = request.form['serie_id']
            if Serie.get_serie_by_id(serie_id) is None:
                serie_json = get_tv_serie(serie_id)
                serie = Serie.from_json(serie_json)
                save_obj(serie)
            subscription = Subscription(user_id, serie_id)
            try:
                save_obj(subscription)
            except IntegrityError:
                abort(403)
            return subscription.as_dict()

        @app.errorhandler(403)
        def forbidden_error(error):
            return {'error_code': 403, 'error_message': 'This operation is forbidden'}

        @app.errorhandler(404)
        def not_found_error(error):
            app.logger.error('404 Not Found Error: %s', (error))
            return {'error_code': 404, 'error_message': 'The ressource you have requested could not be found'}

        @app.errorhandler(500)
        def internal_server_error(error):
            app.logger.error('Server Error: %s', (error))
            return {'error_code': 500, 'error_message': 'Internal Server Error'}

        @app.errorhandler(Exception)
        def unhandled_exception(error):
            app.logger.error('Unhandled Exception: %s \n Stack Trace: %s', (error, str(traceback.format_exc())))
            return {'error_code': 500, 'error_message': 'Internal Server Error'}


        @app.route("/serie/<serie_id>")
        def get_serie(serie_id):
            serie_id = int(serie_id)
            return jsonify(get_tv_serie(serie_id))
    return app


application = create_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
