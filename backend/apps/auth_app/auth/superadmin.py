from django.shortcuts import redirect

from apps.auth_app.services.superadmin_service import (
    get_superadmin,
)

from apps.auth_app.constants import (
     SESSION_SUPERADMIN_ID,
)

def get_current_superadmin(
    request
):

    superadmin_id = request.session.get(        
        SESSION_SUPERADMIN_ID        
    )

    if superadmin_id is None:

        return None

    superadmin = get_superadmin(
        superadmin_id
    )

    if superadmin is None:

        request.session.flush()

        return None

    if not superadmin[
        'is_active'
    ]:

        request.session.flush()

        return None

    return superadmin

def require_superadmin_authentication(
    request
):

    superadmin = get_current_superadmin(
        request
    )

    if superadmin is None:

        return redirect(
            '/superadmin/login/'
        )

    return None