$(document).on('ready', inicio);
$( document ).tooltip();
 function inicio()
 {
    /*$(document).keypress(function(e)
     {

         if(e.which == 67)
         {
                showModalDialog('/fabricacion/costos/')
         }


     });*/


     $('#id_precioTotal').on('focus',calculoGanado);
     $('#id_difPesos').on('focus',calculoCanal);
     $('#id_vrCompraProducto').on('focus', calculoCompra);
     $('#id_pesoPapaina').on('blur', calculoEnsalinado);
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
     $('#Guardatraslado').on('click',GuardarTraslado);
     $('#id_productoTraslado').on('change',ConsultaStock);
     $('#id_productoCondimento').on('change',VerificarExistencias);
     $('#id_productoMiga').on('change',VerificarExistenciasMiga);
     $('#id_desposteHistorico').on('change',TraerCosto);
     $('#id_polloHistorico').on('change',TraerCostoPollo);
     $('#guardarTajado').on('click',GuardarTajado);
     $('#id_vrKiloDescongelado').on('focus',calculoKiloDescongelado);
     $('#id_costoFilete').on('focus',traerCostoFilete);
     $('#id_pesoFileteCond').on('focus',calculaPesoCondimentado);
     $('#id_costoFileteCond').on('focus',calculaCostoCondimentado);
     $('#id_productoEnsalinado').on('change',TraecostoEnsalinado);


     $('#canalPendiente').dataTable();
     $('#tablaenTajados').dataTable();
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
     $('#descarnes').dataTable();
     $('#TablaCondimentado').dataTable();

     $('#id_fecha').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaCompra').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaDesposte').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaTajado').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaEnsalinado').datepicker({ dateFormat: "dd/mm/yy" });


     //$( "#id_fechaCompra" ).tooltip();

}

/**************************************************** METODOS *********************************************************/
function TraecostoEnsalinado()
{
    var producto = $('#id_productoEnsalinado').val();
    var peso = $('#id_pesoProducto').val();
    Existencias(producto,6,peso);
}
function GuardarEnsalinado(idEnsalinado)
{
    var opcion = confirm('Desea guardar este Registro, recuerde que esto afectara el inventario?');
    if (opcion == true)
    {
        $.ajax({

            url : '/fabricacion/guardarEnsalinado/',
            dataType : "json",
            type : "get",
            data : {'idEnsalinado':idEnsalinado},
            success : function(respuesta)
            {
                if (respuesta != '')
                {
                    $('#id_costoFilete').val(respuesta)
                }

            }

        });
    }

}
function GuardarCondimentado(idCondimentado)
{
    var opcion = confirm('Desea guardar este Registro?');
    if (opcion == true)
    {
        $.ajax({

            url : '/fabricacion/guardarCondimentado/',
            dataType : "json",
            type : "get",
            data : {'idCondimentado':idCondimentado},
            success : function(respuesta)
            {
                if (respuesta != '')
                {
                    $('#id_costoFilete').val(respuesta)
                }

            }

        });
    }

}
function calculaCostoCondimentado()
{
    var pesoFilete = parseInt($('#id_pesoACondimentar').val());
    var condimento = parseInt($('#id_condimento').val());
    var costoFilete = parseInt($('#id_costoFilete').val());
    var costoCondimento = parseInt($('#id_costoCondimento').val());

    var costoTotalFilete = (pesoFilete / 1000) * costoFilete;
    var costoTotalCond = (condimento / 1000) * costoCondimento;
    var totalCondimentado = pesoFilete + condimento;
    var costoFileteCondimentado = Math.round((costoTotalFilete + costoTotalCond)/(totalCondimentado/1000));
    $('#id_costoFileteCond').val(costoFileteCondimentado);

}
function calculaPesoCondimentado()
{
    var pesoFilete = parseInt($('#id_pesoACondimentar').val());
    var condimento = parseInt($('#id_condimento').val());
    var totalCondimentado = pesoFilete + condimento;
    $('#id_pesoFileteCond').val(totalCondimentado);


}
function traerCostoFilete()
{
    var producto = $('#id_producto').val();

    $.ajax({

            url : '/fabricacion/traercostoFilete/',
            dataType : "json",
            type : "get",
            data : {'producto':producto},
            success : function(respuesta)
            {
                if (respuesta != '')
                {
                    $('#id_costoFilete').val(respuesta)
                }

            }

        });


}
function calculoKiloDescongelado()
{
    var vrFactura = $('#id_subtotal').val();
    var pesoDesc = $('#id_pesoDescongelado').val();
    var total = Math.round(vrFactura / (pesoDesc/1000));
    $('#id_vrKiloDescongelado').val(total);
}
function TraerCostoPollo()
{
    var compra = $('#id_polloHistorico').val();
    var producto = $('#id_producto').val();


    $.ajax({

            url : '/fabricacion/traercostopollo/',
            dataType : "json",
            type : "get",
            data : {'compra':compra,'producto':producto},
            success : function(respuesta)
            {
                if (respuesta != '')
                {
                    $('#id_costoKiloFilete').val(respuesta)
                }

            }

        });

}

function TraerCosto()
{
    var desposte = $('#id_desposteHistorico').val();
    var producto = $('#id_producto').val();


    $.ajax({

            url : '/fabricacion/traercosto/',
            dataType : "json",
            type : "get",
            data : {'desposte':desposte,'producto':producto},
            success : function(respuesta)
            {
                if (respuesta != '')
                {
                    $('#id_costoKiloFilete').val(respuesta)
                }

            }

        });

}
function GuardaDescarne(idDescarne)
{

   var opcion = confirm('Desea guardar el descarne No.'+ idDescarne + '?')
    if(opcion == true)
    {
        $.ajax({

            url : '/fabricacion/guardaDescarne/',
            dataType : "json",
            type : "get",
            data : {'descarne':idDescarne},
            success : function(respuesta)
            {
                if (respuesta != '')
                {
                    alert(respuesta);
                }

            }

        });
    }


}

function VerificarExistenciasMiga()
{
    var id = $('#id_productoMiga').val();
    var peso = $('#id_PesoProducto').val();
    var pesoTotal = parseInt($('#cantFormulas').text());
    var pesoReal = peso * pesoTotal;

    Existencias(id,6,pesoReal);
}
function VerificarExistencias()
{
    var id = $('#id_productoCondimento').val();
    var peso = $('#id_pesoProducto').val();
    var pesoTotal = parseInt($('#cantFormulasCond').text());

    var pesoReal = peso * pesoTotal;

    Existencias(id,6,pesoReal);
}

function Existencias(idProducto,idBodega,pesoProducto)
{
    /*Metodo para verificar el stock del producto seleccionado*/

    $.ajax({

            url : '/fabricacion/existencias/',
            dataType : "json",
            type : "get",
            data : {'producto':idProducto,'bodega':idBodega,'peso':pesoProducto},
            success : function(respuesta)
            {
                if (respuesta != '')
                {
                    alert(respuesta);
                }

            }

        });
}

function ConsultaStock()
{
    var codigoTraslado = $('#codigoTraslado').text();
    var pesoTraslado = $('#id_pesoTraslado').val();
    var undTraslado = $('#id_unidadesTraslado').val();
    var producto = $('#id_productoTraslado').val();
    $.ajax({

            url : '/inventario/consultaStock/',
            dataType : "json",
            type : "get",
            data : {'producto':producto,'codigoTraslado':codigoTraslado,
                'pesoTraslado':pesoTraslado,'undTraslado':undTraslado},
            success : function(respuesta)
            {
                if (respuesta != '')
                {
                    alert(respuesta);
                }

            }

        });
}
function GuardarTraslado()
{
    var codigoTraslado = $('#codigoTraslado').text();
    var opcion = confirm('Desea guardar el traslado?');

    if (opcion == true)
    {
        $.ajax({

        url : '/inventario/guardaTraslado/',
         dataType: "json",
         type: "get",
         data : {'codigoTraslado':codigoTraslado},
         success : function(respuesta){
             alert(respuesta);
                      }
    });
    }

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
    var kiloCarnes2 = parseInt($('#kiloCarnes2').text());
    var kiloCarnes3 = parseInt($('#kiloCarnes3').text());
    var kiloCarnes4 = parseInt($('#kiloCarnes4').text());
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
             'kiloCarnes2':kiloCarnes2,'kiloCarnes3':kiloCarnes3,'kiloCarnes4':kiloCarnes4,
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
    var subtotal = $('#id_subtotal').val();

    if (unidades !=0){

        var totalUnidades = subtotal / unidades;
        $('#id_vrCompraProducto').val(totalUnidades);

    }
    if (pesoProducto != 0){

        var totalPeso = Math.round(subtotal / (pesoProducto/ 1000));
        $('#id_vrCompraProducto').val(totalPeso);

    }

}

function calculoEnsalinado()
{
    /* Metodo que verifica las existencias de sal y papaina */

    var pesoProducto = $('#id_pesoProducto').val();
    var pesoSal = $('#id_pesoSal').val();
    var pesoPapaina = $('#id_pesoPapaina').val();
    var pesoAntes = parseFloat(pesoProducto) + parseFloat(pesoSal) + parseFloat(pesoPapaina);
    $('#id_pesoProductoAntes').val(pesoAntes);
    /* se envia la sal y la papaina como parametros de busqueda
    * Sal = 89
    * Papaina = 95
    * */
    Existencias(89,6,pesoSal);
    Existencias(95,6,pesoPapaina);

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
    var tipo = $('#tipo').text();
    var idTajado = $('#idTajado').text();
    var peso = $('#id_pesoProducto').val();

     $.ajax({

        url : '/fabricacion/costearTajado/',
         dataType: "json",
         type: "get",
         data : {'peso':peso,'tipo':tipo,'idTajado':idTajado},
         success : function(respuesta){
             alert(respuesta)
         }
    });
}

function GuardarTajado()
{
    var idTajado = $('#idTajado').text();
    var opcion = confirm('Desea guardar el tajado?')
    if (opcion == true)
    {
        $.ajax({

        url : '/fabricacion/guardarTajado/',
         dataType: "json",
         type: "get",
         data : {'idTajado':idTajado},
         success : function(respuesta){
             alert(respuesta)
         }
    });
    }

}
