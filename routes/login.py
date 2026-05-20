from flask import Blueprint, request, jsonify

from services.login_service import login_user


login_route = Blueprint(
    'login_route',
    __name__
)


@login_route.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    email = data.get('email')

    password = data.get('password')

    result, status_code = login_user(
        email,
        password
    )

    return jsonify(result), status_code