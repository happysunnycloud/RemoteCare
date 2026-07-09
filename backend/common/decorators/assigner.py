from functools import wraps

from django.shortcuts import redirect

from apps.auth_app.services.assigner_service import (
    get_assigner
)

from apps.auth_app.constants import (
    SESSION_ASSIGNER_ID
)


def assigner_required(
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

        assigner_id = request.session.get(
            SESSION_ASSIGNER_ID
        )

        if assigner_id is None:

            return redirect(
                '/login/'
            )

        assigner = get_assigner(
            assigner_id
        )

        if assigner is None:

            request.session.flush()

            return redirect(
                '/login/'
            )

        if not assigner['is_active']:

            request.session.flush()

            return redirect(
                '/login/'
            )

        request.assigner = assigner

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper