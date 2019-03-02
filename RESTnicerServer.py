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
    global id_counter
    if request.headers['Content-Type'] == 'application/json':
        data = json.loads(request.data)
        players.append(Player(id_counter, data))
        id_counter += 1
        return 'OK', 200, id_counter - 1
    else:
        return "Unsupported Media Type", 415


@app.route("/player", methods=['GET'])
def player_get():
    if request.headers['Content-Type'] == 'application/json':
        data = json.loads(request.data)
        print(data)
        current_id = data['id']
        player = next((x for x in players if x.id == current_id), None)
        if player is not None:
            return json.dumps(player.__dict__)
        else:
            return 'player not existo ok', 200
    else:
        return "Unsupported Media Type", 415


if __name__ == '__main__':
    app.run(debug = True)
