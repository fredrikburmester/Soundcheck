/*
This view containes the entire game. There are 2 stages, a room lobby/waiting room, and the game itself. 
 */

<template>
    <div
        v-if="found"
        id="gameroom"
        :key="found"
        class="gameroom"
    >
        <div
            v-if="showQR"
            class="bigQR"
            @click="showQR = false"
        >
            <img
                :src="qr"
                @click="showQR = false"
            >
        </div>
        <div @click="openChat" :style="started ? 'bottom: 190px;' : 'bottom: 230px;' " class="chat-icon"> 
            <img src="@/assets/chat-icon.jpg" alt="chat-icon">
        </div>

        <div v-on:keyup.escape="closeChat()" v-if="chat" class="chat-room" tabindex="0">
            <CloseButton  color="red" id="closeChatButton" @click="closeChat" />
            <div class="messages" id="messages">
                <div v-for="(message, index) in messages" :key="message" :class="index == 0 ? 'message first-message' : 'message'">
                    <ChatAvatar 
                        :player-name="message.player.name"
                        :color="message.player.color"
                        :host="message.player.host"
                        :isMe="message.player.name == name"
                    />
                    <p>{{ message.text }}</p>
                </div>
                <div style="height: 1px" id="chat-end"></div>
            </div>
            <div class="input-area">
                <hr>
                <input v-on:keyup.enter="sendMessage($event)" type="text" placeholder="Type here...">
            </div>
        </div>
        <div
            v-if="leaveRoomModal == true"
            :key="leaveRoomModal"
            class="leaveroom-modal"
        >
            <div>
                <h2 v-if="host" style="padding: 0 2rem 0 2rem">
                    Do you really want to end the game?
                </h2>
                <h2 v-else>
                    Do you really want to leave?
                </h2>
                <p>All progress will be lost...</p>
                <Button
                    v-if="host"
                    button-text="end game"
                    color="#CD1A2B"
                    @click="leaveRoom"
                />
                <Button
                    v-else
                    button-text="Leave room"
                    color="#CD1A2B"
                    @click="leaveRoom"
                />
                <Button
                    button-text="Go back"
                    color="#1DB954"
                    @click="toggleModal"
                />
            </div>
        </div>
        <div
            v-if="started"
            :key="started"
            class="started-grid"
            :style="startedGridStyle"
        >
            <div class="started-grid-header">
                <ProgressBar
                    :key="current_question"
                    :time="progressbarTime"
                    class="progressbar"
                />
                <h2 class="code">
                    Guess!
                </h2>
                <p class="title">
                    Who's song is this?
                </p>
                <div class="stats">
                    <p>
                        Players guessed: {{ getPlayersGuessed }} /
                        {{ players.length }}
                    </p>
                    <p>
                        Question: {{ current_question + 1 }} / {{ nr_of_questions }}
                    </p>
                </div>
            </div>
            <div id="active-list" :key="my_guess" class="list">
                <PlayerAvatar
                    v-for="player in players"
                    :id="player.id"
                    :key="player.id"
                    class="player-guess"
                    :player-name="player.name"
                    :color="player.color"
                    :host="player.host"
                    :selected="selected(player.sid)"
                    @click="guess(player)"
                    :guesses="player.guesses"
                />
            </div>
            <div>
                <div
                    v-if="host"
                    class="next-song"
                >
                    <Button
                        :key="current_question"
                        :button-text="(current_question + 1) == nr_of_questions ? 'Go to results' : 'next question'"
                        color="#1DB954"
                        @click="sendNextQuestion"
                    />
                </div>
                <div class="close-button">
                    <CloseButton 
                        @click="toggleModal"
                    />
                </div>
            </div>
            <iframe
                class="webplayer"
                :src="iframeurl"
                allowtransparency="true"
                allow="encrypted-media"
            />
        </div>
        <div
            v-else 
            class="lobby-grid-outer"
        >
            <div class="qr">
                <img :src="qr" @click="showQR = true">
            </div>
            <div 
                :style="lobbyGridStyle"
                class="lobby-grid"
            >
                <div class="lobby-grid-header">
                    <h1 class="code">
                        {{ code }}
                    </h1>
                    <div class="hr" style="margin-top: 1rem; margin-bottom: 1rem" />
                    <h3 class="title">
                        <p v-if="players.length > 1">
                            {{players.length}} Players:
                        </p>
                        <p v-else>
                            So empty... Invite some friends!
                        </p>
                    </h3>
                </div>
                <div class="list">
                    <PlayerLobbyAvatar 
                        @updateName="sendName"
                        v-for="player in players"
                        :key="player.id"
                        :player-name="player.name"
                        :color="player.color"
                        :host="player.host"
                        :isMe="player.name == name"
                    />
                </div>
                <div class="buttons">
                    <p v-if="!host">
                        {{ status }}
                    </p>
                    <div class="copycode">
                        <Button
                            :key="clipboardtext"
                            color="#FFF"
                            :button-text="clipboardtext"
                            @click="copyToClipboard"
                        />
                    </div>
                    <div v-if="host" :key="host" class="startgame">
                        <Button
                            button-text="Start Game"
                            @click="startGame()"
                        />
                    </div>
                    <div class="leave">
                        <Button
                            v-if="host"
                            button-text="end game"
                            color="#CD1A2B"
                            @click="toggleModal"
                        />
                        <Button
                            v-else
                            button-text="Leave Room"
                            color="#CD1A2B"
                            @click="toggleModal"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import PlayerAvatar from '../components/PlayerAvatar';
import Button from '../components/Button';
import ProgressBar from '../components/ProgressBar';
import CloseButton from '../components/CloseButton';
import PlayerLobbyAvatar from '../components/PlayerLobbyAvatar';
import { nextTick } from 'vue'
import ChatAvatar from '../components/ChatAvatar.vue'

const QRCode = require('qrcode');
import API from "../libs/api"
// const axios = require('axios');

export default {
    name: 'Home',
    components: {
        PlayerAvatar,
        Button,
        ProgressBar,
        CloseButton,
        PlayerLobbyAvatar,
        ChatAvatar
    },
    data: function () {
        return {
            code: this.$route.params.code,
            clipboardtext: `copy invite link`,
            status: 'Waiting for host to start the game...',
            iframeurl: '',
            settings: '',
            my_guess: '',
            qr: '',
            current_question: 0,
            nr_of_questions: 0,
            started: false,
            showQR: false,
            found: false,
            host: false,
            leaveRoomModal: false,
            players: [],
            progressbarTime: 0,
            players_guessed: [],
            name: "",
            chat: false,
            messages: []
        };
    },
    // All functions under the "sockets" are websockets from the sever and the functions are 
    // automatically run when the client recieves the corresponding socket function call. 
    sockets: {
        // The server responds to the request to join the room. Depending on the state of the game, the client is updated with
        // all relevant information about the game like: 
        connectToRoom({
            status, // Has the game started? 
            access, // Does the client have access to the game is progress? (used for rejoining active game)
            question, // What is the current question? 
            settings, // What are the game settings? 
            answers, // What are the answers to the questions? (encoded)
            questionTimeStarted, // How long has it been since the last question started? Used in progressbar.
            players_guessed, // How many players have guessed on a question? 
            new_sid,
            error
        }) {
            // console.log({
            //     status,
            //     access,
            //     question,
            //     settings,
            //     answers,
            //     questionTimeStarted,
            // });
            // The game has not started and the client should be put in the lobby
            if (status == 'lobby') {
                // join lobby
                this.generateQR();
                this.settings = settings;
                this.getTopTrack();
                this.found = true;

                if(new_sid.length > 0) {
                    this.$store.commit('setSid', new_sid)
                }

            // If the game has started the player can either rejoin or is redirected if not in the game. 
            } else if (status == 'playing') {
                if (access == true) {
                    // enter room
                    this.settings = settings;
                    // set current song
                    this.current_question = question;
                    this.setIframeUrl(answers[question]['info']);
                    this.nr_of_questions = answers.length;
                    this.players_guessed = players_guessed;

                    // Set progressbar progression
                    var unixTime = Date.now().toString();
                    unixTime = unixTime.substring(0, unixTime.length - 3);

                    var diff = unixTime - questionTimeStarted + 1;
                    if (diff > 30) {
                        this.progressbarTime = 1;
                    } else {
                        this.progressbarTime = diff / 30;
                    }

                    this.started = true;
                    this.found = true;
                } else {
                    // set error
                    this.$store.commit(
                        'updateError',
                        error || 'Game has already started!'
                    );
                    // go to join
                    this.$router.push('/join');
                }
            // If the game has ended the client is pushed to the results page. 
            } else if (status == 'ended') {
                // game has ended
                this.$router.push(`/${this.code}/results`);
            // If the room for some reason does not exist the client is sent to the join page with a error code. 
            } else if (status == 'NaR') {
                // Room does not exist
                // set error
                this.$store.commit('updateError', error || 'That room does not exist!');
                // go to join
                this.$router.push('/join');
            } 
        },
        // Updating the list of current players each time a player joines or leaves. 
        update_list_of_players({ players }) {
            // Set the current player name
            players.forEach(player => {
                if (player.sid == this.$store.getters.getSid) {
                    this.name = player.name
                }
            });
            
            this.players = players;

            // Check who is host
            this.isHost();
        },
        // Used if the host closes the room. 
        room_closed_by_host() {
            this.started = false;
            this.status = 'Host ended the game...';
            this.players = [];
            this.$store.commit('clearPlayersGuessed');
        },
        // Updates the number of players that have guess on a question
        nr_of_players_guessed(data) {
            this.players_guessed = data.players; // set the array of players who have guessed
        },
        // Updates the current question if the host goes to the next question
        next_question(data) {
            // Set the current question and reset the progressbar
            this.current_question = data.current_question;
            this.progressbarTime = 0;

            // If the current question is -1 then the game is ending and we show a loading screen and await the "game_ended" socket
            if (data.current_question == '-1') {
                // this.loading = true;
            } else {
                this.setIframeUrl(data.trackid); // Set the song in the iframe
                this.my_guess = ''; // Reset the guess
            }

            // Reset number of players guessed
            this.players_guessed = [];
        },
        start_game(data) {
            this.nr_of_questions = data.nr_of_questions;
            this.started = true;
        },
        recieve_message({ text, sid }) {
            var user;
            this.players.forEach(player => {
                if(player.sid == sid) {
                    user = player
                }
            });
            let message = {
                'text': text,
                'player': user
            }
            this.messages.push(message)
            this.scrollToBottom()
        },
     },
    computed: {
        getPlayersGuessed() {
            return this.players_guessed.length;
        },
        lobbyGridStyle() {
            if(this.host) {
                return {
                    'height': `${window.innerHeight}px`,
                    'grid-template-rows': '180px auto 210px'
                }
            } else {
                return {
                    'height': `${window.innerHeight}px`,
                    'grid-template-rows': '180px auto 190px'
                    
                };
            }
        },
        startedGridStyle() {
            if(this.host) {
                return {
                    'height': `${window.innerHeight}px`,
                    'grid-template-rows': '190px auto 70px 100px'
                }
            } else {
                return {
                    'height': `${window.innerHeight}px`,
                    'grid-template-rows': '190px auto 0px 100px'
                    
                };
            }
        },
    },
    mounted: function () {
        // Function called when the dom has loaded. 
        this.connectToRoom();
    },
    watch: {
        chat() {   
            if (this.chat === false) {
                window.removeEventListener("keyup", this.onEscapeKeyUp);
            } else {
                window.addEventListener("keyup", this.onEscapeKeyUp);
            }
        }
    },
    methods: {
        // toggles the leave room modal 
        openChat() {
            this.chat = true
            this.$nextTick(() => {
                this.scrollToBottom()
            })
        },
        closeChat() {
            this.chat = false
        },
        onEscapeKeyUp(event) {
            if (event.which === 27) {
                this.chat = false;
            }
        },
        toggleModal() {
            this.leaveRoomModal = !this.leaveRoomModal;
        },
        scrollToBottom() {
            this.$nextTick(() => {
                let chat = document.getElementById("chat-end")
                if(chat) {
                    chat.scrollIntoView({ behavior: "smooth", block: "end" });
                }
            })
        },
        sendMessage(event) {
            this.$socket.client.emit('send_message', {
                sid: this.$store.getters.getSid,
                message: event.target.value,
                code: this.code
            });
            event.target.value = ""
        },
        sendName(name) {
            for(let player in this.players) {
                if(player.sid == this.$store.getters.getSid) {
                    //
                }
            }

            this.$socket.client.emit('update_name', {
                sid: this.$store.getters.getSid,
                name: name,
                code: this.code
            });
        },
        async copyToClipboard() {
            await navigator.clipboard.writeText(window.location.href);
            this.clipboardtext = 'copied!';
        },
        // When the page has loaded the client requests to join the room by sending a websocket to the server with credentials, room code and personal information. 
        connectToRoom() {
            var access_token = this.$store.getters.getAccessToken;
            var refresh_token = null;
            this.$socket.client.emit('connect_to_room', {
                code: this.code,
                sid: this.$store.getters.getSid,
                access_token: access_token,
                refresh_token: refresh_token,
            });
        },
        generateQR() {
            var self = this;
            QRCode.toDataURL(
                `${process.env.VUE_APP_PROTOCOL}://${process.env.VUE_APP_PUBLIC_URL}/${this.code}`, {scale: 30, margin: 1, color: {dark: '#eee', light: '#191414'}}, 
                function (err, url) {
                    self.qr = url;
                }
            );
        },
        isHost() {
            var self = this;
            this.players.forEach((player) => {
                if (player.sid == this.$store.getters.getSid) {
                    if (player.host == true) {
                        self.host = true;
                    }
                }
            });
        },
        startGame() {
            this.$socket.client.emit('start_game', { code: this.code });
            this.sendNextQuestion();
        },
        // notifies the server to advance to the next question 
        sendNextQuestion() {
            // Send next question
            this.$socket.client.emit('next_question', {
                code: this.code,
            });
        },
        // when guessing, the guess is sent to the server.
        async guess(player) {
            var pos = document.getElementById('active-list')
            var pos = pos.scrollTop

            this.my_guess = player.sid;
            this.$socket.client.emit('player_guess', {
                sid: this.$store.getters.getSid,
                code: this.code,
                guess: this.my_guess,
            });

            await nextTick()
            document.getElementById('active-list').scrollTop = pos
        },
        selected(id) {
            if (id == this.my_guess) {
                return true;
            }
            return false;
        },
        setIframeUrl(id) {
            this.iframeurl = `https://open.spotify.com/embed?uri=spotify:track:${id}`;
        },
        leaveRoom() {
            this.$socket.client.emit('leave_room', {
                code: this.code,
                sid: this.$store.getters.getSid,
            });
            this.$router.push('/');
        },
        // gets the top track for the user when joining the room. These are then sent to the server. 
        getTopTrack: async function() {
            var token = this.$store.getters.getAccessToken;

            var time_range = this.settings[0];
            var nr_songs = this.settings[1];

            var trackIds = await API.getTopSongsForUser(time_range, nr_songs, token)

            var time_range_text;
            if(time_range == 'short_term') {
                time_range_text = 'month'
            } else if (time_range == 'medium_term') {
                time_range_text = 'half a year'
            } else if (time_range == 'long_term') {
                time_range_text = 'year'
            }

            if (trackIds.length < nr_songs) {
                let error = `Not enough top song! ${trackIds.length} top songs the last ${time_range_text}. Try creating a room with another time-frame or fewer songs. `

                this.$socket.client.emit('leave_room', {
                    code: this.code,
                    sid: this.$store.getters.getSid,
                });

                // set error
                this.$store.commit(
                    'updateError', error
                );
                // go to join
                this.$router.push('/join');
            } else {
                this.$socket.client.emit('toptrack', {
                    trackid: trackIds,
                    sid: this.$store.getters.getSid,
                    room: this.code,
                });
            }
 
        },
    },
};
</script>

<style scoped>
.gameroom {
    display: grid;
}
.lobby-grid-outer {
    display: grid;
}
.lobby-grid {
    display: grid;
    grid-template-rows: minmax(160px,170px) auto minmax(0px, 220px);
}
.lobby-grid-header {
    margin-top: 40px;
}
.started-grid {
    display: grid;
    grid-template-rows: 140px auto minmax(0px, 70px) 100px;
    height: 99vh;
}
.started-grid-header {
    margin-top: 45px
}
.buttons {
    margin-top: 20px;
    margin-bottom: 20px;
    margin-right: 2rem;
    margin-left: 2rem;
    
}
.buttons p {
    margin-top: 0;
}
.code {
    text-align: left;
    margin-left: 2rem;
    margin-bottom: 0;
}
.title {
    font-style: italic;
    color: darkgrey;
    text-align: left;
    margin-left: 2rem;
    margin-top: 0;
}
.stats {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    text-align: center;
    color: darkgrey;
    margin-left: 2rem;
    margin-right: 2rem;
    margin-top: 0;
    margin-bottom: 20px;
}
.hr {
    height: 2px;
    background-color: rgb(63, 63, 63);
    margin: 0 2rem 0 2rem;
}
.QR {
    transform: scale(0.5);
    border: 5px solid rgb(255, 255, 255);
}
.qr {
    position: fixed;
    right: 0;
    top: 30px;
    padding: 1rem 2rem;
}
.qr > img {
    width: 50px;
}
.messages {
    display: flex;
    padding: 0 2rem 0 2rem;
    overflow-y: scroll;
    height: 100%;
    flex-direction: column;
}
.messages > .first-message {
    margin-top: auto !important;
    
}
.message {
    display: grid;
    grid-template-columns: 60px auto;
    justify-content: start;
    align-items: start;
    margin-bottom: 10px;
}
.message > p {
    margin: 0;
    margin-top: 18px;
    text-align: left;
}
.message-icon {
    height: 40px;
    width: 40px;
    border-radius: 20px;
}
.chat-icon {
    position: fixed;
    right: 30px;
    cursor: pointer;
}
.chat-icon > img {
    border-radius: 50px;
    outline: thick solid white;
    border: 10px;
    width: 30px;
    height: 30px;
}

.chat-room {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 99;
    height: 100vh;
    width: 100vw;
    background-color: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(5px);
    display: grid;
    grid-template-columns: 1;
    grid-template-rows: auto 225px;
    justify-items: start;
    align-items: end;
}
.chat-room > .input-area {
    width: 100%;
    display: grid;
    justify-content: stretch;
    margin-bottom: auto
}
.chat-room > .input-area > input {
    margin: 0 2rem 0 2rem;
    height: 45px;
    font-size: 15px;
    justify-self: stretch;
    border-radius: 40px;
    padding-left: 20px;
    padding-right: 20px;
    border: none;
}
.chat-room > .input-area > hr {
    margin: 1rem 2rem 1rem 2rem;
    height: 1px;
    background-color: rgb(255, 255, 255);
    border:none;
}
#closeChatButton {
    position: fixed;
    top: 45px;
    right: 0;
    padding: 2rem
}
.list {
    margin-left: 2rem;
    margin-right: 2rem;
    /* height: 100%; */
    overflow: scroll;
    border-color: aquamarine;
    border-bottom: 1px solid gray;
}
.webplayer {
    height: 80px;
    width: 100vw;
}
.progressbar {
    position: fixed;
    top: 130px;
    width: calc(100vw - 4rem);
    margin-left: 50%;
    transform: translateX(-50%);
}
.progressbar {
    height: 5px !important;
    overflow: hidden;
}
.bigQR {
    position: fixed;
    top: 0;
    left: 0;
    background-color: rgba(0, 0, 0, 0.7);
    width: 100vw;
    height: 100vh;
    z-index: 100;
}
.bigQR > img {
    width: 60vw;
    height: auto;
    position: fixed;
    top: 20%;
    left: 50%;
    transform: translateX(-50%);
}
.leave-started-game {
    position: fixed;
    bottom: 100px;
    left: 50%;
    transform: translateX(-50%);
}
/* .loading {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    background-color: rgba(0, 0, 0, 0.832);
    display: grid;
    place-items: center;
    z-index: 2;
} */
.leaveroom-modal {
    display: grid;
    place-items: center;
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    background-color: black;
    z-index: 2;
}

.close-button {
    position: fixed;
    top: 70px;
    right: 2rem;
}

.next-song {
    margin-top: 10px;
    margin-right: 2rem;
    margin-left: 2rem;
}

.webplayer {
    border: none !important;
    border-radius: 15px;
    width: calc(100vw - 2rem);
    margin-left: 1rem;
}

@media only screen and (min-width: 700px) {
    .bigQR > img {
    width: 45vw;
    height: auto;
    position: fixed;
    top: 20%;
    left: 50%;
    transform: translateX(-50%);
    }
}
@media only screen and (min-width: 1100px) {
    .bigQR > img {
    width: 30vw;
    height: auto;
    position: fixed;
    top: 20%;
    left: 50%;
    transform: translateX(-50%);
    }
}
</style>
