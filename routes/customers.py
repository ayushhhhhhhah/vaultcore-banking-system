from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.customers_service import (
    get_all_customers,
    add_new_customer,
    delete_specific_customer,
    get_specific_customer,
    update_specific_customer,
    change_customer_password
)

customer_routes = Blueprint(
    'customer_routes',
    __name__
)


# GET LOGGED-IN CUSTOMER INFO
@customer_routes.route('/customers')
@jwt_required()
def get_customers():
    logged_in_customer_id = int(
        get_jwt_identity()
    )

    result = get_all_customers(
        logged_in_customer_id
    )

    return jsonify(result), 200


# ADD CUSTOMER
@customer_routes.route('/customers', methods=['POST'])
def add_customer():

    data = request.get_json()

    result = add_new_customer(
        data['first_name'],
        data['middle_name'],
        data['last_name'],
        data['email'],
        data['phone'],
        data['password']
    )

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 201


# GET SPECIFIC CUSTOMER
@customer_routes.route('/customers/<customer_id>')
@jwt_required()
def get_customer(customer_id):
    logged_in_customer_id = int(
        get_jwt_identity()
    )

    # OWNERSHIP VALIDATION
    if int(customer_id) != logged_in_customer_id:

        return jsonify({
            "error": "Unauthorized access"
        }), 403

    result = get_specific_customer(customer_id)

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200


# UPDATE CUSTOMER
@customer_routes.route('/customers/<customer_id>', methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    logged_in_customer_id = int(
        get_jwt_identity()
    )

    # OWNERSHIP VALIDATION
    if int(customer_id) != logged_in_customer_id:

        return jsonify({
            "error": "Unauthorized access"
        }), 403

    data = request.get_json()

    result = update_specific_customer(
        data['first_name'],
        data['middle_name'],
        data['last_name'],
        data['email'],
        data['phone'],
        data['password'],
        customer_id
    )

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


# DELETE CUSTOMER
@customer_routes.route('/customers/<customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    logged_in_customer_id = int(
        get_jwt_identity()
    )

    # OWNERSHIP VALIDATION
    if int(customer_id) != logged_in_customer_id:

        return jsonify({
            "error": "Unauthorized access"
        }), 403

    result = delete_specific_customer(customer_id)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200

@customer_routes.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():

    logged_in_customer_id = int(get_jwt_identity())

    data = request.get_json()

    old_password = data['old_password']
    new_password = data['new_password']

    result = change_customer_password(
        logged_in_customer_id,
        old_password,
        new_password
    )

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200
