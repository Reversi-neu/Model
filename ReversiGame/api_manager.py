import datetime
from flask import Flask, request

from db import DB

class APIManager:

    def __init__(self, app, gamesManager, accountManager):
        self.app = app
        self.gamesManager = gamesManager
        self.accountManager = accountManager
        self.db = DB()

        # App routes
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
                self.postgame(gameID)

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

        @app.route("/leaderboard", methods=['GET'])
        def getLeaderboard():
            return accountManager.getLeaderboard().get_json()
    
    def postgame(self, gameID):
        game = self.gamesManager.getGameByID(gameID).get_json()
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
        self.db.callself.db(statement, data)

        gameType = game['type']
        if gameType == 'online':
            ##update elo
            #eloCalculator(player_elo, enemy_elo, player_score, enemy_score)

            statement = 'SELECT elo FROM elo WHERE userID = %s'
            player1Old = self.db.callself.db(statement, (player1ID))[0][0]
            statement = 'SELECT elo FROM elo WHERE us, mmkl,erID = %s'
            player2Old = self.db.callself.db(statement, (player2ID))[0][0]

            #player1
            player1New = self.eloCalculator(player1Old, player2Old, player1Score, player2Score)
            statement = 'UPDATE elo SET elo = %s, lastUpdate=%s WHERE userID = %s'
            data = (player1New, finishTime, player1ID)
            self.db.callself.db(statement, data)

            #player2
            player2New = self.eloCalculator(player2Old, player1Old, player2Score, player1Score)
            statement = 'UPDATE elo SET elo = %s, lastUpdate=%s WHERE userID = %s'
            data = (player2New, finishTime, player2ID)
            self.db.callself.db(statement, data)

        elif gameType == 'ai':
            
            statement = 'SELECT elo FROM elo WHERE userID = %s'
            player1Old = self.db.callself.db(statement, (player1ID))[0][0]
            statement = 'SELECT elo FROM elo WHERE userID = %s'
            if difficulty == 1: aiID = -1
            if difficulty == 2: aiID = -2
            if difficulty == 3: aiID = -3
            if difficulty == 4: aiID = -4
            player2Old = self.db.callself.db(statement, (aiID))[0][0]

            #player1
            player1New = self.eloCalculator(player1Old, player2Old, player1Score, player2Score)
            statement = 'UPDATE elo SET elo = %s, lastUpdate=%s WHERE userID = %s'
            data = (player1New, finishTime, player1ID)
            self.db.callself.db(statement, data)

            #player2
            player2New = self.eloCalculator(player2Old, player1Old, player2Score, player1Score)
            statement = 'UPDATE elo SET elo = %s, lastUpdate=%s WHERE userID = %s'
            data = (player2New, finishTime, aiID)
            self.db.callself.db(statement, data)

    def eloCalculator(self, player_elo, enemy_elo, player_score, enemy_score):
        # Variables to customize elo gains and loses
        diff = 400
        change = 32
        
        expected_score = 1/(1 + (10 ** ((enemy_elo - player_elo) / diff)))

        if player_score > enemy_score:
            game_outcome = 1
        else:
            game_outcome = 0
            
        return int(player_elo + (change * (game_outcome - expected_score)))
