import axios from 'axios'
var url = ''

if (
    process.env.NODE_ENV == 'development' ||
            process.env.NODE_ENV == 'dev'
) {
    url = `http://${process.env.VUE_APP_SERVER_URL}/api/`;
} else {
    url = `https://${process.env.VUE_APP_SERVER_URL}/api/`;
}

export default {
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
    async getAlbumArt(uri) {
        var token = localStorage.getItem('access_token');
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



