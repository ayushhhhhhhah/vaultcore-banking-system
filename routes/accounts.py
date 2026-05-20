from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.accounts_service import (
    get_all_accounts,
    get_account_byid,
    create_account_newaccount
) # Importing everything from the service layer

account_routes = Blueprint(
    'account_routes',
    __name__
) #blueprint


# GET ALL ACCOUNTS
@account_routes.route('/accounts', methods=['GET'])
@jwt_required()
def get_accounts():
    logged_in_customer_id = get_jwt_identity()

    result = get_all_accounts(
        logged_in_customer_id,
    )

    return jsonify(result), 200


# GET SINGLE ACCOUNT
@account_routes.route('/accounts/<account_id>')
@jwt_required()
def get_account(account_id):
    logged_in_customer_id = int(
        get_jwt_identity()
    )

    result = get_account_byid(
        logged_in_customer_id,
        account_id
    )

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result), 200


# CREATE ACCOUNT
@account_routes.route('/accounts', methods=['POST'])
@jwt_required()
def create_account():
    logged_in_customer_id = int(
        get_jwt_identity()
    )

    data = request.get_json()

    result = create_account_newaccount(
        logged_in_customer_id,
        data['branch_id'],
        data['account_type'],
        data['balance']
    )

    return jsonify(result), 201