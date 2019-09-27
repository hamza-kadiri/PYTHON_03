class Config(object):
    """DB Base config."""
    DB_SERVER = 'db'
    DB_USER = 'admin'
    DB_PASSWORD = 'password'
    DB_NAME = 'series_app'

    @property
    def DATABASE_URI(self):         # Note: all caps
        return 'postgresql://{}:{}@{}/{}'.format(self.DB_USER, self.DB_PASSWORD, self.DB_SERVER, self.DB_NAME)

    """API Config"""

    API_KEY = "84eae13884eb7a9e47fcc760ca08f593"
    API_URL = "https://api.themoviedb.org/3"
    THUMBNAIL_BASE_URL = "https://image.tmdb.org/t/p/w300"
