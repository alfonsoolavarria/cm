$(document).ready(function() {

  $('form').submit(function (e) {
    e.preventDefault();
    $("#forgotSubmit").css("visibility","hidden");

    function validateEmail(email) {
      var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    }

    var validate = validateEmail($("#forgotuser").val());

    if (!validate ) {
      swal("Email incorrecto", " ", "warning");
      $("#forgotSubmit").css("visibility","visible");
      return false;
    }

    $.post('/forgot/password/',{
      csrfmiddlewaretoken:e.currentTarget[0].value,
      email:$("#forgotuser").val(),
    }).done(function (result) {
      if (result.code==200) {
        swal("Enviado con Exito", " ", "success");
        var delayInMilliseconds = 3000; //1 second
        setTimeout(function() {
          window.location.href = '/';
        }, delayInMilliseconds);
      }else {
        swal(result.message, " ", "warning");
        $("#forgotSubmit").css("visibility","visible");
      }
    }).fail(function(error) {
      console.log(error.responseText);
      $("#forgotSubmit").css("visibility","visible");
    });
//8895384
  });

});
