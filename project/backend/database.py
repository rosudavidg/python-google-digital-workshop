import psycopg2
from get_docker_secret import get_docker_secret
from exceptions import ServerException
import os
from utils import hash_password


def create_connection():
    connection = psycopg2.connect(user=get_docker_secret(os.environ['DATABASE_USER']),
                                  password=get_docker_secret(
                                      os.environ['DATABASE_PASSWORD']),
                                  host="database",
                                  port="5432",
                                  database=get_docker_secret(os.environ['DATABASE_DB']))
    return connection


def close_connection(connection):
    connection.close()


def get_user_by_email(email):
    connection = create_connection()
    cursor = connection.cursor()

    sql = 'SELECT u.id, u.first_name, u.last_name, u.email, u.phone, u.pass, r.role_name, u.company_id, u.activated FROM users u JOIN user_roles r ON u.user_role_id = r.id WHERE email = %s'
    val = (email,)

    try:
        cursor.execute(sql, val)
        data = cursor.fetchone()

        if data is None:
            return None

        return {
            "id": data[0],
            "first_name": data[1],
            "last_name": data[2],
            "email": data[3],
            "phone": data[4],
            "password": data[5],
            "role_name": data[6],
            "company_id": data[7],
            "activated": data[8]
        }
    except:
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def get_user_id_by_token(token):
    connection = create_connection()
    cursor = connection.cursor()

    sql = "SELECT user_id FROM activation_tokens WHERE token = %s"
    val = (token,)

    try:
        cursor.execute(sql, val)

        return cursor.fetchone()[0]

    except:
        connection.rollback()
        raise ServerException('Invalid token', 400)
    finally:
        cursor.close()
        close_connection(connection)


def activate_account(token):
    connection = create_connection()
    cursor = connection.cursor()

    # Get linked user_id
    user_id = get_user_id_by_token(token)

    try:
        # Delete activation token
        sql_activation_tokens = "DELETE FROM activation_tokens WHERE user_id = %s"
        val_activation_tokens = (user_id,)

        cursor.execute(sql_activation_tokens, val_activation_tokens)

        # Update user
        sql_users = "UPDATE users SET activated = True WHERE id = %s"
        val_users = (user_id,)

        cursor.execute(sql_users, val_users)

        connection.commit()

    except:
        connection.rollback()
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def approve_company(company_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Approve company
        sql_approve_company = "UPDATE companies SET approved = TRUE WHERE id = %s RETURNING id"
        val_approve_company = (company_id,)

        cursor.execute(sql_approve_company, val_approve_company)
        updated = len(cursor.fetchall()) != 0

        connection.commit()

    except:
        connection.rollback()
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)

    if not updated:
        raise ServerException(f'Approving company {company_id} failed', 400)


def create_company(company_name, first_name, last_name, email, phone, password, activation_token):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Create company
        sql_create_company = 'INSERT INTO companies (company_name) VALUES (%s) RETURNING id'
        val_create_company = (company_name,)

        cursor.execute(sql_create_company, val_create_company)
        company_id = cursor.fetchone()[0]

        # Get company user role
        sql_select_user_role = 'SELECT id FROM user_roles WHERE role_name = %s'
        val_select_user_role = ('company',)

        cursor.execute(sql_select_user_role, val_select_user_role)
        user_role_id = cursor.fetchone()[0]

        # Create user
        sql_create_user = 'INSERT INTO users (first_name, last_name, email, phone, pass, user_role_id, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id'
        val_create_user = (first_name, last_name, email,
                           phone, hash_password(password), user_role_id, company_id)

        cursor.execute(sql_create_user, val_create_user)
        user_id = cursor.fetchone()[0]

        # Insert activation token
        sql_insert_activation_token = "INSERT INTO activation_tokens (user_id, token) VALUES (%s, %s)"
        val_insert_activation_token = (user_id, activation_token)

        cursor.execute(sql_insert_activation_token,
                       val_insert_activation_token)

        connection.commit()

        # Return data
        return {
            'company_id': company_id,
            'user_id': user_id,
            'company_name': company_name,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone
        }

    except:
        connection.rollback()
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def company_approved(company_id):
    connection = create_connection()
    cursor = connection.cursor()

    sql = "SELECT approved FROM companies WHERE id = %s"
    val = (company_id,)

    try:
        cursor.execute(sql, val)

        return cursor.fetchone()[0]

    except:
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def company_has_parking_lots(company_id):
    connection = create_connection()
    cursor = connection.cursor()

    sql = "SELECT COUNT(*) FROM parking_lots WHERE company_id = %s"
    val = (company_id,)

    try:
        cursor.execute(sql, val)

        return cursor.fetchone()[0] != 0

    except:
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def insert_parking_lots(company_id, parking_lots_count, begin_with):
    connection = create_connection()
    cursor = connection.cursor()

    sql = "INSERT INTO parking_lots (company_id, internal_id) VALUES (%s, %s)"

    try:
        for internal_id in range(begin_with, begin_with + parking_lots_count):
            cursor.execute(sql, (company_id, internal_id))

        connection.commit()

    except:
        connection.rollback()
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def create_employee_user(company_id, first_name, last_name, email, phone, password, activation_token):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Get employee user role
        sql_select_user_role = 'SELECT id FROM user_roles WHERE role_name = %s'
        val_select_user_role = ('employee',)

        cursor.execute(sql_select_user_role, val_select_user_role)
        user_role_id = cursor.fetchone()[0]

        # Create user
        sql_create_user = 'INSERT INTO users (first_name, last_name, email, phone, pass, user_role_id, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id'
        val_create_user = (first_name, last_name, email,
                           phone, hash_password(password), user_role_id, company_id)

        cursor.execute(sql_create_user, val_create_user)
        user_id = cursor.fetchone()[0]

        # Insert activation token
        sql_insert_activation_token = "INSERT INTO activation_tokens (user_id, token) VALUES (%s, %s)"
        val_insert_activation_token = (user_id, activation_token)

        cursor.execute(sql_insert_activation_token,
                       val_insert_activation_token)

        connection.commit()

        # Return data
        return {
            'company_id': company_id,
            'user_id': user_id,
            'company_id': company_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone
        }

    except:
        connection.rollback()
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def get_accounts(company_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Get employee user role
        sql_select_user_role = 'SELECT id FROM user_roles WHERE role_name = %s'
        val_select_user_role = ('employee',)

        cursor.execute(sql_select_user_role, val_select_user_role)
        user_role_id = cursor.fetchone()[0]

        # Get all employees
        sql = "SELECT id, first_name, last_name, email, phone FROM users WHERE company_id = %s AND user_role_id = %s"
        val = (company_id, user_role_id)

        cursor.execute(sql, val)

        data = []

        for employee in cursor.fetchall():
            data.append({
                'id': employee[0],
                'first_name': employee[1],
                'last_name': employee[2],
                'email': employee[3],
                'phone': employee[4]
            })
        return data

    except:
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def book_parking_lot(user_id, company_id, date):
    connection = create_connection()
    cursor = connection.cursor()

    sql = "SELECT id FROM parking_lots WHERE company_id = %s"
    val = (company_id,)

    sql_2 = "SELECT p.id FROM parking_lots p JOIN schedules s ON s.parking_lot_id = p.id WHERE p.company_id = %s AND s.sch_date = %s"
    val_2 = (company_id, date)

    try:
        cursor.execute(sql, val)
        all_parking_lot_ids = [e[0] for e in cursor.fetchall()]

        cursor.execute(sql_2, val_2)
        not_available_parking_lot_ids = [e[0] for e in cursor.fetchall()]

        available_parking_lot_ids = [
            e for e in all_parking_lot_ids if e not in not_available_parking_lot_ids]

        if len(available_parking_lot_ids) == 0:
            return None

        parking_lot_id = available_parking_lot_ids[0]

        # Create schedule
        sql = 'INSERT INTO schedules (user_id, parking_lot_id, sch_date) VALUES (%s, %s, %s) RETURNING id'
        val = (user_id, parking_lot_id, date)
        cursor.execute(sql, val)

        connection.commit()

        return {
            'schedule': {
                'date': date,
                'parking_lot_id': parking_lot_id,
                'schedule_id': cursor.fetchone()[0]
            }
        }

    except:
        connection.rollback()
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def has_parking_lot_booked(user_id, company_id, date):
    connection = create_connection()
    cursor = connection.cursor()

    sql = "SELECT COUNT(*) FROM schedules WHERE user_id = %s AND sch_date = %s"
    val = (user_id, date)

    try:
        cursor.execute(sql, val)

        return cursor.fetchone()[0] != 0

    except:
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def get_parking_lot_books(user_id, company_id, date):
    connection = create_connection()
    cursor = connection.cursor()

    sql = "SELECT s.id, s.sch_date, p.internal_id, p.blocked, p.id FROM schedules s JOIN parking_lots p ON s.parking_lot_id = p.id WHERE p.company_id = %s AND s.user_id = %s AND s.sch_date >= %s"
    val = (company_id, user_id, date)

    try:
        cursor.execute(sql, val)

        schedules = cursor.fetchall()

        schedules = list(
            map(lambda sch: {'id': sch[0], 'date': str(sch[1]), 'internal_id': sch[2], 'blocked': sch[3], 'parking_lot_id': sch[4]}, schedules))

        today_schedules = list(
            filter(lambda sch: sch['date'] == date, schedules))
        rest_schedules = list(filter(
            lambda sch: sch not in today_schedules, schedules))

        return {
            'today_schedules': today_schedules,
            'future_schedules': rest_schedules
        }

    except:
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def get_companies():
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Get all companies
        sql = "SELECT id, company_name, approved FROM companies"

        cursor.execute(sql)
        data = []

        for company in cursor.fetchall():
            data.append({
                'id': company[0],
                'company_name': company[1],
                'approved': company[2]
            })

        return data

    except:
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def get_company(company_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Get all companies
        sql = "SELECT id, internal_id, blocked FROM parking_lots WHERE company_id = %s ORDER BY blocked DESC, internal_id"
        val = (company_id,)

        cursor.execute(sql, val)

        parking_lots = []

        for parking_lot in cursor.fetchall():
            parking_lots.append({
                'id': parking_lot[0],
                'internal_id': parking_lot[1],
                'blocked': parking_lot[2]
            })

        accounts = get_accounts(company_id)

        return {'has_parking_lots': len(parking_lots) != 0, 'parking_lots': parking_lots, 'accounts': accounts}

    except:
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def delete_parking_lot(company_id, id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Get all companies
        sql = "DELETE FROM parking_lots WHERE id = %s AND company_id = %s"
        val = (id, company_id)

        cursor.execute(sql, val)

        connection.commit()

    except:
        connection.rollback()
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def delete_parking_lot_books(user_id, id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Get all companies
        sql = "DELETE FROM schedules WHERE id = %s AND user_id = %s"
        val = (id, user_id)

        cursor.execute(sql, val)

        connection.commit()

    except:
        connection.rollback()
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def delete_parking_lots(company_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Get all companies
        sql = "DELETE FROM parking_lots WHERE company_id = %s"
        val = (company_id,)

        cursor.execute(sql, val)

        connection.commit()

    except:
        connection.rollback()
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def delete_employee(company_id, id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Get all companies
        sql = "DELETE FROM users WHERE id = %s AND company_id = %s"
        val = (id, company_id)

        cursor.execute(sql, val)

        connection.commit()

    except:
        connection.rollback()
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def block_parking_lot(company_id, id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Get all companies
        sql = "UPDATE parking_lots SET blocked = TRUE WHERE id = %s AND company_id = %s"
        val = (id, company_id)

        cursor.execute(sql, val)

        connection.commit()

    except:
        connection.rollback()
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)


def unblock_parking_lot(company_id, id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Get all companies
        sql = "UPDATE parking_lots SET blocked = FALSE WHERE id = %s AND company_id = %s"
        val = (id, company_id)

        cursor.execute(sql, val)

        connection.commit()

    except:
        connection.rollback()
        raise ServerException('Database internal error', 500)

    finally:
        cursor.close()
        close_connection(connection)
