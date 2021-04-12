import os
from flask import Flask
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room
import json
import random
import requests

CLIENT_SECRET = "5c04ecc65221460587462cd9dabd9eae"
CLIENT_ID = "bad02ecfaf4046638a1daa7f60cbe42b"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# DATABASE #
class Player:
  def __init__(self, name, id):
    self.host = False
    self.name = name # Name of player
    self.id = id # Spotify username
    self.points = 0

class Room:
  def __init__(self, code):
    self.code = code # Room code
    self.players = []

ROOMS = []
ROOM_IDs = []
PLAYERS = []

############

# @socketio.on('token')
# def handle_message(data):
#     print(data['token'])

@socketio.on('createRoom')
def createRoom():
    print("Creating room...")

    global ROOMS
    code = generateId()

    ROOMS.append(Room(code))

    socketio.emit('roomCode', {'code': code})

@socketio.on('joinRoom')
def joinRoom(data):
    token = data['token']
    code = data['code']

    global ROOMS

    for Room in ROOMS:
        if Room.code == code:
            # sending get request and saving the response as response object
            r = requests.get(url = "https://api.spotify.com/v1/me", headers={"Authorization": "Bearer " + token})
            
            # extracting data in json format
            data = r.json()

            # Create player object
            player = Player(data['display_name'], data['id'])

            # Have the player join the room
            join_room(code)

            # Tell everyone in the room that player has joined 
            socketio.emit("playerJoined", {'name': player.name}, room=code)

            # If the room is empty, make the user host
            if len(Room.players) == 0:
                player.host = True
            else:
                # if the room is not empty, send a list of all players already in the room 
                for player in Room.players:
                    list_of_players.append(player.name)
                socketio.emit("listofplayers", {'players': list_of_players})
            
            # Add the player to the list of players for that room
            Room.players.append(player)
        else: 
            print("Room does not exist")

def add_player_to_room():
    # creates a new Player object and add it to the array ? 
    pass

def generateId():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    for i in range(4):
        code += letters[random.randint(1, 25)]

    return code

def room_exists(code):
    global ROOMS

    for ROOM in ROOMS: 
        print(ROOM.code)

    if ROOM in ROOMS:
        if ROOM.code == code:
            return True

    return False

def delete_room():
    # call leave_room() for all players
    pass

def leave_room():
    # remove the player from the room and delete the player object
    pass

def re_assign_host(): 
    # remove old host for the room and assign a new random player as the host
    pass

def recieve_answer(player, results_object, gamemode):
    # recieve answer 
    pass

if __name__ == '__main__':
    #app.run()
    socketio.run(app)