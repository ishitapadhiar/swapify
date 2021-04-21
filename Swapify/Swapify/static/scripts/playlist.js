// JavaScript source code

const SONG_API_ENDPOINT = "https://api.spotify.com/v1/tracks/";
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
            //console.log(data)
            ACCESS_TOKEN = data.spotify_auth
            if (mood == "happy"){
                songlist = data.happysongs;
                document.getElementById("title_playlist").innerHTML = "Happy Playlist";
            }
            if(mood =="sad"){
                songlist = data.sadsongs;
                document.getElementById("title_playlist").innerHTML = "Sad Playlist";
            }
            if(mood == "study"){
                songlist = data.studysongs;
                document.getElementById("title_playlist").innerHTML = "Study Playlist";
            }
            if(mood == "party"){
                songlist = data.partysongs;
                document.getElementById("title_playlist").innerHTML = "Party Playlist";
            }

            //console.log(songlist)
            document.getElementById("playlist").innerHTML = ""
            for (song in songlist){
                //console.log(songlist[song]);
                endpoint = SONG_API_ENDPOINT + songlist[song];
                //console.log(endpoint)
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
                    //console.log(new_name)
                    document.getElementById("playlist").innerHTML += "<li>" + new_name + "</li>";
                    // console.log(test_artist)
                    // console.log(new_uri);
                    //document.getElementById("songPlayer").src = "https://open.spotify.com/embed/track/" + new_uri;
                    //document.getElementById("length").innerHTML = json['tracks'][0]['duration_ms']
                    //sdocument.getElementById('genre').innerHTML = genre;

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
