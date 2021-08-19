from flask import Flask, request, Response, json
from flask_cors import CORS, cross_origin
from exceptions import ServerException
from utils import extract_fields
import auth
import core
import datetime

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/status', methods=['GET'])
def status():
    '''
    Check server's status
    '''

    return Response('Server is running', status=200, mimetype='application/json')


@app.route('/api/auth/login', methods=['POST'])
def login():
    '''
    Authenticate user
    Returns JWT token
    '''

    try:
        # Extract email and password
        email, password = extract_fields(request, 'email', 'password')

        # Authenticate user
        token = auth.login(email, password)

        # Compose response
        data = {'token': token}

        # Return response
        return Response(json.dumps(data), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/companies', methods=['POST'])
def create_company():
    '''
    Create a company
    '''

    try:
        # Extract data
        company_name, first_name, last_name, email, phone, password = extract_fields(
            request, 'company_name', 'first_name', 'last_name', 'email', 'phone', 'password')

        # Create company
        company = core.create_company(
            company_name, first_name, last_name, email, phone, password)

        # Return response
        return Response(json.dumps(company), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/companies/<id>/approve', methods=['POST'])
def approve_company(id):
    '''
    Approve a company request
    '''

    try:
        # Authenticate user
        auth.authenticate(request, roles=['admin'])

        # Approve company
        core.approve_company(id)

        # Return response
        return Response(json.dumps('Successfully approved'), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/users/activate/<token>', methods=['GET'])
def activate_user(token):
    '''
    Activate account using activation_token
    '''

    try:
        # Activate account
        core.activate_account(token)

        # Return response
        return Response(json.dumps('Account successfully activated'), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/parking_lots', methods=['POST'])
def create_parking_lots():
    '''
    Create parking lots
    '''

    try:
        # Authenticate user
        user = auth.authenticate(request, roles=['company'])

        # Extract data
        parking_lots_count, begin_with = extract_fields(
            request, 'parking_lots_count', 'begin_with')

        # Create parking lots
        core.create_parking_lots(
            user['company_id'], int(parking_lots_count), int(begin_with))

        # Return response
        return Response(json.dumps('Parking lots successfully created'), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/accounts', methods=['POST'])
def create_accounts():
    '''
    Create employee accounts for company
    '''

    try:
        # Authenticate user
        user = auth.authenticate(request, roles=['company'])

        # Extract data
        (accounts,) = extract_fields(request, 'accounts')

        # Create accounts
        data = core.create_accounts(user['company_id'], accounts)

        # Return response
        return Response(json.dumps(data), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    '''
    Get employee accounts for company
    '''

    try:
        # Authenticate user
        user = auth.authenticate(request, roles=['company'])

        # Get accounts
        data = core.get_accounts(user['company_id'])

        # Return response
        return Response(json.dumps(data), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/parking_lot/book', methods=['POST'])
def book_parking_lot():
    '''
    Book parking lot
    '''

    try:
        # Authenticate user
        user = auth.authenticate(request, roles=['employee'])

        # Compute tomorrow date
        # TODO: may skip weekend days
        date = str(datetime.date.today() + datetime.timedelta(days=1))

        # Book parking lot
        data = core.book_parking_lot(user['id'], user['company_id'], date)

        # Return response
        return Response(json.dumps(data), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/parking_lot/books', methods=['GET'])
def get_parking_lot_books():
    '''
    Get parking lot books
    '''

    try:
        # Authenticate user
        user = auth.authenticate(request, roles=['employee'])

        # Compute today date
        date = str(datetime.date.today())

        # Get books
        data = core.get_parking_lot_books(user['id'], user['company_id'], date)

        # Return response
        return Response(json.dumps(data), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/parking_lot/books/<id>', methods=['DELETE'])
def delete_parking_lot_books(id):
    '''
    Delete parking lot book
    '''

    try:
        # Authenticate user
        user = auth.authenticate(request, roles=['employee'])

        # Delete book
        core.delete_parking_lot_books(user['id'], id)

        # Return response
        return Response(json.dumps('Deleted'), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/companies', methods=['GET'])
def get_companies():
    try:
        # Authenticate user
        user = auth.authenticate(request, roles=['admin'])

        # Get companies
        data = core.get_companies()

        # Return response
        return Response(json.dumps(data), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/company', methods=['GET'])
def get_company():
    try:
        # Authenticate user
        user = auth.authenticate(request, roles=['company'])

        # Get company
        data = core.get_company(user['company_id'])

        # Return response
        return Response(json.dumps(data), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/parking_lots/<id>', methods=['DELETE'])
def delete_parking_lot(id):
    '''
    Delete a parking lot
    '''

    try:
        # Authenticate user
        user = auth.authenticate(request, roles=['company'])

        # Approve company
        core.delete_parking_lot(user['company_id'], id)

        # Return response
        return Response(json.dumps('Successfully deleted'), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/parking_lots', methods=['DELETE'])
def delete_parking_lots():
    '''
    Delete a parking lot
    '''

    try:
        # Authenticate user
        user = auth.authenticate(request, roles=['company'])

        # Approve company
        core.delete_parking_lots(user['company_id'])

        # Return response
        return Response(json.dumps('Successfully deleted'), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/parking_lots/<id>/block', methods=['POST'])
def block_parking_lot(id):
    '''
    Block a parking lot
    '''

    try:
        # Authenticate user
        user = auth.authenticate(request, roles=['company', 'employee'])

        # Approve company
        core.block_parking_lot(user['company_id'], id)

        # Return response
        return Response(json.dumps('Successfully blocked'), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/parking_lots/<id>/unblock', methods=['POST'])
def unblock_parking_lot(id):
    '''
    Block a parking lot
    '''

    try:
        # Authenticate user
        user = auth.authenticate(request, roles=['company'])

        # Approve company
        core.unblock_parking_lot(user['company_id'], id)

        # Return response
        return Response(json.dumps('Successfully unblocked'), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


@app.route('/api/employees/<id>', methods=['DELETE'])
def delete_employees(id):
    '''
    Delete employee
    '''

    try:
        # Authenticate user
        user = auth.authenticate(request, roles=['company'])

        # Approve company
        core.delete_employee(user['company_id'], id)

        # Return response
        return Response(json.dumps('Successfully deleted'), status=200, mimetype='application/json')

    except ServerException as e:
        return e.to_response()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
