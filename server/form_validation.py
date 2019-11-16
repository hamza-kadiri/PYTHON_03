from validator_collection import checkers, validators, errors
from api_exceptions import InvalidForm, InvalidField


def validate_user_registration_form(json):
    username = json['username']
    username_valid = checkers.is_not_empty(username) and checkers.is_string(username)
    password = json['password']
    password_valid = checkers.is_not_empty(password) and checkers.is_string(password)
    email = json['email']
    email_valid = checkers.is_email(email)
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
    username = json['username']
    username_valid = checkers.is_not_empty(username) and checkers.is_string(username)
    password = json['password']
    password_valid = checkers.is_not_empty(password) and checkers.is_string(password)
    invalid_fields = []
    if not username_valid:
        invalid_fields.append(InvalidField('username', 'Invalid username'))
    if not password_valid:
        invalid_fields.append(InvalidField('password', 'Invalid password'))
    if not (username_valid & password_valid):
        raise InvalidForm(invalid_fields)
    return username, password


def validate_add_serie_form(form:dict):
    serie_id = form.get('serie_id')
    serie_id_valid = checkers.is_integer(serie_id)
    invalid_fields = []
    if not serie_id_valid:
        invalid_fields.append(InvalidField('serie_id', f'Invalid value : {serie_id}'))
        raise InvalidForm(invalid_fields)
    return serie_id


def validate_notifications_list_form(form:dict):
    array_ids = form.get('notifications')
    array_ids_valid = checkers.is_iterable(array_ids)
    invalid_fields = []
    if not array_ids_valid:
        invalid_fields.append(InvalidField('array_ids', f'Invalid value (Must be an iterable) : {array_ids}'))
        raise InvalidForm(invalid_fields)
    for notif_id in array_ids:
        notif_id_valid = checkers.is_string(notif_id)
        if not notif_id:
            invalid_fields.append(InvalidField('array_ids', f'Invalid id : {id}'))
    if len(invalid_fields) > 0:
        raise InvalidForm(invalid_fields)
    return array_ids
