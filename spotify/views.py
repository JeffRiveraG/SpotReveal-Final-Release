# spotify/views.py

from django.shortcuts import render, redirect
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from .models import SpotifyUser
from .credentials import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

SPOTIPY_SCOPE = 'user-top-read playlist-modify-public playlist-read-private'

sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SPOTIPY_SCOPE)

def index(request):
    return render(request, 'spotify/index.html')

def login(request):
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def callback(request):
    code = request.GET.get('code', '')
    token_info = sp_oauth.get_access_token(code)

    if 'access_token' not in token_info:
        return redirect('login')

    access_token = token_info['access_token']
    sp = Spotify(auth=access_token)

    # Fetch user information
    user_info = sp.current_user()

    # Check if the user is already in the database
    user, created = SpotifyUser.objects.get_or_create(spotify_id=user_info['id'])

    # Update or create the SpotifyUser instance with the new access token
    user.access_token = access_token
    user.save()

    request.session['user_id'] = user.id  # Store the user ID in the session

    return redirect('top_combined')

def top_combined(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    try:
        user = SpotifyUser.objects.get(id=user_id)
    except SpotifyUser.DoesNotExist:
        return redirect('login')

    access_token = user.access_token
    sp = Spotify(auth=access_token)

    # Fetch top tracks
    top_tracks = sp.current_user_top_tracks(limit=5, time_range='short_term')

    # Fetch top artists
    top_artists = sp.current_user_top_artists(limit=5, time_range='short_term')

    # Extract track IDs from top tracks
    top_track_ids = [track['id'] for track in top_tracks['items']]

    # Get recommendations based on top tracks
    recommendations = sp.recommendations(seed_tracks=top_track_ids, limit=10)

    # Create a playlist
    playlist_name = "Recommended Playlist"
    playlist_description = "A playlist generated based on your top tracks"
    playlist = sp.user_playlist_create(user=sp.current_user()['id'], name=playlist_name, description=playlist_description)

    # Add recommended tracks to the playlist
    track_uris = [track['uri'] for track in recommendations['tracks']]
    sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)

    return render(request, 'spotify/top_combined.html', {'tracks': top_tracks['items'], 'artists': top_artists['items'], 'playlist_url': playlist['external_urls']['spotify'], 'recommendations': recommendations['tracks']})
