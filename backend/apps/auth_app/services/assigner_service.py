from common.db import get_connection

def get_assigners():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        '''
        SELECT *
        FROM auth.get_assigners();
        '''
    )

    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    return rows


def get_assigner(
    assigner_id
):
    connection = get_connection()
    cursor = connection.cursor()
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
    cursor = connection.cursor()
    cursor.execute(
        '''
        SELECT auth.create_assigner(
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        );
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

    assigner_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    return assigner_id
    
def get_assigner_by_login(
    login
):

    connection = get_connection()
    cursor = connection.cursor()
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
    cursor = connection.cursor()
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