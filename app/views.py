# app/views.py

import requests
from flask import Blueprint, render_template,jsonify
from requests import request
from geniusapi import get_image_html, search_song_and_recommend


# Create a Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# Error handlers
@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404



client_access_token = "kuxm_2_TG5XXwjFrFF5zK8PGx9RxIlSXYRInuMFB7GAmRLFhlOvl1kfzuRMgAOp2"

# Route to handle search requests
@main.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term')
    client_access_token = "kuxm_2_TG5XXwjFrFF5zK8PGx9RxIlSXYRInuMFB7GAmRLFhlOvl1kfzuRMgAOp2"
    recommendations = search_song_and_recommend(search_term, client_access_token)
    
    # Format response
    response = []
    for rec in recommendations:
        response.append({
            'original_song': rec['original_song'],
            'similar_songs': rec['similar_songs']
        })
    
    return jsonify(response)

        
    

    
