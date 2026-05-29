from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from apps.auth_app.services.assigner_service import create_assigner
from apps.auth_app.services.assigner_service import get_assigners
from apps.auth_app.services.assigner_service import get_assigner_by_login
from apps.auth_app.services.assigner_service import get_assigner_by_email

from common.password import hash_password

def alert_back(message):
    return HttpResponse(
        f'''
        <script>
            alert('{message}');
            window.history.back();
        </script>
        '''
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

def get_assigner_filters(
    request
):
    return {
        'assigner_id': get_query_param(
            request,
            'id'
        ),

        'first_name': get_query_param(
            request,
            'first_name'
        ),

        'middle_name': get_query_param(
            request,
            'middle_name'
        ),

        'last_name': get_query_param(
            request,
            'last_name'
        ),

        'login': get_query_param(
            request,
            'login'
        ),

        'email': get_query_param(
            request,
            'email'
        ),

        'is_active': get_query_param(
            request,
            'is_active'
        ) == 'true',
    }

def get_assigner_sorting(request):
    return {
        'sort_by': get_query_param(
            request,
            'sort_by',
            'id'
        ),

        'sort_order': get_query_param(
            request,
            'sort_order',
            'asc'
        ),
    }

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

def assigner_list(request):
    filters = get_assigner_filters(
        request
    )    

    if not request.GET:
        filters['is_active'] = True
    
    sorting = get_assigner_sorting(
        request
    )    
    
    rows = get_assigners(
        **filters,
        **sorting
    )
    
    html = f'''
    <h1>Assigners</h1>
    <form method="get">
    <a href="/assigners/create/">
        Create assigner
    </a>
    <br>
    <br>
    <table border="1" cellpadding="5">
        <tr>
        <th>
            <a href="{build_sort_link(filters, sorting, 'id')}">
                ID
            </a>
        </th>
        <th>
            <a href="{build_sort_link(filters, sorting, 'first_name')}">
                First Name
            </a>
        </th>
        <th>
            <a href="{build_sort_link(filters, sorting, 'middle_name')}">
                Middle Name
            </a>
        </th>
        <th>
            <a href="{build_sort_link(filters, sorting, 'last_name')}">
                Last Name
            </a>
        </th>
        <th>
            <a href="{build_sort_link(filters, sorting, 'login')}">
                Login
            </a>
        </th>
        <th>
            <a href="{build_sort_link(filters, sorting, 'email')}">
                Email
            </a>
        </th>
        <th>
            Active
        </th>
        </tr>
    '''
    
    html += f'''
    <tr>
        <td>
            <input
                type="text"
                name="id"
                value="{filters['assigner_id'] or ''}"
                style="width:70px;"
            >
        </td>
        <td>
            <input
                type="text"
                name="first_name"
                value="{filters['first_name'] or ''}"
            >
        </td>
        <td>
            <input
                type="text"
                name="middle_name"
                value="{filters['middle_name'] or ''}"
            >
        </td>
        <td>
            <input
                type="text"
                name="last_name"
                value="{filters['last_name'] or ''}"
            >
        </td>
        <td>
            <input
                type="text"
                name="login"
                value="{filters['login'] or ''}"
            >
        </td>
        <td>
            <input
                type="text"
                name="email"
                value="{filters['email'] or ''}"
            >
        </td>
        <td align="center">

            <input
                type="checkbox"
                name="is_active"
                value="true"
                {'checked' if filters['is_active'] else ''}
            >
        </td>
    </tr>
    '''    

    for row in rows:
        html += f'''
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
            <td>{row[4]}</td>
            <td>{row[5]}</td>
            <td>{row[6]}</td>
        </tr>
        '''

    html += '''
    </table>
    <br>

    <button type="submit">
        Search
    </button>

    </form>
    '''

    return HttpResponse(html)

@csrf_exempt
def assigner_create(request):
    if request.method == 'GET':
        html = '''
        <h1>Create assigner</h1>
        <form method="post">

            <div>
                First name
            </div>

            <input
                type="text"
                name="first_name"
            >
            <br>
            <br>
            <div>
                Middle name
            </div>

            <input
                type="text"
                name="middle_name"
            >            
            <br>
            <br>
            <div>
                Last name
            </div>

            <input
                type="text"
                name="last_name"
            >
            <br>
            <br>
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
                Email
            </div>

            <input
                type="email"
                name="email"
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
            <div>
                Confirm password
            </div>

            <input
                type="password"
                name="password_confirm"
            >
            <br>
            <br>
            <button type="submit">
                Save
            </button>
        </form>
        '''

        return HttpResponse(html)

    first_name = request.POST.get('first_name')
    middle_name = request.POST.get('middle_name')
    last_name = request.POST.get('last_name')
    login = request.POST.get('login')
    email = request.POST.get('email')    
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')    
    existing_assigner = get_assigner_by_login(login)    
    existing_email = get_assigner_by_email(email)

    required_fields = [
        (
            first_name,
            'First name'
        ),
        (
            last_name,
            'Last name'
        ),
        (
            login,
            'Login'
        ),
        (
            email,
            'Email'
        ),
        (
            password,
            'Password'
        ),
        (
            password_confirm,
            'Confirm password'
        ),
    ]

    for field_value, field_name in required_fields:
        if not field_value:
            return alert_back(
                f'{field_name} is required'
            )       
    
    if existing_assigner is not None:
        return alert_back(
            f'Login "{login}" already exists'
        )  

    if existing_email is not None:
        return alert_back(
            f'Email "{email}" already exists'
        )
        
    if password != password_confirm:
        return alert_back(
            'Passwords do not match'
        )      
              
    password_hash = hash_password(password)
    
    create_assigner(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        login=login,
        email=email,
        password_hash=password_hash
    )

    return redirect('/assigners/')