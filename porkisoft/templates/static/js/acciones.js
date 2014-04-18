$(document).on('ready', inicio);
 function inicio()
 {
     $('#id_precioTotal').on('focus',calculoGanado);

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
function calculoGanado(){


         var pesoEnPie = $('#id_pesoEnPie').val();
         var vrKiloEnPie = $('#id_precioKiloEnPie').val();
         var total = pesoEnPie * vrKiloEnPie;
            $('#id_precioTotal').val(total);



}

 }



