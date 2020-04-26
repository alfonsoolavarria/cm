$(document).ready(function() {

  $("#miBoton").on( "click", function() {
    console.log('-');
  });

  $("#miBoton").trigger("click");
  /*Todos los productos*/
  /*$('#allId').click(function (e) {
    $(".isotope-grid1").empty();
    $(".isotope-grid1").css({"position":"relative"});
    $(".isotope-grid1").css({height:''});
    var data = JSON.parse('['+$('#dataJson').val()+']');
    for (var i = 0; i < data.length; i++) {
      for (var ii = 0; ii < data[i].length; ii++) {
          $(".isotope-grid1").append("\
          <div class='col-sm-6 col-md-4 col-lg-3 p-b-35 isotope-item women'>\
          <div class='block2'>\
          <div class='block2-pic hov-img0'>\
          <img src='/static/"+data[i][ii].image+"' alt=''>\
          <!--modal=js-show-modal1 -->\
          <a href='#' style='left:25%' data-name='"+data[i][ii].name+"' data-price='+"+data[i][ii].price+"+' class='block2-btn flex-c-m stext-103 cl2 size-102 bg0 bor2 hov-btn1 p-lr-15 trans-04 js-show-modal1'>\
            Detalles\
          </a>\
          <a href='#' style='left:70%' data-name='"+data[i][ii].name+"' data-price='+"+data[i][ii].price+"+' class='block2-btn flex-c-m stext-103 cl2 size-102 bg0 bor2 hov-btn1 p-lr-15 trans-04 js-show-modal1'>\
            carrito\
          </a>\
          </div>\
          <div class='block2-txt flex-w flex-t p-t-14'>\
          <div class='block2-txt-child1 flex-col-l '>\
          <a href='' class='stext-104 cl4 hov-cl1 trans-04 js-name-b2 p-b-6'>\
          "+data[i][ii].description+"\
          </a>\
          <span class='stext-105 cl3'>\
          precio\
          </span>\
          </div>\
          <div class='block2-txt-child2 flex-r p-t-3'>\
          <a href='#' class='btn-addwish-b2 dis-block pos-relative js-addwish-b2'>\
          <img class='icon-heart1 dis-block trans-04' src='static/images/icons/icon-heart-01.png'  alt='ICON'>\
          <img class='icon-heart2 dis-block trans-04 ab-t-l' src=' static/images/icons/icon-heart-02.png' alt='ICON'>\
          </a>\
          </div>\
          </div>\
          </div>\
          </div>\
          ");
      }
    }


  });*/

  /*Solo viveres*/
  /*$('#viveresId').click(function (e) {
    $(".isotope-grid1").empty();
    $(".isotope-grid1").css({"position":"relative"});
    $(".isotope-grid1").css({height:''});
    var data = JSON.parse('['+$('#dataJson').val()+']');
    for (var i = 0; i < data.length; i++) {
      for (var ii = 0; ii < data[i].length; ii++) {
        if (data[i][ii].category === 1) {
          $('.isotope-grid1').append("\
          <div class='col-sm-6 col-md-4 col-lg-3 p-b-35 isotope-item women'>\
          <div class='block2'>\
          <div class='block2-pic hov-img0'>\
          <img src='/static/"+data[i][ii].image+"' alt=''>\
          <!--modal=js-show-modal1 -->\
          <a href='#' data-name='name' data-price='price' data-description='description' class='block2-btn flex-c-m stext-103 cl2 size-102 bg0 bor2 hov-btn1 p-lr-15 trans-04 js-show-modal1'>\
          Quick View\
          </a>\
          </div>\
          <div class='block2-txt flex-w flex-t p-t-14'>\
          <div class='block2-txt-child1 flex-col-l '>\
          <a href='' class='stext-104 cl4 hov-cl1 trans-04 js-name-b2 p-b-6'>\
          "+data[i][ii].description+"\
          </a>\
          <span class='stext-105 cl3'>\
          precio\
          </span>\
          </div>\
          <div class='block2-txt-child2 flex-r p-t-3'>\
          <a href='#' class='btn-addwish-b2 dis-block pos-relative js-addwish-b2'>\
          <img class='icon-heart1 dis-block trans-04' src='static/images/icons/icon-heart-01.png'  alt='ICON'>\
          <img class='icon-heart2 dis-block trans-04 ab-t-l' src=' static/images/icons/icon-heart-02.png' alt='ICON'>\
          </a>\
          </div>\
          </div>\
          </div>\
          </div>\
          ");
        }

      }
    }


  });
*/
  /*Solo Frigorifico*/
  /*$('#frigorificoId').click(function (e) {
    $(".isotope-grid1").empty();
    $(".isotope-grid1").css({"position":"relative"});
    $(".isotope-grid1").css({height:''});
    var data = JSON.parse('['+$('#dataJson').val()+']');
    for (var i = 0; i < data.length; i++) {
      for (var ii = 0; ii < data[i].length; ii++) {
        if (data[i][ii].category==2) {
          $(".isotope-grid1").append("\
          <div class='col-sm-6 col-md-4 col-lg-3 p-b-35 isotope-item women'>\
          <div class='block2'>\
          <div class='block2-pic hov-img0'>\
          <img src='/static/"+data[i][ii].image+"' alt=''>\
          <!--modal=js-show-modal1 -->\
          <a href='#' data-name='name' data-price='price' data-description='description' class='block2-btn flex-c-m stext-103 cl2 size-102 bg0 bor2 hov-btn1 p-lr-15 trans-04 js-show-modal1'>\
          Quick View\
          </a>\
          </div>\
          <div class='block2-txt flex-w flex-t p-t-14'>\
          <div class='block2-txt-child1 flex-col-l '>\
          <a href='' class='stext-104 cl4 hov-cl1 trans-04 js-name-b2 p-b-6'>\
          "+data[i][ii].description+"\
          </a>\
          <span class='stext-105 cl3'>\
          precio\
          </span>\
          </div>\
          <div class='block2-txt-child2 flex-r p-t-3'>\
          <a href='#' class='btn-addwish-b2 dis-block pos-relative js-addwish-b2'>\
          <img class='icon-heart1 dis-block trans-04' src='static/images/icons/icon-heart-01.png'  alt='ICON'>\
          <img class='icon-heart2 dis-block trans-04 ab-t-l' src=' static/images/icons/icon-heart-02.png' alt='ICON'>\
          </a>\
          </div>\
          </div>\
          </div>\
          </div>\
          ");
        }
      }
    }


  });
*/
  /*Solo enlatados*/
  /*$('#enaltadoId').click(function (e) {
    $(".isotope-grid1").empty();
    $(".isotope-grid1").css({"position":"relative"});
    $(".isotope-grid1").css({height:''});
    var data = JSON.parse('['+$('#dataJson').val()+']');
    for (var i = 0; i < data.length; i++) {
      for (var ii = 0; ii < data[i].length; ii++) {
        if (data[i][ii].category==3) {
          $(".isotope-grid1").append("\
          <div class='col-sm-6 col-md-4 col-lg-3 p-b-35 isotope-item women'>\
          <div class='block2'>\
          <div class='block2-pic hov-img0'>\
          <img src='/static/"+data[i][ii].image+"' alt=''>\
          <!--modal=js-show-modal1 -->\
          <a href='#' data-name='name' data-price='price' data-description='description' class='block2-btn flex-c-m stext-103 cl2 size-102 bg0 bor2 hov-btn1 p-lr-15 trans-04 js-show-modal1'>\
          Quick View\
          </a>\
          </div>\
          <div class='block2-txt flex-w flex-t p-t-14'>\
          <div class='block2-txt-child1 flex-col-l '>\
          <a href='' class='stext-104 cl4 hov-cl1 trans-04 js-name-b2 p-b-6'>\
          "+data[i][ii].description+"\
          </a>\
          <span class='stext-105 cl3'>\
          precio\
          </span>\
          </div>\
          <div class='block2-txt-child2 flex-r p-t-3'>\
          <a href='#' class='btn-addwish-b2 dis-block pos-relative js-addwish-b2'>\
          <img class='icon-heart1 dis-block trans-04' src='static/images/icons/icon-heart-01.png'  alt='ICON'>\
          <img class='icon-heart2 dis-block trans-04 ab-t-l' src=' static/images/icons/icon-heart-02.png' alt='ICON'>\
          </a>\
          </div>\
          </div>\
          </div>\
          </div>\
          ");
        }
      }
    }


  });
*/

});
