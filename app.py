from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from routes.customers import customer_routes
from routes.accounts import account_routes
from routes.transactions import transaction_routes
from routes.login import login_route

app = Flask(__name__)

CORS(app)

app.config['JWT_SECRET_KEY'] = 'vaultcore-super-secure-banking-system-secret-key'

jwt = JWTManager(app)

app.register_blueprint(customer_routes)
app.register_blueprint(account_routes)
app.register_blueprint(transaction_routes)
app.register_blueprint(login_route)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)