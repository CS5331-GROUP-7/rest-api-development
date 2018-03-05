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

function deleteDiary(id) {
    var data ={
        id: id,
        token: localStorage.getItem("token")
    }
    ajax_post(API_ENDPOINT + '/diary/delete', data, function(data) {
        if (data.status) {
            document.getElementById("response_status").innerHTML = "Users delete success";
            window.location.reload();
        }
        else {
            document.getElementById("response_status").innerHTML = "Users delete failed";
        }
    });
}


function toggleDiaryTo(id, to) {
    var data = {
        id: id,
        token: localStorage.getItem("token"),
        public: !to 
    }

    ajax_post(API_ENDPOINT + '/diary/permission', data, function(data) {
        if (data.status) {
            document.getElementById("response_status").innerHTML = "Users toggle permission success";
            window.location.reload();
        }
        else {
            document.getElementById("response_status").innerHTML = "Users toggle permission failed";
        }
    });
}

ajax_post(API_ENDPOINT + '/diary', {'token': localStorage.getItem('token')}, function(data) {
    if (data.status) {
        var members = data.result;
        var output = "<ul>";
        for (var i = 0; i < members.length; i++) {
            member = JSON.parse(members[i]);
            output += "<div class='form-group row'>" + 
                "<div class='col-sm-12'>Title: " + member["title"] + "</div>" +
                "<div class='col-sm-12'>Text: " + member["text"] + "</div>" +
                "<div class='col-sm-12'>Public: " + member["public"] + "</div>";
            output += "<div class='col-sm-12'><button class='btn btn-danger' onclick='deleteDiary("+ member["id"]+ ")'>Delete</button>";  
            var message = member["public"]? "Toggle to private": "Toggle to public";
            output += "<button class='btn btn-info' onclick='toggleDiaryTo("+ member["id"]+"," +member["public"] +  ")'>" + message + "</button></div></div>"; 

        }
        output += "</ul>";
        document.getElementById("my-diary-list").innerHTML = output;
    }
    else {
        document.getElementById("my-diary-list").innerHTML = "Diary list failed";
    }
});
