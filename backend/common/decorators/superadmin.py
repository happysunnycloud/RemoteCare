from functools import wraps

from django.shortcuts import redirect

from apps.auth_app.services.superadmin_service import (
    get_superadmin
)

from apps.auth_app.constants import (
    SESSION_SUPERADMIN_ID
)


def superadmin_required(
    view_func
):

    @wraps(
        view_func
    )
    def wrapper(
        request,
        *args,
        **kwargs
    ):

        superadmin_id = request.session.get(
            SESSION_SUPERADMIN_ID
        )

        if superadmin_id is None:

            return redirect(
                '/superadmin/login/'
            )


        superadmin = get_superadmin(
            superadmin_id
        )


        if superadmin is None:

            request.session.flush()

            return redirect(
                '/superadmin/login/'
            )


        if not superadmin['is_active']:

            request.session.flush()

            return redirect(
                '/superadmin/login/'
            )


        request.superadmin = superadmin


        return view_func(
            request,
            *args,
            **kwargs
        )


    return wrapper