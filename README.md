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
