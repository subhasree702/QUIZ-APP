from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("home/", views.home_view, name="home"),  
    path("logout/", views.logout_view, name="logout"),
    path("quiz/<int:topic_id>/", views.quiz_view, name="quiz"),
    path("quiz/<int:topic_id>/next/", views.next_level_view, name="next_level"),
    path("quiz/<int:topic_id>/reset/", views.reset_level_view, name="reset_level"),
    path('retry_level/<int:topic_id>/', views.retry_level_view, name='retry_level'),
]

