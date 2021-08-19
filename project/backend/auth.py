from database import get_user_by_email
from exceptions import ServerException
from utils import verify_password, jwt_encode, jwt_decode


def login(email, password):
    '''
    Authenticate an user
    Returns JWT token
    '''

    # Get user from database
    user = get_user_by_email(email)

    # Check if user exists
    if user is None:
        raise ServerException('User does not exist', 403)

    # Verify password
    if not verify_password(user['password'], password):
        raise ServerException('Wrong password', 403)

    # Verify activation
    if not user['activated']:
        raise ServerException('Your account is not activated', 403)

    # Delete unnecessary fields
    del user['password']
    del user['activated']

    if user['company_id'] is None:
        del user['company_id']

    # Return JWT token
    return jwt_encode(user)


def authenticate(request, roles=['admin', 'company', 'employee']):
    '''
    Authenticate an user
    Check user role permissions
    '''

    # Extract token from request
    try:
        token = request.headers.get('Authorization').split(" ")[1]
    except:
        raise ServerException(
            'Authentication failed: user not logged in', 403)

    # Decode JWT token
    user = jwt_decode(token)

    # Check user role
    if user['role_name'] not in roles:
        raise ServerException('Permission denied', 401)

    # Return decoded token
    return user
