$(document).on('ready', inicio);
 function inicio()
 {

     $('#id_precioTotal').on('focus',calculoGanado);

     $('#id_difPesos').on('focus',calculoCanal);

     $('#id_subtotal').on('focus', calculoCompra);

     $('#id_pesoProductoAntes').on('focus', calculoEnsalinado);

     $('#tablacostos').dataTable({

         "bPaginate": true,
         "bLengthChange": true,
         "bFilter": true,
         "bSort": true,
         "bInfo": true,
         "bAutoWidth": false

    });
     $('#tablastock').dataTable({

         "bPaginate": true,
         "bLengthChange": true,
         "bFilter": true,
         "bSort": true,
         "bInfo": true,
         "bAutoWidth": false

    });

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

     $('#tablaProductos').dataTable( {
        "bPaginate": true,
         "bFilter": true,
         "bSort": true,
         "bInfo": true,
         "bAutoWidth": true,
         "bLengthChange": false
    } );

    $('#ListaSubp').dataTable({

         "sDom": '<"top"iflp<"clear">>',
          "sPaginationType" : "full_numbers"
    });
     $('#tablabodegas').dataTable({

         "bPaginate": true,
         "bFilter": true,
         "bSort": true,
         "bInfo": true,
         "bAutoWidth": true,
         "bLengthChange": false
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

function calculoCompra()
{
    var unidades = $('#id_unidades').val();
    var pesoProducto = $('#id_pesoProducto').val();
    var vrUnitario = $('#id_vrCompraProducto').val();

    if (unidades !=0){

        var totalUnidades = unidades * vrUnitario;
        $('#id_subtotal').val(totalUnidades);
    }
    if (pesoProducto != 0){

        var totalPeso = (pesoProducto/ 1000) * vrUnitario;
        $('#id_subtotal').val(totalPeso);
    }

}

function calculoEnsalinado()
{
    var pesoProducto = $('#id_pesoProducto').val();
    var pesoSal = $('#id_pesoSal').val();
    var pesoPapaina = $('#id_pesoPapaina').val();
    var pesoAntes = parseFloat(pesoProducto) + parseFloat(pesoSal) + parseFloat(pesoPapaina);

    $('#id_pesoProductoAntes').val(pesoAntes);

}




