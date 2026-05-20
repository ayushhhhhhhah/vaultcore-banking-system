from flask import Blueprint, jsonify, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from services.transaction_service import (
    get_all_transactions,
    deposit_money,
    transfer_funds,
    withdraw_any_funds
)

transaction_routes = Blueprint(
    'transaction_routes',
    __name__
)


# =========================
# GET ALL TRANSACTIONS
# =========================

@transaction_routes.route(
    '/transactions',
    methods=['GET']
)
@jwt_required()
def get_transactions():

    logged_in_customer_id = int(
        get_jwt_identity()
    )

    result = get_all_transactions(
        logged_in_customer_id
    )

    return jsonify(result), 200



# =========================
# DEPOSIT MONEY
# =========================

@transaction_routes.route(
    '/deposit',
    methods=['POST']
)
@jwt_required()
def deposit():

    logged_in_customer_id = int(
        get_jwt_identity()
    )

    data = request.get_json()

    account_id = int(
        data.get('account_id')
    )

    amount = float(
        data.get('amount')
    )

    result = deposit_money(
        logged_in_customer_id,
        account_id,
        amount
    )

    return jsonify(result), 200



# =========================
# WITHDRAW MONEY
# =========================

@transaction_routes.route(
    '/withdraw',
    methods=['POST']
)
@jwt_required()
def withdraw():

    logged_in_customer_id = int(
        get_jwt_identity()
    )

    data = request.get_json()

    account_id = int(
        data.get('account_id')
    )

    amount = float(
        data.get('amount')
    )

    result = withdraw_any_funds(
        logged_in_customer_id,
        account_id,
        amount
    )

    return jsonify(result), 200



# =========================
# TRANSFER MONEY
# =========================

@transaction_routes.route(
    '/transfer',
    methods=['POST']
)
@jwt_required()
def transfer():

    logged_in_customer_id = int(
        get_jwt_identity()
    )

    data = request.get_json()

    sender_account_id = int(
        data.get('sender_account_id')
    )

    receiver_account_id = int(
        data.get('receiver_account_id')
    )

    amount = float(
        data.get('amount')
    )

    result = transfer_funds(
        logged_in_customer_id,
        sender_account_id,
        receiver_account_id,
        amount
    )

    return jsonify(result), 200