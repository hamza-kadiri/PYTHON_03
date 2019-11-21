def init_helpers_context(app):
    HelpersContext.init_helpers_context(app)

class HelpersContext:
    _has_been_initialized = False
    _thumbnail_base_url = None
    _backdrop_base_url = None
    _poster_base_url = None
    _original_base_url = None

    @classmethod
    def init_helpers_context(cls, app):
        try:
            cls._has_been_initialized = True
            cls._thumbnail_base_url = app.config['THUMBNAIL_BASE_URL']
            cls._backdrop_base_url = app.config['BACKDROP_BASE_URL']
            cls._poster_base_url = app.config['POSTER_BASE_URL']
            cls._original_base_url = app.config['ORIGINAL_BASE_URL']
        except RuntimeError:
            raise AttributeError(
                "Cannot initialize HelpersContext without a proper app configuration")

    @classmethod
    def get_thumbnail_base_url(cls):
        if not cls._has_been_initialized:
            raise AttributeError("Request Context not initialized")
        return cls._thumbnail_base_url

    @classmethod
    def get_backdrop_base_url(cls):
        if not cls._has_been_initialized:
            raise AttributeError("Request Context not initialized")
        return cls._backdrop_base_url

    @classmethod
    def get_poster_base_url(cls):
        if not cls._has_been_initialized:
            raise AttributeError("Request Context not initialized")
        return cls._poster_base_url

    @classmethod
    def get_original_base_url(cls):
        return cls._original_base_url

def generate_assets_url(dict) :
    if dict.get('poster_path') is not None:
        dict['poster_url'] = f"{HelpersContext.get_poster_base_url()}{dict.get('poster_path')}"
    if dict.get('backdrop_path') is not None:
        dict['backdrop_url'] = f"{HelpersContext.get_backdrop_base_url()}{dict.get('backdrop_path')}"
        dict['thumbnail_url'] = f"{HelpersContext.get_backdrop_base_url()}{dict.get('backdrop_path')}"
    if dict.get('still_path') is not None:
        dict['still_url'] = f"{HelpersContext.get_original_base_url()}{dict.get('still_path')}"
        dict['thumbnail_url'] = f"{HelpersContext.get_thumbnail_base_url()}{dict.get('still_path')}"
    return dict

def sortListByLambda(list,func):
    filteredList = filter(lambda x : func(x) != 0,list)
    numberZero = filter(lambda x : func(x) == 0,list)
    sortedList = sorted(filteredList, key=func)
    sortedList.extend(numberZero)
    return sortedList

