$(document).on('ready', inicio);
 function inicio()
 {

     $('#id_precioTotal').on('focus',calculoGanado);

     $('#id_difPesos').on('focus',calculoCanal);

     $('#tablaTraslados').dataTable({

         "bPaginate": true,
         "bLengthChange": true,
         "bFilter": true,
         "bSort": true,
         "bInfo": true,
         "bAutoWidth": true,
         "aaSorting": [[ 4, "desc" ]]
    });

     $('#tablaCompras').dataTable({

         "bPaginate": true,
         "bFilter": true,
         "bSort": true,
         "bInfo": true,
         "bAutoWidth": true,
         "bLengthChange": false
    });
     $('#tablaProductos').dataTable({

        "bPaginate": true,
         "bFilter": true,
         "bSort": true,
         "bInfo": true,
         "bAutoWidth": true,
         "bLengthChange": false

    });
    $('#ListaSubp').dataTable({

         "sDom": '<"top"iflp<"clear">>',
          "sPaginationType" : "full_numbers"
    });
     $('#tablabodegas').dataTable({

         "sDom": '<"top"iflp<"clear">>',
          "sPaginationType" : "full_numbers"
    });
     $('#tablaproveedor').dataTable({

         "sDom": '<"top"iflp<"clear">>',
          "sPaginationType" : "full_numbers"
    });
     $('#despostes').dataTable({

         "bPaginate": true,
         "bFilter": true,
         "bSort": true,
         "bInfo": true,
         "bAutoWidth": true,
         "bLengthChange": false
       });
 }
function calculoGanado(){


         var pesoEnPie = $('#id_pesoEnPie').val();
         var vrKiloEnPie = $('#id_precioKiloEnPie').val();
         var total = pesoEnPie * vrKiloEnPie;
            $('#id_precioTotal').val(total);



}
     function calculoCanal(){

         var pesoPorkilandia = $('#id_pesoPorkilandia').val();
         var pesoFrigovito = $('#id_pesoFrigovito').val();
         var totalCanal =  pesoFrigovito - pesoPorkilandia;

         $('#id_difPesos').val(totalCanal.toFixed(2));
     }




