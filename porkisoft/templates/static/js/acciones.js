$(document).on('ready', inicio);
 function inicio()
 {
   
     $('#tablaCompras').dataTable({

         "sDom": '<"top"i>rt<"bottom"flp><"clear">'
    });
     $('#tablaProductos').dataTable({

         "sDom": '<"top"i>rt<"bottom"flp><"clear">'
    });
    $('#ListaSubp').dataTable({

         "sDom": '<"top"i>rt<"bottom"flp><"clear">'
    });
     $('#tablabodegas').dataTable({

         "sDom": '<"top"i>rt<"bottom"flp><"clear">'
    });

    $('#borrador').on('click',pregunta);
 }
function pregunta(){

    if(confirm('Desea usted borrar el registro?'))this.form.submit();
}


