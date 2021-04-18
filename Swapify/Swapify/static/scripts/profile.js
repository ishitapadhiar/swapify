// JavaScript source code

tdata = {
    id : "17"
}

var app = new Vue({
    el: "profile",
    delimiters: ['[[', ']]'],
    data: {
        items: []
    },
    created: function () {
        id = getIDCookie()
        console.log("in mount");
        $.ajax({
            url: "/user",
            type: 'GET',
            dataType: "json",
            contentType: "application/json",
            data: tdata,
            success: function () {
                console.log("vue created");
            }

        });
    }
});


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
            return c.substring(name.length, c.length-path.length);
        }
    }
    return "";
}

$(function () {
    console.log("MY id is: "+getIDCookie())
})