from apps.auth_app.services.assigner_service import (
    get_assigner,
)

from apps.auth_app.constants import (
    SESSION_ASSIGNER_ID,
)

def get_current_assigner (
    request
):

    assigner_id = request.session.get(
        SESSION_ASSIGNER_ID
    )

    if assigner_id is None:

        return None

    assigner = get_assigner(
        assigner_id
    )

    if assigner is None:

        request.session.flush()

        return None

    if not assigner[
        'is_active'
    ]:

        request.session.flush()

        return None

    return assigner
