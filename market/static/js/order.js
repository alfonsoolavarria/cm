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
              "Panamá":"PAB",/*PAB/USD*/
              "Paypal":"USD",
              "Perú":"PEN",/*PEN/USD*/
              "Portugal":"EUR",
              "USA":"USD",
              "Banesco":"Bs",
              "Mercantil":"Bs",
              "Venezuela":"Bs",
              "PagoMovil":"Bs",
            }

           // if ($(".totalDinamicFinal2").val())

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
            tipodePago = 'Pago Movil'
            lugarPago = 'PagoMovil'
            if (tipodePago == '' || tipodePago != 'Pago Movil') {
              swal("Debe seleccionar una forma de pago", " ", "warning");
              //alertify.error("");
              return false;
            }
          }

          if (tipodePago == '') {
            swal("Debe seleccionar una forma de pago", " ", "warning");
            //alertify.error("");
            return false;
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
          $(".loader05").css("visibility","visible");

          var carrito = JSON.parse(localStorage.getItem("carrito"));
          var costo = JSON.parse(localStorage.getItem("costoenvio"));
          var fechadeinicio = moment().utc().format("YYYY-MM-DD HH:mm");// en utc
          
          $.post('/orden/entrega/',{
            pago:tipodePago,
            lugarpago:lugarPago,
            categoria_pago:categoria_pago,
            total:$(".totalDinamicFinal2").text(),
            moneda:moneda,
            carrito:JSON.stringify(carrito),
            costoenvio:costo,
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
              $("#loader05").css("visibility","hidden");
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

$('.radio').change(function(){
  if ($('#optionsRadios1').is(':checked')) {
    $("#banescoTransf").css("visibility","visible");
    $("#banescoTransf").css("position","static");
    $("#cuentasTransferencia").css("visibility","visible");
    $("#cuentasTransferencia").css("position","static");
  }else{
    $("#banescoTransf").css("visibility","hidden");
    $("#banescoTransf").css("position","fixed");
    $("#cuentasTransferencia").css("visibility","hidden");
    $("#cuentasTransferencia").css("position","fixed");
  }
  if ($('#optionsRadios2').is(':checked')) {
    $("#movilTransf").css("visibility","visible");
    $("#movilTransf").css("position","static");
  }else{
    $("#movilTransf").css("visibility","hidden");
    $("#movilTransf").css("position","fixed");
  }

  if ($('#optionsRadios3').is(':checked')) {
    $("#paypalTransf").css("visibility","visible");
    $("#paypalTransf").css("position","static");
  }else{
    $("#paypalTransf").css("visibility","hidden");
    $("#paypalTransf").css("position","fixed");
  }

  if ($('#inlineRadio1').is(':checked')) {
    $("#inlineFormCustomSelect1").prop("disabled", false)
  }else{
    $("#inlineFormCustomSelect1").prop("disabled", true)
  }
  if ($('#inlineRadio2').is(':checked')) {
    $("#inlineFormCustomSelect2").prop("disabled", false)
  }else{
    $("#inlineFormCustomSelect2").prop("disabled", true)
  }

  });

  var listPriceTotal = 0;
  var carrito = JSON.parse(localStorage.getItem("carrito"));
  var costo = JSON.parse(localStorage.getItem("costoenvio"));
  var lugar = localStorage.getItem("lugarenvio");
  console.log(carrito);
  if (carrito.length>0) {
    for (var i = 0; i < carrito.length; i++) {
      var price = parseFloat(carrito[i].price);
      var cant = parseFloat(carrito[i].cantidad);
      calculo = parseFloat(price*cant);
      listPriceTotal = parseFloat(listPriceTotal)+parseFloat(calculo)

    }
    $("#coenconf").text(costo);
    $("#lugarE").text(lugar);
    var total = parseFloat(listPriceTotal) + parseFloat(costo);
    $(".totalDinamicFinal2").text(parseFloat(total).toFixed(2));
    $(".subTotalDinamic2").text("$"+parseFloat(listPriceTotal).toFixed(2));
  }else{
    window.location.href = '/';
  }
  $('#action').click(function (e) {
    e.preventDefault();
    if ($('#minPlus').attr('class') == 'fa fa-plus'){
      $(".section1").show(900);
      $('#minPlus').attr('class','fa fa-minus');
    }else{
      $(".section1").hide(900);
      $('#minPlus').attr('class','fa fa-plus')
    }
   });
  $('#action2').click(function (e) {
    e.preventDefault();
    if ($('#minPlus2').attr('class') == 'fa fa-plus'){
      $(".section2").show(900);
      $('#minPlus2').attr('class','fa fa-minus');
    }else{
      $(".section2").hide(900);
      $('#minPlus2').attr('class','fa fa-plus')
    }
   });
  $('#action3').click(function (e) {
    e.preventDefault();
    if ($('#minPlus3').attr('class') == 'fa fa-plus'){
      $(".section3").show(900);
      $('#minPlus3').attr('class','fa fa-minus');
    }else{
      $(".section3").hide(900);
      $('#minPlus3').attr('class','fa fa-plus')
    }
   });
