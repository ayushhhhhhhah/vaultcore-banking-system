from flask import Blueprint, request, jsonify

from services.login_service import login_customer


login_route = Blueprint(
    'login_route',
    __name__
)


@login_route.route('/login', methods=['POST'])
def login():

    try:

        data = request.get_json()

        email = data.get('email')

        password = data.get('password')

        if not email or not password:

            return jsonify({

                "error": "Email and password required"

            }), 400

        result, status_code = login_customer(
            email,
            password
        )

        return jsonify(result), status_code

    except Exception as e:

        print(e)

        return jsonify({

            "error": "Login failed"

        }), 500