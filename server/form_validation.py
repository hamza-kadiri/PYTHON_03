from validator_collection import checkers, validators, errors
from api_exceptions import InvalidForm, InvalidField

def validate_user_registration_form(form):
    username = form.get('username')
    username_valid = checkers.is_string(username)
    password = form.get('password')
    password_valid = checkers.is_string(password)
    email = form.get('email')
    email_valid = checkers.is_email(email)
    invalid_fields = []
    if not username_valid:
        invalid_fields.append(InvalidField('username',f'Invalid value : {username}'))
    if not password_valid:
        invalid_fields.append(InvalidField('password',f'Invalid value : {password}'))
    if not email_valid:
        invalid_fields.append(InvalidField('email',f'Invalid value : {email}'))
    if not (username_valid & password_valid & email_valid):
        raise InvalidForm(invalid_fields)
    return True

def validate_user_login_form(form):
    username = form.get('username')
    username_valid = checkers.is_string(username)
    password = form.get('password')
    password_valid = checkers.is_string(password)
    invalid_fields = []
    if not username_valid:
        invalid_fields.append(InvalidField('username',f'Invalid value : {username}'))
    if not password_valid:
        invalid_fields.append(InvalidField('password',f'Invalid value : {password}'))
    if not (username_valid & password_valid):
        raise InvalidForm(invalid_fields)
    return True

def validate_add_serie_form(form):
    serie_id = form.get('serie_id')
    serie_id_valid = checkers.is_integer(serie_id)
    invalid_fields = []
    if not serie_id_valid:
        invalid_fields.append(InvalidField('serie_id',f'Invalid value : {serie_id}'))
    if not serie_id_valid:
        raise InvalidForm(invalid_fields)
    return True