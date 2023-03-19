import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import uuid

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
    date = datetime.datetime.now()

    cursor = conn.cursor()
    cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s)', (newId, username, password, date))
    cursor.execute('INSERT INTO elo VALUES (%s, %s, %s)', (newId, default_elo, date))
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
    newId = uuid.uuid1().int
    date = datetime.datetime.now()

    cursor = conn.cursor()
    cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s)', (newId, None, None, date))
    cursor.execute('INSERT INTO elo VALUES (%s, %s, %s)', (newId, default_elo, date))
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

@app.route('/games/ai/<userID>', methods=['GET'])
def getAIGamesByUserID(userID):
    # cursor = conn.cursor()
    # cursor.execute('SELECT * FROM games WHERE player1 = %s', (userID))
    # rv = cursor.fetchall()
    # conn.commit()
    # cursor.close()

    # playerGames = games.filter(lambda game: game['game'].player1 == userID and game['type'] == 'ai')

    return jsonify(list(filter(lambda game: game['game'].player1 == userID and game['type'] == 'ai', games)))

@app.route("/games", methods=['PUT'])# do we create games with one player and put them on a lobby for others to join, or do we create the games with the two usernames
def create_game():
    requestBody = request.json
    player1ID = requestBody['player1ID']
    player2ID = requestBody['player2ID']
    size = requestBody['size']
    gameType = requestBody['gameType']
    difficulty = requestBody['difficulty']
    newId = uuid.uuid1().int
    date = datetime.datetime.now()

    if (gameType == 'ai'):
        
        pass
    
    elif (gameType == 'local'):
        pass
    else: 
        # game type is online
        pass
app.run()