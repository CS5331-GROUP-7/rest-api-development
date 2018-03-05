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

function submitLogin() {
    var username = document.forms["loginForm"]["username"].value;
    var password = document.forms["loginForm"]["password"].value;
    var data = {
        'username': username,
        'password': password
    }

    ajax_post(API_ENDPOINT + '/users/authenticate', data, function(data) {
        if (data.status) {
            localStorage.setItem("token", data.result.token);
            document.getElementById("response_status").innerHTML = "<div class='alert alert-info'>Login User succeeded</div>";
        }
        else {
            document.getElementById("response_status").innerHTML = "<div class='alert alert-info'>Login User failed</div>";
        }
    });
    return false;
}

