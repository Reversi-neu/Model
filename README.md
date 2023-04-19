# Deployment
Frontend can be found here [https://reversi-2023.vercel.app/](https://reversi-2023.vercel.app/)  
Backend can be found here [https://reversi-backend-4520.herokuapp.com/](https://reversi-backend-4520.herokuapp.com/)

# Model
Contains the game, server, others...

TO DO:
- Make oberserver interface for socketio to follow DP guidelines
- No globals for players searching

REQUIRMENTS NEEDED:
- See players searching for game and choose opponent
- Leaderboard of the top 5 players by ELO
  - Prob want to move elo calculator out of controller to the model as it's own file
- We think we have it, stores games in event of a crash to be recovered
- Comment and standardize our code
- Unit tests
