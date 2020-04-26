
(function ($) {
    "use strict";

    /*[ Load page ]
    ===========================================================*/
    $(".animsition").animsition({
        inClass: 'fade-in',
        outClass: 'fade-out',
        inDuration: 1500,
        outDuration: 800,
        linkElement: '.animsition-link',
        loading: true,
        loadingParentElement: 'html',
        loadingClass: 'animsition-loading-1',
        loadingInner: '<div class="loader05"></div>',
        timeout: false,
        timeoutCountdown: 5000,
        onLoadEvent: true,
        browser: [ 'animation-duration', '-webkit-animation-duration'],
        overlay : false,
        overlayClass : 'animsition-overlay-slide',
        overlayParentElement : 'html',
        transition: function(url){ window.location.href = url; }
    });

    /*[ Back to top ]
    ===========================================================*/
    var windowH = $(window).height()/2;

    $(window).on('scroll',function(){
        if ($(this).scrollTop() > windowH) {
            $("#myBtn").css('display','flex');
        } else {
            $("#myBtn").css('display','none');
        }
    });

    $('#myBtn').on("click", function(){
        $('html, body').animate({scrollTop: 0}, 300);
    });


    /*==================================================================
    [ Fixed Header ]*/
    var headerDesktop = $('.container-menu-desktop');
    var wrapMenu = $('.wrap-menu-desktop');

    if($('.top-bar').length > 0) {
        var posWrapHeader = $('.top-bar').height();
    }
    else {
        var posWrapHeader = 0;
    }


    if($(window).scrollTop() > posWrapHeader) {
        $(headerDesktop).addClass('fix-menu-desktop');
        $(wrapMenu).css('top',0);
    }
    else {
        $(headerDesktop).removeClass('fix-menu-desktop');
        $(wrapMenu).css('top',posWrapHeader - $(this).scrollTop());
    }

    $(window).on('scroll',function(){
        if($(this).scrollTop() > posWrapHeader) {
            $(headerDesktop).addClass('fix-menu-desktop');
            $(wrapMenu).css('top',0);
        }
        else {
            $(headerDesktop).removeClass('fix-menu-desktop');
            $(wrapMenu).css('top',posWrapHeader - $(this).scrollTop());
        }
    });


    /*==================================================================
    [ Menu mobile ]*/
    $('.btn-show-menu-mobile').on('click', function(){
        $(this).toggleClass('is-active');
        $('.menu-mobile').slideToggle();
    });

    var arrowMainMenu = $('.arrow-main-menu-m');

    for(var i=0; i<arrowMainMenu.length; i++){
        $(arrowMainMenu[i]).on('click', function(){
            $(this).parent().find('.sub-menu-m').slideToggle();
            $(this).toggleClass('turn-arrow-main-menu-m');
        })
    }

    $(window).resize(function(){
        if($(window).width() >= 992){
            if($('.menu-mobile').css('display') == 'block') {
                $('.menu-mobile').css('display','none');
                $('.btn-show-menu-mobile').toggleClass('is-active');
            }

            $('.sub-menu-m').each(function(){
                if($(this).css('display') == 'block') { console.log('hello');
                    $(this).css('display','none');
                    $(arrowMainMenu).removeClass('turn-arrow-main-menu-m');
                }
            });

        }
    });


    /*==================================================================
    [ Show / hide modal search ]*/
    $('.js-show-modal-search').on('click', function(){
        $('.modal-search-header').addClass('show-modal-search');
        $(this).css('opacity','0');
    });

    $('.js-hide-modal-search').on('click', function(){
        $('.modal-search-header').removeClass('show-modal-search');
        $('.js-show-modal-search').css('opacity','1');
    });

    $('.container-search-header').on('click', function(e){
        e.stopPropagation();
    });


    /*==================================================================
    [ Isotope ]*/
    var $topeContainer = $('.isotope-grid');
    var $filter = $('.filter-tope-group');

    // filter items on button click
    $filter.each(function () {
        $filter.on('click', 'button', function () {
            var filterValue = $(this).attr('data-filter');
            $topeContainer.isotope({filter: filterValue});
        });

    });

    // init Isotope
    $(window).on('load', function () {
        var $grid = $topeContainer.each(function () {
            $(this).isotope({
                itemSelector: '.isotope-item',
                layoutMode: 'fitRows',
                percentPosition: true,
                animationEngine : 'best-available',
                masonry: {
                    columnWidth: '.isotope-item'
                }
            });
        });
    });

    var isotopeButton = $('.filter-tope-group button');

    $(isotopeButton).each(function(){
        $(this).on('click', function(){
            for(var i=0; i<isotopeButton.length; i++) {
                $(isotopeButton[i]).removeClass('how-active1');
            }

            $(this).addClass('how-active1');
        });
    });

    /*==================================================================
    [ Filter / Search product ]*/
    $('.js-show-filter').on('click',function(){
        $(this).toggleClass('show-filter');
        $('.panel-filter').slideToggle(400);

        if($('.js-show-search').hasClass('show-search')) {
            $('.js-show-search').removeClass('show-search');
            $('.panel-search').slideUp(400);
        }
    });

    $('.js-show-search').on('click',function(){
        $(this).toggleClass('show-search');
        $('.panel-search').slideToggle(400);

        if($('.js-show-filter').hasClass('show-filter')) {
            $('.js-show-filter').removeClass('show-filter');
            $('.panel-filter').slideUp(400);
        }
    });




    /*==================================================================
    [ Cart ]*/
    $('.js-show-cart').on('click',function(){
        console.log('pum mandar el post o el get con la data');
        var carrito = JSON.parse(localStorage.getItem("carrito"));
        //console.log(carrito);
        //+JSON.stringify(carrito)
        window.location = "/cart/shopping/";
        //$.get("/cart/shopping/",JSON.stringify(carrito));
        /*$.ajax({
          url:'/cart/shopping?=data"'+JSON.stringify(carrito)+'" ',
          type: 'GET',
          success: function functionName(){}});*///endAjax

        //$('.js-panel-cart').addClass('show-header-cart');
    });

    $('.js-hide-cart').on('click',function(){
        $('.js-panel-cart').removeClass('show-header-cart');
    });

    /*==================================================================
    [ Cart ]*/
    $('.js-show-sidebar').on('click',function(){
        $('.js-sidebar').addClass('show-sidebar');
    });

    $('.js-hide-sidebar').on('click',function(){
        $('.js-sidebar').removeClass('show-sidebar');
    });

    /*==================================================================
    [ +/- num product ]*/
    $('.btn-num-product-down').on('click', function(e){
      var numProduct = Number($(this).next().val());
      if (numProduct <= parseInt($('.cantHidden').text())) {
        if(numProduct >= 1){
          if (numProduct!=1) {
            $(this).next().val(numProduct - 1);
            $('.js-addcart-detail').attr('data-cantidad',numProduct - 1);
          }
        }
      }
    });

    $('.btn-num-product-up').on('click', function(e){
      var numProduct = Number($(this).prev().val());
      if (numProduct <= parseInt($('.cantHidden').text())) {
        numProduct = numProduct+1;
        if (numProduct <= parseInt($('.cantHidden').text())) {
          $(this).prev().val(numProduct);
          $('.js-addcart-detail').attr('data-cantidad',numProduct);
        }else {
          swal("Ya no hay mas productos", " ", "warning");
        }
      }
    });

    /*==================================================================
    [ Rating ]*/
    $('.wrap-rating').each(function(){
        var item = $(this).find('.item-rating');
        var rated = -1;
        var input = $(this).find('input');
        $(input).val(0);

        $(item).on('mouseenter', function(){
            var index = item.index(this);
            var i = 0;
            for(i=0; i<=index; i++) {
                $(item[i]).removeClass('zmdi-star-outline');
                $(item[i]).addClass('zmdi-star');
            }

            for(var j=i; j<item.length; j++) {
                $(item[j]).addClass('zmdi-star-outline');
                $(item[j]).removeClass('zmdi-star');
            }
        });

        $(item).on('click', function(){
            var index = item.index(this);
            rated = index;
            $(input).val(index+1);
        });

        $(this).on('mouseleave', function(){
            var i = 0;
            for(i=0; i<=rated; i++) {
                $(item[i]).removeClass('zmdi-star-outline');
                $(item[i]).addClass('zmdi-star');
            }

            for(var j=i; j<item.length; j++) {
                $(item[j]).addClass('zmdi-star-outline');
                $(item[j]).removeClass('zmdi-star');
            }
        });
    });

    /*==================================================================
    [ Show modal1 ]*/
    $('.js-show-modal1').on('click',function(e){
        e.preventDefault();
        console.log('---->',e.currentTarget.dataset);
        //clean
        $('#imageDinamic').empty();
        $('#imageDinamic2').empty();

        //Set
        $('.item-slick3').data('thumb',e.currentTarget.dataset.image);
        $('#imageDinamic2').attr('href',e.currentTarget.dataset.image);
        $('.mtext-105').text(e.currentTarget.dataset.name);//name
        $('.mtext-106').text(e.currentTarget.dataset.price);//price
        $('.stext-102').text(e.currentTarget.dataset.description);//description
        $('.cantHidden').text(e.currentTarget.dataset.cant);//cantidad de productos
        $('#imageDinamic').append("<img id='' src='"+e.currentTarget.dataset.image+"' alt=''>");//description
        $('.js-addcart-detail').attr('data-image',e.currentTarget.dataset.image);
        $('.js-addcart-detail').attr('data-name',e.currentTarget.dataset.name);
        $('.js-addcart-detail').attr('data-cant',e.currentTarget.dataset.cant);
        $('.js-addcart-detail').attr('data-id',e.currentTarget.dataset.id);
        $('.js-addcart-detail').attr('data-price',e.currentTarget.dataset.price);

        /*apendo el id en el boton up y down*/
        $('.btn-num-product-down').attr('data-id',e.currentTarget.dataset.id);
        $('.btn-num-product-up').attr('data-id',e.currentTarget.dataset.id);
        $('#cantHidden').text(e.currentTarget.dataset.cant);



        $('.js-modal1').addClass('show-modal1');
    });

    $('.js-hide-modal1').on('click',function(){
      $('#imageDinamic').empty();
      $('#imageDinamic2').empty();

      //Set
      $('.item-slick3').data('thumb','');
      $('#imageDinamic2').attr('href','');
      $('.mtext-104').val('0');//name
      $('.mtext-105').text('');//name
      $('.mtext-106').text('');//price
      $('.stext-102').text('');//description
      $('.cantHidden').text('');//cantidad de productos
      $('#imageDinamic').append("<img id='' src='' alt=''>");//description
        $('.js-modal1').removeClass('show-modal1');
    });



})(jQuery);
