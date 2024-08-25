# app/views.py

from flask import Blueprint, render_template

# Create a Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# Error handlers
@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
