from flask import Blueprint, request, jsonify

from err import validate_body_contains
from models import Household


def make_household_route(db_session):
    household_routes = Blueprint('household_routes', __name__)

    @household_routes.route('/create_household', methods=['POST'])
    def create():
        body = request.get_json()
        validate_body_contains(['name'], body)

        household = Household(name=body['name'])

        db_session.add(household)
        db_session.commit()

        return jsonify({'name': household.name, 'code': household.id})

    return household_routes
