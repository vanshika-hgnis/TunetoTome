
# from flask import Flask
# from flask_cors import CORS

# def create_app():
#     app = Flask(__name__)
#     CORS(app)  
#     app.config.from_object('app.config.Config')
#     app.config['DEBUG'] = True

#     # Import the Blueprint and register it
#     from app.views import main as main_blueprint
#     app.register_blueprint(main_blueprint)

#     # Add a test route to the main app
#     @app.route('/test_app')
#     def test_app():
#         return "Main app is working!"

#     return app


from flask import Flask, send_from_directory
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app)  
    app.config.from_object('app.config.Config')
    app.config['DEBUG'] = True

    # Import the Blueprint and register it
    from app.views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    print("Registered main blueprint")

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    @app.route('/test_app')
    def test_app():
        return "Main app is working!"

    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"- {rule}")

    return app

print("App initialization completed.")