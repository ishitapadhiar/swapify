// JavaScript source code




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
    console.log("MY id is: " + getIDCookie())
    //use cookie to get user row from db, including access token
    //use access token to make spotify endpoint calls

    var tdata = {
        cookie: "1"
    }
    $.ajax({
        url: "/user",
        type: 'GET',
        dataType: "json",
        contentType: "application/json",
        data: tdata,
        async: false,
        success: function (data) {
            console.log("vue created");
            //data.spotifyauth access token
            //save the token to a local var
            

        }

    });
    //spotify fetch random song endpoint
    //return song uri
    //initialize spotify player object with random song uri from ^
})