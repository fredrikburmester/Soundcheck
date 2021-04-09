# tddd27

## Info

A spotify-authenticated website game for friends to guess each others favourite songs and genres. 

Each player joins a room hosted by 1 player and authenticates with their spotify login. The host selects a gamemode and the game is on!

## Infrastructure
### Backend
The backend is REST API build with flask and sockets.io for websockets. Communication will be Peer->Server->Peer.

This game requires a connection to the Spotify API. We have therefore created an application in the Spotify developer console which gives us a private client_id and secret that we can use to get information from the API. 

When a user enters our site they will be required to log in to their Spotify account from a link on our website. From this request a token is given, unique to the user, that the client can use to get information about the current user from the Spotify API. 

### Frontend
The frontend is built with Vue. 

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
 
