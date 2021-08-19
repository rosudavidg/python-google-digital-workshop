import database
import random
import string
from utils import generate_activation_token
from email_utils import send_activation_link, send_activation_link_with_password
from exceptions import ServerException


def create_company(company_name, first_name, last_name, email, phone, password):
    '''
    Create a company and a linked user
    '''

    # Generate activation token
    activation_token = generate_activation_token()

    # Create company and user
    data = database.create_company(
        company_name, first_name, last_name, email, phone, password, activation_token)

    # Send activation token via email
    send_activation_link(email, activation_token)

    # Return created company and user details
    return data


def approve_company(company_id):
    database.approve_company(company_id)


def create_parking_lots(company_id, parking_lots_count, begin_with):
    if not database.company_approved(company_id):
        raise ServerException('Company is not approved', 403)

    if database.company_has_parking_lots(company_id):
        raise ServerException('Company already has parking lots', 403)

    database.insert_parking_lots(company_id, parking_lots_count, begin_with)


def activate_account(token):
    '''
    Activate account using activation_token
    '''

    database.activate_account(token)


def create_accounts(company_id, accounts):
    letters = string.ascii_lowercase
    data = {'created_accounts': [], 'failed': []}

    for account in accounts:
        try:
            password = ''.join(random.choice(letters) for _ in range(16))
            first_name = account['first_name']
            last_name = account['last_name']
            phone = account['phone']
            email = account['email']

            # Generate activation token
            activation_token = generate_activation_token()

            # Create user
            user_data = database.create_employee_user(
                company_id, first_name, last_name, email, phone, password, activation_token)

            data['created_accounts'].append(user_data)

            # Send activation token via email
            send_activation_link_with_password(
                email, activation_token, password)

        except:
            data['failed'].append(account)

    return data


def get_accounts(company_id):
    return database.get_accounts(company_id)


def book_parking_lot(user_id, company_id, date):
    has_parking_lot_booked = database.has_parking_lot_booked(
        user_id, company_id, date)

    if has_parking_lot_booked:
        raise ServerException(
            'You already have a parking lot for tomorrow!', 400)

    schedule = database.book_parking_lot(user_id, company_id, date)

    if schedule is None:
        raise ServerException('No available parking lot', 400)

    return schedule


def get_parking_lot_books(user_id, company_id, date):
    return database.get_parking_lot_books(user_id, company_id, date)


def get_companies():
    return database.get_companies()


def get_company(company_id):
    return database.get_company(company_id)


def delete_parking_lot(company_id, id):
    return database.delete_parking_lot(company_id, id)


def delete_parking_lots(company_id):
    return database.delete_parking_lots(company_id)


def delete_employee(company_id, id):
    return database.delete_employee(company_id, id)


def block_parking_lot(company_id, id):
    return database.block_parking_lot(company_id, id)


def unblock_parking_lot(company_id, id):
    return database.unblock_parking_lot(company_id, id)


def delete_parking_lot_books(user_id, id):
    return database.delete_parking_lot_books(user_id, id)
