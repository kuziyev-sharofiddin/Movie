from django.urls import path
from . import views
urlpatterns = [
    path('movie/', views.MovieListAPIView.as_view()),
    path('movie/<int:pk>', views.MovieDetailAPIView.as_view()),
    path('review/', views.ReviewCreateAPIView.as_view()),
    path('rating/', views.AddStarRatingAPIView.as_view()),
    path('actors/', views.ActorListAPIView.as_view()),
    path('actors/<int:pk>', views.ActorDetailAPIView.as_view()),
]
