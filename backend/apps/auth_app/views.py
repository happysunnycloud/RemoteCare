from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from common.password import hash_password
from common.password import verify_password

from apps.auth_app.services.assigner_service import create_assigner
from apps.auth_app.services.assigner_service import get_assigners
from apps.auth_app.services.assigner_service import get_assigner
from apps.auth_app.services.assigner_service import get_assigner_by_login
from apps.auth_app.services.assigner_service import get_assigner_by_email
from apps.auth_app.services.assigner_service import update_assigner

from apps.auth_app.services.superadmin_service import (
    get_superadmin_by_login,
    get_superadmin,
    touch_superadmin
)

PAGE_SIZE = 20
PASSWORD_PLACEHOLDER = '********'

ASSIGNER_ID = 'id'
ASSIGNER_FIRST_NAME = 'first_name'
ASSIGNER_MIDDLE_NAME = 'middle_name'
ASSIGNER_LAST_NAME = 'last_name'
ASSIGNER_LOGIN = 'login'
ASSIGNER_EMAIL = 'email'
ASSIGNER_PASSWORD_HASH = 'password_hash'
ASSIGNER_IS_ACTIVE = 'is_active'
ASSIGNER_CREATED_AT = 'created_at'
ASSIGNER_UPDATED_AT = 'updated_at'

def alert_back(message):
    return HttpResponse(
        f'''
        <script>
            alert('{message}');
            window.history.back();
        </script>
        '''
    )

def assigner_logout(
    request
):

    request.session.pop(
        'assigner_id',
        None
    )

    return redirect(
        '/login/'
    )

def get_current_assigner_id(
    request
):

    return request.session.get(
        'assigner_id'
    )

def require_assigner_authentication(
    request
):

    assigner_id = (
        get_current_assigner_id(
            request
        )
    )

    if assigner_id is None:

        return redirect(
            '/login/'
        )

    return None

def get_current_superadmin(
    request
):

    superadmin_id = request.session.get(
        'superadmin_id'
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

def validate_assigner_uniqueness(        
        login, 
        email,
        id=None
):

    existing_assigner = get_assigner_by_login(login)  
    existing_email = get_assigner_by_email(email)   

    assigner_id = None
    if existing_assigner is not None:
        assigner_id = existing_assigner['id']
        if (
            id is None 
            or
            id != assigner_id 
        ):
            return (
                False,     
                alert_back(            
                    f'Login "{login}" already exists'
                )
            )

    assigner_id = None
    if existing_email is not None:
        assigner_id = existing_email['id']
        if (
            id is None 
            or
            id != assigner_id 
        ):
            return (
                False,     
                alert_back(            
                    f'Email "{email}" already exists'
                )
            )

    return (
        True,
        None
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

def get_assigner_paging(
    request
):

    page_number = get_query_param(
        request,
        'page',
        '1'
    )

    return {

        'page_number': int(
            page_number
        ),

        'page_size': PAGE_SIZE,
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

def assigner_list(request):
    filters = get_assigner_filters(
        request
    )    

    response = require_superadmin_authentication(
        request
    )

    if response is not None:

        return response

    if not request.GET:
        filters['is_active'] = True
    
    sorting = get_assigner_sorting(
        request
    )    

    paging = get_assigner_paging(
        request
    )
    
    rows = get_assigners(
        **filters,
        **sorting,
        **paging        
    )
    
    total_count = 0
    if rows:
        total_count = rows[0].get('total_count', 0)

    page_number = paging['page_number']
    page_size = paging['page_size']
        
    total_pages = (
        total_count
        +
        page_size
        -
        1
    ) // page_size
    
    if total_pages == 0:
        total_pages = 1

    if page_number < 1:
        page_number = 1

    if page_number > total_pages:
        page_number = total_pages

    paging['page_number'] = page_number    
    
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
            <td>{row[ASSIGNER_ID]}</td>
            <td>{row[ASSIGNER_FIRST_NAME]}</td>
            <td>{row[ASSIGNER_MIDDLE_NAME]}</td>
            <td>{row[ASSIGNER_LAST_NAME]}</td>
            <td>
                <a href="/assigners/edit/{row[ASSIGNER_ID]}/">
                    {row[ASSIGNER_LOGIN]}
                </a>
            </td>
            <td>{row[ASSIGNER_EMAIL]}</td>
            <td>{row[ASSIGNER_IS_ACTIVE]}</td>
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

    html += '<br><br>'
    if page_number > 1:
        html += f'''
        <a href="{build_page_link(
            filters,
            sorting,
            page_number - 1
        )}">
            Previous
        </a>
        '''

    html += f'''
    &nbsp;&nbsp;
    Page {page_number} of {total_pages}
    &nbsp;&nbsp;
    '''

    if page_number < total_pages:
        html += f'''
        <a href="{build_page_link(
            filters,
            sorting,
            page_number + 1
        )}">
            Next
        </a>
        '''

    return HttpResponse(html)

@csrf_exempt
def assigner_create(request):

    response = require_superadmin_authentication(
        request
    )

    if response is not None:

        return response

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

    is_valid, response = validate_required_fields(
        required_fields
    ) 
    
    if not is_valid:
        return response   
        
    is_valid, response = validate_assigner_uniqueness(
        login,
        email
    )   
    
    if not is_valid:
        return response      
 
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

@csrf_exempt
def assigner_edit(
    request,
    assigner_id
):
  
    response = require_superadmin_authentication(
        request
    )

    if response is not None:

        return response

    assigner = get_assigner(
        assigner_id
    )

    if assigner is None:

        return HttpResponse(
            'Assigner not found'
        )
        
    if request.method == 'POST':
        is_active = (
            request.POST.get(
                'is_active'
            ) == 'true'
        )

        first_name = request.POST.get(
            'first_name'
        )
        
        middle_name = request.POST.get(
           'middle_name'
        )

        last_name = request.POST.get(
            'last_name'
        )

        login = request.POST.get(
            'login'
        )

        email = request.POST.get(
            'email'
        )

        password = request.POST.get(
            'password'
        )

        password_confirm = request.POST.get(
            'password_confirm'
        )
        
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
        ]

        is_valid, response = validate_required_fields(
            required_fields
        )

        if not is_valid:
            return response

        is_valid, response = validate_assigner_uniqueness(
            login,
            email,
            assigner_id
        )

        if not is_valid:
            return response
            
        if (
            password != PASSWORD_PLACEHOLDER
            or
            password_confirm != PASSWORD_PLACEHOLDER
        ):

            if not password:

                return alert_back(
                    'Password is required'
                )

            if not password_confirm:

                return alert_back(
                    'Confirm password is required'
                )

            if password != password_confirm:

                return alert_back(
                    'Passwords do not match'
                )
                        
        password_hash = None

        if (
            password != PASSWORD_PLACEHOLDER
            and
            password_confirm != PASSWORD_PLACEHOLDER
        ):
            password_hash = hash_password(
                password
            )            

        update_assigner(
            assigner_id=assigner_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            login=login,
            email=email,
            is_active=is_active, 
            password_hash=password_hash
        )

        return redirect(
            '/assigners/'
        )            
        
    html = f'''
    <h1>Edit assigner</h1>
    <form method="post">
        <div>
            Active
        </div>
        <input
            type="checkbox"
            name="is_active"
            value="true"
            {'checked' if assigner[ASSIGNER_IS_ACTIVE] else ''}
        >                  
        <br>
        <br>        
        <div>
            First name
        </div>
        <input
            type="text"
            name="first_name"
            value="{assigner[ASSIGNER_FIRST_NAME]}"
        >
        <br>
        <br>
        <div>
            Middle name
        </div>
        <input
            type="text"
            name="middle_name"
            value="{assigner[ASSIGNER_MIDDLE_NAME] or ''}"
        >
        <br>
        <br>
        <div>
            Last name
        </div>
        <input
            type="text"
            name="last_name"
            value="{assigner[ASSIGNER_LAST_NAME]}"
        >
        <br>
        <br>
        <div>
            Login
        </div>
        <input
            type="text"
            name="login"
            value="{assigner[ASSIGNER_LOGIN]}"
        >
        <br>
        <br>
        <div>
            Email
        </div>
        <input
            type="text"
            name="email"
            value="{assigner[ASSIGNER_EMAIL]}"
        >               
        <br>
        <br>
        <div>
            Password
        </div>
        <input
            type="password"
            name="password"
            value="{PASSWORD_PLACEHOLDER}"
        >              
        <br>
        <br>
        <div>
            Confirm password
        </div>
        <input
            type="password"
            name="password_confirm"
            value="{PASSWORD_PLACEHOLDER}"
        >  
        <br>
        <br>
        <br>
        <br>           
        <button type="submit">
            Save
        </button>
    </form>
    '''

    return HttpResponse(
        html
    )

@csrf_exempt
def assigner_login(
    request
):

    if request.method == 'GET':

        return HttpResponse(
            '''
            <h1>Assigner login</h1>

            <form method="post">

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

    assigner = get_assigner_by_login(
        login
    )    

    if assigner is None:

        return alert_back(
            'Invalid login or password'
        )
        
    if not assigner[ASSIGNER_IS_ACTIVE]:
        return alert_back(
            'User is inactive'
        )
    
    if not verify_password(
        password,
        assigner[ASSIGNER_PASSWORD_HASH]
    ):

        return alert_back(
            'Invalid login or password'
        )

    request.session[
        'assigner_id'
    ] = assigner[
        ASSIGNER_ID
    ]

    return redirect(
        '/assigner/'
    )

def assigner_home(
    request
):

    response = (
        require_assigner_authentication(
            request
        )
    )

    if response is not None:

        return response

    return HttpResponse(
        '''
        <h1>
            Assigner home
        </h1>

        <a href="/logout/">
            Logout
        </a>
        '''
    )

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
        'is_active'
    ]:

        return alert_back(
            'User is inactive'
        )

    if not verify_password(
        password,
        superadmin[
            'password_hash'
        ]
    ):

        return alert_back(
            'Invalid login or password'
        )

    touch_superadmin(
        superadmin[
            'id'
        ]
    )

    request.session.flush()

    request.session[
        'superadmin_id'
    ] = superadmin[
        'id'
    ]

    return HttpResponse(
        'Login successful'
    )

def superadmin_logout(
    request
):

    request.session.pop(
        'superadmin_id',
        None
    )

    request.session.flush()

    return redirect(
        '/superadmin/login/'
    )