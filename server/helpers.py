def get_assets_url(app, dict) :
    poster_base_url = app.config["POSTER_BASE_URL"]
    backdrop_base_url = app.config["BACKDROP_BASE_URL"]
    thumbnail_base_url = app.config['THUMBNAIL_BASE_URL']
    original_base_url = app.config['ORIGINAL_BASE_URL']
    if dict.get('poster_path') is not None:
        dict['poster_url'] = f"{poster_base_url}{dict.get('poster_path')}"
    if dict.get('backdrop_path') is not None:
        dict['backdrop_url'] = f"{backdrop_base_url}{dict.get('backdrop_path')}"
        dict['thumbnail_url'] = f"{backdrop_base_url}{dict.get('backdrop_path')}"
    if dict.get('still_path') is not None:
        dict['still_url'] = f"{original_base_url}{dict.get('still_path')}"
        dict['thumbnail_url'] = f"{thumbnail_base_url}{dict.get('still_path')}"
    return dict
