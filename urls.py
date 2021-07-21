from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework import routers

from . import views

app_name = 'it_training_repo'
router = routers.DefaultRouter()
router.register(r'opportunity', views.OpportunityViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('opportunity/agenda',views.agenda, name= 'agenda'),
    path('opportunity/upcoming',views.upcoming_opportunity, name= 'upcoming_opportunity'),
    path('opportunity/create', views.create_edit_display_opportunity, name='create_opportunity'),
    path('opportunity/edit/<int:id>', views.create_edit_display_opportunity, name='edit_opportunity'),
    path('opportunity/detail/<int:id>', views.create_edit_display_opportunity, name='display_opportunity'),
    path('opportunity/delete/<int:id>', views.delete_opportunity, name='delete_opportunity'),
    path('opportunity/list', views.list_opportunity, name='list_opportunity'),
    path('opportunity/add_rating_comment', views.add_rating_comment, name='add_rating_comment'),
    path('static_stars/<str:stars>', views.static_stars, name='static_stars'),
    url('^api/', include(router.urls)),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
