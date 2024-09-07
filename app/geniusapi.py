import os
import requests
import pandas as pd
from fuzzywuzzy import fuzz
from flask import Flask, request, jsonify, render_template

# Load client access token from environment variables
CLIENT_ACCESS_TOKEN = os.getenv('GENIUS_CLIENT_ACCESS_TOKEN')

# Function to get image HTML
def get_image_html(image_url):
    """Generate HTML for displaying images."""
    return f'<img src="{image_url}" width="100" height="100"/>'

# Function to search song and recommend
def search_song_and_recommend(search_term, client_access_token):
    """Search for a song and recommend similar songs based on their titles."""
    try:
        # Create the search URL
        genius_search_url = f"https://api.genius.com/search?q={search_term}&access_token={client_access_token}"
        
        # Perform the search request
        response = requests.get(genius_search_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        json_data = response.json()

        # Extract song information
        songs = []
        for song in json_data.get('response', {}).get('hits', []):
            result = song.get('result', {})
            title = result.get('full_title', 'Unknown Title')
            pageviews = result.get('stats', {}).get('pageviews', 'N/A')
            image_url = result.get('song_art_image_url', 'https://via.placeholder.com/100')
            # songs.append((title, pageviews, image_url))
            songs.append((title, pageviews))
        
        # Create a DataFrame
        # artist_df = pd.DataFrame(songs, columns=['song_title', 'page_views', 'album_cover_url'])
        artist_df = pd.DataFrame(songs, columns=['song_title', 'page_views'])
        # artist_df['album_cover'] = artist_df['album_cover_url'].apply(get_image_html)
        
        def find_similar_songs(df, title, threshold=80):
            """Find songs similar to the given title."""
            recommendations = []
            for _, row in df.iterrows():
                score = fuzz.ratio(title.lower(), row['song_title'].lower())
                if score >= threshold and row['song_title'].lower() != title.lower():
                    recommendations.append(row['song_title'])
            return recommendations
        
        # Initialize the recommendations list
        recommendations = []
        
        # Iterate over each song in the DataFrame to find similar songs
        for _, row in artist_df.iterrows():
            similar_songs = find_similar_songs(artist_df, row['song_title'])
            recommendations.append({
                'original_song': row['song_title'],
                'similar_songs': similar_songs
                # 'album_cover': row['album_cover']
            })
        
        # Print the recommendations to the console
        for recommendation in recommendations:
            print(f"Original Song: {recommendation['original_song']}")
            print(f"Similar Songs: {recommendation['similar_songs']}")
            # print(f"Album Cover: {recommendation['album_cover']}\n")
        
        return recommendations

    except requests.exceptions.RequestException as e:
        print(f"Error while accessing Genius API: {e}")
        return []

def get_image_html_ex(image_url):
    return f'<img src="{image_url}" width="100" height="100"/>'

# def search_song_and_recommend_ex(search_term, client_access_token):
#     genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"
#     response = requests.get(genius_search_url)
#     json_data = response.json()
    
#     songs = []
#     for song in json_data.get('response', {}).get('hits', []):
#         result = song.get('result', {})
#         title = result.get('full_title', 'Unknown Title')
#         pageviews = result.get('stats', {}).get('pageviews', 'N/A')
#         image_url = result.get('song_art_image_url', 'https://via.placeholder.com/100')
#         songs.append((title, pageviews, image_url))
    
#     artist_df = pd.DataFrame(songs, columns=['song_title', 'page_views', 'album_cover_url'])
#     artist_df['album_cover'] = artist_df['album_cover_url'].apply(get_image_html)

#     def find_similar_songs(df, title, threshold=80):
#         recommendations = []
#         for _, row in df.iterrows():
#             score = fuzz.ratio(title.lower(), row['song_title'].lower())
#             if score >= threshold:
#                 recommendations.append(row['song_title'])
#         return recommendations
    
#     recommendations = []
#     for _, row in artist_df.iterrows():
#         similar_songs = find_similar_songs(artist_df, row['song_title'])
#         recommendations.append({
#             'original_song': row['song_title'],
#             'similar_songs': similar_songs
#         })
    
#     return recommendations



def search_song_and_recommend_ex(search_term, client_access_token):
    genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"
    response = requests.get(genius_search_url)
    json_data = response.json()
    
    songs = []
    for song in json_data.get('response', {}).get('hits', []):
        result = song.get('result', {})
        title = result.get('full_title', 'Unknown Title')
        pageviews = result.get('stats', {}).get('pageviews', 'N/A')
        image_url = result.get('song_art_image_url', 'https://via.placeholder.com/100')
        songs.append((title, pageviews, image_url))
    
    artist_df = pd.DataFrame(songs, columns=['song_title', 'page_views', 'album_cover_url'])
    artist_df['album_cover'] = artist_df['album_cover_url'].apply(get_image_html)

    def find_similar_songs(df, title, threshold=80):
        recommendations = []
        for _, row in df.iterrows():
            score = fuzz.ratio(title.lower(), row['song_title'].lower())
            if score >= threshold:
                recommendations.append(row['song_title'])
        return recommendations
    
    recommendations = []
    for _, row in artist_df.iterrows():
        similar_songs = find_similar_songs(artist_df, row['song_title'])
        recommendations.append({
            'original_song': row['song_title'],
            'similar_songs': similar_songs,
            'album_cover': row['album_cover_url']  # Include album cover in response
        })
    
    return recommendations



