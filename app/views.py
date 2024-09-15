import requests
from flask import Blueprint, render_template, jsonify, request, session
from .geniusapi import search_song_and_recommend_ex,fetch_lyrics
import os
import traceback
from bs4 import BeautifulSoup
import re


# Create a Blueprint
main = Blueprint('main', __name__)
main.secret_key = os.getenv('SECRET_KEY')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/recommend-songs', methods=['POST'])
def recommend_songs():
    CLIENT_ACCESS_TOKEN = os.getenv('GENIUS_CLIENT_ACCESS_TOKEN')
    data = request.json
    search_term = data.get('search_term')
    recommendations = search_song_and_recommend_ex(search_term, CLIENT_ACCESS_TOKEN)
    return jsonify(recommendations)


@main.route('/api/fetch-lyrics', methods=['POST'])
def fetch_lyrics_route():
    data = request.json
    print(f"Received data: {data}")

    song_title = data.get('song_title')
    artist_name = data.get('artist_name')
    lyrics = fetch_lyrics(artist_name, song_title)
    session['lyrics'] = lyrics
    return jsonify({"lyrics": lyrics})



@main.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Test route is working"}), 200

print("Views module loaded and routes registered.")
# Error handlers
@main.app_errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404



