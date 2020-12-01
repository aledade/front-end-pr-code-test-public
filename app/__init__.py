from flask import Flask
import os
from flask_assets import Environment, Bundle
from flask_migrate import Migrate
from app.models import db
from app.views import app_view

app = Flask(__name__)

# Set up asset management
env = Environment()
assets_config = {
    'base_css': Bundle(
        'css/base.css',
        'bower_components/bootstrap/dist/css/bootstrap.css',
        output='gen/base.css'
    ),

    'main_js': Bundle(
        'bower_components/jquery/dist/jquery.js',
        'bower_components/jquery-ui/jquery-ui.js',
        'bower_components/bootstrap/dist/js/bootstrap.js',
        'js/base.js',
        output='gen/main.js'
    ),
}

for asset, bundle in assets_config.items():
    env.register(asset, bundle)

migrate = Migrate()


def create_app():
    # Setup app configurations
    app.config.update(dict(
        SQLALCHEMY_DATABASE_URI='sqlite:///../test.db',
        DEBUG=True,
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='password',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    ))

    # Setup SQLAlchemy
    db.init_app(app)

    # Setup environment assets
    env.init_app(app)

    # Setup migrations
    migrate.init_app(app, db)

    # Register app views
    app.register_blueprint(app_view, url_prefix='')
    return app
