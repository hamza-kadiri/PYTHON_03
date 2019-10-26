from flask import Flask, request, jsonify, abort, g
from flask_cors import CORS
from form_validation import validate_add_serie_form, validate_user_registration_form, validate_user_login_form, validate_notifications_list_form
from database import init_models, save_obj, delete_obj, db_session
from models import User, Serie, Notification
from tmdb_api import search_tv_serie_by_title, get_tv_serie
from sqlalchemy.exc import IntegrityError
from flask_httpauth import HTTPTokenAuth
from api_exceptions import InvalidForm


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    CORS(app)
    # Set globals
    init_models()
    auth = HTTPTokenAuth(scheme='Token')
    with app.app_context():

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db_session.remove()  # Teardown connexion after every request

        @auth.verify_token
        def verify_token(token):
            # try to authenticate by token
            user = User.verify_auth_token(token)
            if not user:
                return False
            g.user = user
            return True

        @app.route('/token', methods=['POST'])
        def generate_auth_token():
            username, password = validate_user_login_form(request.form) # Might raise an InvalidForm exception
            # try to authenticate with username/password
            user = User.get_user_by_username(username)
            if not user or not user.verify_password(password):
                abort(401)
            g.user = user
            token = g.user.generate_auth_token()
            return jsonify({'token': token.decode('ascii'), "user":user.as_dict()})

        # Add some routes
        @app.route("/", methods=['GET'])
        def index():
            return jsonify("Welcome to our API")

        # TODO Handle multiple pages results
        @app.route("/search", methods=['GET'])
        @auth.login_required
        def search():
            query = request.args.get('query')
            return jsonify(search_tv_serie_by_title(query))

        @app.route("/series/<int:serie_id>", methods=['GET'])
        @auth.login_required
        def get_serie_details(serie_id):
            return jsonify(get_tv_serie(serie_id))

        @app.route("/users", methods=['POST'])
        def add_user():
            username, email, password = validate_user_registration_form(request.form) # Might raise an InvalidForm exception
            user = User(username, email, password)
            try:
                save_obj(user)
            except IntegrityError:
                abort(403)
            return jsonify(user.as_dict())

        @app.route("/users/<int:user_id>", methods=['GET'])
        @auth.login_required
        def get_user_details(user_id):
            if user_id != g.user.id:
                abort(403)
            user = User.get_user_by_id(user_id)
            if user is None:
                abort(404)
            return jsonify(user.as_dict())

        @app.route("/users/<int:user_id>/series", methods=['GET'])
        @auth.login_required
        def get_favorite_series(user_id):
            if user_id != g.user.id:
                abort(403)
            Serie.update_series(user_id)
            user = User.get_user_by_id(user_id)
            series = user.get_favorite_series()
            return jsonify({"series": [serie.as_dict() for serie in series]})

        @app.route("/users/<int:user_id>/series", methods=['POST'])
        @auth.login_required
        def add_serie_to_favorites(user_id):
            if user_id != g.user.id:
                abort(403)
            serie_id = validate_add_serie_form(request.form) # Might raise an InvalidForm exception
            user = User.get_user_by_id(user_id)
            serie = Serie.get_serie_by_id(serie_id)
            if serie is None:
                serie_json = get_tv_serie(serie_id)
                serie = Serie.from_json(serie_json)
                save_obj(serie)
            if user.get_subscription_by_serie_id(serie_id) is not None:
                abort(403)
            try:
                user.series.append(serie)
                save_obj(user)
                notif = Notification.from_serie(user_id, serie)
                app.logger.error(serie.as_dict())
                save_obj(notif)
                return jsonify({"user_id":user_id,"serie_id":serie_id})
            except IntegrityError:
                abort(403)

        @app.route("/users/<int:user_id>/series/<int:serie_id>", methods=['DELETE'])
        @auth.login_required
        def delete_serie_from_favorites(user_id, serie_id):
            if user_id != g.user.id:
                abort(403)
            user = User.get_user_by_id(user_id)
            serie = Serie.get_serie_by_id(serie_id)
            if not(serie in user.series):
                abort(404)
            try:
                user.series.remove(serie)
                save_obj(user)
            except IntegrityError:
                abort(403)
            except ValueError as err:
                abort(404)
            return jsonify({'user_id' : user_id, 'serie_id' : serie_id})


        @app.route("/users/<int:user_id>/notifications", methods=['GET'])
        @auth.login_required
        def get_notifications(user_id):
            if user_id != g.user.id:
                abort(403)
            Serie.update_series(user_id)
            notifications = Notification.get_notification_by_user_id(user_id)
            return jsonify({"notifications":[notification.as_dict() for notification in notifications]})


        @app.route("/users/<int:user_id>/notifications", methods=['POST'])
        @auth.login_required
        def mark_notifications_as_read(user_id):
            if user_id != g.user.id:
                abort(403)
            user = User.get_user_by_id(user_id)
            array_ids = validate_notifications_list_form(request.form)
            response_array = []
            for notification_id in array_ids:
                notification = Notification.get_notification_by_id(notification_id)
                if notification is None:
                    response_array.append({'id':notification_id,'status':404})
                elif notification.user_id != user_id:
                    response_array.append({'id': notification_id, 'status': 403})
                else :
                    notification.mark_as_read()
                    response_array.append({'id': notification_id, 'status': 200})
            return jsonify({'responses':response_array})

        @app.errorhandler(InvalidForm)
        def handle_invalid_usage(error):
            response = jsonify(error.to_dict())
            response.status_code = error.status_code
            app.logger.error(response)
            return response


        @app.errorhandler(403)
        def forbidden_error(error):
            return jsonify({'error_code': 403, 'error_message': 'This operation is forbidden'})

        @app.errorhandler(404)
        def not_found_error(error):
            app.logger.error('404 Not Found Error: %s', (error))
            return jsonify({'error_code': 404, 'error_message': 'The ressource you have requested could not be found'})

        @app.errorhandler(500)
        def internal_server_error(error):
            app.logger.error('Server Error: %s', (error))
            return jsonify({'error_code': 500, 'error_message': 'Internal Server Error'})

        @app.errorhandler(Exception)
        def unhandled_exception(error):
            app.logger.error('Unhandled Exception: %s \n Stack Trace: %s', (error, str(traceback.format_exc())))
            return jsonify({'error_code': 500, 'error_message': 'Internal Server Error'})

        @app.route("/serie/<serie_id>")
        def get_serie(serie_id):
            serie_id = int(serie_id)
            return jsonify(get_tv_serie(serie_id))
    return app


application = create_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
