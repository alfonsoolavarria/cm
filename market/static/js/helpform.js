$(document).ready(function() {

  $("#helpForm").click(function(e){
    e.preventDefault();
    $("#helpForm").css("visibility","hidden");
    $("#preloader").css("visibility","visible");
    forma_email = $("#asuntoSelect").val();

    if (forma_email == 'Pagos-Transferencias') {
      var file = document.getElementById('filepago')
      var input = file;
      var reader = new FileReader();
      reader.onload = function () {
        // console.log('--3->',input.files[0]);
        // console.log('4',input.files[0].name);
        // reader.fileName = files[i].name;
        var filedata = reader.result;
        var nombreimagen = input.files[0].name
        var extension = input.files[0].type
        $.post('/help/form/',{
          csrfmiddlewaretoken:$("#token")[0].children.defaultValue,
          email:$("#ejemplo_password_3").val(),
          asunto:$("#asuntoSelect").val(),
          mensaje:$("#messageText").val(),
          imagen:filedata,
          nombre_imagen:nombreimagen,
          extension:extension,
          codigo:$("#codigo1").val(),
        }).done(function (result) {
          $("#helpForm").css("visibility","visible");
          $("#preloader").css("visibility","hidden");

          if (result.code==200) {
            swal("Mensaje enviado con Éxito", " ", "success");
            var delayInMilliseconds = 1000; //menos de 1 second
            setTimeout(function() {
              location.reload(true);
            }, delayInMilliseconds);
          }else {
            //poner un tootip
            swal(result.error, " ", "warning");
          }
        }).fail(function(error) {
          console.log(error.responseText);
        });/*fin ajax*/

      };

    }

    $("#preloader").css("visibility","visible");
    function validateEmail(email) {
      var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    }

    if ($("#ejemplo_password_3").val().length<1) {
        swal("Debe ingresar un Email", " ", "warning");
        $("#helpForm").css("visibility","visible");
        $("#preloader").css("visibility","hidden");
        return false;
    }else{
      var validate = validateEmail($("#ejemplo_password_3").val());
      if (!validate ) {
        swal("Email incorrecto", " ", "warning");
        $("#helpForm").css("visibility","visible");
        $("#preloader").css("visibility","hidden");
        return false;
      }
    }
    if ($("#messageText").val().length<1) {
      swal("Debe ingresar un Mensaje", " ", "warning");
      $("#helpForm").css("visibility","visible");
      $("#preloader").css("visibility","hidden");
      return false;
    }
    if (forma_email == 'Pagos-Transferencias') {
      if ($("#codigo1").val().length<1) {
        swal("Debe ingresar un Código de Compra", " ", "warning");
        $("#helpForm").css("visibility","visible");
        $("#preloader").css("visibility","hidden");
        return false;
      }
    }
    if ($("#asuntoSelect").val().length<1) {
      swal("Debe seleccionar un Asunto", " ", "warning");
      $("#helpForm").css("visibility","visible");
      $("#preloader").css("visibility","hidden");
      return false;
    }

    if (forma_email == 'Pagos-Transferencias') {

      if (input.files.length>0) {
        if (input.files && input.files[0].type == 'image/png' || input.files[0].type == 'image/jpeg') {
          reader.readAsDataURL(input.files[0]);
        }else {
          swal("Debe seleccionar un achivo tipo imagen", " ", "warning");
          $("#helpForm").css("visibility","visible");
          $("#preloader").css("visibility","hidden");
          return false;
        }
      }else {
        swal("Debe seleccionar un achivo tipo imagen", " ", "warning");
        $("#helpForm").css("visibility","visible");
        $("#preloader").css("visibility","hidden");
        return false;
      }
    }

    if (forma_email != 'Pagos-Transferencias') {
      $.post('/help/form/',{
        csrfmiddlewaretoken:$("#token")[0].children.defaultValue,
        email:$("#ejemplo_password_3").val(),
        asunto:$("#asuntoSelect").val(),
        mensaje:$("#messageText").val(),
      }).done(function (result) {
        $("#helpForm").css("visibility","visible");
        $("#preloader").css("visibility","hidden");

        if (result.code==200) {
          swal("Mensaje enviado con Éxito", " ", "success");
          var delayInMilliseconds = 1000; //menos de 1 second
          setTimeout(function() {
            location.reload(true);
          }, delayInMilliseconds);
        }else {
          //poner un tootip
          swal(result.error, " ", "warning");
        }
      }).fail(function(error) {
        console.log(error.responseText);
      });/*fin ajax*/
    }

  });

  $("#asuntoSelect").change(function() {
    if ($("#asuntoSelect").val() != 'Pagos-Transferencias'){
      $("#ccompra").css('visibility','hidden');
      $("#ccompra").css('display','none');
      $("#xcompra").css('visibility','hidden');
      $("#xcompra").css('display','none');
    }else {
      $("#ccompra").css('visibility','visible');
      $("#ccompra").css('display','grid');
      $("#xcompra").css('visibility','visible');
      $("#xcompra").css('display','grid');
    }
});

});
