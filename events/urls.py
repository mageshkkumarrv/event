from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("event/<int:event_id>/", views.event_details, name="event_details"),
    path("event/<int:event_id>/book/", views.book_event, name="book_event"),
    path("booking-history/", views.booking_history, name="booking_history"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]
