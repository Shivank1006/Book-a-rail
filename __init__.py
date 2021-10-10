import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='secret',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth
    app.register_blueprint(auth.bp)

    from . import user
    app.register_blueprint(user.bp)
    app.add_url_rule('/home', endpoint='user.index')
    app.add_url_rule('/schedule', endpoint='user.schedule')
    app.add_url_rule('/book', endpoint='user.book')
    app.add_url_rule('/history', endpoint='user.history')
    app.add_url_rule('/search', endpoint='user.search')

    return app