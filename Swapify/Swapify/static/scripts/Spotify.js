// JavaScript source code


const API_ENDPOINT = 'https://api.spotify.com/v1/me';
let ACCESS_TOKEN;

function getAccessToken() {
    const currentLocation = String(window.location).split('#')[1];
    const params = new URLSearchParams(currentLocation);
    return params;
}
function getProfileInformation() {
    const currentQueryParameters = getAccessToken();
    ACCESS_TOKEN = currentQueryParameters.get('access_token');

    const fetchOptions = {
        method: 'GET',
        headers: new Headers({
            'Authorization': `Bearer ${ACCESS_TOKEN}`
        })
    };

    fetch(API_ENDPOINT, fetchOptions).then(function (response) {
        return response.json();
    }).then(function (json) {
        console.log(json);
        DISPLAY_NAME = json.display_name;

        var tdata = {
            token: ACCESS_TOKEN,
            display_name: json.display_name,
            email: json.email,

        }
        //request to save user in datatable
        $.ajax({
            url: "/user",
            type: 'POST',
            //processData: false,
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(tdata),
            success: function (data) {
                console.log(data);
                //make user cookie here from return id
                setIDCookie(data.id)
            },
        });

    }).catch(function (error) {
        console.log(error);
    });
}

function setIDCookie(id) {
    document.cookie = "SwapifyID=" + id + ",path=/";
}

function getIDCookie() {
    var name = "SwapifyID=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

$(function () {
    getProfileInformation()
    console.log(ACCESS_TOKEN);
});

