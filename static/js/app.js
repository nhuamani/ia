console.log("Hola mundo");

$(document).ready(function(){

    function ajax_login(){
        $.ajax({
            url: '/ajax-login',
            data: $('form').serialize(),
            type: 'POST',
            success: function(d) {
                console.log(d);
                var html = "";
                html += '<thead><tr><th>Edad</th><th>Colesterol</th><th>Diagnostico</th></tr></thead>'
                html += '<tbody><tr>'
                html += '<td>'+ d.data.edad +'</td>'
                html += '<td>'+ d.data.colesterol +'</td>'
                html += '<td>'+ d.msg.mensaje1 +'</td>'
                html += '</tr></tbody>'

                $("#datos").html(html);

                console.log(d);
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

    $("#login-form").submit(function(event) {
        event.preventDefault();
        ajax_login();
    });
});

