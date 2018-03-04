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

function registerSubmit() {
    var fullname = document.forms["registerForm"]["fullname"].value;
    var age = document.forms["registerForm"]["age"].value;
    var username = document.forms["registerForm"]["username"].value;
    var password = document.forms["registerForm"]["password"].value;
    var data = {
        'fullname': fullname,
        'age': age,
        'username': username,
        'password': password
    }

    ajax_post(API_ENDPOINT + '/users/register', data, function(data) {
        if (data.status) {
            document.getElementById("response_status").innerHTML = "Register User succeeded";
        }
        else {
            document.getElementById("response_status").innerHTML = "Register User failed";
        }
    });
    return false;
}

