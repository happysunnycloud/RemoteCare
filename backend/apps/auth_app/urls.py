from django.urls import path

from apps.auth_app.views import assigner_create
from apps.auth_app.views import assigner_list
from apps.auth_app.views import assigner_edit
from apps.auth_app.views import assigner_login
from apps.auth_app.views import assigner_home
from apps.auth_app.views import (
    assigner_logout
)

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
    
    path(
        'assigners/edit/<int:assigner_id>/',
        assigner_edit
    ),    
    
    path(
        'login/',
        assigner_login,
        name='assigner_login'
    ),

    path(
        'assigner/',
        assigner_home
    ),

    path(
        'logout/',
        assigner_logout
    ),

]