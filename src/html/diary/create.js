var API_ENDPOINT = "http://localhost:8080"

function ajax_post(url, data, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 201) {
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

function createDiary() {
    var title = document.forms["diaryForm"]["title"].value;
    var text = document.forms["diaryForm"]["text"].value;
    var public = document.forms["diaryForm"]["public"].value;
    var token = localStorage.getItem("token");

    var data = {
        'title': title,
        'text': text,
        'token': token,
        'public': (public === "true")? true: false
    }

    ajax_post(API_ENDPOINT + '/diary/create', data, function(data) {
        if (data.status) {
            document.getElementById("response_status").innerHTML = "Create diary success";
        }
        else {
            document.getElementById("response_status").innerHTML = "Create diary failed";
        }
    });
    return false;
}


