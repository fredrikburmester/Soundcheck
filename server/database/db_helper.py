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

def update_player_sid(old_sid, new_sid, code): 
    for Room in ROOMS:
        if code == Room.code:
            for player in Room.players:
                if player.sid == old_sid:
                    player.sid = new_sid
                    break
            for answer in Room.answers:
                if answer['player'] == old_sid:
                    answer['player'] = new_sid
                    break
            break
    return

def get_list_of_players(code):
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
                    'host': player.host,
                })
            break
    return list_of_players

def update_player_name(sid, code, name):
    if len(name) < 2 or len(name) > 20:
        return

    print(f"[{code}] {sid} updated name to: {name}")
    
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
    return list_of_players

def get_user_by_sid(sid):
    for Room in ROOMS:
        for player in Room.players:
            if player.sid == sid:
                return player.name
    return None

def set_top_track(trackid, code, sid):
    trackids = []
    trackids.append(trackid)

    for Room in ROOMS:
        if code == Room.code:
            # Make sure to not add songs again on reconnect
            reconnecting = False
            for answer in Room.answers:
                if answer['player'] == sid:
                    reconnecting = True

            if not reconnecting:
                user = get_user_by_sid(sid)
                print(f"[{code}] Adding top song(s) for {user}")
                for x in range(len(trackids[0])):
                    Room.answers.append({
                        'player': sid,
                        'info': trackids[0][x],
                    })
            return

def close_room(code):
    for Room in ROOMS:
            if Room.code == code:
                ROOMS.remove(Room)
                return