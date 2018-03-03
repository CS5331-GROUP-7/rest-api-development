var API_ENDPOINT = "http://localhost:8080"

function ajax_get(url, callback) {
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

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

ajax_get(API_ENDPOINT + '/diary', function(data) {
    if (data.status) {
        var members = data.result;
        var output = "<p>All Diaries</p><ul>";
        for (var i = 0; i < members.length; i++) {
            var member = JSON.parse(members[i]);
            output += 
                "<li><div>" + 
                "Title: " + member["title"] + "<br>" +
                "Text: " + member["text"] + "<br>" +
                "Public: " + member["public"] + "<br>" +
                "<div></li>";
        }
        output += "</ul>";
        document.getElementById("diary-list").innerHTML = output;
        //document.getElementById("response_status").innerHTML = "Get Diary list succeeded";
    }
    else {
        document.getElementById("response_status").innerHTML = "Diary list failed";
    }
});
