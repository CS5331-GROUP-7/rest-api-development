var API_ENDPOINT = "http://localhost:8080"

function ajax_post_delete(url, data, callback) {
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

function ajax_post_toggle(url, data, callback) {
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
            //document.getElementById("demo_dbg").innerHTML = xmlhttp.responseText;
        }
    };

    xmlhttp.open("POST", url, true); 
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send("token="+localStorage.getItem("token"));
}

function deleteDiary(id) {
    var data ={
        id: id,
        token: localStorage.getItem("token")
    }
    ajax_post_delete(API_ENDPOINT + '/diary/delete', data, function(data) {
        if (data.status) {
            document.getElementById("response_status").innerHTML = "Users delete success";
        }
        else {
            document.getElementById("response_status").innerHTML = "Users delete failed";
        }
    });
    return false;
}


function toggleDiaryTo(id, to) {
    var data = {
        id: id,
        token: localStorage.getItem("token"),
        public: !to 
    }

    ajax_post_toggle(API_ENDPOINT + '/diary/permission', data, function(data) {
        if (data.status) {
            document.getElementById("response_status").innerHTML = "Users toggle permission success";
        }
        else {
            document.getElementById("response_status").innerHTML = "Users toggle permission failed";
        }
    });
    return false;          
}

ajax_post(API_ENDPOINT + '/diary', function(data) {
    if (data.status) {
        var members = data.result;
        var output = "<p>All Diaries</p><ul>";
        for (var i = 0; i < members.length; i++) {
            member = JSON.parse(members[i]);
            output += "<li><div>" + 
                "Title: " + member["title"] + "<br>" +
                "Text: " + member["text"] + "<br>" +
                "Public: " + member["public"] + "<br>" +
                "<div></li>";
            output += "<button onclick='deleteDiary("+ member["id"]+ ")'>Delete</button>";  
            var message = member["public"]? "Toggle to private": "Toggle to public";
            output += "<button onclick='toggleDiaryTo("+ member["id"]+"," +member["public"] +  ")'>" + message + "</button>"; 

        }
        output += "</ul>";
        document.getElementById("my-diary-list").innerHTML = output;
    }
    else {
        document.getElementById("my-diary-list").innerHTML = "Diary list failed";
    }
});