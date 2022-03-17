# Soundcheck - A Music Game for Friends!
Made during the course TDDD27 at Linköping University with continued development ongoing.

![Soundcheck Logo](https://raw.githubusercontent.com/fredrikburmester/Soundcheck/master/frontend/src/assets/soundcheck-logo.png)

## 🚀 Website

|Branch      |Environment|URL                           |
|------------|-----------|------------------------------|
|main        |prod       |https://soundcheckgame.com    |
|development |dev        |                              |

## 🔎 Info

A spotify-authenticated webbased game for friends to guess each others favourite songs! 

Each player joins a room hosted by 1 player and authenticates with their spotify login. The host chooses the game settings and the game is on!

Press on an avatar to guess who's favourite song is playing. At the bottom is spotify web player (which sadly is limited to 30s of streaming on mobile) were you can listen to the song. *If you are on desktop the player is able to play the entire song, so we recommend that the host is on desktop if you are all gathered and want the full song experience. This is a spotify issue and we can't do anything about it sadly...*

## 📦 Infrastructure
### Backend
The backend is a REST API build with flask and sockets.io for websockets. Communication is Peer->Server->Peer for all game-related communication.

This game requires a connection to the Spotify API. We have therefore created an application in the Spotify developer console which gives us a private client_id and secret that we can use to get information from the API. 

When a user enters our site they will be required to log in to their Spotify account by clicking a link on our website. From this request an access_token is given, unique to the user. The client can use this token to get information about their top songs or personal info from the Spotify API. We can then use this information about the user, like top songs or genres, in the game. 

### Frontend
The frontend is built with Vue and Vuex for global states. The website is responsive but build from a mobile perspective. 

### Database
To store information about the rooms we use a small database called TinyDB. This way we can store and retrieve information about the users in a room and their scores. When a game starts, a room and user object is created. The room object holds information like the room id, name, players and so on. The user object holds the score of the player, the player id and name. ~~After each game the user object and room object will be deleted. This means that no scores will be saved for future review at this point.~~ All games are saved and can be viewed after the fact! Just go to the start page and look at your previous games.
### Hosting
The server is hosted under an SSL certified domain name: https://soundcheckgame.com. 

The website is routed through an nginx reverse proxy and static files will be served from there as well. The webserver config file can be found in the folder `nginx`. 

The nameservers are handeled by Cloudflare without proxying. 

The server is running on a 1-core 512GB RAM Viritual Ubuntu Server.

## 🔆 Getting started

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

## Buttons
The button structure looks like this. 

- The button component is `48px` tall with a `10px` bottom margin. 
- The standard grid on the page has a footer that is `62px + <button-size> + <button-margin> = 120`
- Adding another button will therefore result in a footer that is `178px` tall.   

A fixed button looks like this, firstly we need a button container: 
```
.button-container {
    position: fixed;
    left: 50%;
    bottom: 15px;
    transform: translate(-50%, -50%);
    margin: 0 auto;
    width: 100vw;
}

```
And then a div for the button actual button: 
```
.logout-button-div {
    padding: 0 2rem 0 2rem;
}
```
And then just place the button inside that div: 
```
<div class="button-container">
    <div class="logout">
        <Button
            color="#CD1A2B"
            button-link="/logout"
            button-text="Log out"
            class="logout"
            @click="logout"
        />
    </div>
</div>
```

## Issues and Bugs
https://trello.com/b/7ShV1pMC/spotifygame

# More Information and Presentations 
Group screencast: [TDDD27 - LiU - Soundcheck - Group Screencast](https://youtu.be/Ds02lgNWZ20)

## Individual Screencasts 
Fredrik Burmester (frebu645): [TDDD27 - LiU - Individual Screencast - Soundcheck - Fredrik Burmester](https://youtu.be/DkEs84ja3XI)
Josef Hamnert (josha196): [TDDD27 - LiU - Individual Screencast - Soundcheck - Josef Hamnert](https://youtu.be/mitou7tS_KI)
Daniel Hagstedt (danha896): [TDDD27 - LiU - Individual Screencast - Soundcheck - Daniel Hagstedt](https://youtu.be/Jh9TE5do6Os)

