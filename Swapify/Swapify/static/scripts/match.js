// JavaScript source code

const SONG_API_ENDPOINT = "https://api.spotify.com/v1/recommendations?seed_genres=";
let ACCESS_TOKEN;
let new_uri;

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

$(function () { 
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
            //creates endpoint
            endpoint = SONG_API_ENDPOINT + document.getElementById('genre').innerHTML;
            const fetchOptions = {
                method: 'GET',
                headers: new Headers({
                    'Authorization': `Bearer ${ACCESS_TOKEN}`
                })
            };
            //gets endpoint and json of reccommended song data
            fetch(endpoint, fetchOptions).then(function (response) {
                return response.json();
            }).then(function (json) {
                console.log(json);
                //obtains spotify song ID
                new_uri = (json['tracks'][0]['uri'].split(":")[2])
                console.log(new_uri);
                //fills in Mood Match page HTML with specific song info to play
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
    //series of if statements to help determine which flask route to call
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
            //gets current song ID and length to add to playlist
            let url = document.getElementById("songPlayer").src; 
            let song_length = document.getElementById("length").innerHTML;
            song_uri = url.split("track/")[1];

            var songData = {
                //all the data that will be used in the flask route
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
                    //creates endpoint URL
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
                        //gets next song info and updates HTML file
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
    //This function specifies genre of displayed songs
    //Songs will stay the same genre unless specified differently
    //genre is passed in as an argument
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