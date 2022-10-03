from django.urls import path

from . import views

urlpatterns = [
    path(r"", views.index, name="index"),
    path("message", views.send_message, name="message"),
]
