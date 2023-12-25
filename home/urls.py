from django.urls import path 
from home.views import home_view,match_users,match_view

urlpatterns = [
    path('',home_view,name='home_view'),
    path('matchusers',match_users,name='match_users'),
    path('matchview',match_view,name='match_view'),
]
