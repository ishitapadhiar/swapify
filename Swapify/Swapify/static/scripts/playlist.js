// JavaScript source code

const SONG_API_ENDPOINT = "https://api.spotify.com/v1/recommendations?seed_genres=";
let ACCESS_TOKEN;
let new_uri;
// JavaScript source code

var tdata = {
    id: getIDCookie(),
}

// var self = this, self.happyplaylist => returns array of spotify uri's 
function getIDCookie() {
    //return access token from cookie
    var name = "SwapifyID=";
    var path = ",path=/";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length - path.length);
        }
    }
    return "";
}
function displayPlaylist(mood){
    var tdata = {
        id: getIDCookie()
    }
    $.ajax({
        async: false,
        url: "/user",
        dataType: "json",
        contentType: "application/json",
        data: tdata,
        success: function(data) {
            console.log(data)
            ACCESS_TOKEN = data.spotify_auth
            if (mood == "happy"){
                songlist = data.happysongs;
            }

            for (song in songlist){
                endpoint = SONG_API_ENDPOINT + song;
                const fetchOptions = {
                    method: 'GET',
                    headers: new Headers({
                        'Authorization': `Bearer ${ACCESS_TOKEN}`
                    })
                };
                fetch(endpoint, fetchOptions).then(function(response) {
                    return response.json();
                }).then(function (json) {
                    console.log(json);
                    new_name = (json.name)
                    // new_uri = (json['tracks'][0]['uri'].split(":")[2])
                    // test_name = (json['tracks'][0]['name'])
                    // test_artist = (json['tracks'][0]['artists'][0].name)
                    console.log(new_name)
                    document.getElementById("playlist").innerHTML = new_name;
                    // console.log(test_artist)
                    // console.log(new_uri);
                    document.getElementById("songPlayer").src = "https://open.spotify.com/embed/track/" + new_uri;
                    document.getElementById("length").innerHTML = json['tracks'][0]['duration_ms']
                    document.getElementById('genre').innerHTML = genre;

                }).catch(function (error) {
                    console.log(error);
                });
            }
        }, 
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            //if choosing a genre causes an error
            alert("Error: cannot select genre");
        }
    });
}

function addGenre(genre) {
    //This function specifies genre of displayed songs
    //Songs will stay the same genre unless specified differently
    //genre is passed in as an argument
    var tdata = {
        id: getIDCookie()
    }

    var self = this
    var playlistData = self.songList

    $.ajax({
        async: false,
        url: "/user",
        type: 'GET',
        dataType: "json",
        contentType: "application/json",
        data: tdata,
        success: function (data) {
            console.log(data);
            ACCESS_TOKEN = data.spotify_auth

            //endpoint = "https://api.spotify.com/v1/tracks/" + uri
            endpoint = SONG_API_ENDPOINT + genre;
            // add the uri to the end of the link in order to get the information
            // for uri in the list of songs, get uri and add to end
            endpointtest = "https://api.spotify.com/v1/tracks/5Pgq1Gfeth2CuUhyCXwlfC"
            console.log(endpoint)
            const fetchOptions = {
                method: 'GET',
                headers: new Headers({
                    'Authorization': `Bearer ${ACCESS_TOKEN}`
                })
            };
            fetch(endpointtest, fetchOptions).then(function (response) {
                return response.json();
            }).then(function (json) {
                console.log(json);
                new_name = (json.name)
                // new_uri = (json['tracks'][0]['uri'].split(":")[2])
                // test_name = (json['tracks'][0]['name'])
                // test_artist = (json['tracks'][0]['artists'][0].name)
                console.log(new_name)
                document.getElementById("playlist").innerHTML = new_name;
                // console.log(test_artist)
                // console.log(new_uri);
                document.getElementById("songPlayer").src = "https://open.spotify.com/embed/track/" + new_uri;
                document.getElementById("length").innerHTML = json['tracks'][0]['duration_ms']
                document.getElementById('genre').innerHTML = genre;

            }).catch(function (error) {
                console.log(error);
            });

        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            //if choosing a genre causes an error
            alert("Error: cannot select genre");
        }

    });