from validator_collection import checkers, validators, errors

def validate_user_registration_form(form):
    username = form.get('username')
    username_valid = checkers.is_string(username)
    password = form.get('password')
    password_valid = checkers.is_string(password)
    email = form.get('email')
    email_valid = checkers.is_email(email)
    return username_valid & password_valid & email_valid

def validate_add_serie_form(form):
    serie_id = form.get('serie_id')
    serie_id_valid = checkers.is_integer(serie_id)
    return serie_id_valid