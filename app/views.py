import requests
from flask import Blueprint, render_template, jsonify, request
from .geniusapi import search_song_and_recommend,search_song_and_recommend_ex

# Create a Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# Error handlers
@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404



@main.route('/search_song', methods=['GET'])
def search_song():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    headers = {
        "Authorization": f"Bearer {GENIUS_API_TOKEN}"
    }
    params = {
        "q": query
    }
    
    # Make a GET request to the Genius API
    response = requests.get("https://api.genius.com/search", headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()

        # Extract song information from the response
        songs = [
            {
                "title": hit["result"]["title"], 
                "id": hit["result"]["id"],
                "image_url": hit["result"]["song_art_image_url"]
            }
            for hit in data["response"]["hits"]
        ]

        return jsonify(songs)
    else:
        return jsonify({"error": "Unable to fetch songs"}), response.status_code






@main.route('/api/recommend-songs', methods=['POST'])
def recommend_songs():
    data = request.json
    search_term = data.get('search_term')
    client_access_token = "kuxm_2_TG5XXwjFrFF5zK8PGx9RxIlSXYRInuMFB7GAmRLFhlOvl1kfzuRMgAOp2"
    recommendations = search_song_and_recommend_ex(search_term, client_access_token)
    return jsonify(recommendations)
