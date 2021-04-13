import os

from flask import Flask
from flask_socketio import join_room, leave_room
from flask_socketio import SocketIO

import json
import random
import requests

# For Spotify
CLIENT_SECRET = "5c04ecc65221460587462cd9dabd9eae"
CLIENT_ID = "bad02ecfaf4046638a1daa7f60cbe42b"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Allow cross origin to be able to do websockets from different servers
socketio = SocketIO(app, cors_allowed_origins="*")

#### DATABASE ####
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
PLAYERS = [] 

##################

@socketio.on('connect')
def connected():
    socketio.emit('connect')

@socketio.on('createRoom')
def createRoom():
    # Get the global variable (think of the scope)
    global ROOMS

    # Generate a random room code, 4 letters
    code = generateId()

    ROOMS.append(Room(code))

    socketio.emit('roomCode', {'code': code})

    print(f"[Server] Creating room: {code}")

@socketio.on('joinRoom')
def joinRoom(data):
    token = data['token']
    code = data['code']

    global ROOMS
    global PLAYERS

    for Room in ROOMS:
        if Room.code == code:
            # sending get request and saving the response as response object
            r = requests.get(url = "https://api.spotify.com/v1/me", headers={"Authorization": "Bearer " + token})
            
            # extracting data in json format
            data = r.json()

            # Have the player join the room
            join_room(code)

            # Create player object
            new_player = Player(data['display_name'], data['id'])
            print(f"[{code}] {new_player.name} joined")

            # Check if the player already exists, i.e. reconnected
            reconnected = False
            for player in Room.players:
                if new_player.id == player.id:
                    reconnected = True
                    print(f"[{code}] {new_player.name} reconnected")

            list_of_players = []
            if reconnected == False:
                # Tell everyone in the room that player has joined 
                socketio.emit("playerJoined", {'name': new_player.name}, room=code)

                # If the room is empty, make the user host
                if len(Room.players) == 0:
                    new_player.host = True
                    print(f"[{code}] Making {new_player.name} host")
                else:
                    # if the room is not empty, send a list of all players already in the room 
                    for new_player in Room.players:
                        list_of_players.append(new_player.name)
                    socketio.emit("listofplayers", {'players': list_of_players})
                
                # Add the player to the list of players for that room
                Room.players.append(new_player)
            else: 
                for new_player in Room.players:
                    list_of_players.append(new_player.name)
                socketio.emit("listofplayers", {'players': list_of_players})
        else: 
            print(f"[{code}] Room does not exist")

"""
Function to add a player to a room
@args: none
@return: none
"""
def add_player_to_room():
    # creates a new Player object and add it to the array ? 
    pass

"""
Function to generate random 4 letter room code
@args: none
@return: String
"""
def generateId():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    for i in range(4):
        code += letters[random.randint(1, 25)]

    #for Room in ROOMS:
    #    if Room.code == code:
    #        code = generateId() # Make sure this works!!!
    
    return code

# Check if a room exists - not used right now
# def room_exists(code):
#     global ROOMS
#     for ROOM in ROOMS: 
#         print(ROOM.code)
#     if ROOM in ROOMS:
#         if ROOM.code == code:
#             return True
#     return False

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