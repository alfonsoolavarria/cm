/*SECCION DE CAJA, PARA SUBIR BAJAR Y REMOVER PRODUCTOS DEL CARRITO*/
$('#selectEnvio').on('change', function() {
  $("#coen").text(this.value);
  localStorage.setItem("costoenvio",this.value);//inclusion de cosoto de envio
  localStorage.setItem("lugarenvio",this.options[this.selectedIndex].text);//inclusion de lugar de envio

  /*actualizacion del monto total*/
  subtotal = $(".subTotalDinamic").text();
  nuev_total = parseFloat(subtotal)+parseFloat(this.value);
  $(".totalDinamicFinal").text((parseFloat(nuev_total).toFixed(2)).toString());
});

var costo = JSON.parse(localStorage.getItem("costoenvio"));
var lis_cost = [2,3,4,5]
var lis_lugar = ["Bermudez","Urb Centro","Las Acacias","San Ignacio",
  "Los Samanes","Urb Calicanto","Fundacion Mendoza","Zonas Cercanas 1",
  "23 de Enero","La Coromoto","Arsenal","El Limon","Cana de Azucar","Palo Negro",
  "Los Olivos","Av Dr Montoya","Zonas Cercanas 2","La Cabrera Mariara","Turmero",
  "Cagua-Bella Vista","Zonas Cercanas 3","La Victoria"]

if (costo){
  if (lis_cost.indexOf(costo)!=-1) {
    $("#coen").text(costo);

    var lugar = localStorage.getItem("lugarenvio");
    if (lugar) {
      if (lis_lugar.indexOf(lugar)!=-1) {
        $("#selectEnvio option[class='"+lugar+"']").attr('selected', 'selected');
      }else {
        swal("Lugar incorrecto", " ", "warning");
      }
    }
  }else {
    swal("Costo incorrecto", " ", "warning");
  }
}

function buscaIdIndice(lista,id) {
  for (var i = 0; i < lista.length; i++) {
    if (lista[i]['id'] == id) {
      return i
    }
  }
  return -1
}

  var listPriceTotal = 0;
  var carrito = JSON.parse(localStorage.getItem("carrito"));
  if (carrito.length<1) {
    $(".wrap-table-shopping-cart").css("visibility","hidden");
    //$(".twoColum").css("visibility","hidden");
    $(".wrap-table-shopping-cart").after("<h4 style='text-align:center;'>Aún no hay artículos en su carrito, anda y <a href='/all'>compra</a></h4>");
    $("#paymentBox").remove();
  }else{
    for (var i = 0; i < carrito.length; i++) {
      $("#dinamicItems").after("<tr class='table_row'>\
        <td class='column-1'>\
          <div class='how-itemcart1' onclick='return removeItems(this,"+carrito[i].id+")' id='removeItems-"+carrito[i].id+"'>\
            <img src='"+carrito[i].image+"' alt='IMG'>\
          </div>\
        </td>\
        <td class='column-2'>"+carrito[i].name+"</td>\
        <td class='column-3'><h5><b class='pricechange-"+carrito[i].id+"'>$</b><b>"+carrito[i].price+"</b></h5></td>\
        <td class='column-4'>\
          <div class='wrap-num-product flex-w m-l-auto m-r-0'>\
            <div onclick='return buttonDown(this,"+carrito[i].id+")' data-id="+carrito[i].id+" class='btn-num-product-down cl8 hov-btn3 trans-04 flex-c-m'>\
              <i class='fs-16 zmdi zmdi-minus'></i>\
            </div>\
            <input disabled class='mtext-104 cl3 txt-center num-product' type='number' name='num-product1' value='"+carrito[i].cantidad+"'>\
            <div onclick='return buttonUp(this,"+carrito[i].id+")' data-id="+carrito[i].id+" class='btn-num-product-up cl8 hov-btn3 trans-04 flex-c-m'>\
              <i class='fs-16 zmdi zmdi-plus'></i>\
            </div>\
          </div>\
          <label class='cantHidden-"+carrito[i].id+"' style='visibility:hidden;position:absolute;'>"+carrito[i].cant+"</label>\
        </td>\
        <td class='column-5'><h5><b class='currency-"+carrito[i].id+"'>$</b><b class='dinamicPrice-"+carrito[i].id+"'>"+((parseFloat(carrito[i].price).toFixed(2))*(parseFloat(carrito[i].cantidad).toFixed(2))).toFixed(2)+"</b></h5></td>\
      </tr>");
      listPriceTotal = listPriceTotal+(parseFloat(carrito[i].price)*parseFloat(carrito[i].cantidad));
    }

    var montototal = (parseFloat(listPriceTotal)+parseFloat($("#coen").text())).toFixed(2);
    $(".totalDinamicFinal").text(montototal.toString());
    $(".subTotalDinamic").text(listPriceTotal.toFixed(2));
  }

  function buttonUp(param,id) {
    // console.log(carrito,id.toString());
    // var indice = _.findIndex(carrito, ['id',id.toString()]);
    var indice = buscaIdIndice(carrito,id.toString());
    var numProduct = Number($(param).prev().val());
    if (numProduct <= parseInt($('.cantHidden-'+id).text())) {
      numProduct = numProduct+1;
      if (numProduct <= parseInt($('.cantHidden-'+id).text())) {
        $(param).prev().val(numProduct);
        if (indice!=-1) {
          carrito[indice].cantidad=numProduct.toString();
          $(".dinamicPrice-"+id).text((numProduct * parseFloat(carrito[indice].price)).toFixed(2));
          localStorage.setItem("carrito",JSON.stringify(carrito));
          /*updateo el total*/
          var carritoUp = JSON.parse(localStorage.getItem("carrito"));
          var sub = 0;
          for (var i = 0; i < carritoUp.length; i++) {
            sub = sub +(parseFloat(carritoUp[i].price)*parseFloat(carritoUp[i].cantidad));
          }
          $(".subTotalDinamic").text(sub.toFixed(2));
          var montototal = (parseFloat(sub)+parseFloat($("#coen").text())).toFixed(2);
          $(".totalDinamicFinal").text(montototal.toString());
        }
      }else {
        swal("Ya no hay mas productos", " ", "warning");
      }
    }
  }

  function buttonDown(param,id) {
    var indice = buscaIdIndice(carrito,id.toString());
    // var indice = _.findIndex(carrito, ['id',id.toString()]);
    var numProduct = Number($(param).next().val());
    if (numProduct <= parseInt($('.cantHidden-'+id).text())) {
      if(numProduct >= 1){
        if (numProduct!=1) {
          $(param).next().val(numProduct - 1);
          if (indice!=-1) {
            carrito[indice].cantidad=(numProduct-1).toString();
            $(".dinamicPrice-"+id).text(((numProduct-1) * parseFloat(carrito[indice].price)).toFixed(2));
            localStorage.setItem("carrito",JSON.stringify(carrito));
            /*updateo el total*/
            var carritoDown = JSON.parse(localStorage.getItem("carrito"));
            var sub = 0;
            for (var i = 0; i < carritoDown.length; i++) {
              sub = sub +(parseFloat(carritoDown[i].price)*parseFloat(carritoDown[i].cantidad));
            }
            $(".subTotalDinamic").text(sub.toFixed(2));
            var montototal = (parseFloat(sub)+parseFloat($("#coen").text())).toFixed(2);
            $(".totalDinamicFinal").text(montototal.toString());
          }
        }
      }
    }
  }

  function removeItems(param,id) {
    var indice = buscaIdIndice(carrito,id.toString());
    // var indice = _.findIndex(carrito, ['id',id.toString()]);
    swal({
      title:"¿Esta seguro de borrar el articulo?",
      text:carrito[indice].name,
      icon:"warning",
      buttons:['No','Si'],
      dangerMode:true,
    }).then((willDelete)=>{
      if (willDelete){
        // console.log("222222-->reject",_.reject(list,{'id':id.toString()}));
        myNewCar = carrito.filter(function( obj ) {
          return obj.id !== id.toString();
        });
        localStorage.setItem("carrito",JSON.stringify(myNewCar));
        location.reload(true);
      }
    })
  }
/******************************************************/
