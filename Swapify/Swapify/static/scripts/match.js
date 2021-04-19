// JavaScript source code

const SONG_API_ENDPOINT = "https://api.spotify.com/v1/recommendations?seed_genres=pop";
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

            const fetchOptions = {
                method: 'GET',
                headers: new Headers({
                    'Authorization': `Bearer ${ACCESS_TOKEN}`
                })
            };
            fetch(SONG_API_ENDPOINT, fetchOptions).then(function (response) {
                return response.json();
            }).then(function (json) {
                console.log(json);
                new_uri = (json['tracks'][0]['uri'].split(":")[2])
                console.log(new_uri);
                document.getElementById("songPlayer").src = "https://open.spotify.com/embed/track/" + new_uri;
        
            }).catch(function (error) {
                console.log(error);
            });

        }

    });

    
    //spotify fetch random song endpoint
    //return song uri
    //initialize spotify player object with random song uri from ^
})

//onclick nextsong
    //ajax to get access token -token, email
        //on success
            //post to the playlists
            //spotify api call to get uri document.getElementById("songPlayer").src = "https://open.spotify.com/embed/track/" + new_uri;