// JavaScript source code

//const { get } = require("jquery");

const API_ENDPOINT = 'https://api.spotify.com/v1/me';
let ACCESS_TOKEN;
let DISPLAY_NAME;

function getAccessToken() {
    const currentLocation = String(window.location).split('#')[1];
    const params = new URLSearchParams(currentLocation);
    return params;
}
function fetchProfileInformation() {
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

        $.ajax({
            url: "/user",
            type: 'POST',
            //processData: false,
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(tdata),
            success: function (data) {
                //alert("it worked");
                console.log(data);
            },


        });

    }).catch(function (error) {
        console.log(error);
    });
}
$(function () {
    //x = getAccessToken().get('access_token');
    
    fetchProfileInformation()
    console.log(ACCESS_TOKEN);


    

    
    //alert(document.cookie)
});