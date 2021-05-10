<template>
    <div v-if="existingPlaylist" class="existing-playlist">
        <p>existing</p>
    </div>
    <div v-else-if="newPlaylist" class="new-playlist">
        <p>New</p>
    </div>
    <div v-else>      
        <div>
            <div v-for="track in tracks" :key="track" :class="{ iconlist: track[1]}">
                <TrackIcon
                    :trackid="track[0]"
                    @click="selectTrack(tracks.indexOf(track))"
                />
            </div>
        </div>
        <select v-model="selectedPlaylist" class="drop-down">
            <option v-for="playlist in userPlaylists" :key="playlist" :value="playlist[1]">
                {{ playlist[0] }}
            </option>
        </select> 
        <p>Add {{ nrOfTrackstoAdd }} songs to:</p>
        <Button
            button-text="Existing playlist"
            @click="addToPlaylist()"
        />
        <Button
            button-text="New playlist"
            @click="createNewPlaylist()"
        />
    </div>
</template>

<script>

import Button from '../components/Button';
import TrackIcon from '../components/TrackIcon';

const axios = require('axios');

export default {
    name: 'Playlist',
    components:{
        Button,
        TrackIcon,
    },
    data: function () {
        return {
            code: this.$route.params.code,
            tracks: this.$store.state.tracksForPlaylist,
            userPlaylists: [],
            selectedPlaylist: '',
            existingPlaylist: false,
            newPlaylist: false,
            nrOfTrackstoAdd: this.$store.state.nrOfTrackstoAdd,

        };
    },
    mounted(){
        var token = localStorage.getItem('access_token');
        var user_id = localStorage.getItem('user_id');
        var self = this;
        axios
            .get(
                `https://api.spotify.com/v1/users/${user_id}/playlists`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        Accept: 'application/json',
                        'Content-Type': 'application/json',
                    },
                }
            ).then(function (response) {
                for(let item of response.data.items){
                    //console.log(item)
                    //allow user to modify their own + collaborative playlists
                    if((item.owner.id == user_id) || (item.owner.id != user_id && item.collaborative == true)){
                        self.userPlaylists.push([item.name, item.id])
                    }
                    //TODO sort data
                }
            });
    },
    methods:{
        log(){
            //console.log(this.tracks);
            //console.log(this.userPlaylists);  
            console.log(this.selectedPlaylist)
        },
        selectTrack(index){
            //change boolean value associated with track in store
            this.$store.commit('updateTracksForPlaylist', index)
        },
        addToPlaylist(){
            this.existingPlaylist = true;
            // for(let track of this.tracks){
            //     if(track[1] == true){
                    
            //     }
            // }
        },
        createNewPlaylist(){
            this.newPlaylist = true;
        }
    }

}
</script>

<style scoped>
.iconlist{
    background: linear-gradient(90deg, rgba(25,20,20,1) 0%, rgba(29,185,84,1) 100%);
    border-radius: 0 40px 40px 0;
    margin-right: 5px;
    }
.new-playlist{
    height
}
.existing-playlist{

}
</style>