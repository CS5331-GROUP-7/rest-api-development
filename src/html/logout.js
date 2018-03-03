var API_ENDPOINT = "http://localhost:8080"

function ajax_post(url, callback) {
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
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send("token="+localStorage.getItem("token"));
}

ajax_post(API_ENDPOINT + '/users/expire', function(data) {
    if (data.status) {
        localStorage.setItem("token", '');
        document.getElementById("response_status").innerHTML = "User logout succeeded";
    }
    else {
        document.getElementById("response_status").innerHTML = "User logout failed";
    }
});



