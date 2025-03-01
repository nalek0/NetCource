import os

from flask import send_file, request, Flask
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploaded/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

products = {}
icons = {}
id_counter = 1


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

@app.route("/product/<int:product_id>/image", methods=['GET', 'POST'])
def product_image_api(product_id: int):
    if request.method == 'GET':
        return send_file(icons[product_id], as_attachment=True)
    elif request.method == 'POST':
        file = request.files['icon']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            icons[product_id] = filepath

            return ""
        else:
            return "", 500
