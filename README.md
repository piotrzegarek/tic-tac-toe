# Tic Tac Toe Game

This is a tic tac toe game project implemented using Flask, PostgreSQL, Docker, Docker-Compose and Flask-SocketIO. There are 2 game modes, singleplayer - to play with implemented computer player and multiplayer - based on SocketIO connection. All the games history is stored and can be viewed in the profile page.

## Demo
![](https://github.com/piotrzegarek/tic-tac-toe/blob/main/DOCS/game_demo.gif)
![](https://github.com/piotrzegarek/tic-tac-toe/blob/main/DOCS/profile_ss.png)
## Setup
Instruction for quick setup after pulling the project.
```
make build
make up
make logs
```

After you can see app service and database is running, go to the http://172.19.0.3:5000/create_db route to create database.

Next, go to the "/" route, create an account and start playing!
