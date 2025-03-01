from flask import request, Flask

app = Flask(__name__)
products = {}
id_counter = 1

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/product", methods=['POST'])
def post_product():
    product_json = {
        "id": id_counter,
        "name": request.form['name'],
        "description": request.form['description']
    }
    products[id_counter] = product_json

    return product_json

@app.route("/product/<int:product_id>", methods=['GET'])
def get_product(product_id: int):
    return products[product_id]

@app.route("/product/<int:product_id>", methods=['PUT'])
def update_product(product_id: int):
    product_json = products[product_id]

    if request.form['name'] is not None:
        product_json['name'] = request.form['name']

    if request.form['description'] is not None:
        product_json['description'] = request.form['description']

    products[product_id] = product_json

    return product_json

@app.route("/product/<int:product_id>", methods=['DELETE'])
def remove_product(product_id: int):
    product_json = my_dict.pop('key', None)

    return product_json

@app.route("/products", methods=['GET'])
def get_products():
    result = []

    for product_json in products.values():
        result.append(product_json)

    return result
