from flask import Flask
# from model import ReversiBoard
# import model
from model.game import Reversi
# from ReversiGame.model import Reversi
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import uuid
import copy

app = Flask(__name__)
CORS(app)

conn = pymysql.connect(
    host= 'reversi-db.co96znypdwjk.us-east-2.rds.amazonaws.com', 
    port = 3306,
    user = 'admin', 
    password = 'e5YVS9D11OBvShYwu8gA',
    db = 'reversidb',       
)

default_elo = 1000
games = []
game_id_counter : int = 0

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
    newId = getNextUserID()
    date = datetime.datetime.now()

    cursor = conn.cursor()
    cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s)', (newId, username, password, date))
    cursor.execute('INSERT INTO elo VALUES (%s, %s, %s)', (newId, default_elo, date))
    # need this stupid select call for the fetch to return something
    cursor.execute('SELECT * FROM users WHERE userID = %s', (newId))
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

@app.route('/guest', methods=['PUT'])
def guest():
    newId = getNextUserID()
    date = datetime.datetime.now()

    cursor = conn.cursor()
    cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s)', (newId, None, None, date))
    cursor.execute('INSERT INTO elo VALUES (%s, %s, %s)', (newId, default_elo, date))
    # need this stupid select call for the fetch to return something
    cursor.execute('SELECT * FROM users WHERE userID = %s', (newId))
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
def makeMove():
    requestBody = request.json
    gameType = requestBody['gameType']
    gameID = requestBody['gameID']
    move = requestBody['move']

    if (gameType == 'ai') or (gameType == 'local'):
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
                if (len(possibleMoves) == 0):
                    game['game'].change_cur_player()
                else:
                    break

        game['winner'] = game['game'].check_win()
        game['player1Score'] = game['game'].player1_score
        game['player2Score'] = game['game'].player2_score
        game['board'] = game['game'].board.get_grid()
        game['currentPlayer'] = game['game'].cur_player
        game['possibleMoves'] = game['game'].possible_moves()

        game_copy = copy.deepcopy(game)
        game_copy.pop('game')
        return jsonify(game_copy)

@app.route("/games", methods=['PUT'])# do we create games with one player and put them on a lobby for others to join, or do we create the games with the two usernames
def createGame():
    global game_id_counter
    requestBody = request.json
    player1ID = requestBody['player1ID']
    player2ID = requestBody['player2ID']
    size = requestBody['size']
    gameType = requestBody['gameType']
    difficulty = requestBody['difficulty'] or 0
    newId = copy.copy(game_id_counter)
    game_id_counter = game_id_counter + 1
    # date = datetime.datetime.now()

    if (gameType == 'ai') or (gameType == 'local'):
        reversiBoard = Reversi(size, ai_depth = difficulty) if gameType == 'ai' else Reversi(size)

        # this is basically where we define what our 'games' dicts are gonna look like (THIS IS ALL THE STUFF I WANT FOR THE FRONT END, IT GOTTA BE UPDATED W/ THE GAME)
        game = {
            "id": newId, "game": reversiBoard, "board": reversiBoard.board.get_grid(),
            "type": gameType, "size": size, "difficulty": difficulty,
            "player1": getUserByID(player1ID), "player2": getUserByID(player2ID), 
            "winner": None, "player1Score": 2, "player2Score": 2, 
            "currentPlayer": 1, "possibleMoves": reversiBoard.possible_moves(),
        }
        games.append(game)
        
        g_copy = copy.deepcopy(game)
        g_copy.pop('game')
        return jsonify(g_copy)

    elif (gameType == 'online'):
        pass

# helpers / future routes

def getUserByID(userID):
    if (userID == 0): # AI
        return {
            'userID': 0,
            'username': None,
            'password': None,
        }

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE userID = %s', (userID))
    rv = cursor.fetchall()
    conn.commit()
    cursor.close()

    if (len(rv) == 0):
        return None

    return {
        'userID': rv[0][0],
        'username': rv[0][1],
        'password': rv[0][2],
    }

def getNextUserID():
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(userID) FROM users')
    rv = cursor.fetchall()
    conn.commit()
    cursor.close()

    if (len(rv) == 0):
        return 1

    return rv[0][0] + 1

app.run()