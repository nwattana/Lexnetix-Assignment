from django.urls import path

from lexscool import views

urlpatterns = [
	path("", views.redirect_docs, name="docs"),
]
