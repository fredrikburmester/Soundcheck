# tddd27

Link to website: [Soundcheck](https://soundcheck.fdrive.se/)

Group screencast: [TDDD27 - LiU - Soundcheck - Group Screencast](https://youtu.be/Ds02lgNWZ20)

## Individual Screencasts 
Fredrik Burmester (frebu645): [TDDD27 - LiU - Individual Screencast - Soundcheck - Fredrik Burmester](https://youtu.be/DkEs84ja3XI)

Josef Hamnert (josha196): [TDDD27 - LiU - Individual Screencast - Soundcheck - Josef Hamnert](https://youtu.be/mitou7tS_KI)

Josef Hamnert (danha896): [TDDD27 - LiU - Individual Screencast - Soundcheck - Daniel Hagstedt](https://youtu.be/Jh9TE5do6Os)

## Info

A spotify-authenticated website game for friends to guess each others favourite songs and genres. 

Each player joins a room hosted by 1 player and authenticates with their spotify login. The host selects a gamemode and the game is on!

## Deadlines
- April 14th: Specifications in README.md file
- April 14th: Complete wireframe/design
- April 14th: Project setup ready and first commit done. 
- May 8th: functional prototype - (time for new functionality) - **Mid course screencast**: https://youtu.be/aEppwet_UZ8
- May 16th: Project ready for testing and bug fixes
- May 20th: Fully functioning project, ready for refactoring
- May 31st: Refactoring done
- June 4th: Fully finished project

## Infrastructure
### Backend
The backend is a REST API build with flask and sockets.io for websockets. Communication will be Peer->Server->Peer.

This game requires a connection to the Spotify API. We have therefore created an application in the Spotify developer console which gives us a private client_id and secret that we can use to get information from the API. 

When a user enters our site they will be required to log in to their Spotify account from a link on our website. From this request an access_token is given, unique to the user. The client can use this token to get information about their top songs or personal info from the Spotify API. We can then use this information about the user, like top songs or genres, in the game. 

### Frontend
The frontend is built with Vue. We will be using the state manager Vuex for global states. The website will be responsive but build from a mobile perspective. 

### Database
To store information about the rooms we will use a small database called TinyDB. This way we can store and retrieve information about the users in a room and their scores. When a game starts, a room and user object is created. The room object holds information like the room id, name, players and so on. The user object will hold the score of the player, the player id and name. After each game the user object and room object will be deleted. This means that no scores will be saved for future review at this point. 

### Hosting
The server will be hosted under a SSL certified domain name: https://soundcheck.fdrive.se. 

The website is routed through an nginx reverse proxy and static files will be served from there as well. The webserver config file can be found in the folder `nginx`. 

The nameservers are handeled by Cloudflare without proxying. 

The server is running on a 1-core 512GB RAM Viritual Ubuntu Server.

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

### Run locally 
For the frontend:

`npm run dev`

For the backend:

`python3 app.py dev`

### Run in production 
For the frontend:

`npm run prod`

For the backend:

`python3 app.py prod`

## Run with PM2

`pm2 start app.py --name "TDDD27-Backend" --watch -- prod`

`pm2 start npm --name "TDDD27-Frontend" -- run prod`

## Issues and Bugs
https://trello.com/b/7ShV1pMC/spotifygame


 
