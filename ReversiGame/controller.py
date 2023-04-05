from flask import Flask
import datetime
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from db import DB
from model.games_manager import GamesManager
from account_manager import AccountManager

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

db = DB()

# -- helpers / future routes
def getNextGameID():
    rv = db.callDB('SELECT MAX(gameID) FROM games', ())

    if (len(rv) == 0):
        return 1

    return rv[0][0] + 1

def postgame(gameID):
    game = gamesManager.getGameByID(gameID).get_json()
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

# -- global variables
gamesManager = GamesManager(getNextGameID())
accountManager = AccountManager()
players_searching = []

# -- routes
@app.route('/user/<userID>', methods=['GET'])
def getUserByID(userID):
    return accountManager.getUserByID(userID).get_json()

@app.route('/login', methods=['POST'])
def login():
    requestBody = request.json
    username = requestBody['username']
    password = requestBody['password']

    return accountManager.login(username, password).get_json()

@app.route('/signup', methods=['PUT'])
def signup():
    requestBody = request.json
    username = requestBody['username']
    password = requestBody['password']
    
    return accountManager.signup(username, password).get_json()

@app.route('/guest', methods=['PUT'])
def guest():
    return accountManager.guest().get_json()

@app.route('/games/<gameType>/<userID>', methods=['GET'])
def getGamesByTypeByUserID(gameType, userID):
    return gamesManager.getGamesByTypeByUserID(gameType, userID).get_json();

@app.route('/games/<gameID>', methods=['GET'])
def getGameByID(gameID):
    return gamesManager.getGameByID(gameID).get_json();

@app.route('/games', methods=['POST'])
def moveRoute():
    requestBody = request.json
    gameType = requestBody['gameType']
    gameID = requestBody['gameID']
    move = requestBody['move']

    gameDict = gamesManager.makeMove(gameType, gameID, move).get_json()
    if (gameDict['winner']):
        postgame(gameID)

    return gameDict

@app.route("/games", methods=['PUT'])
def createGameRoute():
    global game_id_counter
    requestBody = request.json
    player1 = accountManager.getUserByID(requestBody['player1ID']).get_json()
    player2 = accountManager.getUserByID(requestBody['player2ID']).get_json()
    size = requestBody['size']
    gameType = requestBody['gameType']
    difficulty = requestBody['difficulty'] or 0

    return gamesManager.createGame(player1, player2, size, gameType, difficulty).get_json()

#  -------- SOCKET STUFF --------
@socketio.on("connect")
def connected():
    print("client has connected: ", request.sid)
    emit("connect",{"data":f"id: {request.sid} is connected"})

@socketio.on('makeMove')
def handleSocketMove(data):
    # only gotta make move here and not return shit, bc the frontend will get game info on socket 'makeMove'
    gamesManager.makeMove(data['gameType'],data["gameID"],data["move"])
    emit("makeMove",{},broadcast=True)

@socketio.on('searchForLobby')
def searchForLobby(data):
    players_searching.append(data)
    print(players_searching)
    for player1 in players_searching:
        for player2 in players_searching:
            res = (player1['id'] != player2['id'] and player1['size'] == player2['size'])
            if res:
                print('creating online game')
                user1 = accountManager.getUserByID(player1['id']).get_json()
                user2 = accountManager.getUserByID(player2['id']).get_json()
                gameDict = gamesManager.createGame(user1, user2, player1['size'], 'online', 0).get_json()

                emit("lobbyFound",gameDict,broadcast=True)
                break

@socketio.on('cancelLobbySearch')
def cancelLobbySearch(data):
    print('canceling', data)
    global players_searching
    players_searching = list(filter(lambda player: player['id'] == data['id'], players_searching))

@socketio.on("disconnect")
def disconnected():
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)

#if __name__ == "__main__":
#    from waitress import serve
#    serve(app, host="0.0.0.0", port=8080)

# running the server
socketio.run(app)