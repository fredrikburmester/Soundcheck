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
                console.log(response)
            })
            .catch(function (err) {
                console.log("Error: ", err)
                result = null
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
    async getTopSongsForUser(time_range, nr_songs, token) {
        var trackIds = []
        await axios
            .get(
                `https://api.spotify.com/v1/me/top/tracks?time_range=${time_range}&limit=${nr_songs}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        Accept: 'application/json',
                        'Content-Type': 'application/json',
                    },
                }
            )
            .then(function (response) {
                (response.data.items)
                if(response.data.items.length > 0) {
                    response.data.items.forEach(item => {
                        trackIds.push(item.uri.split(':')[2])
                    });
                }
            });
        return trackIds

    }
};



