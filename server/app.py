# ---------
# This file contains API endpoints, sockets that handle communication with frontend, and database logic
# ---------

import os
from flask import Flask
from flask_socketio import join_room, leave_room, close_room
from flask_socketio import SocketIO
from flask import request, jsonify, Response
import time
import logging

import threading

from flask_cors import CORS

import json
import random
import requests
import base64
import sys

# Database
from tinydb import TinyDB, Query, where
from datetime import date
import time

db = TinyDB('db.json')
# Rooms = db.table("Rooms")
# Rooms.insert({'code':'FDSA'})


# For Spotify
CLIENT_SECRET = "5c04ecc65221460587462cd9dabd9eae"
CLIENT_ID = "bad02ecfaf4046638a1daa7f60cbe42b"

ENV = sys.argv[1]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
log = logging.getLogger('werkzeug')
log.disabled = False

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
        self.name = ''  # Name of player
        self.id = ''  # Spotify username
        self.points = 0
        self.access_token = ''
        self.refresh_token = ''
        self.guesses = []
        self.color = ''

        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                              sort_keys=True, indent=4)


class Room:
    def __init__(self, code):
        self.questions = ["Who's top song is this?"]
        self.code = code  # Room code
        self.players = []  # player object
        # every persons top track for example {player: sid, answer: trackid}
        self.answers = []
        self.results = []  # points for each person
        self.players_guessed = []
        self.started = False
        self.ended = False
        self.current_question = -1
        self.settings = []
        self.guesses = 0
        self.questionTimeStarted = 0


ROOMS = []
PLAYERS = []

COLOR_COUNTER = 0
# Used for player icons
COLORS = [
    '#FF8360',
    '#E8E288',
    '#7DCE82',
    '#3CDBD3',
    '#B9C0DA',
    '#998DA0',
    '#B5838D'
]

################## API Endpoints ##################

# Personal results endpoint. Searches DB for any rooms containing the user and returns game statistics.


@app.route('/api/me/<username>/results', methods=['GET'])
def personal_results(username):
    global ROOMS
    table_Rooms = db.table("Rooms")
    Room = Query()
    Player = Query()
    result = table_Rooms.search(Room.players.any(Player.id == username))
    if result:

        return Response(json.dumps({
            'results': result,
        }), status=200, mimetype='application/json', headers={
            "Access-Control-Allow-Origin": "*"
        })

    return Response(status=200, headers={
        "Access-Control-Allow-Origin": "*"
    })

# Room results endpoint. Searches DB for room that matches code, and returns game statistics.


@app.route('/api/<code>/results', methods=['GET'])
def results(code):
    global ROOMS
    table_Rooms = db.table("Rooms")
    result = table_Rooms.search(where('code') == code)
    if result:
        result = result[0]

        return Response(json.dumps({
            'questions': result['questions'],
            'code': result['code'],
            'players': result['players'],
            'answers': result['answers'],
            'results': result['results'],
            'date': result['date']
        }), status=200, mimetype='application/json', headers={
            "Access-Control-Allow-Origin": "*"
        })

    return Response(status=404, headers={
        "Access-Control-Allow-Origin": "*"
    })
#############################################


################## SOCKETS ##################

# Generate access_token from the spotify authentication token
@socketio.on('generate_access_token')
def check_token(data):
    access_token, refresh_token = generate_access_token(data['code'])
    socketio.emit("access_token", {'access_token': access_token, 'refresh_token': refresh_token, 'sid': data['sid']},
                  to=data['sid'])

@socketio.on('generate-sid')
def generate_sid():
    print("Generating SID", str(request.sid))
    socketio.emit("generate_sid", {'sid': request.sid}, to=request.sid)

# Checks if room exists with specific code
@socketio.on('isRoom')
def isRoom(data):
    global ROOMS
    for Room in ROOMS:
        if Room.code == data['code']:
            socketio.emit('isRoom', {'isRoom': 'true'}, to=request.sid)
            return

    socketio.emit('isRoom', {'isRoom': 'false'}, to=request.sid)
    return

# When the user makes a guess on the client side, it emits a websocket that is recieved here, and the logic is handled.


@socketio.on('player_guess')
def player_guess(data):
    sid = data['sid']
    player_guess = data['guess']
    code = data['code']

    global ROOMS
    for Room in ROOMS:
        if Room.code == code:
            current_question = Room.current_question
            for player in Room.players:
                if player.sid == sid:
                    for guess in player.guesses:
                        # if guess exist -> update
                        if guess['question'] == current_question:
                            guess['guess'] = player_guess
                            return
                    # if no quess exist -> add
                    player.guesses.append({
                        'question': current_question,
                        'guess': player_guess,
                        'correct_answer': Room.answers[current_question]['player'],
                        'info': Room.answers[current_question]['info']
                    })
                    Room.players_guessed.append(sid)

                    # send to room total guesses amount
                    socketio.emit('nr_of_players_guessed', {
                        'players': Room.players_guessed
                    }, room=code)
                    return

# Here are the scores calculated, for each right answer you get 10 points.


def compile_results(code):
    global ROOMS
    for Room in ROOMS:
        if Room.code == code:
            Room.ended = True
            for player in Room.players:
                for guess in player.guesses:
                    if guess['guess'] == guess['correct_answer']:
                        player.points += 10

            players = []

            for player in Room.players:
                players.append({
                    'id': player.id,
                    'host': player.host,
                    'name': player.name,
                    'points': player.points,
                    'color': player.color,
                    'guesses': player.guesses,
                    'sid': player.sid
                })
                # Adds the result to the database.
            db.table('Rooms').insert({
                "code": code,
                "questions": Room.questions,
                "answers": Room.answers,
                "results": Room.results,
                "started": Room.started,
                "ended": Room.ended,
                "players": players,
                "date": str(time.time()),
            })

            return
    return

# Handles the backend logic when a user enters a room.


@socketio.on('connect_to_room')
def connect_to_room(data):
    code = data['code']
    sid = data['sid']
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    reconnecting = False

    global ROOMS
    for Room in ROOMS:
        if Room.code == code:

            # Initializing variables
            settings = Room.settings[0]
            player_in_room = False
            started = False
            access = False
            status = ''
            current_question = 0

            # Checking access and status of room
            if Room.started == False:
                status = 'lobby'
                access = True

                for player in Room.players:
                    if player.sid == sid:  # player is reconnecting to lobby
                        reconnecting = True
                        print(f"[{code}]{player.name} reconnecting")

                if not reconnecting:
                    # sending get request and saving the response as response object
                    r2 = requests.get(url="https://api.spotify.com/v1/me",
                                      headers={"Authorization": "Bearer " + access_token})

                    # extracting data in json format
                    data = r2.json()

                    # Create player object
                    new_player = Player()
                    new_player.name = str(data['display_name'])
                    new_player.id = str(data['id'])
                    new_player.points = 0
                    new_player.access_token = access_token
                    new_player.refresh_token = refresh_token
                    new_player.sid = sid
                    new_player.color = getColor()

                    # If the room is empty, make the user host
                    if len(Room.players) == 0:
                        new_player.host = True
                        print(f"[{code}] Making {new_player.name} host")

                    # Add the player to the Room
                    Room.players.append(new_player)

                # always add the new sid of the player to the websocket room
                join_room(code)
            elif Room.started == True and Room.ended == False:
                status = 'playing'
                current_question = Room.current_question
                for player in Room.players:
                    if player.sid == sid:
                        access = True
                join_room(code)
            else:
                status = 'ended'
                access = True

            # Send the connection variables to the person
            socketio.emit("connectToRoom", {
                'status': status,
                'access': access,
                'question': current_question,
                'settings': settings,
                'answers': Room.answers,  # also defines total number of questions
                'questionTimeStarted': Room.questionTimeStarted,
                'players_guessed': Room.players_guessed
            }, to=request.sid)

            # Send a updated list of the current players in the room
            send_list_of_players(code)
            return
    status = 'NaR'
    socketio.emit("connectToRoom", {
        'status': status,
        'access': None,
        'question': None,
        'settings': None,
        'answers': None
    }, to=request.sid)
    return

# Creates a list of all players in a room and sends it to the client.


def send_list_of_players(code):
    global ROOMS
    list_of_players = []
    for Room in ROOMS:
        if Room.code == code:
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
            break

    socketio.emit("update_list_of_players", {
        'players': list_of_players,
    }, room=code)

@socketio.on('update_name')
def update_player_name(data):
    sid = data['sid']
    code = data['code']
    name = data['name']

    print("UPDATE PLAYER NAME")
    
    for Room in ROOMS:
        if Room.code == code:
            list_of_players = []
            for player in Room.players:
                if player.sid == sid:
                    player.name = name
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
            break                
    socketio.emit("update_list_of_players", {
        'players': list_of_players,
    }, room=code)



# When the host proceeds to the next question on the frontend, it sends a websocket that is recieved here.


@socketio.on('next_question')
def next_question(data):
    code = data['code']  # Specifying the room code.

    global ROOMS
    for Room in ROOMS:
        if code == Room.code:
            Room.guesses = 0
            Room.current_question += 1
            current_question = Room.current_question
            Room.players_guessed = []
            # answer is track id in this case
            if current_question == len(Room.answers) and len(Room.answers) != 0:

                print(f"[{code}] Sending: Game is over, loading...")
                socketio.emit('game_ended', room=code)

                print(f"[{code}] Compiling results")
                #compile_results(code)
                
                thread = threading.Thread(target=compile_results, args=(code,))
                thread.start()
                thread.join()

                print(f"[{code}] Sending: Go to results")
                socketio.emit("connectToRoom", {
                    'status': 'ended',
                    'access': None,
                    'question': None,
                    'settings': None,
                    'answers': None
                }, room=code)
                return
            else:
                Room.questionTimeStarted = str(int(time.time()))
                socketio.emit('next_question', {
                    'answer': Room.answers[current_question]['player'],
                    'current_question': current_question,
                    'trackid': Room.answers[current_question]['info'],
                    'questionTimeStarted':  Room.questionTimeStarted
                }, room=code)
                return

# Used to start the game. Sends out a socket to all players in the room that the game is starting.


@socketio.on('start_game')
def start_game(data):
    code = data['code']
    num_of_players = 0

    # Get the room
    global ROOMS
    for Room in ROOMS:
        if Room.code == code:
            num_of_players = len(Room.players)
            nr_of_questions = len(Room.answers)
            Room.started = True
            random.shuffle(Room.answers)
            socketio.emit(
                'start_game', {'nr_of_questions': nr_of_questions}, room=code)
            Room.questionTimeStarted = time.time()
            print(f"[{code}] Game has started!")
            print(f"[{code}] Number of players: {num_of_players}")
            return


@socketio.on('toptrack')
def get_top_track(data):
    trackid = []
    trackid.append(data['trackid'])
    code = data['room']
    sid = data['sid']

    global ROOMS
    # Go thorugh each room and find the one sending the 'toptrack' emit
    for Room in ROOMS:
        if code == Room.code:
            # Make sure to not add songs again on reconnect
            reconnecting = False
            for answer in Room.answers:
                if answer['player'] == sid:
                    reconnecting = True

            if not reconnecting:
                print(f"[{code}] Adding top song(s) for {sid}")
                for x in range(len(trackid[0])):
                    Room.answers.append({
                        'player': sid,
                        'info': trackid[0][x],
                    })

# Deleting and closing the room on host close room


def close_socket_room(code):
    for Room in ROOMS:
        if Room.code == code:
            ROOMS.remove(Room)
            socketio.emit("room_closed_by_host", room=Room.code)

            close_room(code)
            print(f"[Server] Deleting room {code}")

# Removes a player from the Room object if the player decides to leave the room
# Also sends a updated list of all players to the users in the room.


@socketio.on('leave_room')
def remove_player_from_room(data):
    code = data['code']
    sid = data['sid']

    global ROOMS
    for Room in ROOMS:
        if Room.code == code:
            for player in Room.players:
                if player.sid == sid:
                    print(f"[{code}] {player.name} disconnected!")

                    # Remove the player from the list of players for that room
                    Room.players.remove(player)

                    # Remove the player from the websocket room
                    if player.host == True or len(Room.players) == 0:
                        close_socket_room(code)
                        return
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

                    socketio.emit("update_list_of_players", {
                                  'players': list_of_players}, room=code)
                    return

# Creating a Room object to store all room information in and sends the code of the room to the host client requesting
# to create the room


@socketio.on('createRoom')
def createRoom(data):
    sid = data['sid']
    time_range = data['time_range']
    no_songs = data['no_songs']
    # Generate a random room code, 4 letters
    code = generateId()

    # Get the global variable (think of the scope?)
    global ROOMS

    reconnecting = False
    for _Room in ROOMS:
        for player in _Room.players:
            if player.sid == sid and player.host == True and _Room.ended == False:
                code = _Room.code
                reconnecting = True
                print(
                    f"[Server] User {player.name} already has an active room: {code}. Rejoining.")

    if not reconnecting:
        ROOMS.append(Room(code))
        print(f"[Server] Creating room: {code}")

    for _Room in ROOMS:
        if _Room.code == code:
            _Room.settings.append([time_range, no_songs])

    socketio.emit('roomCode', {'code': code}, to=request.sid)

# Called from /playlist route on frontend. Generates a new playlist with tracks chosen by the user.


@socketio.on('createPlaylist')
def createPlaylist(data):
    # create playlist on users account
    req = requests.post(
        url=f"https://api.spotify.com/v1/users/{data['user_id']}/playlists",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {data['access_token']}"
        },
        json={
            "name": f"{data['name']}"
        })
    # Store the new playlist ID that gets created by request above
    playlist_id = req.json()['id']
    trackList = ""

    # Collect tracks which user wants to save. Format them into a string which Spotify API will accept.
    for i in data['tracksForPlaylist']:
        trackList = trackList + "spotify:track:" + i + ","

    trackList = trackList[:-1]

    # Add tracks to the new playlist and emit to the client
    req2 = requests.post(
        url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={trackList}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {data['access_token']}"
        })
    print("playlist created")
    socketio.emit('playlistCreated', to=request.sid)

# Add tracks to existing playlist


@socketio.on('addToPlaylist')
def addToPlaylist(data):
    # playlist ID user wants to add the tracks to.
    playlist_id = data['playlist_id']
    trackList = ""
    # format (same as function above)
    for i in data['tracksForPlaylist']:
        trackList = trackList + "spotify:track:" + i + ","

    trackList = trackList[:-1]

    # add tracks and emit to client
    req = requests.post(
        url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={trackList}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {data['access_token']}"
        })
    print("playlist created")
    socketio.emit('playlistCreated', to=request.sid)
#############################################

################## Regular functions ##################

# Generates a access_token based on the token from the spotify authentication logincallback


def generate_access_token(code):
    global CLIENT_ID
    global CLIENT_SECRET

    scope = "streaming app-remote-control user-read-currently-playing user-read-playback-state user-modify-playback-state user-read-email user-read-private"

    if ENV == 'production' or ENV == 'prod':
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "scope": scope,
            "redirect_uri": "https://soundcheck.fdrive.se/logincallback",
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    else:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "scope": scope,
            "redirect_uri": "http://localhost:8080/logincallback",
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

    req = requests.post(
        url="https://accounts.spotify.com/api/token",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data=data
    )

    if req.status_code == 400:
        print("Error")
    else:
        response = req.json()
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        return access_token, refresh_token

# Generates a color for a player


def getColor():
    global COLORS
    global COLOR_COUNTER

    color = COLORS[COLOR_COUNTER]
    COLOR_COUNTER += 1

    if (COLOR_COUNTER == len(COLORS) - 1):
        COLOR_COUNTER = 0

    return color

# Generates a random room code and checks that the code is unique


def generateId():
    letters = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    code = ""
    for i in range(4):
        code += letters[random.randint(0, 31)]

    # Check for bad words and make sure the room doesn't already exist
    if code in ['NGGR', 'NIGR', 'FACK', 'FUCK', 'SHIT', 'CUNT', 'DICK', 'NSFW', 'BICH', 'HORE', 'HORA', 'KUKA', '6969', '6666', '8008', 'BOOB', 'DWRF', 'MILF', 'WEED']:
        code = generateId()

    table_Rooms = db.table("Rooms")
    result = table_Rooms.search(where('code') == code)
    if result:
        print(f"[Server] Room code {code} in use, creating new")
        code = generateId()

    return code


# Run the server in either dev or prod
if __name__ == '__main__':
    if ENV == 'production' or 'prod':
        socketio.run(app, host='0.0.0.0', port=5001)
    else:
        socketio.run(app)
