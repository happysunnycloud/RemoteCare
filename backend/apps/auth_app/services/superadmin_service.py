from psycopg.rows import dict_row

from common.db import get_connection


def get_superadmin_by_login(
    login
):

    connection = get_connection()

    cursor = connection.cursor(
        row_factory=dict_row
    )

    cursor.execute(
        '''
        SELECT *
        FROM auth.get_superadmin_by_login(%s);
        ''',
        (
            login,
        )
    )

    row = cursor.fetchone()

    cursor.close()

    connection.close()

    return row

def get_superadmin(
    superadmin_id
):

    connection = get_connection()

    cursor = connection.cursor(
        row_factory=dict_row
    )

    cursor.execute(
        '''
        SELECT *
        FROM auth.get_superadmin(
            %s
        );
        ''',
        (
            superadmin_id,
        )
    )

    row = cursor.fetchone()

    cursor.close()

    connection.close()

    return row

def touch_superadmin(
    superadmin_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        '''
        SELECT auth.touch_superadmin(
            %s
        );
        ''',
        (
            superadmin_id,
        )
    )

    connection.commit()

    cursor.close()

    connection.close()