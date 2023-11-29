# spotify/models.py

from django.db import models

class SpotifyUser(models.Model):
    spotify_id = models.CharField(max_length=255, unique=True)
    access_token = models.CharField(max_length=255)

    def __str__(self):
        return self.spotify_id
