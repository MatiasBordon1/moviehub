# movies/models.py
from django.db import models
from django.contrib.auth.models import User

class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tmdb_id = models.IntegerField()
    title = models.CharField(max_length=200)
    overview = models.TextField()
    poster_url = models.URLField(blank=True, null=True)
    release_date = models.CharField(max_length=10, blank=True)
    genre_ids = models.CharField(max_length=200, blank=True)
    rating = models.FloatField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    favorite = models.ForeignKey("FavoriteMovie", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField("Comentario personal")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comentario sobre {self.favorite.title}"