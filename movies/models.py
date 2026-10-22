
# Create your models here.
from django.db import models

from django.contrib.auth.models import User
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ]

    id = models.AutoField(primary_key=True)
    value = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    date = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='movie_ratings'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['movie', 'user'],
                name='unique_movie_user_rating'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.movie.name}: {self.value}/5'

