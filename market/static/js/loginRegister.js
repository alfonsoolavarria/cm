$(document).ready(function() {

  $('.login').submit(function (e) {
    e.preventDefault();
    /*console.log('Login',e.currentTarget);
    console.log(e.currentTarget[0].value); // csrf
    console.log(e.currentTarget[2].value); // email
    console.log(e.currentTarget[3].value); // password*/
    $.post('/login/',{
      csrfmiddlewaretoken:e.currentTarget[0].value,
      email:e.currentTarget[2].value,
      password:e.currentTarget[3].value
    }).done(function (result) {
      if (result.code==200) {
        if ($("#flagReload").val()=='0'){
          window.location.href = '/'
        }else{
          location.reload();
        }
      }else {
        //poner un tootip
        swal("Intente de nuevo", " ", "warning");
        //alertify.error('intente de nuevo '+result.message);
      }
    }).fail(function(error) {
      console.log(error.responseText);
    });
   });

  $('#msform').submit(function (e) {
    e.preventDefault();
    var formData = $("#msform").serializeArray()
    len = formData.length,
    dataObj = {};
    for (i=0; i<len; i++) {
      dataObj[formData[i].name] = formData[i].value;
    }
    console.log(dataObj);

    /*console.log("nuevo registro");
    console.log('Registro',e.currentTarget);
    console.log(e.currentTarget[1].value); // email
    console.log(e.currentTarget[2].value); // password
    console.log(e.currentTarget[3].value); // confir password

    console.log(e.currentTarget[6].value); // name
    console.log(e.currentTarget[7].value); // lastname
    console.log(e.currentTarget[8].value); // phone
    console.log(e.currentTarget[9].value); // direction

    console.log(e.currentTarget[13].value); // Tw
    console.log(e.currentTarget[14].value); // Fb
    console.log(e.currentTarget[15].value); // Goo*/
    if (len>0) {

        function validateEmail(email) {
          var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return re.test(email);
        }

      var validate = validateEmail(dataObj.email);
      if (!validate ) {
        swal("Email incorrecto", " ", "warning");
        //alertify.error("Email incorrecto");
        return false;
      }
      if (dataObj.pass != dataObj.pass2) {
        swal("Claves incorrectas", " ", "warning");
        return false;
      }

      $.post('/profile/',{
        email:dataObj.email,
        password:dataObj.pass,
        name:dataObj.fname,
        lastname:dataObj.lname,
        phone:dataObj.telefono,
        direction:dataObj.direccion,
      }).done(function (result) {
        console.log("resultresult",result);
        if (result.code==200) {
          alertify.success('Usuario Creado con Éxito');
          var delayInMilliseconds = 1000; //menos de 1 second
          setTimeout(function() {
            if ($("#flagReload").val()=='0'){
              window.location.href = '/'
            }else{
              location.reload(true);
            }
          }, delayInMilliseconds);
        }else {
          //poner un tootip
          alertify.error(result.error[0]);
        }
      }).fail(function(error) {
        console.log(error.responseText);
      });

    }else {
      swal("Hace falta llenar un campo requerido", " ", "warning");
      //alertify.error('Hace falta llenar un campo requerido');
    }

   });

});
