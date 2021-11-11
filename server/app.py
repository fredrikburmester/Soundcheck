# ---------
# This file contains API endpoints, sockets that handle communication with frontend, and database logic
# ---------

import os
from flask import Flask
from flask_socketio import join_room, leave_room, close_room
from flask_socketio import SocketIO
from flask import request, jsonify, Response
from flask_cors import CORS
import time
import logging
import threading
import json
import random
import requests
import base64
import sys

# Database
from tinydb import TinyDB, Query, where
from datetime import date
from database import db_helper

# Variables
from variables import CLIENT_SECRET, CLIENT_ID, ENV

db = TinyDB('db.json')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
log = logging.getLogger('werkzeug')
log.disabled = True

# Allow cross origin to be able to do websockets from different servers
# socketio = SocketIO(app)
if ENV == 'production' or ENV == 'prod':
    print("Running production mode")
    socketio = SocketIO(app, path="/ws", cors_allowed_origins='*')
else:
    print("Running development mode")
    socketio = SocketIO(app, cors_allowed_origins='*')

################## API Endpoints ##################

# Personal results endpoint. Searches DB for any rooms containing the user and returns game statistics.
@app.route('/api/me/<username>/results', methods=['GET'])
def personal_results(username):
    
    table_Rooms = db.table("Rooms")
    Room = Query()
    Player = Query()
    result = table_Rooms.search(Room.players.any(Player.id == username))
    if result and len(result) > 0:
        return Response(json.dumps({
            'results': result,
        }), status=200, mimetype='application/json', headers={
            "Access-Control-Allow-Origin": "*"
        })

    return Response(status=401, headers={
        "Access-Control-Allow-Origin": "*"
    })

# Room results endpoint. Searches DB for room that matches code, and returns game statistics.

@app.route('/api/<code>/results', methods=['GET'])
def results(code):
    
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

@socketio.on('generate_sid')
def generate_sid(data):
    print(f"[Clent Reload - {data['path']}] Updating SID: {str(request.sid)}")
    socketio.emit("generate_sid", {'sid': request.sid}, to=request.sid)

# Checks if room exists with specific code
@socketio.on('isRoom')
def isRoom(data):
    
    for Room in db_helper.ROOMS:
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
    
    for Room in db_helper.ROOMS:
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

def guesses_per_player(sid, code):
    for Room in db_helper.ROOMS:
        if Room.code == code:
            for player in Room.players:
                if player.sid == sid:
                    guesses_per_player = {}
                    for guess in player.guesses:
                        if guess['guess'] not in guesses_per_player:
                            guesses_per_player[guess['guess']] = 1
                        else:
                            guesses_per_player[guess['guess']] += 1
                    return guesses_per_player

# Here are the scores calculated, for each right answer you get 10 points.
def compile_results(code):
    for Room in db_helper.ROOMS:
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

@socketio.on("send_message")
def send_message(data):
    code = data['code']
    id = data['id']
    message = data['message']

    socketio.emit("recieve_message", {
        'text': message, 'id': id
    }, to=code)

# Handles the backend logic when a user enters a room.
@socketio.on('connect_to_room')
def connect_to_room(data):
    code = data['code']
    sid = data['sid']
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    reconnecting = False
    
    for Room in db_helper.ROOMS:
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

                # sending get request and saving the response as response object
                r2 = requests.get(url="https://api.spotify.com/v1/me",
                                    headers={"Authorization": "Bearer " + access_token})

                # extracting data in json format
                data = r2.json()

                for player in Room.players:
                    if player.sid == request.sid or player.id == str(data['id']):  # player is reconnecting to lobby
                        reconnecting = True
                        
                        print(f"[{code}] {player.name} reconnecting")

                        # Kick other instance of player
                        if player.sid != sid:
                            socketio.emit("connectToRoom", {
                                'status': 'playing',
                                'access': None,
                                'question': None,
                                'settings': None,
                                'answers': None,
                                'error': "You connected from another device!"
                            }, to=player.sid)
                        
                        db_helper.update_player_sid(player.sid, request.sid, code)
                        break

                if not reconnecting:
                    # Create player object
                    new_player = db_helper.Player()
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
                'players_guessed': Room.players_guessed,
                'new_sid': request.sid
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
    list_of_players = db_helper.get_list_of_players(code)
    socketio.emit("update_list_of_players", {
        'players': list_of_players,
    }, room=code)

@socketio.on('update_name')
def update_player_name(data):
    sid, code, name = data['sid'], data['code'], data['name']
    list_of_players = db_helper.update_player_name(sid, code, name)            
    socketio.emit("update_list_of_players", {
        'players': list_of_players,
    }, room=code)

# When the host proceeds to the next question on the frontend, it sends a websocket that is recieved here.
@socketio.on('next_question')
def next_question(data):
    code = data['code']  # Specifying the room code.

    for Room in db_helper.ROOMS:
        if code == Room.code:
            Room.guesses = 0
            Room.current_question += 1
            current_question = Room.current_question
            Room.players_guessed = []
            # answer is track id in this case
            if current_question == len(Room.answers) and len(Room.answers) != 0:

                print(f"[{code}] Game has ended.")
                socketio.emit('game_ended', room=code)

                print(f"[{code}] Compiling results...")
                #compile_results(code)
                
                thread = threading.Thread(target=compile_results, args=(code,))
                thread.start()
                thread.join()

                print(f"[{code}] Redirecting users to results...")
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
    
    for Room in db_helper.ROOMS:
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
    trackid = data['trackid']
    code = data['room']
    userid = data['userid']
    db_helper.set_top_track(trackid, code, userid)

# Deleting and closing the room on host close room
def close_socket_room(code):
    db_helper.close_room(code)
    
    socketio.emit("room_closed_by_host", room=code)

    # Close socket connection
    close_room(code)
    print(f"[Server] Closing room {code}")

# Removes a player from the Room object if the player decides to leave the room
# Also sends a updated list of all players to the users in the room.
@socketio.on('leave_room')
def remove_player_from_room(data):
    code = data['code']
    sid = data['sid']
    
    for Room in db_helper.ROOMS:
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

                    break

            # Update answers for player songs
            Room.answers = [answer for answer in Room.answers if not answer['player'] == sid]

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
    id = data['id']
    time_range = data['time_range']
    no_songs = data['no_songs']
    show_correct_answers = data['show_correct_answers']

    # Generate a random room code, 4 letters
    code = generateId()

    reconnecting = False
    for _Room in db_helper.ROOMS:
        for player in _Room.players:
            if player.id == id and player.host == True and _Room.ended == False:
                code = _Room.code
                reconnecting = True
                print(f"[Server] Host {player.name} already has an active room: {code}. Rejoining as host.")

    if not reconnecting:
        db_helper.ROOMS.append(db_helper.Room(code))
        print(f"[Server] Player: {sid} created room: {code}")

        for _Room in db_helper.ROOMS:
            if _Room.code == code:
                _Room.settings.append([time_range, no_songs, show_correct_answers])

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
    socketio.emit('playlistCreated', to=request.sid)

@socketio.on('clearPlayerData')
def clearPlayerData(data):
    clear_player_data(data['id'])

#######################################################

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
            "redirect_uri": "https://soundcheckgame.com/logincallback",
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
    color = db_helper.COLORS[db_helper.COLOR_COUNTER]
    db_helper.COLOR_COUNTER += 1

    if (db_helper.COLOR_COUNTER == len(db_helper.COLORS) - 1):
        db_helper.COLOR_COUNTER = 0

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

def clear_player_data(id):
    for room in db.table("Rooms"):
        code = room['code']
        players = room['players']
        for player in players:
            if player['id'] == id:
                player['id'] = '[deleted]'
                player['name'] = '[deleted]'
            
            for guesses in player['guesses']:
                if guesses['id'] == id:
                    guesses['id'] = '[deleted]'

        db.table("Rooms").update({'players': players}, Query().code == code)

# Run the server in either dev or prod
if __name__ == '__main__':
    if ENV == 'production' or 'prod':
        socketio.run(app, host='0.0.0.0', port=5001)
    else:
        socketio.run(app)
