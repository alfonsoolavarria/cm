function demoFromHTML() {
    var pdf = new jsPDF('p', 'pt', 'letter');
    // source can be HTML-formatted string, or a reference
    // to an actual DOM element from which the text will be scraped.
    source = $('#productsAdmin')[0];

    // we support special element handlers. Register them with jQuery-style
    // ID selector for either ID or node name. ("#iAmID", "div", "span" etc.)
    // There is no support for any other type of selectors
    // (class, of compound) at this time.
    specialElementHandlers = {
        // element with id of "bypass" - jQuery style selector
        '#bypassme': function (element, renderer) {
          console.log(element);
            // true = "handled elsewhere, bypass text extraction"
            return true
        }
    };
    margins = {
        top: 100,
        bottom: 100,
        left: 100,
        width: 500
    };
    // all coords and widths are in jsPDF instance's declared units
    // 'inches' in this case
    pdf.fromHTML(
    source, // HTML string or DOM elem ref.
    margins.left, // x coord
    margins.top, { // y coord
        'width': margins.width, // max width of content on PDF
        'elementHandlers': specialElementHandlers
    },

    function (dispose) {
        // dispose: object with X, Y of the last line add to the PDF
        //          this allow the insertion of new lines after html
        pdf.save('Test.pdf');
    }, margins);
}



function action_cotizacion(numero) {
  var totalc = parseFloat($("#totalcotizaciongeneral").text());
  if (isNaN(totalc)) {
    totalc = 0;
  }
  /*corregir esta restando y esta comiendose un numero creo que le falta un decimal y dejar los label por el html para efectos del pdf*/
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

$(document).ready(function() {

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

  $("body").on("click", "#btnExport", function () {
      html2canvas($('#productsAdmin')[0], {
          onrendered: function (canvas) {
              var data = canvas.toDataURL();
              var docDefinition = {
                  content: [{
                      image: data,
                      width: 500
                  }]
              };
              pdfMake.createPdf(docDefinition).download("cutomer-details.pdf");
          }
      });
  });

});
