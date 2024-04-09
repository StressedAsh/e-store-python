from flask import Blueprint, jsonify, request, redirect, url_for
from db import db
from models import Customer

# Create a Blueprint for the customers API
api_customers_bp = Blueprint("api_customers", __name__)

@api_customers_bp.route("/", methods=["GET"])
def get_customers():
    statement = db.select(Customer).order_by(Customer.name)
    records = db.session.execute(statement)
    results = records.scalars()
    return jsonify([cust.to_json() for cust in results])

@api_customers_bp.route("/<int:id>", methods=["PUT"])
def update_balance(id):
    data = request.get_json()
    customer = db.get_or_404(Customer, id)
    if "balance" not in data:
        return "Invalid Request", 405
    balance = data["balance"]
    if not isinstance(balance, (int, float)):
        return "Invalid Request", 405
    customer.balance = balance
    db.session.commit()
    return "", 204

@api_customers_bp.route("/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = db.get_or_404(Customer, id)
    db.session.delete(customer)
    db.session.commit()
    return "", 204

@api_customers_bp.route("/<int:id>", methods=["POST"])
def delete_customer_post(id):
    customer = db.get_or_404(Customer, id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for("html.customers_info"))

@api_customers_bp.route("/", methods=["POST"])
def customers_json():
    # ! This method uses the form in my html so not as per the project instructions
    if request.form:
        data = request.form.to_dict()
        customer = Customer(**data)
        db.session.add(customer)
        db.session.commit()
    else:
        data = request.get_json()
        if "name" not in data or "balance" not in data or "phone" not in data:
            return "Invalid Request", 400
        name = data["name"]
        if not isinstance(name, str):
            return "Invalid Request", 400
        balance = data["balance"]
        if not isinstance(balance, (int, float)) or balance < 0:
            return "Invalid Request", 400
        phone = data["phone"]
        db.session.add(Customer(name=name, balance=balance, phone=phone))
        db.session.commit()
    return redirect(url_for("html.customers_info"))