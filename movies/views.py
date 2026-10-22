from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from .models import Movie, Review, Rating
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Count, Sum
from cart.models import Item
from cart.regions import REGIONS, REGIONS_BY_KEY


def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = get_object_or_404(Movie, id=id)
    reviews = Review.objects.filter(movie=movie)

    rating_stats = movie.ratings.aggregate(
        average=Avg('value'),
        count=Count('id')
    )

    user_rating = None
    if request.user.is_authenticated:
        user_rating = (
            Rating.objects
            .filter(movie=movie, user=request.user)
            .values_list('value', flat=True)
            .first()
        )

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['average_rating'] = rating_stats['average']
    template_data['rating_count'] = rating_stats['count']
    template_data['user_rating'] = user_rating

    return render(request, 'movies/show.html', {'template_data': template_data})


@login_required
def rate_movie(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == 'POST':
        try:
            value = int(request.POST.get('rating', ''))
        except (TypeError, ValueError):
            value = 0

        if 1 <= value <= 5:
            Rating.objects.update_or_create(
                movie=movie,
                user=request.user,
                defaults={'value': value}
            )

    return redirect('movies.show', id=id)


@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect('movies.show', id=id)

@staff_member_required
def admin_stats(request):
    most_purchased = (Movie.objects
        .annotate(times_bought=Sum('item__quantity'))
        .filter(times_bought__gt=0)
        .order_by('-times_bought')
        .first())
    most_reviewed = (Movie.objects
        .annotate(times_reviewed=Count('review'))
        .filter(times_reviewed__gt=0)
        .order_by('-times_reviewed')
        .first())
    context = dict(admin.site.each_context(request),
        title='Movie Stats',
        most_purchased=most_purchased,
        most_reviewed=most_reviewed)
    return render(request, 'admin/movie_stats.html', context)


@login_required
def popularity_map(request):
    """User story 1: trending (most purchased) movies in each region."""
    regions = []
    for region in REGIONS:
        top = list(
            Item.objects.filter(order__region=region["key"])
            .values("movie__id", "movie__name")
            .annotate(count=Sum("quantity"))
            .order_by("-count", "movie__name")[:5]
        )
        total = Item.objects.filter(order__region=region["key"]).aggregate(n=Sum("quantity"))["n"] or 0
        regions.append({**region, "top": top, "total": total})

    selected_key = request.GET.get("region", "")
    selected = next((r for r in regions if r["key"] == selected_key), None)

    my_items = (Item.objects.filter(order__user=request.user)
                .select_related("movie", "order")
                .order_by("-order__date")[:10])

    template_data = {
        "title": "Local Popularity Map",
        "regions": regions,
        "selected": selected,
        "my_items": my_items,
        "map_points": [
            {"key": r["key"], "name": r["name"], "lat": r["lat"], "lng": r["lng"],
             "total": r["total"], "top": r["top"][0]["movie__name"] if r["top"] else None}
            for r in regions
        ],
    }
    return render(request, "movies/popularity_map.html", {"template_data": template_data})