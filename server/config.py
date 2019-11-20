class Config(object):
    """DB Base config."""
    DB_SERVER = 'db'
    DB_USER = 'admin'
    DB_PASSWORD = 'password'
    DB_NAME = 'series_app'
    DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_SERVER, DB_NAME)
    DROP_ON_INIT = True

    """API Config"""
    API_KEY = "84eae13884eb7a9e47fcc760ca08f593"
    API_URL = "https://api.themoviedb.org/3"
    ORIGINAL_BASE_URL = "https://image.tmdb.org/t/p/original"
    THUMBNAIL_BASE_URL = "https://image.tmdb.org/t/p/w300"
    BACKDROP_BASE_URL = "https://image.tmdb.org/t/p/w1280"
    POSTER_BASE_URL = "https://image.tmdb.org/t/p/w185"

    """Auth Config"""
    SECRET_KEY = "gjEq2dHoU3A45WhDQDGJTj3jF8MHa6oN"

    """Mail Config"""
    MAILING_HOST = 'smtp.gmail.com'
    MAILING_PORT = 465
    MAILING_ADDRESS = "my.series.no.reply@gmail.com"
    MAILING_PASSWORD = "test1234@"
    