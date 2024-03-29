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
        <CheckMark v-if="correctGuess" /> 
        <CrossMark v-if="wrongGuess" /> 
        <div :style="chatIconStyle" class="chat-icon" @click="openChat"> 
            <div v-if="newMessages > 0 && !read" id="unread-bubble">
                <p>
                    {{ newMessages }}
                </p>
            </div>
            <img src="@/assets/chat-icon-small-green.jpg" alt="chat-icon">
        </div>
        <transition name="fade">
            <div v-if="chat" class="chat-room" tabindex="0" @keyup.escape="closeChat()">
                <CloseButton id="closeChatButton" color="red" @click="closeChat" />
                <div id="messages" class="messages">
                    <div v-if="messages.length == 0" id="no-messages">
                        {{ chatStatusText }}
                    </div>
                    <div v-for="(m, index) in messages" :key="m" :class="index == 0 ? 'message first-message' : 'message'">
                        <ChatAvatar 
                            :player-name="m.player.name"
                            :color="m.player.color"
                            :host="m.player.host"
                            :is-me="m.player.name == name"
                        />
                        <p>{{ m.text }}</p>
                    </div>
                    <div id="chat-end" style="height: 1px" />
                </div>
                <div class="input-area">
                    <input
                        id="chat-input" v-model="message" type="text" placeholder="Type here..." @focus="scrollWebsite"
                        @keyup.enter="sendMessage"
                    >
                    <div class="send-button" @click="sendMessage">
                        <p>Send</p>
                    </div>
                    <div id="bottom-chat-element" />
                </div>
            </div>
        </transition>
        <div
            v-if="leaveRoomModal == true"
            :key="leaveRoomModal"
            class="leaveroom-modal"
        >
            <div style="padding: 0 2rem 0 2rem">
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
                    :selected="selected(player.id)"
                    :guesses="player.guesses"
                    @click="guess(player)"
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
                            {{ players.length }} Players:
                        </p>
                        <p v-else>
                            So empty... Invite some friends!
                        </p>
                    </h3>
                </div>
                <div :key="players" class="list">
                    <PlayerLobbyAvatar 
                        v-for="player in players"
                        :key="player.id"
                        :player-name="player.name"
                        :color="player.color"
                        :host="player.host"
                        :is-me="player.name == name"
                        @updateName="sendName"
                    />
                </div>
                <div class="buttons">
                    <p v-if="!host">
                        {{ status }}
                    </p>
                    <div class="copycode">
                        <Button
                            v-if="status != 'Host ended the game...'"
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
import CheckMark from '../components/CheckMark.vue'
import CrossMark from '../components/CrossMark.vue'
// const axios = require('axios');

export default {
    name: 'Home',
    components: {
        PlayerAvatar,
        Button,
        ProgressBar,
        CloseButton,
        PlayerLobbyAvatar,
        ChatAvatar,
        CheckMark,
        CrossMark
        
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
            message: '',
            messages: [],
            read: false,
            newMessages: 0,
            chatStatusText: 'Messages are deleted after each game 🔒 ',
            correctGuess: false,
            wrongGuess: false
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
            var list_of_players = []; 

            // Set the current player name
            players.forEach(player => {
                if (player.id == this.$store.getters.getUserId) {
                    this.name = player.name
                }
                list_of_players.push(player)
            });
            
            this.players = list_of_players;

            // Check who is host
            this.isHost();
        },
        // Used if the host closes the room. 
        room_closed_by_host() {
            this.started = false;
            this.status = 'Host ended the game...';
            this.players = [];
            this.$store.commit('clearPlayersGuessed');
            this.chatStatusText = 'Room is closed and will not recieve messages...'
            this.messages = []
            this.newMessages = 0
            this.read = true
        },
        // Updates the number of players that have guess on a question
        nr_of_players_guessed(data) {
            this.players_guessed = data.players; // set the array of players who have guessed
        },
        // Updates the current question if the host goes to the next question
        next_question(data) {
            console.log(data)

            if (this.settings[2] == "Yes") {
                this.checkAnswer(data)
            }

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
            this.chat = false
        },
        recieve_message({ text, id }) {
            var user;
            this.newMessages += 1

            this.players.forEach(player => {
                if(player.id == id) {
                    user = player
                }
            });

            let message = {
                'text': text,
                'player': user
            }
            this.messages.push(message)

            this.read = false
            if(this.chat) {
                this.scrollToBottom()
                this.read = true
                this.newMessages = 0
            }
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
                    'grid-template-rows': '180px auto 240px'
                }
            } else {
                return {
                    'height': `${window.innerHeight}px`,
                    'grid-template-rows': '180px auto 220px'
                    
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
        chatIconStyle() {
            if(this.host) {
                if(this.started) {
                    return {
                        'bottom': '180px',
                    };
                } else {
                    return {
                        'bottom': '250px',
                    }
                }
            } else {
                if(this.started) {
                    return {
                        'bottom': '115px',
                    };
                } else {
                    return {
                        'bottom': '230px',
                    };
                }
            }
        }
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
    mounted: function () {
        // Function called when the dom has loaded. 
        this.connectToRoom();
    },
    methods: {
        // toggles the leave room modal 
        openChat() {
            this.chat = true
            this.read = true
            this.newMessages = 0
            this.$nextTick(() => {
                this.scrollToBottom()
            })
        },
        checkAnswer(data) {
            var self = this
            if(data.current_question > 0) {
                if(this.my_guess == this.currentAnswer) {
                    this.correctGuess = true

                    setTimeout(function(){ 
                        self.correctGuess = false
                    }, 1500);
                } else if (this.my_guess != this.currentAnswer){
                    this.wrongGuess = true

                    setTimeout(function(){ 
                        self.wrongGuess = false
                    }, 1500);
                }
            }
            this.currentAnswer = data.answer    
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
        sendMessage() {
            document.getElementById('chat-input').focus()
            if(this.message.length > 0) {
                this.$socket.client.emit('send_message', {
                    id: this.$store.getters.getUserId,
                    message: this.message,
                    code: this.code
                });
                this.message = ""
            } else {
                //
            }
        },
        sendName(name) {
            var oldName = name.old
            var newName = name.new

            var same = false
            this.players.forEach(player => {
                if(player.name.toLowerCase() == newName.toLowerCase() || player.id.toLowerCase() == newName.toLowerCase()) {
                    same = true
                }
            });

            if(!same) {
                this.players.forEach(player => {
                    if(player.name == oldName) {
                        player.name = newName
                    }
                });
                this.$socket.client.emit('update_name', {
                    sid: this.$store.getters.getSid,
                    name: newName,
                    code: this.code
                });
            }
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

            this.my_guess = player.id;
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
                    room: this.code,
                    userid: this.$store.getters.getUserId
                });
            }
 
        },
    },
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .2s ease;
  -webkit-transition: opacity .2s ease;
  -moz-transition: opacity .2s ease;
  -o-transition: opacity .2s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.gameroom {
    display: grid;
}
.lobby-grid-outer {
    display: grid;
}
.lobby-grid {
    display: grid;
}
.lobby-grid-header {
    margin-top: 40px;
}
.started-grid {
    display: grid;
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
    padding: 0 2rem 2rem 2rem;
    overflow-y: scroll;
    flex-direction: column;
    height: inherit;
}
.messages > .first-message {
    margin-top: auto !important;
    
}
.message {
    display: grid;
    grid-template-columns: 60px auto;
    justify-content: start;
    align-items: start;
}
.message > p {
    margin: 0;
    margin-top: 8px;
    text-align: left;
    background-color: white;
    border-radius: 10px;
    padding: 15px;
}
.send-button {
    position:fixed;
    width: 80px;
    height: 40px;
    border-radius: 20px ;
    background-color: rgb(71, 138, 255);
    cursor: pointer;
    display: flex;
    justify-self: end;
    right: 1rem;
    bottom: 65px
}
.send-button > p {
    margin-left: 20px;
    margin-top: 10px;
    color: white
}
.send-button > img {
    margin-top:12px;
    margin-left: 12px;
    width: 20px;
    height: 20px;
    filter: invert(100%);
}
#no-messages {
    position: fixed;
    left: 20px;
    bottom: 135px;
    color: white;
    text-align: left;
}
.message-icon {
    height: 40px;
    width: 40px;
    border-radius: 20px;
}
input {
  -webkit-appearance: none;
}
.chat-icon {
    position: fixed;
    right: 30px;
    cursor: pointer;
    z-index: 2;
}
.chat-icon > img {
    border-radius: 50px;
    border: 10px;
    width: 40px;
    height: 40px;
}
#unread-bubble {
    position: relative;
    border-radius: 10px;
    background-color: red;
    height: 16px;
    width: 16px;
    z-index: 3;
    margin-bottom: -10px;
    margin-left: 25px;
}
#unread-bubble > p {
    position: relative;
    padding: 0;
    margin: 0;
    font-size: 12px;
}
.chat-room {
    position: fixed;
    bottom: 0;
    left: 0;
    z-index: 4;
    height: 100vh;
    width: 100vw;
    background-color: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(5px);
    display: grid;
    grid-template-columns: 1;
    grid-template-rows: calc(100vh - 120px) 120px;
    justify-items: start;
    align-items: end;
    color: black;
    margin-top: 10px
}
.chat-room > .input-area {
    width: 100%;
    display: grid;
    justify-content: stretch;
    margin-bottom: auto;
    height: 120px;
}
.chat-room > .input-area > input {
    height: 120px;
    font-size: 15px;
    line-height: 20px;
    justify-self: stretch;
    padding-left: 20px;
    padding-right: 120px;
    border: 0 none;
    -webkit-appearance: none;
    background: white;
    color: black;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    border-bottom: 2px solid white;
    border-top: 2px solid white;
    padding-bottom: 50px;
}
#messages-background {
    width: 100vw;
    height: calc(100vh - 120px);
    position: fixed;
    top: 0;
    left: 0;
    z-index: 2;
}
.chat-room > .input-area > input:focus {
    outline-width: 0;
}
.chat-room > .input-area > hr {
    margin: 1rem 2rem 1rem 2rem;
    height: 1px;
    background-color: rgb(255, 255, 255, 0.1);
    border:none;
}
#closeChatButton {
    position: fixed;
    top: 30px;
    right: 0;
    padding: 2rem;
    filter: drop-shadow(0px 0px 8px red);
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
    z-index: 3;
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
    z-index: 5;
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
