$(document).ready(function() {

  $("#helpForm").click(function(e){
    console.log("...........................");
    function validateEmail(email) {
      var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    }

    if ($("#ejemplo_password_3").val().length<1) {
        alertify.error("Debe ingresar un Email",2);
        return false;
    }else{
      var validate = validateEmail($("#ejemplo_password_3").val());
      if (!validate ) {
        alertify.error("Email incorrecto");
        return false;
      }
    }
    if ($("#messageText").val().length<1) {
      alertify.error("Debe ingresar un Mensaje",2);
      return false;
    }
    if ($("#asuntoSelect").val().length<1) {
      alertify.error("Debe seleccionar un Asunto",2);
      return false;
    }

    if ($("#filepago").val().length<1) {
        alertify.error("Debe seleccionar archivo de pago",2);
        return false;
    }
    var img = $("#filepago")[0].files[0];

    console.log("Voyyyy",img);
    // $.ajax({
    //   url:'/help/form/',
    //   type: 'POST',
    //   dataType: 'json',
    //   // csrfmiddlewaretoken:$("#token")[0].children.defaultValue,
    //   data:{'imagen':img,'email':$("#ejemplo_password_3").val(),
    //       "asunto":$("#asuntoSelect").val(),
    //       "mensaje":$("#messageText").val()
    //     },
    // }).done(function (result) {
    //   if (result.code==200) {
    //     alertify.success('Mensaje enviado con Éxito');
    //     var delayInMilliseconds = 1000; //menos de 1 second
    //     setTimeout(function() {
    //       location.reload(true);
    //     }, delayInMilliseconds);
    //   }else {
    //     //poner un tootip
    //     alertify.error(result.error[0]);
    //   }
    // }).fail(function(error) {
    //   console.log(error.responseText);
    // });
    // data = {'imagen':,'email':$("#ejemplo_password_3").val(),
    //       "asunto":$("#asuntoSelect").val(),
    //       "mensaje":$("#messageText").val()
    //     }
    var fd
    fd = new FormData();
    fd.append("image", img);
    fd.append("asunto", $("#asuntoSelect").val());
    fd.append("mensaje", $("#messageText").val());
    fd.append("email", $("#ejemplo_password_3").val());
    console.log(fd);
    $.ajax({
    method: 'POST',
    processData: false,
    contentType: false,
    // cache: false,
    data: fd,
    // enctype: 'multipart/form-data',
    url: '/help/form/',
    success: function (response) {
      location.reload();
    }
});
  });
});
