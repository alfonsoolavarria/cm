$(document).ready(function() {

  $("#selectFirst").trigger( "click" );

  $("#paymentBox2").click(function(e){
    swal({
     title:"¿Està seguro de continuar con la compra?",
     text:"",
     icon:"warning",
     buttons:['No','Si'],
     dangerMode:true,
   }).then((willDelete)=>{
     if (willDelete){

          var tipodePago = ''

          if ($('#optionsRadios1').is(':checked')) {
            tipodePago = 'Transferencia'
          }
          if ($('#optionsRadios2').is(':checked')) {
            tipodePago = 'Pago Mòvil'
          }
          if ($('#optionsRadios3').is(':checked')) {
            tipodePago = 'Paypal'
          }

          if (tipodePago == '') {
            swal("Debe seleccionar una forma de pago", " ", "warning");
            //alertify.error("");
            return false;
          }
          $("#paymentBox2").remove();
          $("#sendUserSection1").css("visibility","hidden");
          $("#sendUserSection2").css("visibility","hidden");
          $("#preloader").css("visibility","visible");

          var carrito = JSON.parse(localStorage.getItem("carrito"));
          var fechadeinicio = moment().utc().format("YYYY-MM-DD HH:mm");// en utc

          $.post('/orden/entrega/',{
            pago:tipodePago,
            total:$("#totalDinamicFinal").val(),
            carrito:JSON.stringify(carrito),
            start_date:fechadeinicio,
          }).done(function (result) {
            if (result.code==200) {
              var delayInMilliseconds = 3000; //menos de 1 second
              setTimeout(function() {
                window.location.href = '/confirmacion';
              }, delayInMilliseconds);
            }else {
              //poner un tootip
              swal(result.message, " ", "warning");
              //alertify.error(result.message);
              window.location.href = '/confirmacion';
            }
          }).fail(function(error) {
            console.log(error.responseText);
            window.location.href = '/confirmacion';
          });
     }
   })

  });

  $("#sendUserSection1").click(function(e){
    var text = $("#sendUserSection1").text().trim();

    if ($("#sendUserSection1").text()== 'Editar') {
      $("#sendUserSection1").text("Guardar");
    }else {
      $("#sendUserSection1").text("Editar");

      if ($("#2phone").val().length>0){
      }else{
        alertify.error("El teléfono está vacío",2);
        $("#sendUserSection1").text("Guardar");
        return false;
      }

      if ($("#rif").val().length>0){
      }else{
        alertify.error("El rif está vacío",2);
        $("#sendUserSection1").text("Guardar");
        return false;
      }
      if ($("#name").val().length>0){
      }else{
        alertify.error("El nombre está vacío",2);
        $("#sendUserSection1").text("Guardar");
        return false;
      }
      if ($("#apellido").val().length>0){
      }else{
        alertify.error("El apellido está vacío",2);
        $("#sendUserSection1").text("Guardar");
        return false;
      }

      $.ajax({
        url: '/profile/',
        type: 'PUT',
        data: {
          flagProfileonly:false,
          user:$("#flagUser").val(),
          name:$("#name").val(),
          lastname:$("#apellido").val(),
          phone:$("#2phone").val(),
          rif:$("#rif").val()
        },
        success: function(result) {
          if (result.code==200) {
            alertify.success("Se ha guardado correctamente",2);
          }else {
            alertify.error("Error al editar los datos",2);
            location.reload(true);
          }
        }
      });

    }


    if ($("#2phone").is(':disabled')) {
      $("#2phone").prop('disabled', false);
    }else{
      $("#2phone").prop('disabled', true);
    }

    if ($("#rif").is(':disabled')) {
      $("#rif").prop('disabled', false);
    }else{
      $("#rif").prop('disabled', true);
    }

    if ($("#name").is(':disabled')) {
      $("#name").prop('disabled', false);
    }else{
      $("#name").prop('disabled', true);
    }

    if ($("#apellido").is(':disabled')) {
      $("#apellido").prop('disabled', false);
    }else {
      $("#apellido").prop('disabled', true);
    }


  });


  $("#sendUserSection2").click(function(e) {
    var text = $("#sendUserSection2").text().trim();
    if ($("#sendUserSection2").text()== 'Editar') {
      $("#sendUserSection2").text("Guardar");
    }else {
      $("#sendUserSection2").text("Editar");

      if ($("#2address").val().length>0){
      }else{
        alertify.error("La dirección está vacía",2);
        $("#sendUserSection2").text("Guardar");
        return false;
      }


      $.ajax({
        url: '/profile/',
        type: 'PUT',
        data: {
          user:$("#flagUser").val(),
          flagProfileonly:true,
          direction:$("#2address").val(),
          localphone:$("#localphone").val(),
          reference:$("#reference").val()
        },
        success: function(result) {
          if (result.code==200) {
            alertify.success("Se ha guardado correctamente",2);
          }else {
            alertify.error("Error al editar los datos",2);
            location.reload(true);
          }
        }
      });


    }

    if ($("#2address").is(':disabled')) {
      $("#2address").prop('disabled', false);
    }else{
      $("#2address").prop('disabled', true);
    }
    if ($("#reference").is(':disabled')) {
      $("#reference").prop('disabled', false);
    }else{
      $("#reference").prop('disabled', true);
    }
    if ($("#localphone").is(':disabled')) {
      $("#localphone").prop('disabled', false);
    }else{
      $("#localphone").prop('disabled', true);
    }

  });

});
