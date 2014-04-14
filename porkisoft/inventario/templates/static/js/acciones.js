$(document).on('ready', inicio);
 function inicio()
 {
     $('#tablaProductos').dataTable({

         "sDom": '<"top"i>rt<"bottom"flp><"clear">'
    });
    $('#ListaSubp').dataTable({

         "sDom": '<"top"i>rt<"bottom"flp><"clear">'
    });

    $('#borrador').on('click',pregunta);
 }
function pregunta(){

    if(confirm('Desea usted borrar el registro?'))this.form.submit();
}


