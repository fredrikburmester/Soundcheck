# tddd27 - project

## Info

A spotify-authenticated website game for friends to guess each others favourite songs and genres. 

Each player joins a room hosted by 1 player and authenticates with their spotify login. The host selects a gamemode and the game is on!

## Infrastructure
### Backend
The backend is REST API build with flask and sockets.io for websockets. Communication will be Peer->Server->Peer.

This game requires a connection to the Spotify API. We have therefore created an application in the Spotify developer console which gives us a private client_id and secret that we can use to get information from the API. 

When a user enters our site they will be required to log in to their Spotify account from a link on our website. From this request a token is given, unique to the user, that the client can use to get information about the current user from the Spotify API. This way we can retrieve information about the user, like top songs or genres that can be used in the game. 

### Frontend
The frontend is built with Vue. We are using the state manager Vuex for global states. The website will be respontive but build from a mobile perspective. 

### Database
To store information about the rooms we will use a small database called TinyDB. This way we can store and retrieve information about the users in a room and their scores. When a game starts a room and user object is created. The room object holds information like the room id, name, players and so on. The user object will hold the score of the player, the player id and name. After each game the user object and room object will be deleted. This means that no scores will be saved for future review at this point. 

### Hosting
The server will be hosted under a SSL certified domain name. 

## Getting started

Clone this repo to your computer. You will have two folders, frontend and backend. 

### Backend
The backend contains all files for the REST API. This is the Flask project. To run this you will need to run it inside a virtual enviroment and install all dependencies. 

- Install virtualenv: `pip3 install virtualenv --user`
- Make sure you are in the folder `tddd27`
- Initialize virtual env: `virtualenv .`
- Run virtual enviroment: `source bin/activate`
- Run `pip install -r requirements.txt`

After this you can run the backend with `python3 app.js` 

### Frontend
This is the frontend for the project, made with Vue. Make sure to have NPM, Node and Vue installed for this to work.

Run `npm install` inside the frontend folder to install all dependencies. 

Now you can run `npm run serve` to run the server in development. 

Run `npm run build` to build the project for production. 
 
