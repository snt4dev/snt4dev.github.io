from django.urls import path

from . import views

urlpatterns = [
    path('', views.RedirectToHome.as_view(), name="redirect_view"),
    path("home/", views.HomeView.as_view(), name="home_view"),
    path("submission/", views.SubmissionView.as_view(), name="submission_view"),
]