// JavaScript source code

const SONG_API_ENDPOINT = "https://api.spotify.com/v1/recommendations?seed_genres=";
let ACCESS_TOKEN;
let new_uri;

function getIDCookie() {
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

$(function () {
    console.log("My id is: " + getIDCookie())
    //use cookie to get user row from db, including access token
    //use access token to make spotify endpoint calls
    var tdata = {
        id: getIDCookie()
    }
    $.ajax({
        url: "/user",
        type: 'GET',
        dataType: "json",
        contentType: "application/json",
        data: tdata,
        success: function (data) {
            console.log(data);
            ACCESS_TOKEN = data.spotify_auth
            endpoint = SONG_API_ENDPOINT + document.getElementById('genre').innerHTML;

            const fetchOptions = {
                method: 'GET',
                headers: new Headers({
                    'Authorization': `Bearer ${ACCESS_TOKEN}`
                })
            };
            fetch(endpoint, fetchOptions).then(function (response) {
                return response.json();
            }).then(function (json) {
                console.log(json);
                new_uri = (json['tracks'][0]['uri'].split(":")[2])
                console.log(new_uri);
                document.getElementById("songPlayer").src = "https://open.spotify.com/embed/track/" + new_uri;
                document.getElementById("length").innerHTML = json['tracks'][0]['duration_ms']  
                document.getElementById('genre').innerHTML = document.getElementById('genre').innerHTML;

            }).catch(function (error) {
                console.log(error);
            });

        }

    });
})

function addSong(mood) {
    let moodRoute;
    if (mood == "happy"){
        moodRoute = '/addHappySong';
    }
    if (mood == "sad"){
        moodRoute = '/addSadSong';
    }
    if (mood == "study"){
        moodRoute = '/addStudySong';
    }
    if (mood == "party"){
        moodRoute = '/addPartySong';
    }
    var tdata = {
        id: getIDCookie()
    }
    $.ajax({
        url: "/user",
        type: 'GET',
        dataType: "json",
        contentType: "application/json",
        data: tdata,
        success: function (data) {
            console.log(data);
            ACCESS_TOKEN = data.spotify_auth
            let url = document.getElementById("songPlayer").src;
            let song_length = document.getElementById("length").innerHTML;
            song_uri = url.split("track/")[1];
            console.log(song_uri);
            console.log(song_length)

            var songData = {
                token: data.spotify_auth,
                email: data.email,
                uri: song_uri,
                length: song_length
            }
            console.log(songData);
            $.ajax({
                url: moodRoute,
                type: 'POST',
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(songData),
                success: function (sData) {
                    console.log(sData)
                    endpoint = SONG_API_ENDPOINT + document.getElementById('genre').innerHTML;
                    const fetchOptions = {
                        method: 'GET',
                        headers: new Headers({
                            'Authorization': `Bearer ${ACCESS_TOKEN}`
                        })
                    };
                    fetch(endpoint, fetchOptions).then(function (response) {
                        return response.json();
                    }).then(function (json) {
                        console.log(json);
                        new_uri = (json['tracks'][0]['uri'].split(":")[2])
                        console.log(new_uri);
                        document.getElementById("songPlayer").src = "https://open.spotify.com/embed/track/" + new_uri;
                        document.getElementById("length").innerHTML = json['tracks'][0]['duration_ms']  
                        document.getElementById('genre').innerHTML = document.getElementById('genre').innerHTML;
                    }).catch(function (error) {
                        console.log(error);
                    });

                },
            });

            

        }

    });
}

function addGenre(genre) {
    var tdata = {
        id: getIDCookie()
    }
    $.ajax({
        url: "/user",
        type: 'GET',
        dataType: "json",
        contentType: "application/json",
        data: tdata,
        success: function (data) {
            console.log(data);
            ACCESS_TOKEN = data.spotify_auth
            endpoint = SONG_API_ENDPOINT + genre;
            const fetchOptions = {
                method: 'GET',
                headers: new Headers({
                    'Authorization': `Bearer ${ACCESS_TOKEN}`
                })
            };
            fetch(endpoint, fetchOptions).then(function (response) {
                return response.json();
            }).then(function (json) {
                console.log(json);
                new_uri = (json['tracks'][0]['uri'].split(":")[2])
                console.log(new_uri);
                document.getElementById("songPlayer").src = "https://open.spotify.com/embed/track/" + new_uri;
                document.getElementById("length").innerHTML = json['tracks'][0]['duration_ms']  
                document.getElementById('genre').innerHTML = genre;
        
            }).catch(function (error) {
                console.log(error);
            });

        }

    });
}