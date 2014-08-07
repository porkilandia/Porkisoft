$(document).on('ready', inicio);
 function inicio()
 {

     $('#id_precioTotal').on('focus',calculoGanado);
     $('#id_difPesos').on('focus',calculoCanal);
     $('#id_subtotal').on('focus', calculoCompra);
     $('#id_pesoProductoAntes').on('focus', calculoEnsalinado);
     $('#nuevo').on('click',nuevoRegistro);
     $('#cerrar').on('click',cerrarVentana);
     $('#editaFila').on('click',editaFilas);
     $('#modificar').on('click',modificaRegistro);
     $('#costear').on('click',CostearDesposte);
     $('#costearTajado').on('click',CostearTajado);
     $('#guardar').on('click',GuardarDesposte);
     $('#id_producto').on('change',consultaValorProducto);
     $('#id_vrTotal').on('focus',calculoValorProducto);
     $('#guardarVentas').on('click',GuardarVentas);

     $('#canalPendiente').dataTable();
     $('#tablacostos').dataTable();
     $('#tablastock').dataTable();
     $('#tablaTraslados').dataTable();
     $('#tablaCompras').dataTable();
     $('#tablaProductos').dataTable();
     $('#ListaSubp').dataTable();
     $('#tablabodegas').dataTable();
     $('#tablaproveedor').dataTable();
     $('#despostes').dataTable();
     $('#costos').dataTable();


}
function GuardarVentas()
{
    var opcion = confirm('Desea guardar los cambios?');
    var idVenta = $('#codigoVenta').text();
    var peso = parseFloat($('#peso').text());
    if (opcion == true)
    {
        $.ajax({

        url : '/ventas/guardaVenta/',
         dataType: "json",
         type: "get",
         data : {'idVenta':idVenta,'peso':peso},
         success : function(respuesta){
             alert(respuesta);
                      }
    });
    }
}

function CostearDesposte()
{
    var idDesposte = parseInt($('#codigoPlanilla').text());
    var pesoCanales = parseInt($('#pesoCanales').text());
    var kiloCarnes = parseInt($('#kiloCarnes').text());
    var kiloCostilla = parseInt($('#kiloCostilla').text());
    var kiloHueso = parseInt($('#kiloHueso').text());
    var kiloSubProd = parseInt($('#kiloSubProd').text());
    var kiloDesecho = parseInt($('#kiloDesecho').text());

    var costeo = confirm('Desea Costear La planilla?');

    if (costeo == true)
    {
        $.ajax({

         url : '/fabricacion/costeoDesposte/',
         dataType: "json",
         type: "get",
         data : {'kiloCostilla':kiloCostilla,'idDesposte':idDesposte,'pesoCanales':pesoCanales,'kiloCarnes':kiloCarnes,
             'kiloHueso':kiloHueso,'kiloSubProd':kiloSubProd,'kiloDesecho':kiloDesecho},
         success : function(respuesta){
             alert(respuesta)
         }

     });
    }
}
function calculoValorProducto()
{
    var peso = $('#id_peso').val();
    var vrKilo = $('#id_vrUnitario').val();
    var total = Math.round((vrKilo * peso)/1000);

    $('#id_vrTotal').val(total);
}

function consultaValorProducto()
{
    var combo = $('#id_producto').val();
    var idVenta = $('#codigoVenta').text();
    var peso = $('#id_peso').val();

     $.ajax({

        url : '/ventas/consultaPrecioProducto/',
         dataType: "json",
         type: "get",
         data : {'idProducto':combo,'idVenta':idVenta,'peso':peso},
         success : function(respuesta){

             if(respuesta)
             {
                 $('#id_vrUnitario').val(respuesta)
             }else
             {
                 alert('No hay existencias en almacen')
             }

                      }
    });


}

function GuardarDesposte()
{
    var idDesposte = parseInt($('#codigoPlanilla').text());
    var guardado = confirm('desea Guardad los productos en bodega ');
    if (guardado == true)
    {
        $.ajax({

        url : '/fabricacion/guardarDesposte/',
         dataType: "json",
         type: "get",
         data : {'idDesposte':idDesposte},
         success : function(respuesta){
             alert(respuesta)
         }
    });
    }

}
function cargaDatos(datos)
     {
         var $tabla  = $('#lista');
            $tabla.find("tr:gt(0)").remove();
             for (var indice in datos)
             {
                 desposte = datos[indice];
                 $tabla.append(
                    "<tr><td >" + desposte.codigo +
                    "</td><td >" + desposte.fecha +
                    "</td><td >" + desposte.numReses +
                    "</td></tr>");
             }
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

function nuevoRegistro()
     {
         $('fieldset').fadeIn();
         return false
     }

function cerrarVentana()
{
    $('fieldset').fadeOut();
}

function editaFilas()
{
    $('#tablaproveedor td').attr('contenteditable','true');

}
function eliminarFilas()
{
    /**
         * Funcion para eliminar la ultima columna de la tabla.
         * Si unicamente queda una columna, esta no sera eliminada
         */
    // Obtenemos el total de columnas (tr) del id "tabla"
            var trs=$('tr', $("#tablaproveedor")).length;
            if(trs>1)
            {
                // Eliminamos la ultima columna
                $("#tablaproveedor td:last").remove();
            }
}

function modificaRegistro()
{
    $('fieldset').fadeIn();
    return false
}

function CostearTajado()
{

}
