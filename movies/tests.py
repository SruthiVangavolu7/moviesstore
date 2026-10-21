from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Movie, Rating


class MovieRatingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ratinguser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            name='Rating Test Movie',
            price=10,
            description='Movie used to test ratings.',
            image='movie_images/test.jpg'
        )

    def test_logged_in_user_can_rate_movie(self):
        self.client.login(username='ratinguser', password='testpass123')

        response = self.client.post(
            reverse('movies.rate_movie', kwargs={'id': self.movie.id}),
            {'rating': '4'}
        )

        self.assertRedirects(
            response,
            reverse('movies.show', kwargs={'id': self.movie.id})
        )
        rating = Rating.objects.get(movie=self.movie, user=self.user)
        self.assertEqual(rating.value, 4)

    def test_rating_update_reuses_same_rating(self):
        Rating.objects.create(movie=self.movie, user=self.user, value=2)
        self.client.login(username='ratinguser', password='testpass123')

        self.client.post(
            reverse('movies.rate_movie', kwargs={'id': self.movie.id}),
            {'rating': '5'}
        )

        self.assertEqual(
            Rating.objects.filter(movie=self.movie, user=self.user).count(),
            1
        )
        self.assertEqual(
            Rating.objects.get(movie=self.movie, user=self.user).value,
            5
        )

    def test_movie_detail_shows_average_rating(self):
        Rating.objects.create(movie=self.movie, user=self.user, value=4)
        Rating.objects.create(movie=self.movie, user=self.other_user, value=2)

        response = self.client.get(
            reverse('movies.show', kwargs={'id': self.movie.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '3.0/5')
        self.assertContains(response, '(2 ratings)')

    def test_rating_requires_login(self):
        response = self.client.post(
            reverse('movies.rate_movie', kwargs={'id': self.movie.id}),
            {'rating': '5'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Rating.objects.exists())

    def test_invalid_rating_is_not_saved(self):
        self.client.login(username='ratinguser', password='testpass123')

        self.client.post(
            reverse('movies.rate_movie', kwargs={'id': self.movie.id}),
            {'rating': '6'}
        )

        self.assertFalse(Rating.objects.exists())
