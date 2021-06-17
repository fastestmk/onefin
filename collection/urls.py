from django.urls import path
from .views import *

urlpatterns = [
    path('collection/', CreateGetCollection.as_view()),
    path('collection/<uuid>/', PutGetDeleteCollection.as_view()),
    path('collection/movies', AllMovies.as_view())
]
