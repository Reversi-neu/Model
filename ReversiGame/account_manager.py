from db import DB
from flask import jsonify
import datetime

class AccountManager:

    def __init__(self):
        self.db = DB()
        self.default_elo = 1000
    
    def getUserByID(self, userID):
        userID = int(userID)
        if (userID == 0): # AI
            return {
                'userID': 0,
                'username': None,
                'password': None,
            }

        statement = 'SELECT * FROM users WHERE userID = %s'
        rv = self.db.callDB(statement, (userID))

        if (len(rv) == 0):
            return None

        return jsonify({
            'userID': rv[0][0],
            'username': rv[0][1],
            'password': rv[0][2],
        })

    def login(self, username, password):
        rv = self.db.callDB('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))

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

    def signup(self, username, password):
        newId = self.getNextUserID()
        date = datetime.datetime.now()

        self.db.callDB('INSERT INTO users VALUES (%s, %s, %s, %s)', (newId, username, password, date))
        self.db.callDB('INSERT INTO elo VALUES (%s, %s, %s)', (newId, self.default_elo, date))
        rv = self.db.callDB('SELECT * FROM users WHERE userID = %s', (newId))

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

    def guest(self):
        newId = self.getNextUserID()
        date = datetime.datetime.now()

        self.db.callDB('INSERT INTO users VALUES (%s, %s, %s, %s)', (newId, None, None, date))
        self.db.callDB('INSERT INTO elo VALUES (%s, %s, %s)', (newId, self.default_elo, date))
        rv = self.db.callDB('SELECT * FROM users WHERE userID = %s', (newId))

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
    
    def getNextUserID(self):
        rv = self.db.callDB('SELECT MAX(userID) FROM users', ())

        if (len(rv) == 0):
            return 1

        return rv[0][0] + 1