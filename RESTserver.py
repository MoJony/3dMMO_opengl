from flask import Flask, jsonify, request
from multiprocessing import Value
import requests
import json

counter = Value('i', 0)
app = Flask(__name__)

a = []
help_message = """
API Usage:

- GET    /api/list  # requests.get('http://localhost:5000/api/list',headers=headers)
- POST   /api/add data={"key": "value"}  # requests.post(base_url, headers=headers, data=payload)
- GET    /api/get/<id>  # curl -XGET -H 'Content-Type: application/json' http://localhost:5000/api/get/2
- PUT    /api/update/<id> data={"key": "value_to_replace"}
- DELETE /api/delete/<id>


g = requests.get('http://localhost:5000/api/get/1',headers=headers)
p = 
"""


def id_generator():
    with counter.get_lock():
        counter.value += 1
        return counter.value


@app.route('/api', methods=['GET'])
def help():
    return help_message


@app.route('/api/list', methods=['GET'])
def list():
    return jsonify(a)


@app.route('/api/add', methods=['POST'])
def index():
    payload = request.json
    payload['id'] = id_generator()
    a.append(payload)
    return "Created: {} \n".format(payload)


@app.route('/api/get', methods=['GET'])
def get_none():
    return 'ID Required: /api/get/<id> \n'


@app.route('/api/get/<int:_id>', methods=['GET'])
def get(_id):
    for user in a:
        if _id == user['id']:
            selected_user = user
    return jsonify(selected_user)


@app.route('/api/update', methods=['PUT'])
def update_none():
    return 'ID and Desired K/V in Payload required: /api/update/<id> -d \'{"name": "john"}\' \n'


@app.route('/api/update/<int:_id>', methods=['PUT'])
def update(_id):
    update_req = request.json
    key_to_update = next(iter(update_req))
    update_val = (item for item in a if item['id'] == _id).next()[key_to_update] = next(iter(update_req))
    update_resp = (item for item in a if item['id'] == _id).next()
    return "Updated: {} \n".format(update_resp)
    # need to fix this python 2 stuff

@app.route('/api/delete/<int:_id>', methods=['DELETE'])
def delete(_id):
    deleted_user = (item for item in a if item['id'] == _id).next()
    a.remove(deleted_user)
    return "Deleted: {} \n".format(deleted_user)

if __name__ == '__main__':
    app.debug = True
    app.run()