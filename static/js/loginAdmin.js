$(document).ready(function() {

  $('form').submit(function (e) {
    e.preventDefault();

    function validateEmail(email) {
      var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    }

    var validate = validateEmail($("#userAdmin").val());

    if (!validate ) {
      swal("Email incorrecto", " ", "warning");
      return false;
    }

    if ($("#passwordAdmin").val().length <1) {
      swal("Clave muy corta", " ", "warning");
      return false;
    }

    $.post('/login/',{
      csrfmiddlewaretoken:e.currentTarget[0].value,
      email:$("#userAdmin").val(),
      password:$("#passwordAdmin").val(),
      admin:true,
    }).done(function (result) {
      if (result.code==200) {
        window.location.href = '/criollitos/market/admin/';
      }else {
        //poner un tootip
        swal("intente de nuevo "+result.message, " ", "warning");
      }
    }).fail(function(error) {
      console.log(error.responseText);
    });



  });

});
