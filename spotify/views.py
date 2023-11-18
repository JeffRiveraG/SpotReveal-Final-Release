# spotify/views.py

from django.shortcuts import render, redirect
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = '4eb37ee19dd14e2796b4619a9470b0a0'
SPOTIPY_CLIENT_SECRET = 'ec957ceb84b54da9b3ccecde98ce59f4'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback'
SPOTIPY_SCOPE = 'user-top-read'

sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SPOTIPY_SCOPE)

def index(request):
    return render(request, 'spotify/index.html')

def login(request):
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def callback(request):
    token_info = sp_oauth.get_access_token(request.GET.get('code', ''))
    request.session['token_info'] = token_info
    return redirect('top_combined')

def top_combined(request):
    token_info = request.session.get('token_info', None)

    if not token_info:
        return redirect('login')

    access_token = token_info['access_token']
    sp = Spotify(auth=access_token)

    # Fetch top tracks
    top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')

    # Fetch top artists
    top_artists = sp.current_user_top_artists(limit=10, time_range='short_term')

    return render(request, 'spotify/top_combined.html', {'tracks': top_tracks['items'], 'artists': top_artists['items']})
