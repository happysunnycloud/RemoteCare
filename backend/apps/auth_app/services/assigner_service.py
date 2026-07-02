from psycopg.rows import dict_row
from common.db import get_connection

def get_assigners(
    assigner_id=None,
    first_name=None,
    middle_name=None,
    last_name=None,
    login=None,
    email=None,
    is_active=True,
    sort_by='id',
    sort_order='asc',
    page_number=1,
    page_size=20
):
    connection = get_connection()
    cursor = connection.cursor(
        row_factory=dict_row
    )
    cursor.execute(
        '''
        SELECT *
        FROM auth.get_assigners(
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        );
        ''',
        (
            assigner_id,
            first_name,
            middle_name,
            last_name,
            login,
            email,
            is_active,
            sort_by,
            sort_order,
            page_number,
            page_size,
        )
    )

    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    return rows


def get_assigner(
    assigner_id
):
    connection = get_connection()
    cursor = connection.cursor(
        row_factory=dict_row
    )
    cursor.execute(
        '''
        SELECT *
        FROM auth.get_assigner(%s);
        ''',
        (
            assigner_id,
        )
    )
	
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    return row


def create_assigner(
    first_name,
    middle_name,
    last_name,
    login,
    email,
    password_hash
):

    connection = get_connection()
    cursor = connection.cursor(
        row_factory=dict_row
    )
    cursor.execute(
        '''
        SELECT auth.create_assigner(
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        ) as assigner_id;
        ''',
        (
            first_name,
            middle_name,
            last_name,
            login,
            email,
            password_hash,
        )
    )

    row = cursor.fetchone()
    assigner_id = row['assigner_id']
    
    connection.commit()
    cursor.close()
    connection.close()

    return assigner_id
    
def get_assigner_by_login(
    login
):

    connection = get_connection()
    cursor = connection.cursor(
        row_factory=dict_row
    )
    cursor.execute(
        '''
        SELECT
            id,
            first_name,
            last_name,
            login,
            password_hash,
            is_active
        FROM auth.assigner
        WHERE login = %s;
        ''',
        (
            login,
        )
    )

    row = cursor.fetchone()
    cursor.close()
    connection.close()

    return row
    
def get_assigner_by_email(
    email
):

    connection = get_connection()
    cursor = connection.cursor(
        row_factory=dict_row
    )
    cursor.execute(
        '''
        SELECT
            id
        FROM auth.assigner
        WHERE email = %s;
        ''',
        (
            email,
        )
    )

    row = cursor.fetchone()
    cursor.close()
    connection.close()

    return row 

def update_assigner(
    assigner_id,
    first_name,
    middle_name,
    last_name,
    login,
    email,
    is_active,
    password_hash=None
):

    connection = get_connection()
    cursor = connection.cursor(
        row_factory=dict_row
    )
    cursor.execute(
        '''
        SELECT auth.update_assigner(
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        );
        ''',
        (
            assigner_id,
            first_name,
            middle_name,
            last_name,
            login,
            email,
            is_active,
            password_hash
        )
    )

    connection.commit()
    cursor.close()
    connection.close()

def touch_assigner(
    assigner_id
):

    connection = get_connection()

    cursor = connection.cursor(
        row_factory=dict_row
    )

    cursor.execute(
        '''
        SELECT auth.touch_assigner(
            %s
        );
        ''',
        (
            assigner_id,
        )
    )

    connection.commit()

    cursor.close()

    connection.close()    