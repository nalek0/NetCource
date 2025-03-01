from flask import request, Flask

app = Flask(__name__)
products = {}
id_counter = 1

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/product", methods=['POST'])
def post_product():
    global id_counter
    product_json = {
        "id": id_counter,
        "name": request.form['name'],
        "description": request.form['description']
    }
    products[id_counter] = product_json
    id_counter += 1

    return product_json

@app.route("/product/<int:product_id>", methods=['GET', 'PUT', 'DELETE'])
def product_api(product_id: int):
    if request.method == 'GET':
        return products[product_id]
    elif request.method == 'PUT':
        product_json = products[product_id]

        if 'name' in request.form.keys():
            product_json['name'] = request.form['name']

        if 'description' in request.form.keys():
            product_json['description'] = request.form['description']

        products[product_id] = product_json

        return product_json
    else: # request.method == 'DELETE'
        product_json = products.pop(product_id, {})

        return product_json

@app.route("/products", methods=['GET'])
def products_api():
    result = []

    for product_json in products.values():
        result.append(product_json)

    return result
