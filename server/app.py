import os

from flask import Flask
from flask_socketio import join_room, leave_room
from flask_socketio import SocketIO
from flask import request

# from flask_cors import CORS

import json
import random
import requests
import base64

# For Spotify
CLIENT_SECRET = "5c04ecc65221460587462cd9dabd9eae"
CLIENT_ID = "bad02ecfaf4046638a1daa7f60cbe42b"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Allow cross origin to be able to do websockets from different servers
# socketio = SocketIO(app)
socketio = SocketIO(app, path="/ws/socket.io", cors_allowed_origins='*')
# CORS(app)

#### DATABASE ####
class Player:
  def __init__(self):
    self.host = False
    self.name = '' # Name of player
    self.id = '' # Spotify username
    self.points = 0
    self.access_token = ''
    self.refresh_token = ''

class Room:
  def __init__(self, code):
    self.code = code # Room code
    self.players = []
    self.toptracks = []

ROOMS = []
PLAYERS = [] 

COLOR_COUNTER = 0
COLORS = [
    '#FF8360',
    '#E8E288',
    '#7DCE82',
    '#3CDBD3',
    '#B9C0DA',
    '#998DA0',
    '#63585E',
    '#B5838D'
]

##################

@socketio.on('generate_access_token')
def check_token(data):
    print("[1] - YES")
    access_token, refresh_token = generate_access_token(data['code'])
    socketio.emit("access_token", {'access_token': access_token, 'refresh_token': refresh_token, 'sid': request.sid}, to=request.sid)

@socketio.on('connect')
def connected():
    socketio.emit('connect')

@socketio.on('toptrack')
def get_top_track(data):
    trackid = data['trackid']
    code = data['room']
    sid = data['sid']

    global ROOMS
    for Room in ROOMS:
        if code == Room.code:
            Room.toptracks.append({
                'id': trackid,
                'player': sid
            })
            print(Room.toptracks)
            socketio.emit("top_tracks_list", {'top_tracks_list': Room.toptracks}, room=code)

    

    

@socketio.on('disconnect')
def disconnected():
    global ROOMS
    for Room in ROOMS:
        for player in Room.players:
            if player.sid == request.sid:
                print(f"{player.name} disconnected!")
                Room.players.remove(player)

                list_of_players = []
                for player in Room.players:
                    list_of_players.append({
                        'name': player.name,
                        'id': player.id,
                        'points': player.points,
                        'access_token': player.access_token,
                        'refresh_token': player.refresh_token,
                        'color': player.color,
                        'sid': player.sid,
                    })

                socketio.emit("listofplayers", {'players': list_of_players}, room=Room.code)
                return

@socketio.on('leave_room')
def leave_room(data):
    global ROOMS
    for Room in ROOMS:
        if Room.code == data['code']:
            for player in Room.players:
                if player.sid == request.sid:
                    print(f"{player.name} disconnected!")
                    Room.players.remove(player)

                    list_of_players = []
                    for player in Room.players:
                        list_of_players.append({
                            'name': player.name,
                            'id': player.id,
                            'points': player.points,
                            'access_token': player.access_token,
                            'refresh_token': player.refresh_token,
                            'color': player.color,
                            'sid': player.sid,
                        })

                    socketio.emit("listofplayers", {'players': list_of_players}, room=data['code'])
                    return
        

@socketio.on('createRoom')
def createRoom():
    # Get the global variable (think of the scope)
    global ROOMS

    # Generate a random room code, 4 letters
    code = generateId()

    ROOMS.append(Room(code))

    socketio.emit('roomCode', {'code': code}, to=request.sid)

    print(f"[Server] Creating room: {code}")

@socketio.on('joinRoom')
def joinRoom(data):
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    code = data['code']

    global ROOMS
    global PLAYERS

    global CLIENT_ID
    global CLIENT_SECRET

    for Room in ROOMS:
        print("Room: ", Room.code, code)
        if Room.code == code:
            # sending get request and saving the response as response object
            r = requests.get(url = "https://api.spotify.com/v1/me", headers={"Authorization": "Bearer " + access_token})
            
            # extracting data in json format
            data = r.json()

            # Have the player join the room
            join_room(code)

            # Create player object
            new_player = Player()

            new_player.name = str(data['display_name'])
            new_player.id = str(data['id'])
            new_player.points = 0
            new_player.access_token = access_token
            new_player.refresh_token = refresh_token
            new_player.sid = request.sid
            new_player.color = getColor()

            # print("[0]", new_player.id)

            print(f"[{code}] {new_player.name} joined")

            # Check if the player already exists, i.e. reconnected
            reconnected = False
            for player in Room.players:
                if new_player.id == player.id:
                    reconnected = True
                    print(f"[{code}] {new_player.name} reconnected")

            list_of_players = []
            
            if reconnected == False:
                # If the room is empty, make the user host
                if len(Room.players) == 0:
                    new_player.host = True
                    print(f"[{code}] Making {new_player.name} host")
                
                Room.players.append(new_player)

            for player in Room.players:
                list_of_players.append({
                    'name': player.name,
                    'id': player.id,
                    'points': player.points,
                    'access_token': player.access_token,
                    'refresh_token': player.refresh_token,
                    'color': player.color,
                    'sid': player.sid,
                })

            socketio.emit("listofplayers", {'players': list_of_players}, room=code)
            return
    print("not a room") 
    socketio.emit("not_a_room", to=request.sid)


def generate_access_token(code):
    global CLIENT_ID
    global CLIENT_SECRET

    req = requests.post(
        url = "https://accounts.spotify.com/api/token", 
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "https://musicwithfriends.fdrive.se/logincallback",
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    )
    print(req.json())
    print("Response code: ", req.status_code)

    if req.status_code == 400: 
        print(Error)
    else: 
        response = req.json()
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        return access_token, refresh_token

def getColor():
    global COLORS
    global COLOR_COUNTER

    color = COLORS[COLOR_COUNTER]
    COLOR_COUNTER += 1

    if( COLOR_COUNTER == len(COLORS) - 1 ):
        COLOR_COUNTER = 0

    return color

    

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
    socketio.run(app, host='0.0.0.0', port=5000, log_output=True)