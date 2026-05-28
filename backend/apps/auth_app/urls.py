from django.urls import path

from apps.auth_app.views import assigner_create
from apps.auth_app.views import assigner_list

urlpatterns = [
    path(
        'assigners/',
        assigner_list,
        name='assigner_list'
    ),

    path(
        'assigners/create/',
        assigner_create,
        name='assigner_create'
    ),
]