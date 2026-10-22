from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cart.models import Item, Order
from movies.models import Movie


class PopularityMapTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pw-12345!")
        self.a = Movie.objects.create(name="Avatar", price=10, description="x", image="movie_images/a.jpg")
        self.b = Movie.objects.create(name="Batman", price=10, description="x", image="movie_images/b.jpg")

    def buy(self, movie, qty, region):
        order = Order.objects.create(user=self.user, total=movie.price * qty, region=region)
        Item.objects.create(order=order, movie=movie, price=movie.price, quantity=qty)

    def test_login_required(self):
        response = self.client.get(reverse("movies.popularity_map"))
        self.assertEqual(response.status_code, 302)

    def test_region_shows_top_trending_movie(self):
        self.buy(self.a, 1, "southeast")
        self.buy(self.b, 3, "southeast")
        self.buy(self.a, 5, "west")
        self.client.force_login(self.user)
        response = self.client.get(reverse("movies.popularity_map") + "?region=southeast")
        top = response.context["template_data"]["selected"]["top"]
        self.assertEqual(top[0]["movie__name"], "Batman")
        self.assertEqual(top[0]["count"], 3)
        self.assertEqual(response.context["template_data"]["selected"]["total"], 4)

    def test_purchase_saves_region(self):
        self.client.force_login(self.user)
        session = self.client.session
        session["cart"] = {str(self.a.id): "2"}
        session.save()
        self.client.post(reverse("cart.purchase"), {"region": "midwest"})
        self.assertEqual(Order.objects.get().region, "midwest")

    def test_purchase_requires_region(self):
        self.client.force_login(self.user)
        session = self.client.session
        session["cart"] = {str(self.a.id): "1"}
        session.save()
        self.client.post(reverse("cart.purchase"), {})
        self.assertEqual(Order.objects.count(), 0)
