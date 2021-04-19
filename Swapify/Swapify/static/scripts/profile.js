// JavaScript source code

var tdata = {
    id: getIDCookie(),
}

var app = new Vue({
    el: "#profile",
    delimiters: ['[[', ']]'],
    data: {
        isEdit: false,
        counter: 0,
        items: []
    },
    methods: {
        savebio: function () {
            this.isEdit = !this.isEdit;
            this.counter++;
            console.log("saving");
        }
    },
    created: function () {
        console.log("in mount");
        var self = this;
        $.ajax({
            url: "/user",
            type: 'GET',
            dataType: "json",
            contentType: "application/json",
            data: tdata,
            success: function (data) {
                console.log(data);
                self.items = data;
            }

        });
    },

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
    console.log("MY id is: " + getIDCookie())

    
})