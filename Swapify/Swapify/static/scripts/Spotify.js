// JavaScript source code


const ACCESS_TOKEN

function getAccessToken() {
    const currentLocation = String(window.location).split('#')[1];
    const params = new URLSearchParams(currentLocation);
    return params;
}
function fetchProfileInformation() {
    const currentQueryParameters = getCurrentQueryParameters();
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
        updateProfileInformation(json);
    }).catch(function (error) {
        console.log(error);
    });
}
$.ajax({
    url: 'https://api.spotify.com/v1/me',
    headers: {
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    },
    success: function (response) {
        alert('success!');
   }