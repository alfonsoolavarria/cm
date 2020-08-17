$(document).ready(function() {

  function action_cotizacion(numero) {
    var totalc = parseFloat($("#totalcotizaciongeneral").text());
    if (isNaN(totalc)) {
      totalc = 0;
    }

    if (isNaN($("#cant-"+numero).val()) || $("#cant-"+numero).val().length<1  ) {

      $("#cant-"+numero).val(0);
    }

    var prev_precio = parseFloat($("#total-"+numero).val());

    total = (parseFloat($("#cant-"+numero).val()) * parseFloat($("#price-"+numero).text()))

    $("#total-"+numero).val(total.toFixed(2));
    totalc = totalc+total;
    if (total == 0) {
      totalc = totalc-prev_precio;
    }else {
      totalc = totalc-prev_precio;
    }

    $("#monedacotizador").text("$");
    $("#totalcotizaciongeneral").text(totalc.toFixed(2));
  }


  $("#excelproductos").click(function(e){
    e.preventDefault();
    var file = document.getElementById('fileproducto')
    var input = file;
    var reader = new FileReader();
    reader.onload = function () {
      // console.log('--3->',input.files[0]);
      // console.log('4',input.files[0].name);
      // reader.fileName = files[i].name;
      var filedata = reader.result;
      var nombreimagen = input.files[0].name
      var extension = input.files[0].type
      $.post('/criollitos/market/admin/',{
        csrfmiddlewaretoken:$("#token")[0].children.defaultValue,
        archivo:filedata,
        nombre_archivo:nombreimagen,
        extension:extension,
      }).done(function (result) {
        if (result.code==200) {
          swal(result.mensaje, " ", "success");
          var delayInMilliseconds = 1000; //menos de 1 second
          // setTimeout(function() {
          //   location.reload(true);
          // }, delayInMilliseconds);
        }else {
          //poner un tootip
          swal(result.error, " ", "warning");
        }
      }).fail(function(error) {
        console.log(error.responseText);
      });/*fin ajax*/

    };


    if (input.files && input.files[0].type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || input.files[0].type == 'application/vnd.oasis.opendocument.spreadsheet') {
      reader.readAsDataURL(input.files[0]);
    }else {
      swal("Debe seleccionar un achivo tipo xlsx o ods", " ", "warning");
      return false;
    }

  });



});
