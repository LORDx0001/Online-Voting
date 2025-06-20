from django.urls import path
from .views import voter_create

urlpatterns = [
    path('voter-create/', voter_create, name='voter-create'),
]
