$(document).ready(function() {

  $("#selectFirst").trigger( "click" );

  $("#paymentBox2").click(function(e){
    swal({
     title:"¿Está seguro de continuar con la compra?",
     text:"",
     icon:"warning",
     buttons:['No','Si'],
     dangerMode:true,
   }).then((willDelete)=>{
     if (willDelete){

          var tipodePago = ''
          var lugarPago = ''
          var moneda = ''
          var categoria_pago = ''
          var lista_pago = [
            "Argentina",
             "Chile",
             "Colombia",
             "España",
             "EspañaBizzum",
             "México",
             "Panamá",
             "Paypal",
             "Perú",
             "Portugal",
             "USA",
             "Banesco",
             "Mercantil",
             "Venezuela",
           ]
           var moneda_pago = {
             "Argentina":"USD",
              "Chile":"CLP",
              "Colombia":"COP",
              "España":"EUR",
              "EspañaBizzum":"EUR",
              "México":"MXN",
              "Panamá":"PAB/USD",
              "Paypal":"USD",
              "Perú":"PEN/USD",
              "Portugal":"EUR",
              "USA":"USD",
              "Banesco":"Bs",
              "Mercantil":"Bs",
              "Venezuela":"Bs",
            }

           // if ($(".totalDinamicFinal").val())

          if ($('#optionsRadios1').is(':checked')) {
            tipodePago = 'Transferencia'
            if ($('#inlineRadio1').is(':checked')) {
              lugarPago = $("#inlineFormCustomSelect1").val();
              categoria_pago = "Nacional";
            }
            if ($('#inlineRadio2').is(':checked')) {
              lugarPago = $("#inlineFormCustomSelect2").val();
              categoria_pago = "Internacional";
            }

            if (tipodePago == '' || lugarPago == '') {
              swal("Debe seleccionar una forma de pago", " ", "warning");
              //alertify.error("");
              return false;
            }

            if (lista_pago.indexOf(lugarPago) == -1 ) {
              swal("Debe seleccionar una forma de pago", " ", "warning");
              //alertify.error("");
              return false;
            }

          }
          if ($('#optionsRadios2').is(':checked')) {
            tipodePago = 'Pago Móvil'
            if (tipodePago == '' || tipodePago != 'Pago Móvil') {
              swal("Debe seleccionar una forma de pago", " ", "warning");
              //alertify.error("");
              return false;
            }
          }
          // if ($('#optionsRadios3').is(':checked')) {
          //   tipodePago = 'Paypal'
          // }
          /*Modeda de Pago*/
          moneda=moneda_pago[lugarPago]

          // $("#paymentBox2").remove();
          $("#paymentBox2").css("visibility","hidden");
          $("#sendUserSection1").css("visibility","hidden");
          $("#sendUserSection2").css("visibility","hidden");
          $("#preloader").css("visibility","visible");

          var carrito = JSON.parse(localStorage.getItem("carrito"));
          var fechadeinicio = moment().utc().format("YYYY-MM-DD HH:mm");// en utc

          $.post('/orden/entrega/',{
            pago:tipodePago,
            lugarpago:lugarPago,
            categoria_pago:categoria_pago,
            total:$(".totalDinamicFinal").text(),
            moneda:moneda,
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
              $("#preloader").css("visibility","hidden");
              $("#paymentBox2").css("visibility","visible");
              $("#sendUserSection1").css("visibility","visible");
              $("#sendUserSection2").css("visibility","visible");
              //alertify.error(result.message);
            }
          }).fail(function(error) {
            console.log(error.responseText);
            window.location.href = '/';
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
