from flask import Flask, request, json
import json
"""
will be using SQLlight later on right now.................... not :)
"""


class Player:

    def __init__(self, player_id, data):
        self.id = player_id
        self.data = data


id_counter = 0  # giving id's to peoplez
players = []  # list O' players to show MP works... database later.jpg
app = Flask(__name__)


@app.route("/player", methods=['POST'])
def player_post():
    """
    recive data of a new player, make a new player object and return the id of the new player
    use case: new player connects so he gets an id and initialized in the server
    :return: player id / error
    """
    global id_counter
    if request.headers['Content-Type'] == 'application/json':  # might have different types in the future
        data = json.loads(request.data)  # unload json
        players.append(Player(id_counter, data))
        id_counter += 1
        return json.dumps({'response': 'OK', 'code': 200, 'id': id_counter - 1})
    else:
        return "Unsupported Media Type", 415


@app.route("/player", methods=['GET'])
def player_get():
    """
    get the data of a player using the id in a json - might change it to plain text but i think future use case will
    have more input so json is better for the future
    :return: all the attributes of the requested player object or error / player not found
    """
    if request.headers['Content-Type'] == 'application/json':
        data = json.loads(request.data)
        current_id = data['id']
        if current_id == 'all':
            data = json.dumps([ob.__dict__ for ob in players])
            return data
        else:
            current_id = int(data['id'])
            player = next((x for x in players if x.id == current_id), None)
            print(player, 'gersgdsfrgdf', current_id)
        if player is not None:
            return json.dumps(player.__dict__)
        else:
            return 'player not existo ok', 200
    else:
        return "Unsupported Media Type", 415


@app.route("/player", methods=['PUT'])
def player_put():
    """
    update the data of the given player (id given in the json)
    :return: ok or error if player doesnt exist
    """
    if request.headers['Content-Type'] == 'application/json':
        data = json.loads(request.data)
        current_id = data['id']
        player = next((x for x in players if x.id == current_id), None)
        if player is None:
            return 'player not existo ok', 200
        else:
            player.data = data
            return 'OK', 200


if __name__ == '__main__':
    app.run(debug = True)
