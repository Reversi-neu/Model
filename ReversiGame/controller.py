from flask import Flask
# from model import ReversiBoard
# import model
from model.game import Reversi
#from controller.eloCalculator import eloCalculator
# from ReversiGame.model import Reversi
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import pymysql
import uuid
import copy
from db import DB

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

db = DB()

# -- helpers / future routes

def getNextUserID():
    rv = db.callDB('SELECT MAX(userID) FROM users', ())

    if (len(rv) == 0):
        return 1

    return rv[0][0] + 1

def getNextGameID():
    rv = db.callDB('SELECT MAX(gameID) FROM games', ())

    if (len(rv) == 0):
        return 1

    return rv[0][0] + 1

# -- global constants
default_elo = 1000
games = []
game_id_counter : int = getNextGameID()

# -- routes
@app.route('/user/<userID>', methods=['GET'])
def getUserByID(userID):
    userID = int(userID)
    if (userID == 0): # AI
        return {
            'userID': 0,
            'username': None,
            'password': None,
        }

    statement = 'SELECT * FROM users WHERE userID = %s'
    rv = db.callDB(statement, (userID))

    if (len(rv) == 0):
        return None

    return {
        'userID': rv[0][0],
        'username': rv[0][1],
        'password': rv[0][2],
    }

@app.route('/login', methods=['POST'])
def login():
    requestBody = request.json
    username = requestBody['username']
    password = requestBody['password']

    rv = db.callDB('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))

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
    newId = getNextUserID()
    date = datetime.datetime.now()

    db.callDB('INSERT INTO users VALUES (%s, %s, %s, %s)', (newId, username, password, date))
    db.callDB('INSERT INTO elo VALUES (%s, %s, %s)', (newId, default_elo, date))
    rv = db.callDB('SELECT * FROM users WHERE userID = %s', (newId))

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

@app.route('/guest', methods=['PUT'])
def guest():
    newId = getNextUserID()
    date = datetime.datetime.now()

    db.callDB('INSERT INTO users VALUES (%s, %s, %s, %s)', (newId, None, None, date))
    db.callDB('INSERT INTO elo VALUES (%s, %s, %s)', (newId, default_elo, date))
    rv = db.callDB('SELECT * FROM users WHERE userID = %s', (newId))

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

@app.route('/games/<gameType>/<userID>', methods=['GET'])
def getGamesByTypeByUserID(gameType, userID):
    playerGames = copy.deepcopy(list(
        filter(lambda game: (game['player1']['userID'] == int(userID) or game['player2']['userID'] == int(userID)) 
                and game['type'] == gameType, games)
    ))
    # need to pop game off here bc its not json serializable
    for game in playerGames:
        game.pop('game')

    return jsonify(playerGames)

@app.route('/games/<gameID>', methods=['GET'])
def getGameByID(gameID):
    game = copy.deepcopy(list(filter(lambda game: game['id'] == int(gameID), games))[0])
    game.pop('game')
    return jsonify(game)

@app.route('/games', methods=['POST'])
def moveRoute():
    requestBody = request.json
    gameType = requestBody['gameType']
    gameID = requestBody['gameID']
    move = requestBody['move']

    return makeMove(gameType, gameID, move)

@app.route("/games", methods=['PUT'])# do we create games with one player and put them on a lobby for others to join, or do we create the games with the two usernames
def createGame():
    global game_id_counter
    requestBody = request.json
    player1ID = requestBody['player1ID']
    player2ID = requestBody['player2ID']
    size = requestBody['size']
    gameType = requestBody['gameType']
    difficulty = requestBody['difficulty'] or 0
    newId = game_id_counter
    game_id_counter += 1
    # date = datetime.datetime.now()

    reversiBoard = Reversi(size, ai_depth = difficulty) if gameType == 'ai' else Reversi(size, ai_depth=0)

    # this is basically where we define what our 'games' dicts are gonna look like (THIS IS ALL THE STUFF I WANT FOR THE FRONT END, IT GOTTA BE UPDATED W/ THE GAME)
    game = {
        "id": newId, 
        "game": reversiBoard, 
        "board": reversiBoard.board.get_grid(),
        "type": gameType, 
        "size": size, 
        "difficulty": difficulty,
        "player1": getUserByID(player1ID), 
        "player2": getUserByID(player2ID), 
        "winner": None, 
        "player1Score": 2, 
        "player2Score": 2, 
        "currentPlayer": 1, 
        "possibleMoves": reversiBoard.possible_moves(),
        "active": True
    }
    games.append(game)
    
    g_copy = copy.deepcopy(game)
    g_copy.pop('game')
    return jsonify(g_copy)

def makeMove(gameType, gameID, move):
    game = list(filter(lambda game: game['id'] == int(gameID), games))[0]
    game['game'].make_move([move["x"], move["y"]])

    # this logic is not good, maybe... either the bot is goated and i suck, or its cheating and i cant tell
    game['game'].change_cur_player()
    possibleMoves = game['game'].possible_moves()
    if (len(possibleMoves) == 0):
        game['game'].change_cur_player()
    elif (gameType == 'ai'):
        while True:
            game['game'].make_move(game['game'].get_ai_move())
            game['game'].change_cur_player()
            possibleMoves = game['game'].possible_moves()
            if game['game'].check_win(): break
            if (len(possibleMoves) == 0):
                game['game'].change_cur_player()
            else:
                break
    
    game['winner'] = game['game'].check_win()
    if (game['winner']):
        postgame(int(gameID))
        #set game inactive
        game["active"] = False

    game['player1Score'] = game['game'].player1_score
    game['player2Score'] = game['game'].player2_score
    game['board'] = game['game'].board.get_grid()
    game['currentPlayer'] = game['game'].cur_player
    game['possibleMoves'] = game['game'].possible_moves()

    game_copy = copy.deepcopy(game)
    game_copy.pop('game')
    return jsonify(game_copy)

def postgame(gameID):
    game = list(filter(lambda game: game['id'] == gameID, games))[0]
    print(game)
    player1ID = game['player1']['userID']
    player2ID = game['player2']['userID']
    player1Score = game['player1Score']
    player2Score = game['player2Score']
    difficulty = game['difficulty']
    finishTime = datetime.datetime.now()
    
    if game['player1Score'] > game['player2Score']:
        winnerID = player1ID
    elif game['player1Score'] < game['player2Score']:
        winnerID = player2ID
    # elif game['player1Score'].userID == game['player2Score'].userID:
    #     winnerID = None
    else: 
        winnerID = None
    
    statement = 'INSERT INTO games VALUES (%s, %s, %s, %s, %s, %s, %s)'
    data = (gameID, player1ID, player2ID, winnerID, player1Score, player2Score, finishTime)
    db.callDB(statement, data)

    gameType = game['type']
    if gameType == 'online':
        ##update elo
        #eloCalculator(player_elo, enemy_elo, player_score, enemy_score)

        statement = 'SELECT elo FROM elo WHERE userID = %s'
        player1Old = db.callDB(statement, (player1ID))[0][0]
        statement = 'SELECT elo FROM elo WHERE us, mmkl,erID = %s'
        player2Old = db.callDB(statement, (player2ID))[0][0]

        #player1
        player1New = eloCalculator(player1Old, player2Old, player1Score, player2Score)
        statement = 'UPDATE elo SET elo = %s, lastUpdate=%s WHERE userID = %s'
        data = (player1New, finishTime, player1ID)
        db.callDB(statement, data)

        #player2
        player2New = eloCalculator(player2Old, player1Old, player2Score, player1Score)
        statement = 'UPDATE elo SET elo = %s, lastUpdate=%s WHERE userID = %s'
        data = (player2New, finishTime, player2ID)
        db.callDB(statement, data)

    elif gameType == 'ai':
        
        statement = 'SELECT elo FROM elo WHERE userID = %s'
        player1Old = db.callDB(statement, (player1ID))[0][0]
        statement = 'SELECT elo FROM elo WHERE userID = %s'
        if difficulty == 1: aiID = -1
        if difficulty == 2: aiID = -2
        if difficulty == 3: aiID = -3
        if difficulty == 4: aiID = -4
        player2Old = db.callDB(statement, (aiID))[0][0]

        #player1
        player1New = eloCalculator(player1Old, player2Old, player1Score, player2Score)
        statement = 'UPDATE elo SET elo = %s, lastUpdate=%s WHERE userID = %s'
        data = (player1New, finishTime, player1ID)
        db.callDB(statement, data)

        #player2
        player2New = eloCalculator(player2Old, player1Old, player2Score, player1Score)
        statement = 'UPDATE elo SET elo = %s, lastUpdate=%s WHERE userID = %s'
        data = (player2New, finishTime, aiID)
        db.callDB(statement, data)

def eloCalculator(player_elo, enemy_elo, player_score, enemy_score):
    # Variables to customize elo gains and loses
    diff = 400
    change = 32
    
    expected_score = 1/(1 + (10 ** ((enemy_elo - player_elo) / diff)))

    if player_score > enemy_score:
        game_outcome = 1
    else:
        game_outcome = 0
        
    return int(player_elo + (change * (game_outcome - expected_score)))

#  -------- SOCKET STUFF --------
@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect",{"data":f"id: {request.sid} is connected"})

@socketio.on('makeMove')
def handleSocketMove(data):
    """event listener when client types a message"""
    # print("data from the front end: ",jsonify(data), data)

    gameData = makeMove(data['gameType'],data["gameID"],data["move"])

    emit("makeMove",{},broadcast=True)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)

# running the server
socketio.run(app)