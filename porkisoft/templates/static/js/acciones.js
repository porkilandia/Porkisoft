$(document).on('ready', inicio);
 function inicio()
 {

     $('#id_precioTotal').on('focus',calculoGanado);

     $('#id_peosTotalCanal').on('focus',calculoCanal);


     $('#tablaCompras').dataTable({

         "sDom": '<"top"iflp<"clear">>',
          "sPaginationType" : "full_numbers"
    });
     $('#tablaProductos').dataTable({

        "sDom": '<"top"iflp<"clear">>',
          "sPaginationType" : "full_numbers"
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

         "sDom": '<"top"iflp<"clear">>',
          "sPaginationType" : "full_numbers"
       });
 }
function calculoGanado(){


         var pesoEnPie = $('#id_pesoEnPie').val();
         var vrKiloEnPie = $('#id_precioKiloEnPie').val();
         var total = pesoEnPie * vrKiloEnPie;
            $('#id_precioTotal').val(total);



}
     function calculoCanal(){

         var pesoBrazos = $('#id_pesoBrazos').val();
         var pesoPiernas = $('#id_pesoPiernas').val();
         var totalCanal =  parseInt(pesoBrazos)+ parseInt(pesoPiernas);

         $('#id_peosTotalCanal').val(totalCanal);
     }




