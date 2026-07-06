from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from apps.auth_app.auth import (
    get_current_superadmin,
)

from apps.auth_app.constants import (
    SUPERADMIN_ID,    
    SESSION_SUPERADMIN_ID ,
    SUPERADMIN_IS_ACTIVE,
    SUPERADMIN_PASSWORD_HASH,
)

from common.password import verify_password

from apps.auth_app.services.superadmin_service import (
    get_superadmin_by_login,
    touch_superadmin,
)

from .common import alert_back

def superadmin_login(
    request
):

    if get_current_superadmin(
        request
    ) is not None:

        return redirect(
            '/assigners/'
        )

    if request.method == 'GET':
        return HttpResponse(
            f'''
            <h1>SuperAdmin login</h1>

            <form method="post">

                <input
                    type="hidden"
                    name="csrfmiddlewaretoken"
                    value="{get_token(request)}"
                >

                <div>
                    Login
                </div>

                <input
                    type="text"
                    name="login"
                >

                <br>
                <br>

                <div>
                    Password
                </div>

                <input
                    type="password"
                    name="password"
                >

                <br>
                <br>

                <button type="submit">
                    Login
                </button>

            </form>
            '''
        )

    login = request.POST.get(
        'login'
    )

    password = request.POST.get(
        'password'
    )

    if not login:

        return alert_back(
            'Login is required'
        )

    if not password:

        return alert_back(
            'Password is required'
        )

    if len(login) > 100:

        return alert_back(
            'Login is too long'
        )

    if len(password) > 255:

        return alert_back(
            'Password is too long'
        )

    superadmin = get_superadmin_by_login(
        login
    )

    if superadmin is None:

        return alert_back(
            'Invalid login or password'
        )

    if not superadmin[
        SUPERADMIN_IS_ACTIVE
    ]:

        return alert_back(
            'User is inactive'
        )

    if not verify_password(
        password,
        superadmin[
            SUPERADMIN_PASSWORD_HASH
        ]
    ):

        return alert_back(
            'Invalid login or password'
        )

    touch_superadmin(
        superadmin[
            SUPERADMIN_ID
        ]
    )

    request.session.flush()

    request.session[
        SESSION_SUPERADMIN_ID
    ] = superadmin[
        SUPERADMIN_ID
    ]

    return HttpResponse(
        'Login successful'
    )

def superadmin_logout(
    request
):
    #debug спросить, что делает request.session.pop
    # request.session.pop(
    #     'superadmin_id',
    #     None
    # )
    #debug
    request.session.flush()

    return redirect(
        '/superadmin/login/'
    )

