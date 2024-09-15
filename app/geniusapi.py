import os
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
from fuzzywuzzy import fuzz
from flask import Flask, request, jsonify, render_template
from lyricsgenius import Genius
import azapi

# Load client access token from environment variables
CLIENT_ACCESS_TOKEN = os.getenv('GENIUS_CLIENT_ACCESS_TOKEN')

def get_image_html(image_url):
    """Generate HTML for displaying images."""
    return f'<img src="{image_url}" width="100" height="100"/>'

def search_song_and_recommend_ex(search_term, client_access_token):
    genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"
    response = requests.get(genius_search_url)
    json_data = response.json()
    
    songs = []
    for song in json_data.get('response', {}).get('hits', []):
        result = song.get('result', {})
        full_title = result.get('full_title', 'Unknown Title')
        title = result.get('title', 'Unknown Title')
        artist = result.get('primary_artist', {}).get('name', 'Unknown Artist')
        pageviews = result.get('stats', {}).get('pageviews', 'N/A')
        image_url = result.get('song_art_image_url', 'https://via.placeholder.com/100')
        song_id = result.get('id')
        songs.append((song_id, full_title, title, artist, pageviews, image_url))
    
    artist_df = pd.DataFrame(songs, columns=['song_id', 'full_title', 'title', 'artist', 'page_views', 'album_cover_url'])
    artist_df['album_cover'] = artist_df['album_cover_url'].apply(get_image_html)

    def find_similar_songs(df, title, threshold=80):
        recommendations = []
        for _, row in df.iterrows():
            score = fuzz.ratio(title.lower(), row['title'].lower())
            if score >= threshold:
                recommendations.append(row['full_title'])
        return recommendations
    
    recommendations = []
    for _, row in artist_df.iterrows():
        similar_songs = find_similar_songs(artist_df, row['title'])
        recommendations.append({
            'song_id': row['song_id'],
            'full_title': row['full_title'],
            'title': row['title'],
            'artist': row['artist'],
            'similar_songs': similar_songs,
            'album_cover': row['album_cover_url']
        })
    
    return recommendations


# def fetch_lyrics(artist_name, song_title, client_access_token):
#     genius = Genius(client_access_token)
#     genius.remove_section_headers = True

#     try:
#         # Search for the song
#         search_results = genius.search_song(song_title, artist_name)
#         if search_results:
#             song = search_results
#             lyrics = song.lyrics
#             print(lyrics)
#             return lyrics    
#         else:
#             return "Lyrics not found."
#     except Exception as e:
#         return str(e)


# import requests

def fetch_lyrics(artist_name, song_title):
    # Initialize the AZlyrics API with 'google' as the search engine and set accuracy level
    api = azapi.AZlyrics('google', accuracy=0.5)
    
    # Set the artist and song title
    api.artist = artist_name
    api.title = song_title
    
    try:
        # Fetch lyrics using AZlyrics
        api.getLyrics(save=True, ext='lrc')
        lyrics = api.lyrics
        
        if lyrics:
            # Clean up the lyrics if necessary
            lyrics = '\n'.join(line.strip() for line in lyrics.split('\n') if line.strip())
            return lyrics
        else:
            return "Lyrics not found."
    except Exception as e:
        print(f"Error fetching lyrics: {str(e)}")
        return f"Error fetching lyrics: {str(e)}"