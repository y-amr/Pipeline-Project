function selectVersionChange(){
        $('#select-role').val("");
        $('#select-module').val("");
        $('#select-fromto').val("");
        $('#select-webservices').val("");
        document.getElementById("div-module").style.display="none";
        document.getElementById("div-webservices").style.display="none";
        document.getElementById("div-fromto").style.display="none";
        if($('#select-versions').val() != "")
            document.getElementById("div-role").style.display="block";
         else
            document.getElementById("div-role").style.display="none";
}

function loadfunctions()
{
    $('#select-versions').change(selectVersionChange);


    $('#select-role').change(function(){
        $('#select-module').val("");
        $('#select-fromto').val("");
        $('#select-webservices').val("");
        document.getElementById("div-form").style.display="none";
        document.getElementById("div-module").style.display="none";
        document.getElementById("div-webservices").style.display="none";
        document.getElementById("div-fromto").style.display="none";
        if($(this).val() != ""){
            $.ajax({
                    type: 'GET',
                    url: "/web/unit-tests/ocpimodules?ocpi_version=" + $('#select-versions').val(),
                    data: $(this).serialize(),
                    dataType: 'json',
                    success: function (data) {
                        $('#select-module').find('option').remove().end();
                        var o = new Option("", "");
                        $(o).html("");
                        $("#select-module").append(o);
                        for (var i in data.json_list) {
                            var o = new Option(data.json_list[i].module_name, data.json_list[i].id);
                            $(o).html(data.json_list[i].module_name);
                            $("#select-module").append(o);
                        }
                        document.getElementById("div-module").style.display="block";
                    },
                    complete: function (data) {
                    }
            });
         }
        else
            document.getElementById("div-module").style.display="none";
    });

    $('#select-module').change(function(){
        $('#select-fromto').val("");
        $('#select-webservices').val("");
        document.getElementById("div-form").style.display="none";
        document.getElementById("div-webservices").style.display="none";
        if($(this).val() != "")
            document.getElementById("div-fromto").style.display="block";
        else
            document.getElementById("div-fromto").style.display="none";
    });

     $('#select-fromto').change(function(){
        $('#select-webservices').val("");
        document.getElementById("div-form").style.display="none";
        if($(this).val() != ""){
            $.ajax({
                type: 'GET',
                url: "/web/unit-tests/webservices?module_id=" + $('#select-module').val() + "&role_id=" + $('#select-role').val() + "&type=" + $('#select-fromto').val(),
                data: $(this).serialize(),
                dataType: 'json',
                success: function (data) {
                    $('#select-webservices').find('option').remove().end();
                        if(data.json_list.length == 0)
                        {
                            var o = new Option("No webservice", "");
                            $(o).html("No webservice");
                            $("#select-webservices").append(o);
                        }
                        else
                        {
                             var o = new Option("", "");
                            $(o).html("");
                            $("#select-webservices").append(o);
                            for (var i in data.json_list) {
                                var o = new Option(data.json_list[i].webservice_name, data.json_list[i].webservice_id);
                                $(o).html(data.json_list[i].webservice_name);
                                $("#select-webservices").append(o);
                            }
                        }
                        document.getElementById("div-webservices").style.display="block";
                },
                complete: function (data) {
                }
            });
         }
         else
            document.getElementById("div-webservices").style.display="none";
    });

    $('#select-webservices').change(function(){

        if($(this).val() !== ""){
            $.ajax({
                type: 'GET',
                url: "/web/unit-tests/webservice-form?webservice_id=" + $('#select-webservices').val(),
                data: $(this).serialize(),
                success: function (data) {
                    document.getElementById("div-form").style.display="block";
                    document.getElementById("div-form").innerHTML = data;
                },
                complete: function (data) {
                }
            });
        }
    });

    setTimeout(getRequests, interval);

}

function clearAll() {
        $('#select-versions').val("");
        selectVersionChange();
    }


var interval = 2000;
var lastRequest = null;
function getRequests() {
    var urlGetRequests =  "/web/unit-tests/getRequests";
    if(lastRequest != null)
        urlGetRequests += "?lastRequestId=" + lastRequest;
    $.ajax({
            type: 'GET',
            url: urlGetRequests,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (data) {
                showResults(data);
                //alert(data[0].date_request + data[0].ocpi_request_id);
                lastRequest = data.maxId;
/*
                for (var i in data.json_list) {

                    var req_obj = data.json_list[i];
                    var buttonColor = "success";
                    if(req_obj.status == "KO")
                        buttonColor = "danger";
                    else if(req_obj.status == "OK_BUT_WARNING")
                        buttonColor = "warning";

                    document.getElementById("result").innerHTML = "<button class=\"btn btn-" + buttonColor + "\" type=\"button\" data-toggle=\"collapse\" data-target=\"#collapse" + req_obj.id + "\"" +
                                    "aria-expanded=\"false\" aria-controls=\"collapse" + req_obj.id + "\">" +
                                req_obj.date_report + " => Role : " + req_obj.ocpi_role_name + " | Webservice : " + req_obj.iop_webservice_name + " | Way : " + req_obj.iop_webservice_type +
                            "</button>" +
                            "<div class=\"collapse\" id=\"collapse" + req_obj.id + "\">" +
                                "<div class=\"card card-body\"><pre style=\"white-space: pre-wrap;\">" +
                                    syntaxHighlight(req_obj.report) +
                                "</pre></div>" +
                            "</div>" + "<br/><br/>" + document.getElementById("result").innerHTML;

/!*                    var wrapper = document.getElementById("test");
                    var tree = jsonTree.create(req_obj.report, wrapper);
                    tree.expand(function(node) {
                       return node.childNodes.length < 2 || node.label === 'phoneNumbers';
                    });*!/
                }*/
            },
            complete: function (data) {
                   setTimeout(getRequests, interval);
            }
    });
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


//Lance le formulaire FromServer
function launchForm(urlSend)
{
    $.ajax({
        type: 'POST',
        url: urlSend,
        contentType: "application/json",
        data: JSON.stringify($('#launchRequest').serializeJSON()),
        success: function (data) {
            //document.getElementById("div-form").innerHTML = data;
            alert(data)
        },
        complete: function (data) {
        }
    });
}

//Enregistre les parametres WS definis par l'utilisateur
function setWebserviceParameters()
{
    $.ajax({
        type: 'POST',
        url: '/web/unit-tests/setWebserviceParameters',
        contentType: "application/json",
        data: JSON.stringify($('#setWebserviceParameters').serializeJSON()),
        success: function (data) {
            $('#select-webservices').change();
            alert("Webservice parameters defined");
        },
        complete: function (data) {
        }
    });
}

/*
function credentials()
{
    $.ajax({
        type: 'POST',
        url: '/web/credentials',
        contentType: "application/json",
        data: JSON.stringify($('#registerWithPostCredentials').serializeJSON()),
        success: function (data) {
            alert(data);
        },
        complete: function (data) {
        }
    });
}

*/



function parseArray(arr, type){
    var output = '';
    $.each(arr , function(index , value){
      if(typeof value === 'object' || typeof value === 'array'){
        output+= '<tr>'+
          '<th scope="col">'+index+'</th>'+
          '<th scope="col">'+
              '<button class="btn btn-dark" type="button" data-toggle="collapse" data-target="#'+type+index+'Collapse'+value.id+'" aria-expanded="false" aria-controls="'+type+index+'Collapse'+value.id+'">'+index+'</button>'+
              '<div class="collapse" id="'+type+index+'Collapse'+value.id+'">'+
                 '<div class="card card-body"> '+
                   '<table class="table table-striped">';
                    output += parseArray(value);
                    output +='</table>'+
                   '</div>'+
               '</div>'+
          '</th>'+
        '</tr>';
      }else{
        output+= '<tr>'+
          '<th scope="col">'+index+'</th>'+
          '<th scope="col">'+value+'</th>'+
        '</tr>';
      }
    })
    return output;
}
function showResults(result){
    var response = result.json_list;
    var jsonResults = '';
    $.each(response , function(index , value) {
        //recuperation request et response
        let request = value.report.request;
        let response = value.report.response;
        //création des Report
        let buttonColor = "success";
        if (value.status === "KO") buttonColor = "danger";
        else if (value.status === "OK_BUT_WARNING") buttonColor = "warning";
        let title =  value.date_report + ' => Role : ' + value.ocpi_role_name + ' | Webservice : ' + value.iop_webservice_name + ' | Way : ' + value.iop_webservice_type;
        jsonResults = '<span data-placement="top" data-toggle="tooltip" title="' + title + '"><button style="width:100%" class="btn d-block text-wrap btn-' + buttonColor + '" type="button" data-toggle="collapse" data-target="#collapse' + value.id + '" aria-expanded="false" aria-controls="collapse' + value.id + '">' +
           title + '</button><span>';
        jsonResults += '<div class="collapse" id="collapse' + value.id + '">' +
            '<div class="card card-body">';
        jsonResults += '<hr><p><b>Request</b></p>' +
            '<table class="table table-striped">';

        var testsClass = '';
        var testsStatusText = '';
        if (request.tests.length > 0) {
            $.each(request.tests, function (testIndex, testValue) {
                testsClass = '';
                testsStatusText = '';
                if (testValue.level == 'I') {
                    testsClass = 'success';
                    testsStatusText = 'INFO';
                } else if (testValue.level == 'E') {
                    testsClass = 'danger';
                    testsStatusText = 'ERROR';
                } else if (testValue.level == 'W') {
                    testsClass = 'warning';
                    testsStatusText = 'WARNING';
                }

                jsonResults += '<tr class="table-' + testsClass + '">' +
                    '<th scope="col">' + testsStatusText + '</th>' +
                    '<th scope="col">' + testValue.text + '</th>' +
                    '</tr>';
            })
        }
        jsonResults += '<tbody>' +
            '<tr>' +
            '<th scope="row">URL</th>' +
            '<td>' + request.url + '</td>' +
            '</tr>' +
            '<th scope="row">Headers</th>' +
            '<td>' +
            '<button class="btn btn-dark" type="button" data-toggle="collapse" data-target="#requestHeadersCollapse' + value.id + '" aria-expanded="false" aria-controls="requestHeadersCollapse' + value.id + '">Headers</button>' +
            '<div class="collapse" id="requestHeadersCollapse' + value.id + '">' +
            '<div class="card card-body"> ' +
            '<table class="table table-striped">';
        $.each(request.headers, function (headerArrIndex, headerArr) {
            $.each(headerArr, function (headerIndex, headerValue) {
                if (typeof headerValue === 'object' || typeof headerValue === 'array') {
                    jsonResults += '<tr>' +
                        '<th scope="col">' + headerIndex + '</th>' +
                        '<th scope="col">' +
                        '<button class="btn btn-dark" type="button" data-toggle="collapse" data-target="#response' + headerIndex + 'Collapse' + value.id + '" aria-expanded="false" aria-controls="response' + headerIndex + 'Collapse' + value.id + '">' + headerIndex + '</button>' +
                        '<div class="collapse" id="response' + headerIndex + 'Collapse' + value.id + '">' +
                        '<div class="card card-body"> ' +
                        '<table class="table table-striped">';
                    jsonResults += parseArray(headerValue, 'response');
                    jsonResults += '</table>' +
                        '</div>' +
                        '</div>' +
                        '</th>' +
                        '</tr>';
                } else {
                    let header = headerValue;
                    if(/&|>|</g.test(headerValue)){
                        header =headerValue.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
                    }
                    jsonResults += '<tr>' +
                        '<th scope="col">' + headerIndex + '</th>' +
                        '<th scope="col" style="display:block;width: 400px"><pre style="white-space:break-spaces">' + header + '</pre></th>' +
                        '</tr>';
                }
            })
        });
        jsonResults += '</table>' +
            '</div>' +
            '</div>' +
            '</td>' +
            '</tr>' +
            '<tr>' +
            '<th scope="row">Body </th>' +
            '<td>' +
            '<button class="btn btn-dark" type="button" data-toggle="collapse" data-target="#requestBodyCollapse' + value.id + '" aria-expanded="false" aria-controls="requestBodyCollapse' + value.id + '">Body</button>' +
            '<div class="collapse" id="requestBodyCollapse' + value.id + '">' +
            '<div class="card card-body"> ' +
            '<table class="table table-striped">';

            if(typeof request.body === 'object' || typeof request.body === 'array') {
                /*   console.log(str);
                var wrapper = document.getElementById("bodyCard1");
                console.log(wrapper);
                var tree = jsonTree.create(response.body, wrapper);
                console.log(tree);
                tree.collapse();*/
                jsonResults += "<pre style=\"white-space: pre-wrap;\">";
                jsonResults += syntaxHighlight(request.body);
                jsonResults += "</pre>";

            }else{
                jsonResults += request.body;
            }
/*        $.each(request.body, function (bodyIndex, bodyValue) {
            if (typeof bodyValue === 'object' || typeof bodyValue === 'array') {
                jsonResults += '<tr>' +
                    '<th scope="col">' + bodyIndex + '</th>' +
                    '<th scope="col">' +
                    '<button class="btn btn-dark" type="button" data-toggle="collapse" data-target="#request' + bodyIndex + 'Collapse' + value.id + '" aria-expanded="false" aria-controls="request' + bodyIndex + 'Collapse' + value.id + '">' + bodyIndex + '</button>' +
                    '<div class="collapse" id="request' + bodyIndex + 'Collapse' + value.id + '">' +
                    '<div class="card card-body"> ' +
                    '<table class="table table-striped">';
                jsonResults += parseArray(bodyValue, 'request');
                jsonResults += '</table>' +
                    '</div>' +
                    '</div>' +
                    '</th>' +
                    '</tr>';
            } else {
                console.log(bodyValue);
                jsonResults += '<tr>' +
                    '<th scope="col">' + bodyIndex + '</th>' +
                    '<th scope="col">' + bodyValue + '</th>' +
                    '</tr>';
            }
        });*/

        jsonResults += '</table> ' +
            '</div>' +
            '</div>' +
            '</td>' +
            '</tr>' +
            '</tbody>' +
            '</table>' +
            '<hr><p><b>Response</b></p>';
        //Deuxieme table
        var testsClassResponse = '';
        var testsStatusTextResponse = '';
        if (request.tests.length > 0) {
            $.each(response.tests, function (testIndex, testValue) {
                testsClassResponse = '';
                testsStatusTextResponse = '';
                if (testValue.level == 'I') {
                    testsClassResponse = 'success';
                    testsStatusTextResponse = 'INFO';
                } else if (testValue.level == 'E') {
                    testsClassResponse = 'danger';
                    testsStatusTextResponse = 'ERROR';
                } else if (testValue.level == 'W') {
                    testsClassResponse = 'warning';
                    testsStatusTextResponse = 'WARNING';
                }

                jsonResults += '<tr class="table-' + testsClassResponse + '">' +
                    '<th scope="col">' + testsStatusTextResponse + '</th>' +
                    '<th scope="col">' + testValue.text + '</th>' +
                    '</tr>';
            })
        }
        jsonResults += '<table class="table table-striped">';
        if (response.tests.length > 0) {
            $.each(response.tests, function (testIndex, testValue) {
                testsClass = '';
                testsStatusText = '';
                if (testValue['level'] == 'I') {
                    testsClass = 'success';
                    testsStatusText = 'INFO';
                } else if (testValue['level'] == 'E') {
                    testsClass = 'danger';
                    testsStatusText = 'ERROR';
                } else if (testValue['level'] == 'W') {
                    testsClass = 'warning';
                    testsStatusText = 'WARNING';
                }

                jsonResults += '<tr class="table-' + testsClass + '">' +
                    '<th scope="col">' + testsStatusText + '</th>' +
                    '<th scope="col">' + testValue['text'] + '</th>' +
                    '</tr>';
            })
        }
        jsonResults +='<tbody>'+
              '<tr>'+
                '<th scope="row">URL</th>'+
                '<td>'+request.url+'</td>'+
              '</tr>'+
              '<tr>'+
                '<th scope="row">Status Code</th>'+
                '<td>'+response.http_status_code+'</td>'+
              '</tr>'+
              '<tr>'+
                '<th scope="row">Headers</th>'+
                '<td>'+
                  '<button class="btn btn-dark" type="button" data-toggle="collapse" data-target="#responseHeadersCollapse'+value.id+'" aria-expanded="false" aria-controls="responseHeadersCollapse'+value.id+'">Headers</button>'+
                  '<div class="collapse" id="responseHeadersCollapse'+value.id+'">'+
                    '<div class="card card-body"> '+
                        '<table class="table table-striped">';
                          $.each(response.headers, function(headerArrIndex , headerArr){
                            $.each(headerArr , function(headerIndex , headerValue){
                              if(typeof headerValue === 'object' || typeof headerValue === 'array'){
                                jsonResults+= '<tr>'+
                                  '<th scope="col">'+headerIndex+'</th>'+
                                  '<th scope="col">'+
                                      '<button class="btn btn-dark" type="button" data-toggle="collapse" data-target="#response'+headerIndex+'Collapse'+value.id+'" aria-expanded="false" aria-controls="response'+headerIndex+'Collapse'+value.id+'">'+headerIndex+'</button>'+
                                      '<div class="collapse" id="response'+headerIndex+'Collapse'+value.id+'">'+
                                         '<div class="card card-body"> '+
                                           '<table class="table table-striped">';
                                            jsonResults += parseArray(headerValue, 'response');
                                            jsonResults +='</table>'+
                                           '</div>'+
                                       '</div>'+
                                  '</th>'+
                                '</tr>';
                              }else{
                                  let header = headerValue;
                                  if(/&|>|</g.test(headerValue)){
                                        header =headerValue.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
                                  }
                                  jsonResults +='<tr>'+
                                    '<th scope="col">'+headerIndex+'</th>'+
                                    '<th scope="col" style="display:block;width: 400px"><pre style="white-space:break-spaces">' + header + '</pre></th>'+
                                  '</tr>';
                              }
                            })
                          });
                        jsonResults += '</table>'+
                    '</div>'+
                  '</div>'+
                '</td>'+
               '</tr>'+
               '<tr>'+
                '<th scope="row">Body</th>'+
                '<td>'+
                  '<button class="btn btn-dark" type="button" data-toggle="collapse" data-target="#responseBodyCollapse'+value.id+'" aria-expanded="false" aria-controls="responseBodyCollapse'+value.id+'">Body</button>'+
                  '<div class="collapse" id="responseBodyCollapse'+value.id+'">'+
                    '<div class="card card-body" id="bodyCard'+ value.id +'">';
                            if(typeof response.body === 'object' || typeof response.body === 'array') {
                                /*   console.log(str);
                                var wrapper = document.getElementById("bodyCard1");
                                console.log(wrapper);
                                var tree = jsonTree.create(response.body, wrapper);
                                console.log(tree);
                                tree.collapse();*/
                                jsonResults += "<pre style=\"white-space: pre-wrap;\">";
                                jsonResults += syntaxHighlight(response.body);
                                jsonResults += "</pre>";

                            }else{
                                jsonResults += response.body.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                            }
/*                          $.each(response.body, function(bodyIndex , bodyValue){
                            if(typeof bodyValue === 'object' || typeof bodyValue === 'array'){
                              jsonResults+= '<tr>'+
                              '<th scope="col">'+bodyIndex+'</th>'+
                              '<th scope="col">'+
                                  '<button class="btn btn-dark" type="button" data-toggle="collapse" data-target="#response'+bodyIndex+'Collapse'+value.id+'" aria-expanded="false" aria-controls="response'+bodyIndex+'Collapse'+value.id+'">'+bodyIndex+'</button>'+
                                  '<div class="collapse" id="response'+bodyIndex+'Collapse'+value.id+'">'+
                                     '<div class="card card-body"> '+
                                       '<table class="table table-striped">';
                                        jsonResults += parseArray(bodyValue, 'response');
                                        jsonResults +='</table>'+
                                       '</div>'+
                                   '</div>'+
                              '</th>'+
                            '</tr>';
                            }else{
                              jsonResults +='<tr>'+
                                '<th scope="col">'+bodyIndex+'</th>'+
                                '<th scope="col">'+bodyValue+'</th>'+
                              '</tr>';
                            }
                          });*/
        jsonResults+=           '</div>'+
                  '</div>'+
                '</td>'+
                '</tr>'+
            '</tbody>'+
          '</table>'+
          '</div>'+
            '</div><br>';
          document.getElementById("result").innerHTML = jsonResults + document.getElementById("result").innerHTML;
    })

}
document.onload = loadfunctions();