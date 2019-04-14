from flask import Blueprint, request, jsonify, session

from err import validate_body_contains, InvalidUsage
from models import User


def make_user_routes(db_session):
    user_routes = Blueprint('user_routes', __name__)

    def create_user(user):
        """
        Create the user if their email doesn't exist
        """
        if db_session.query(User).filter(User.email == user.email).count() == 0:
            db_session.add(user)
            db_session.commit()
        else:
            raise InvalidUsage("User with email exists", 404)

    @user_routes.route('/sign_up', methods=['POST'])
    def sign_up():
        body = request.get_json()
        validate_body_contains(['name', 'email', 'venmo', 'password', 'house_code'], body)

        user = User(name=body['name'], email=body['email'], password=body['password'], household_id=body['house_code'],
                    venmo=body['venmo'])

        create_user(user)
        return "OK"

    @user_routes.route('/sign_up_leader', methods=['POST'])
    def sign_up_leader():
        body = request.get_json()
        validate_body_contains(['name', 'email', 'venmo', 'password'], body)

        user = User(name=body['name'], email=body['email'], password=body['password'], venmo=body['venmo'], leader=True)

        create_user(user)
        session['leader'] = True
        return "OK"

    return user_routes
