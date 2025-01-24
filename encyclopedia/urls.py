from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page_title>", views.shows_content, name="shows_content"),
    path("add/", views.add, name="add"),
    path("wiki/edit/<str:title>", views.edit, name="edit")
]
