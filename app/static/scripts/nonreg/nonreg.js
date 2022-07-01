function launchForm(urlSend)
{
    console.log(JSON.stringify($('#launchRequest').serializeJSON()))
    $.ajax({
        type: 'POST',
        url: urlSend,
        data: JSON.stringify($('#launchRequest').serializeJSON()),
        contentType: "application/json",
        success: function (data) {
            //document.getElementById("div-form").innerHTML = data;
            alert(data)
        }
    });
}
function loadfunctions()
{
      setTimeout(getRequests, interval);
}

function truncate(str, n){
  return (str.length > n) ? str.substr(0, n-1) + '&hellip;' : str;
}
function syntaxHighlight(json) {
    if (typeof json != 'string') {
         json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + truncate(match,50) + '</span>';
    });
}
var interval = 2000;
var lastRequest = null;
function getRequests() {
    var urlGetRequests =  "/web/unit-tests/getProcessingRequests";
    if(lastRequest != null)
        urlGetRequests += "?lastRequestId=" + lastRequest;
    $.ajax({
            type: 'GET',
            url: urlGetRequests,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (data) {
                console.log(data);
                //alert(data[0].date_request + data[0].ocpi_request_id);
                lastRequest = data.maxId;

                for (var i in data.json_list) {

                    var req_obj = data.json_list[i];

                    document.getElementById("result").innerHTML = "<div class=\"card\" type=\"button\" data-toggle=\"collapse\" data-target=\"#collapse" + req_obj.non_regression_id + "\"" +
                                    "aria-expanded=\"false\" aria-controls=\"collapse" + req_obj.non_regression_id + "\">" +
                                req_obj.non_regression_id +
                            "</div>" +
                            "<div class=\"collapse\" id=\"collapse" + req_obj.non_regression_id + "\">" +
                                "<div class=\"card card-body\"><pre style=\"white-space: pre-wrap;\">" +
                                    req_obj.status +
                                "</pre></div>" +
                            "</div>" + "<br/><br/>" + document.getElementById("result").innerHTML;
                }
            },
            complete: function (data) {
                   setTimeout(getRequests, interval);
            }
    });
}
document.onload = loadfunctions();