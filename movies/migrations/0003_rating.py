import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_review'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.PositiveSmallIntegerField(choices=[
                    (1, '1 star'),
                    (2, '2 stars'),
                    (3, '3 stars'),
                    (4, '4 stars'),
                    (5, '5 stars'),
                ])),
                ('date', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='ratings',
                    to='movies.movie',
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='movie_ratings',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.UniqueConstraint(
                fields=('movie', 'user'),
                name='unique_movie_user_rating',
            ),
        ),
    ]
