$(document).ready(function() {

  $('.login').submit(function (e) {
    e.preventDefault();
    var formDataLogin = $(".login").serializeArray()
    len = formDataLogin.length,
    dataObjlogin = {};
    for (i=0; i<len; i++) {
      dataObjlogin[formDataLogin[i].name] = formDataLogin[i].value;
    }
    if (len>0) {
      $.post('/login/',{
        csrfmiddlewaretoken:e.currentTarget[0].value,
        email:dataObjlogin.email,
        password:dataObjlogin.pass,
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
    }

   });

  $('#msform').submit(function (e) {
    e.preventDefault();
    var formData = $("#msform").serializeArray()
    len = formData.length,
    dataObj = {};
    for (i=0; i<len; i++) {
      dataObj[formData[i].name] = formData[i].value;
    }

    if (len>0) {

      function validateEmail(email) {
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
      }

      var validate = validateEmail(dataObj.email);
      if (!validate ) {
        swal("Email incorrecto", " ", "warning");
        return false;
      }
      if (dataObj.pass != dataObj.pass2) {
        swal("Claves incorrectas", " ", "warning");
        return;
      }

      $.post('/profile/',{
        email:dataObj.email,
        password:dataObj.pass,
        name:dataObj.fname,
        lastname:dataObj.lname,
        phone:dataObj.telefono,
        direction:dataObj.direccion,
      }).done(function (result) {
        if (result.code==200) {
          swal("Usuario Creado con Éxito", " ", "success");
          var delayInMilliseconds = 1000; //menos de 1 second
          setTimeout(function() {
            if ($("#flagReload").val()=='0'){
              window.location.href = '/'
            }else{
              location.reload(true);
            }
          }, delayInMilliseconds);
          $.post('/client/web/email/',{
            email:dataObj.email
          }).done(function (result) {
            if (result.code!=200) {
              swal(result.error[0], " ", "warning");
            }
            }).fail(function(error) {
              console.log(error.responseText);
            });
        }else {
          //poner un tootip
          swal(result.error[0], " ", "warning");
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
