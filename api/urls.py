from django.urls import path
from . import views

urlpatterns = [
    path('info/<uuid:tocken>', views.link_list, name='get_item'),
    path('update/<uuid:tocken>', views.update_link, name='update'),
    path('create/', views.create_link, name='create')
]
