from django.http import HttpResponse

def alert_back(message):
    return HttpResponse(
        f'''
        <script>
            alert('{message}');
            window.history.back();
        </script>
        '''
    )

def validate_required_fields(
    required_fields
):
    for field_value, field_name in required_fields:
        if not field_value:

            return(
                False,
                alert_back(
                    f'{field_name} is required'
                )
            )

    return (
        True,
        None
    )

def build_sort_link(
    filters,
    sorting,
    column_name
):
    next_sort_order = 'asc'

    if (
        sorting['sort_by'] == column_name
        and
        sorting['sort_order'] == 'asc'
    ):
        next_sort_order = 'desc'

    params = []

    for key, value in filters.items():
        if isinstance(
            value,
            bool
        ):
            if value:
                params.append(
                    f'{key}=true'
                )
            continue

        if value is not None:
            params.append(
                f'{key}={value}'
            )

    params.append(
        f'sort_by={column_name}'
    )

    params.append(
        f'sort_order={next_sort_order}'
    )

    query_string = '&'.join(
        params
    )

    return f'?{query_string}'

def build_page_link(
    filters,
    sorting,
    page_number
):

    params = []

    for key, value in filters.items():
        if isinstance(
            value,
            bool
        ):
            params.append(
                f'{key}={"true" if value else "false"}'
            )
            continue

        if value is not None:
            params.append(
                f'{key}={value}'
            )

    params.append(
        f'sort_by={sorting["sort_by"]}'
    )

    params.append(
        f'sort_order={sorting["sort_order"]}'
    )

    params.append(
        f'page={page_number}'
    )

    return '?' + '&'.join(
        params
    )    

def get_query_param(
    request,
    param_name,
    default_value=None
):
    value = request.GET.get(
        param_name
    )

    if value == '':
        return default_value

    if value is None:
        return default_value

    return value
