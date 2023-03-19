from flask import Flask
from flask import jsonify, request #json serializer
from flask_cors import CORS
import pymysql
import random


# AI Difficulties
#EASY = 3
#MEDIUM = 5
#HARD = 7

class ServerGame:
  def __init__(self, gameType, game):
    self.type = gameType
    self.game = game

app = Flask(__name__)
CORS(app)

conn = pymysql.connect(
    host= 'reversi-db.co96znypdwjk.us-east-2.rds.amazonaws.com', 
    port = 3306,
    user = 'admin', 
    password = 'e5YVS9D11OBvShYwu8gA',
    db = 'reversidb',       
)

games = {}

@app.route("/")
def root_Web():
    # here returns the home page of the front end with possible options to login
    return "<p>Test</p>"

@app.route('/login', methods=['POST'])
def login():
    requestBody = request.json
    username = requestBody['username']
    password = requestBody['password']

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    rv = cursor.fetchall()
    conn.commit()
    cursor.close()

    if (len(rv) == 0):
        return jsonify({
            'userID': None,
            'username': None,
            'password': None,
        })

    return jsonify({
        'userID': rv[0][0],
        'username': rv[0][1],
        'password': rv[0][2],
    })

@app.route('/signup', methods=['PUT'])
def signup():
    requestBody = request.json
    username = requestBody['username']
    password = requestBody['password']
    newId = uuid.uuid1().int

    cursor = conn.cursor()
    cursor.execute('INSERT INTO users VALUES (%d, %s, %s)', (newId, username, password))
    rv = cursor.fetchall()
    conn.commit()
    cursor.close()

    if (len(rv) == 0):
        return jsonify({
            'userID': None,
            'username': None,
            'password': None,
        })

    return jsonify({
        'userID': rv[0][0],
        'username': rv[0][1],
        'password': rv[0][2],
    })

@app.route("/make_move")
def make_move(game_ID, x_pos, y_pos, current_player):
        # check if valid move first if not valid return invalid move (is_move_possible)
        # make_move(x, y)
    return jsonify(gameid = '2354', board='newBoardObject', score1 = 'player1', score2 = 'player2', status='Move Executed/Move OutOfBound')
        
@app.route("/possible_moves")
def possible_moves(game_ID):
    requestBody = request.data
    game_ID = requestBody.game_ID
    for id in games.values():
        if id == game_ID:
            turn = games[id].cur_player.value
            score1 = games[id].player1_score
            score2 = games[id].player2_score
            possibleMovesBoard = games[id].possible_moves()
        # check array games for game_ID
        # check with model possible moves possible_moves(self)
        # make JSON for front end
        # check for possible moves and return JSON of possible moves so the front end can display all possible moves by player highlighted
    return jsonify(gameid = '234', possibleMovesBoard = 'possibleMovesBoard', turn = 'cur_player')

@app.route("/game_state")# this will serve as a function to look for games
def game_state(game_ID):
    requestBody = request.data
    game_ID = requestBody.game_ID
    for id in games.values():
        if id == game_ID:
            turn = games[id].cur_player.value
            score1 = games[id].player1_score
            score2 = games[id].player2_score
            

    return jsonify(gameid = '2354', turn = 'cur_player', score1 = 'player1', score2 = 'player2', status = '0 = awaiting player/ 1-2 = players turn')

@app.route("/create_game", methods=['PUT'])# do we create games with one player and put them on a lobby for others to join, or do we create the games with the two usernames
def create_game(player1, player2, size, gameType, difficulty):
    requestBody = request.data
    player1 = requestBody.player1
    player2 = requestBody.player2
    size = requestBody.size
    gameType = requestBody.gameType
    difficulty = requestBody.difficulty

    if gameType == 'ai':
        ai_depth = difficulty
    else:
        ai_depth = 0
    # id = i
    # games = {"id": id, "gameType": gameType, "game": Reversi()}
    #games[] = Reversi(size, difficulty)
    return jsonify(gameid = '2354', size = '8', status = '0 = awaiting player/ 1-2 = players turn')

@app.route("/join_game")
def join_game(game_ID, player_joining):
    requestBody = request.data
    game_ID = requestBody.game_ID
    player_joining = requestBody.player_joining
    for id in games.values():
        if id == game_ID:
            turn = games[id].cur_player.value
            score1 = games[id].player1_score
            score2 = games[id].player2_score

# join player to game_ID and send empty board to start, also return starting player
    return jsonify(gameid = '2354', board='board array', status = '0 = awaiting player/ 1-2 = players turn')

@app.route("/postgame")
def postgame(gameID):
    return jsonify(gameID = '3542', score1 = 'player1', score2 = 'player2',)

@app.route("/heartbeat")
def heartbeat():
    return jsonify(ping= 'PONG!')

