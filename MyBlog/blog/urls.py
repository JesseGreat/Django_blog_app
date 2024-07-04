from django.urls import path
from . import views

app_name = 'blog' #This is the name of the app the below urls are meant for, it allows one to organize urls by application and use the name when referring to them.
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
]