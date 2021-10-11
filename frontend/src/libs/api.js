/*
Collection of functions for interacting with our API. 
 */

import axios from 'axios'
import store from '../store';

var url = ''

url = `${process.env.VUE_APP_PROTOCOL}://${process.env.VUE_APP_SERVER_URL}/api`;

export default {
    // Used for getting all information about a room results.
    async getRoomResults(code) {
        axios
            .get(`${url}/${code}/results`)
            .then(function (response) {
                return response.data;
            })
            .catch(function (err) {
                return err
            });
    },
    // Used for getting all played games codes for a specific player
    async getPersonalResults(username) {
        var result = null
        await axios
            .get(`${url}/me/${username}/results`)
            .then(function (response) {
                result = response;
            })
            .catch(function (err) {
                result =  err
            });
        return result
    },
    // Gets the album art from spotify API. 
    async getAlbumArt(uri) {
        var token = store.getters.getAccessToken;
        var result = ''
        await axios
            .get(`https://api.spotify.com/v1/tracks/${uri}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                },
            })
            .then(function (response) {
                result = response.data.album.images[0].url
            });
        return result
    },
};



