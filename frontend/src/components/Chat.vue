/* 
Player avatar implemented in the game waiting room. Displays if the person is host or not and the name of the player. 
Takes player name, color, and host as arguments. 

Component also implemented as guessing icon when game has started.
*/

<template>
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
</template>

<script>
import ChatAvatar from '../components/ChatAvatar.vue'
import CloseButton from '../components/CloseButton.vue'

export default {
    name: 'PlayerAvatar',
    components: {
        ChatAvatar,
        CloseButton
    },
    props: {
        chat: {
            type: Boolean,
            default: false
        },
        players: {
            type: Array,
            default: []
        },
    },
    data() {
        return {
            chat: false,
            messages: []
        }
    },
    sockets: {
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
        scrollToBottom() {
            this.$nextTick(() => {
                let chat = document.getElementById("chat-end")
                if(chat) {
                    chat.scrollIntoView({ behavior: "smooth", block: "end" });
                }
            })
        },
        sendMessage(event) {
            if(event.target.value.length > 0) {
                this.$socket.client.emit('send_message', {
                    sid: this.$store.getters.getSid,
                    message: event.target.value,
                    code: this.code
                });
                event.target.value = ""
            } else {
                //
            }
        },
    }
};
</script>

<style scoped>

</style>
