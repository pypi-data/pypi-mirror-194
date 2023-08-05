from psycopg2.extensions import cursor


def get_by_id(db: cursor, user_id: int):
    return db.execute('''
        SELECT * FROM usr WHERE usr_id=%(user_id)s
    ''', {'user_id': user_id})


def get_user_by_email(db: cursor, email: str):
    return db.execute('''
        SELECT * FROM usr WHERE usr_email=%(email)s
    ''', {'email': email})


def create_guest(db: cursor):
    return db.execute('''
        INSERT INTO usr
            (usr_first_name, usr_last_name, usr_email, usr_admin, 
            usr_password, usr_last_seen, usr_created, is_guest)
        VALUES
            ('GUEST', 'GUEST', '', '0', '', NOW(), NOW(), 't')
        RETURNING usr_id;
    ''', {})
