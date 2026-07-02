from django.urls import path

from apps.auth_app.views import (
    assigner_create,
    assigner_list,
    assigner_edit,
    assigner_login,
    assigner_home,
    assigner_logout,
    superadmin_login,
    superadmin_logout
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

    path(
        'superadmin/login/',
        superadmin_login
    ),    

    path(
        'superadmin/logout/',
        superadmin_logout
    ),

]