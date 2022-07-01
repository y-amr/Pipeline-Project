$(fromserver).submit( function(event) {
                event.preventDefault();
                var json_data = new Object();
                json_data.status_code = 1000;
                json_data.status_message = "Success";

                //var url = "/local_api/post" + "?endpoint=" + document.getElementById("endpoint").innerText + "&tokenid=" + document.getElementById("tokenid").innerText + "&repetition=" + parseInt(document.getElementById("repetition").innerText) + "&country_code=" + document.getElementById("country_code").innerText + "&party_id=" + document.getElementById("party_id").innerText;
                var url = "/local_api/post" + "?method=POST" + "&endpoint=" + fromserver.elements["endpoint"].value + "&tokenid=" + fromserver.elements["tokenid"].value + "&repetition=" + parseInt($("#repetition").val()) + "&country_code=" + fromserver.elements["country_code"].value + "&party_id=" + fromserver.elements["party_id"].value;

                $.ajax({
                    type: "POST",
                    url: url,
                    data: JSON.stringify(json_data),
                    dataType: 'json'
                })
} )