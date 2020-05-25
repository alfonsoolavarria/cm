$(document).ready(function() {

  $("#helpForm").click(function(e){

    function validateEmail(email) {
      var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    }

    if ($("#ejemplo_password_3").val().length<1) {
        swal("Debe ingresar un Email", " ", "warning");
        return false;
    }else{
      var validate = validateEmail($("#ejemplo_password_3").val());
      if (!validate ) {
        swal("Email incorrecto", " ", "warning");
        return false;
      }
    }
    if ($("#messageText").val().length<1) {
      swal("Debe ingresar un Mensaje", " ", "warning");
      return false;
    }
    if ($("#asuntoSelect").val().length<1) {
      swal("Debe seleccionar un Asunto", " ", "warning");
      return false;
    }

    $.post('/help/form/',{
      csrfmiddlewaretoken:$("#token")[0].children.defaultValue,
      email:$("#ejemplo_password_3").val(),
      asunto:$("#asuntoSelect").val(),
      mensaje:$("#messageText").val(),
    }).done(function (result) {
      if (result.code==200) {
        swal("Mensaje enviado con Éxito", " ", "success");
        var delayInMilliseconds = 1000; //menos de 1 second
        setTimeout(function() {
          location.reload(true);
        }, delayInMilliseconds);
      }else {
        //poner un tootip
        swal(result.error[0], " ", "warning");
      }
    }).fail(function(error) {
      console.log(error.responseText);
    });

  });
});
