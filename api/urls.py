from django.urls import path
from . import views

urlpatterns = [
    path('jump/<str:slug>', views.link_jump, name='jump'),
    path('get_slug/<str:slug>', views.get_redirect_link, name='get_link'),
    path('info/<uuid:tocken>', views.link_list, name='get_item'),
    path('update/<uuid:tocken>', views.update_link, name='update'),
    path('create/', views.create_link, name='create')
]
