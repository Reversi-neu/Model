from flask_socketio import SocketIO, emit
from flask import Flask, request

class SocketManager:

    def __init__(self, app, gamesManager, accountManager):
        self.app = app
        self.socketio = SocketIO(app, cors_allowed_origins="*")
        self.gamesManager = gamesManager
        self.accountManager = accountManager
        self.players_searching = []

        @self.socketio.on("connect")
        def connected():
            print("client has connected: ", request.sid)
            emit("connect",{"data":f"id: {request.sid} is connected"})

        @self.socketio.on('makeMove')
        def handleSocketMove(data):
            gamesManager.makeMove(data['gameType'],data["gameID"],data["move"])
            emit("makeMove",{},broadcast=True)

        @self.socketio.on('searchForLobby')
        def searchForLobby(data):
            self.players_searching.append(data)
            print(self.players_searching)
            for player1 in self.players_searching:
                for player2 in self.players_searching:
                    res = (player1['id'] != player2['id'] and player1['size'] == player2['size'])
                    if res:
                        print('creating online game')
                        user1 = accountManager.getUserByID(player1['id']).get_json()
                        user2 = accountManager.getUserByID(player2['id']).get_json()
                        gameDict = gamesManager.createGame(user1, user2, player1['size'], 'online', 0).get_json()

                        self.players_searching = list(filter(lambda player: player['id'] != player1['id'] and player['id'] != player2['id'], self.players_searching))

                        emit("lobbyFound",gameDict,broadcast=True)
                        break

        @self.socketio.on('cancelLobbySearch')
        def cancelLobbySearch(data):
            print('canceling', data)
            self.players_searching = list(filter(lambda player: player['id'] == data['id'], self.players_searching))

        @self.socketio.on("disconnect")
        def disconnected():
            print("user disconnected")
            emit("disconnect",f"user {request.sid} disconnected",broadcast=True)
    
    def run(self):
        self.socketio.run(self.app, debug=False)