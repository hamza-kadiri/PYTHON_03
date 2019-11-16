from validator_collection import checkers, validators, errors
from api_exceptions import InvalidForm, InvalidField


def validate_user_registration_form(json):
    try:
        username = json['username']
        username_valid = checkers.is_not_empty(username) and checkers.is_string(username)
    except TypeError:
        username_valid = False
    try:
        password = json['password']
        password_valid = checkers.is_not_empty(password) and checkers.is_string(password)
    except TypeError:
        password_valid = False
    try:
        email = json['email']
        email_valid = checkers.is_email(email)
    except TypeError:
        email_valid = False
    invalid_fields = []
    if not username_valid:
        invalid_fields.append(InvalidField('username', 'Invalid username'))
    if not password_valid:
        invalid_fields.append(InvalidField('password', 'Invalid password'))
    if not email_valid:
        invalid_fields.append(InvalidField('email', 'Invalid email'))
    if not (username_valid & password_valid & email_valid):
        raise InvalidForm(invalid_fields)
    return username, email, password


def validate_user_login_form(json):
    try:
        username = json['username']
        username_valid = checkers.is_not_empty(username) and checkers.is_string(username)
    except TypeError:
        username_valid = False
    try:
        password = json['password']
        password_valid = checkers.is_not_empty(password) and checkers.is_string(password)
    except TypeError:
        password_valid = False
    invalid_fields = []
    if not username_valid:
        invalid_fields.append(InvalidField('username', 'Invalid username'))
    if not password_valid:
        invalid_fields.append(InvalidField('password', 'Invalid password'))
    if not (username_valid & password_valid):
        raise InvalidForm(invalid_fields)
    return username, password


def validate_add_serie_form(json):
    try:
        serie_id = json['serie_id']
        serie_id_valid = checkers.is_integer(serie_id)
    except TypeError:
        serie_id_valid = False
    invalid_fields = []
    if not serie_id_valid:
        invalid_fields.append(InvalidField('serie_id', f'Invalid value'))
        raise InvalidForm(invalid_fields)
    return serie_id


def validate_notifications_list_form(json):
    try:
        array_ids = json['notifications']
        array_ids_valid = checkers.is_iterable(array_ids)
    except TypeError:
        array_ids_valid = False
    invalid_fields = []
    if not array_ids_valid:
        invalid_fields.append(InvalidField('array_ids', f'Invalid value (Must be an iterable)'))
    else:
        for notif_id in array_ids:
            notif_id_valid = checkers.is_string(notif_id)
            if not notif_id_valid:
                invalid_fields.append(InvalidField('array_ids', f'Invalid id : {id}'))
    if len(invalid_fields) > 0:
        raise InvalidForm(invalid_fields)
    return array_ids

def validate_favorite_form(json):
    try:
        user_id = json['user_id']
        user_id_valid = checkers.is_integer(user_id)
    except TypeError:
        user_id_valid = False
    serie_id_valid = False
    try:
        serie_id = json['serie_id']
        serie_id_valid = checkers.is_integer(serie_id)
    except TypeError:
        serie_id_valid = False
    invalid_fields = []
    if not serie_id_valid:
        invalid_fields.append(InvalidField('serie_id', f'Invalid value'))
    if not user_id_valid:
        invalid_fields.append(InvalidField('user_id', f'Invalid value'))
    if len(invalid_fields) > 0:
        raise InvalidForm(invalid_fields)
    return user_id, serie_id