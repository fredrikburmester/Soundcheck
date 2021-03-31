import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')

app = Flask(__name__)

# DATABASE #
class Player:
  def __init__(self, name, id):
    self.host = False
    self.name = name # Name of player
    self.id = id # Spotify username
    self.points = 0

ROOM_ID = ''
PLAYERS = []

############

@app.route('/')
def hello_world():
    return CLIENT_SECRET

def create_room():
    # create room with id
    # creates a new Player object -> assign creator as host and add to array
    pass

def add_player_to_room():
    # creates a new Player object and add it to the array ? 
    pass

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
    app.run()