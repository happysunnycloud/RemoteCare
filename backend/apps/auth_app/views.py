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

def assigner_list(request):
    rows = get_assigners()
    html = '''
    <h1>Assigners</h1>
    <a href="/assigners/create/">
        Create assigner
    </a>
    <br>
    <br>
    <table border="1" cellpadding="5">
        <tr>
            <th>ID</th>
            <th>First Name</th>
            <th>Middle Name</th>
            <th>Last Name</th>
            <th>Login</th>
            <th>Email</th>
            <th>Active</th>
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

    html += '</table>'

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