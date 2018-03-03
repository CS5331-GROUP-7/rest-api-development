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
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send("title="+data.title+"&text="+data.text+"&public="+data.public+"&token="+data.token);
}

function createDiary() {
    var title = document.forms["diaryForm"]["title"].value;
    var text = document.forms["diaryForm"]["text"].value;
    var public = document.forms["diaryForm"]["public"].value;
    var token = localStorage.getItem("token");

    console.log(public);
    var data = {
        'title': title,
        'text': text,
        'token': token,
        'public': (public === "true")? true: false
    }

    ajax_post(API_ENDPOINT + '/diary/create', data, function(data) {
    if (data.status) {
            console.log('success');
            document.getElementById("response_status").innerHTML = "Users success" + data;
    }
    else {
        document.getElementById("response_status").innerHTML = "Users failed";
    }
    console.log(data);
    });
    return false;
}


