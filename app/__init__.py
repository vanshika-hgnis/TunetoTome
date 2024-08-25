# app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Import the Blueprint and register it
    from app.views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
