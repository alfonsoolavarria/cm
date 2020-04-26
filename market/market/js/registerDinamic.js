$(document).ready(function() {
//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function(e){
  var flag=0;
  //if(animating) return false;
  //animating = true;
  if ($(".next").attr('data-section')=='1') {
    if ($("#1pass").val() != $("#1cpass").val()) {
      alertify.error("Las contraseñas no coinciden");
    }else {
      if ($("#1email").val().length<1 || $("#1pass").val().length<1 || $("#1cpass").val().length<1) {
        alertify.error("Hay campos requeridos");
      }else {
        e.preventDefault();
        $(".next").attr('data-section','2')
        $("#m2").addClass("active");
        current_fs = $(this).parent();
        next_fs = $(this).parent().next();

        //activate next step on progressbar using the index of next_fs
        //$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

        //show the next fieldset
        next_fs.show();
        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
          step: function(now, mx) {
            //as the opacity of current_fs reduces to 0 - stored in "now"
            //1. scale current_fs down to 80%
            //scale = 1 - (1 - now) * 0.2;
            scale = 0;
            //2. bring next_fs from the right(50%)
            //left = (now * 50)+"%";
            left = 0+"%";
            //3. increase opacity of next_fs to 1 as it moves in
            opacity = 1 - now;
            current_fs.css({
              'transform': 'scale('+scale+')',
              'position': 'absolute'
            });
            next_fs.css({'left': left, 'opacity': opacity});
          },
          duration: 800,
          complete: function(){
            current_fs.hide();
            animating = false;
          },
          //this comes from the custom easing plugin
          easing: 'easeInOutBack'
        });

        current_fs.animate({opacity: 0}, {
          step: function(now, mx) {
            current_fs.css({
              'position': 'relative'
            });
          }

        });
      }
    }


  }
  else if ($(".next").attr('data-section')=='2') {
    if ($("#2fname").val().length<1 || $("#2lname").val().length<1 || $("#2phone").val().length<1 || $("#2address").val().length<1) {
      alertify.error("Hay campos requeridos");
    }else {
      e.preventDefault();
      $(".next").attr('data-section','3')
      current_fs = $(this).parent();
      next_fs = $(this).parent().next();
      $("#m3").addClass("active");
      //activate next step on progressbar using the index of next_fs
      //$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

      //show the next fieldset
      next_fs.show();
      //hide the current fieldset with style
      current_fs.animate({opacity: 0}, {
        step: function(now, mx) {
          //as the opacity of current_fs reduces to 0 - stored in "now"
          //1. scale current_fs down to 80%
          //scale = 1 - (1 - now) * 0.2;
          scale = 0;
          //2. bring next_fs from the right(50%)
          //left = (now * 50)+"%";
          left = 0+"%";
          //3. increase opacity of next_fs to 1 as it moves in
          opacity = 1 - now;
          current_fs.css({
            'transform': 'scale('+scale+')',
            'position': 'absolute'
          });
          next_fs.css({'left': left, 'opacity': opacity});
        },
        duration: 800,
        complete: function(){
          current_fs.hide();
          animating = false;
        },
        //this comes from the custom easing plugin
        easing: 'easeInOutBack'
      });

      current_fs.animate({opacity: 0}, {
        step: function(now, mx) {
          current_fs.css({
            'position': 'relative'
          });
        }

      });
    }
  }else{
    console.log('error');
  }

});


$(".previous").click(function(){

  if ($(".next").attr('data-section')=='2') {
    $(".next").attr('data-section','1')
    $("#m1").addClass("active");
    $("#m2").removeClass("active");
    $("#m3").removeClass("active");

  }
  if ($(".next").attr('data-section')=='3') {
    $(".next").attr('data-section','2')
    $("#m1").addClass("active");
    $("#m2").addClass("active");
    $("#m3").removeClass("active");
  }
  if(animating) return false;
  animating = true;

  current_fs = $(this).parent();
  previous_fs = $(this).parent().prev();

  //de-activate current step on progressbar
  $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

  //show the previous fieldset
  previous_fs.show();
  //hide the current fieldset with style
  current_fs.animate({opacity: 0}, {
    step: function(now, mx) {
      //as the opacity of current_fs reduces to 0 - stored in "now"
      //1. scale previous_fs from 80% to 100%
      //scale = 0.8 + (1 - now) * 0.2;
      scale = 0.8 + (1 - now) * 0.2;
      //2. take current_fs to the right(50%) - from 0%
      left = ((1-now) * 50)+"%";
      //3. increase opacity of previous_fs to 1 as it moves in
      opacity = 1 - now;
      current_fs.css({'left': left});
      previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
    },
    duration: 800,
    complete: function(){
      current_fs.hide();
      animating = false;
    },
    //this comes from the custom easing plugin
    easing: 'easeInOutBack'
  });
});


});
