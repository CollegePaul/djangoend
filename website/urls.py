
from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name=""),

  path('register', views.register, name="register"),

  path('my-login', views.my_login, name="my-login" ),

  path('user-logout', views.user_logout, name="user-logout"),

  path('hotel', views.hotel, name="hotel"),

  path('education', views.education, name="education"),
  
  path('test', views.test, name="test"),

  path('dashboard', views.dashboard, name="dashboard"),

  path('zoo', views.zoo, name="zoo"),
]

