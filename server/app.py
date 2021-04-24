import os
from flask import Flask
from flask_socketio import join_room, leave_room, close_room
from flask_socketio import SocketIO
from flask import request, jsonify, Response
import time
import logging

from flask_cors import CORS

import json
import random
import requests
import base64
import sys

# For Spotify
CLIENT_SECRET = "5c04ecc65221460587462cd9dabd9eae"
CLIENT_ID = "bad02ecfaf4046638a1daa7f60cbe42b"

ENV = sys.argv[1]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# log = logging.getLogger('werkzeug')
# log.disabled = True

# Allow cross origin to be able to do websockets from different servers
# socketio = SocketIO(app)
if ENV == 'production' or ENV == 'prod':
    print("Running production mode")
    socketio = SocketIO(app, path="/ws", cors_allowed_origins='*')
else:
    print("Running development mode")
    socketio = SocketIO(app, cors_allowed_origins='*')

#### DATABASE ####
class Player:
  def __init__(self):
    self.host = False
    self.name = '' # Name of player
    self.id = '' # Spotify username
    self.points = 0
    self.access_token = ''
    self.refresh_token = ''
    self.guesses = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Room:
  def __init__(self, code):
    self.questions = ["Who's top song is this?"]
    self.code = code # Room code
    self.players = [] # player object 
    self.answers = [] # every persons top track for example {player: sid, answer: trackid}
    self.results = [] # points for each person


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

@app.route('/api/<code>/results', methods=['GET'])
def results(code):
    global ROOMS
    for Room in ROOMS:
        if Room.code == code:
            for player in Room.players:
                player.points = 0;
                for guess in player.guesses:
                    if guess['correct_answer'] == guess['guess']:
                        player.points += 10
            players = []
            for player in Room.players:
                players.append({
                    'host': player.host,
                    'name': player.name,
                    'id': player.id,
                    'points': player.points,
                    'guesses': player.guesses
                })
            return Response(json.dumps({
                'questions': Room.questions,
                'code': Room.code,
                'players': players,
                'answers': Room.answers,
                'results': Room.results
            }), status=200, mimetype='application/json',headers={
                "Access-Control-Allow-Origin": "*"
            })
    return Response(status=404, headers={
        "Access-Control-Allow-Origin": "*"
    })
    

@socketio.on('generate_access_token')
def check_token(data):
    print("[1] - YES")
    access_token, refresh_token = generate_access_token(data['code'])
    socketio.emit("access_token", {'access_token': access_token, 'refresh_token': refresh_token, 'sid': request.sid}, to=request.sid)

# @socketio.on('connect')
# def connected():
#     socketio.emit('connect')

@socketio.on('isRoom')
def isRoom(data):
    global ROOMS
    for Room in ROOMS:
        if Room.code == data['code']:
            socketio.emit('isRoom', {'isRoom':'true'}, to=request.sid)
            return
            
    socketio.emit('isRoom', {'isRoom':'false'}, to=request.sid)
    return

@socketio.on('guess')
def guess(data):
    player_sid = data['sid']
    player_guess_sid = data['guess']
    current_question = data['current_question']
    code = data['code']

    global ROOMS
    for Room in ROOMS:
        if Room.code == code:
            for player in Room.players:
                if player.sid == player_sid: # looking for self
                    player.guesses.append({
                        'question': current_question,
                        'guess': player_guess_sid,
                        'correct_answer': Room.answers[current_question]['player'],
                        'info': Room.answers[current_question]['info']
                    })
                    return

@socketio.on('game_ended')
def game_ended(data):
    code = data['code']
    global ROOMS 

    socketio.emit('game_ended', room=code)
                        
@socketio.on('next_question')
def next_question(data):
    code = data['code']
    current_question = data['current_question']
    global ROOMS
    for Room in ROOMS:
        if code == Room.code:
            # answer is track id in this case
            socketio.emit('next_question', {'answer': Room.answers[current_question]['player'],'current_question': current_question, 'trackid': Room.answers[current_question]['info']}, room=code)

@socketio.on('start_game')
def start_game(data):
    code = data['code']
    socketio.emit('start_game', room=code)
    num_of_players = 0
    global ROOMS
    for Room in ROOMS:
        if Room.code == code:
            num_of_players = len(Room.players)

    print(f"[{code}] Game has started!")
    print(f"[{code}] Numer of players: {num_of_players}")

@socketio.on('toptrack')
def get_top_track(data):
    trackid = data['trackid']
    code = data['room']
    sid = data['sid']

    global ROOMS
    # Go thorugh each room and find the one sending the 'toptrack' emit
    for Room in ROOMS:
        if code == Room.code:
            # When we find the room, double check if the player isn't just reconnecting
            for pair in Room.answers:
                if sid == pair['player']:
                    socketio.emit("top_tracks_list", {'top_tracks_list': Room.answers}, room=code)
                    return
            # Send out top tracks to all players in the room
            Room.answers.append({
                'player': sid,
                'info': trackid
            })
            socketio.emit("top_tracks_list", {'top_tracks_list': Room.answers}, room=code)


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

                socketio.emit("list_of_players", {'players': list_of_players}, room=Room.code)
                return


@socketio.on('close_room')
def close_socket_room(data):
    code = data['code']
    socketio.emit("close_room", room=code)
    close_socket_room(code)

def close_socket_room(code):
    for Room in ROOMS:
        if Room.code == code:
            ROOMS.remove(Room)
            close_room(code)
            print(f"[Server] Deleting room {code}")

@socketio.on('leave_room')
def remove_player_from_room(data):
    print("leaving room")
    code = data['code']
    sid = data['sid']

    global ROOMS
    for Room in ROOMS:
        if Room.code == code:
            for player in Room.players:
                if player.sid == sid:
                    print(f"{player.name} disconnected!")

                    # Remove the player from the list of players for that room
                    Room.players.remove(player)

                    # Remove the player from the websocket room
                    if len(Room.players) == 0:
                        close_socket_room(code)
                    else:
                        leave_room(code)

                    # Send out an updated list of players to the room
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

                    socketio.emit("list_of_players", {'players': list_of_players}, room=code)
                    return
        
@socketio.on('createRoom')
def createRoom(data):
    sid = data['sid']

    # Generate a random room code, 4 letters
    code = generateId()

    # Get the global variable (think of the scope?)
    global ROOMS

    reconnecting = False
    for _Room in ROOMS:
        for player in _Room.players:
            if player.sid == sid and player.host == True:
                code = _Room.code
                reconnecting = True
                print(f"[Server] User {player.name} already has an active room: {code}. Rejoining.")

    if not reconnecting: 
        ROOMS.append(Room(code))
        print(f"[Server] Creating room: {code}")
        
    socketio.emit('roomCode', {'code': code}, to=request.sid)


@socketio.on('joinRoom')
def joinRoom(data):
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    code = data['code']
    sid = data['sid']

    global ROOMS
    global PLAYERS

    global CLIENT_ID
    global CLIENT_SECRET

    for Room in ROOMS:
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
            new_player.sid = sid
            new_player.color = getColor()

            # print("[0]", new_player.id)


            # Check if the player already exists, i.e. reconnected
            reconnected = False
            for player in Room.players:
                if new_player.id == player.id:
                    reconnected = True
                    print(f"[{code}] {new_player.name} reconnected")

            list_of_players = []
            
            if reconnected == False:
                print(f"[{code}] {new_player.name} joined")
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
                    'host': player.host
                })

            socketio.emit("list_of_players", {'players': list_of_players}, room=code)
            return
    print("not a room") 
    socketio.emit("not_a_room", to=request.sid)

def generate_access_token(code):
    global CLIENT_ID
    global CLIENT_SECRET

    if ENV == 'production':
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "https://musicwithfriends.fdrive.se/logincallback",
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    else: 
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:8080/logincallback",
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

    req = requests.post(
        url = "https://accounts.spotify.com/api/token", 
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data = data
    )
    print(req.json())
    print("Response code: ", req.status_code)

    if req.status_code == 400: 
        print("Error")
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

def generateId():
    letters = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    code = ""
    for i in range(4):
        code += letters[random.randint(0, 31)]

    # Check for bad words and make sure the room doesn't already exist
    if code in ['NGGR','FUCK','SHIT','CUNT','DICK','NSFW','BICH','HORE','HORA','KUKA','6969','6666','8008']:
        code = generateId()

    global ROOMS
    for Room in ROOMS:
        if Room.code == code:
            code = generateId()

    return code

if __name__ == '__main__':
    if ENV == 'production' or 'prod':
        socketio.run(app, host='0.0.0.0', port=5000)
    else:
        socketio.run(app)
