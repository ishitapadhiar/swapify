// JavaScript source code

var tdata = {
    id: getIDCookie(),
}
//vue app for data bindings
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
            //save bio
            console.log("saving bio...");
            var self = this;
            console.log(self.items);
            var sdata = {
                token: self.items.spotify_auth,
                display_name: self.items.first_name,
                email: self.items.email,
                bio: self.items.bio,
            }
            console.log(sdata);
            $.ajax({
                url: "/user",
                type: 'POST',
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(sdata),
                success: function (data) {
                    console.log("post successful");
                }
            })
            console.log("saving");
            this.isEdit = !this.isEdit;
        }
    },
    created: function () {
        //get request to db on vue instance creation
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

//function to get Swapify ID cookie
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


function addFriend() {
    // This function is called when a user clicks the button to add a friend
    var remail = document.forms["friendForm"]["friendName"].value;
    if (remail == "") {
        alert("Email must be filled out.");
      }
      var tdata = {
        id: getIDCookie()
    }
    $.ajax({
        //calls user route to obtain the current user's email
        async: false,
        url: "/user",
        type: 'GET',
        dataType: "json",
        contentType: "application/json",
        data: tdata,
        success: function (data) {
            console.log(data);
            var userData = {
                //all the data that will be used in the flask route
                userEmail: data.email,
                friendEmail: remail
            }
            console.log(userData);
            $.ajax({
                async: false,
                url: "/addFriend",
                type: 'POST',
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(userData),
                success: function() {
                    //if adding a friend is successful
                    console.log("friend added");
                    alert("Friend added!");
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    //if adding a friend causes an error
                    alert("Error: User does not exist or user has already been added");
                }
            });         
        }
    });
}

$(function () {
    console.log("My id is: " + getIDCookie())

    
})