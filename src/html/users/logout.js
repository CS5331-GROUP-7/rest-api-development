var API_ENDPOINT = "http://localhost:8080"

function ajax_post(url, data, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            console.log('responseText:' + xmlhttp.responseText);
            try {
                var data = JSON.parse(xmlhttp.responseText);
            } catch(err) {

                document.getElementById("demo_dbg").innerHTML = err.message + " in " + xmlhttp.responseText;
                console.log(err.message + " in " + xmlhttp.responseText);
                return ;
            }
            callback(data);
        }else{
            document.getElementById("demo_dbg").innerHTML = xmlhttp.responseText;
        }
    };

    xmlhttp.open("POST", url, true); 
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.send(JSON.stringify(data));
}

ajax_post(API_ENDPOINT + '/users', {'token': localStorage.getItem("token")}, function(data) {
    if (data.status) {
        var member = JSON.parse(data.result);
        var output = "<div class='form-group'>" + 
                "<div class='row'>Full name: " + member["fullname"] + "</div>" +
                "<div class='row'>Username: " + member["username"] + "</div>" +
                "<div class='row'>Age: " + member["age"] + "</div>" +
                "<div>";
    
        document.getElementById("user-account").innerHTML = output;
        document.getElementById("response_status").innerHTML = "Get User account succeeded";
    }
    else {
        document.getElementById("response_status").innerHTML = "Get User account failed";
    }
});

function logout() {
    ajax_post(API_ENDPOINT + '/users/expire', {'token': localStorage.getItem("token")}, function(data) {
    if (data.status) {
        localStorage.setItem("token", '');
        document.getElementById("response_status").innerHTML = "User logout succeeded";
    }
    else {
        document.getElementById("response_status").innerHTML = "User logout failed";
    }
});
}



