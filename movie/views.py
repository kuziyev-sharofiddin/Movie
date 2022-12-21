from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from .serializers import *
from django.db import models
from rest_framework import generics, permissions
from .service import get_client_ip, MovieFilter
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class MovieListAPIView(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend,)
    serializer_class = MovieListSerializer
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(
                ratings__ip=get_client_ip(self.request)))).annotate(
                    middle_star=models.Sum(
                        models.F('ratings__star')) / models.Count(models.F("ratings"))
        )
        return movies


class MovieDetailAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateAPIView(generics.CreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer


class AddStarRatingAPIView(generics.CreateAPIView):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorListAPIView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailAPIView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
