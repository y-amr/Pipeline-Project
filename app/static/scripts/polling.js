function loadMaPage()
{
    var interval = 5000;  // 1000 = 1 seconde, 3000 = 3 secondes
    var current_text = document.getElementById("result").innerText;
    function doAjax() {
        $.ajax({
                type: 'GET',
                url: "/static/information.json",
                data: $(this).serialize(),
                dataType: 'json',
                success: function (data) {
                        current_text = document.getElementById("result").innerText;
                        document.getElementById("result").innerText = current_text + "\r\n" + data.data;
                        $("result").prop("scrollHeight");
                        //$("#result").val(current_text + "\r\n" + data.data);
                },
                complete: function (data) {
                        // Schedule the next
                        //current_text = $("#result").html();
                        setTimeout(doAjax, interval);
                }
        });
    }
    setTimeout(doAjax, interval);
}

document.onload = loadMaPage();