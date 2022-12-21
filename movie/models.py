from django.db import models
from datetime import date
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.SlugField(max_length=180, unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=200)
    age = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='actors/')

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.SlugField(max_length=180, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    tagline = models.CharField(max_length=200, default="")
    description = models.TextField()
    poster = models.ImageField(upload_to='poster/')
    year = models.PositiveSmallIntegerField(default=2020)
    country = models.CharField(max_length=100)
    directors = models.ManyToManyField(Actor, related_name='film_director')
    actors = models.ManyToManyField(Actor, related_name='actors')
    genre = models.ManyToManyField(Genre)
    world_premiere = models.DateField(default=date.today)
    budjet = models.PositiveIntegerField(
        default=0, help_text='view in dollars')
    fees_in_usa = models.PositiveIntegerField(
        default=0, help_text='view in dollars')
    fees_in_world = models.PositiveIntegerField(
        default=0, help_text='view in dollars')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=180, unique=True)
    draft = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)


class MovieShots(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.value)


class Rating(models.Model):
    ip = models.CharField(max_length=200)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return str(self.star)


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=200)
    text = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True, related_name="children")
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return str(self.name)
