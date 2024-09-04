from flask import Flask, request, jsonify, render_template
import requests
import pandas as pd
from fuzzywuzzy import fuzz



# Function to get image HTML
def get_image_html(image_url):
    """Generate HTML for displaying images."""
    return f'<img src="{image_url}" width="100" height="100"/>'

# Function to search song and recommend
def search_song_and_recommend(search_term, client_access_token):
    """Search for a song and recommend similar songs based on their titles."""
    # Create the search URL
    genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"
    
    # Perform the search request
    response = requests.get(genius_search_url)
    json_data = response.json()
    
    # Extract song information
    songs = []
    for song in json_data.get('response', {}).get('hits', []):
        result = song.get('result', {})
        title = result.get('full_title', 'Unknown Title')
        pageviews = result.get('stats', {}).get('pageviews', 'N/A')
        image_url = result.get('song_art_image_url', 'https://via.placeholder.com/100')
        songs.append((title, pageviews, image_url))
    
    # Create a DataFrame
    artist_df = pd.DataFrame(songs, columns=['song_title', 'page_views', 'album_cover_url'])
    artist_df['album_cover'] = artist_df['album_cover_url'].apply(get_image_html)
    
    def find_similar_songs(df, title, threshold=80):
        """Find songs similar to the given title."""
        recommendations = []
        for _, row in df.iterrows():
            score = fuzz.ratio(title.lower(), row['song_title'].lower())
            if score >= threshold:
                recommendations.append(row['song_title'])
        return recommendations
    
    # Find and recommend similar songs
    recommendations = []
    for _, row in artist_df.iterrows():
        similar_songs = find_similar_songs(artist_df, row['song_title'])
        recommendations.append({
            'original_song': row['song_title'],
            'similar_songs': similar_songs
        })
    
    return recommendations






