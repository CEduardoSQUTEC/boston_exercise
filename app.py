import os

from dotenv import dotenv_values
from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


config = dotenv_values('.env')

DB_USER = config['DB_USER']
DB_PASSWORD = config['DB_PASSWORD']
DB_NAME = config['DB_NAME']
DB_HOST = os.getenv('DB_HOST')
DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric)
    stock = db.Column(db.Integer)


@app.route('/insert-sample-data', methods=['GET'])
def insert_sample_data():
    sample_products = [
        {'name': 'Shirt', 'description': 'Cotton shirt', 'price': 25.99, 'stock': 10},
        {'name': 'Pants', 'description': 'Denim pants', 'price': 39.99, 'stock': 20},
        {'name': 'Shoes', 'description': 'Sports shoes', 'price': 49.99, 'stock': 15}
    ]
    try:
        for product_data in sample_products:
            new_product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                stock=product_data['stock']
            )
            db.session.add(new_product)
            db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Sample data already inserted'}), 409
    return jsonify({'message': 'Sample data inserted successfully'}), 200


@app.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    response = []
    for product in products:
        response.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock
        })
    return jsonify({'products': response}), 200


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    response = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(product.price),
        'stock': product.stock
    }
    return jsonify(response), 200


@app.route('/')
def index():
    return "<h1>The server is up and running.<h1>"


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8080,
    )
