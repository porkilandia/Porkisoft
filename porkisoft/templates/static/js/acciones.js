$(document).on('ready', inicio);

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
     $('#id_productoVenta').on('change',consultaValorProducto);
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
     $('#id_miga').on('blur', ExistenciasApanado);
     $('#id_productoApanado').on('change',existenciasFileteCondimentado);
     $('#id_totalApanado').on('focus',calculoTotalApanado);
     $('#id_productoMolido').on('change',existenciasCarneAMoler);
     $('#id_productoLista').on('change',CostoProdListaPrecios);
     $('#id_produccion').on('change',CostoKiloChuleta);

     //var tablaEmpacado = $('#tablaEmpacado tr');
     //tablaEmpacado.on('click',maneja);

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
     $('#tablaensalinados').dataTable();
     $('#tablaEmpacado').dataTable();

     $('#id_fecha').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaCompra').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaDesposte').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaTajado').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaEnsalinado').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaApanado').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaVenta').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaRecepcion').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaSacrificio').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaFabricacion').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaMolido').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaEmpacado').datepicker({ dateFormat: "dd/mm/yy" });
     $('#inicio').datepicker({ dateFormat: "dd/mm/yy" });
     $('#fin').datepicker({ dateFormat: "dd/mm/yy" });


     $('#acordeon').accordion({ heightStyle: "content" });
     $( "#progressbar" ).progressbar({value: false}).hide();


}

/**************************************************** METODOS *********************************************************/
/*function maneja()
{
    //Funcion para recorrer una tabla de datos y guardar sus registros en variables
    var a, b, c, d, f, g,h;
    $(this).children("td").each(function(e) {

        switch (e)
        {
            case 0:
                a = $(this).text();
                break;
            case 1:
                b = $(this).text();
                break;
            case 2:
                c = $(this).text();
                break;
            case 3:
                d = $(this).text();
                break;
            case 4:
                f = $(this).text();
                break;
            case 5:
                g = $(this).text();
                break;
            case 6:
               h = $(this).text();
                break;

        }

    });
    alert(f);
}*/
function consultaDescarnes ()
{   $( "#progressbar" ).show();
    var inicio = $('#inicio').val();
    var fin = $('#fin').val();
    var grupo = $('#grupo').val();


    $.ajax({

            url : '/fabricacion/promDescarnes/',
            dataType : "json",
            type : "get",
            data : {'inicio':inicio,'fin':fin,'grupo':grupo},
            success : function(respuesta)
            {
                $("#recortes").find("tr:gt(0)").remove();
                $("#procesos").find("tr:gt(0)").remove();
                $("#caretas").find("tr:gt(0)").remove();
                $("#lenguas").find("tr:gt(0)").remove();
                $("#procesosCerdo").find("tr:gt(0)").remove();
                $("#pesoRecortes").find("tr:gt(0)").remove();
                $("#pesoProcesos").find("tr:gt(0)").remove();
                $("#pesoLenguas").find("tr:gt(0)").remove();
                $("#pesoCaretas").find("tr:gt(0)").remove();
                $("#pesoProcesosCerdo").find("tr:gt(0)").remove();

                $.each(respuesta.promedioRecortes,function(key,value){

                    $("#recortes").append("<tr><td>" + 'Recortes' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.promedioProcesos,function(key,value){

                    $("#procesos").append("<tr><td>" + 'Procesos' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.promedioCaretas,function(key,value){

                    $("#caretas").append("<tr><td>" + 'Caretas' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.promedioLenguas,function(key,value){

                    $("#lenguas").append("<tr><td>" + 'Lenguas' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.promedioProcesos,function(key,value){

                    $("#procesosCerdo").append("<tr><td>" + 'Procesos Cerdo' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });

                /********************************************PESOS*****************************************************/
                $.each(respuesta.ListaPesoRecortes,function(key,value){

                    $("#pesoRecortes").append("<tr><td>" + 'Recortes' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ListaPesoProcesos,function(key,value){

                    $("#pesoProcesos").append("<tr><td>" + 'Procesos Cerda' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ListaPesoLenguas,function(key,value){

                    $("#pesoLenguas").append("<tr><td>" + 'Lenguas' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ListaPesoCaretas,function(key,value){

                    $("#pesoCaretas").append("<tr><td>" + 'Caretas' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ListaPesoProcesos,function(key,value){

                    $("#pesoProcesosCerdo").append("<tr><td>" + 'Procesos Cerdo' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });



            $( "#progressbar" ).hide();
            }

        });
}
function consultaInsumos ()
{   $( "#progressbar" ).show();
    var inicio = $('#inicio').val();
    var fin = $('#fin').val();
    var grupo = $('#grupo').val();


    $.ajax({

            url : '/fabricacion/promInsumos/',
            dataType : "json",
            type : "get",
            data : {'inicio':inicio,'fin':fin,'grupo':grupo},
            success : function(respuesta)
            {

                $("#tablaPromedioCostoMiga").find("tr:gt(0)").remove();
                $("#tablaPesoMiga").find("tr:gt(0)").remove();
                $("#tablaPromedioCostoCond").find("tr:gt(0)").remove();
                $("#tablaPesoCond").find("tr:gt(0)").remove();
                $("#tablaPromedioCostoMolida").find("tr:gt(0)").remove();
                $("#tablaPesoMolida").find("tr:gt(0)").remove();

                $.each(respuesta.promedioMiga,function(key,value){

                    $("#tablaPromedioCostoMiga").append("<tr><td>" + 'Miga Preparada' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ListaCantMiga,function(key,value){

                    $("#tablaPesoMiga").append("<tr><td>" + key + "</td><td>" + value + "</td></tr>");
                });
                $.each(respuesta.promedioCondimento,function(key,value){

                    $("#tablaPromedioCostoCond").append("<tr><td>" + 'Condimento Preparado' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ListaCantCond,function(key,value){

                    $("#tablaPesoCond").append("<tr><td>" + key + "</td><td>" + value + "</td></tr>");
                });

                $.each(respuesta.promedioMolidas,function(key,value){

                    $("#tablaPromedioCostoMolida").append("<tr><td>" + 'Carne Molida' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ListaCantMolida,function(key,value){

                    $("#tablaPesoMolida").append("<tr><td>" + key + "</td><td>" + value + "</td></tr>");
                });
                $( "#progressbar" ).hide();
            }

        });
}
function consultaPechugaCond ()
{
    $( "#progressbar" ).show();
    var inicio = $('#inicio').val();
    var fin = $('#fin').val();
    tablaPesoFilete = $("#tablaPesoPolloCond")

    $.ajax({

            url : '/fabricacion/promPechCondPo/',
            dataType : "json",
            type : "get",
            data : {'inicio':inicio,'fin':fin},
            success : function(respuesta)
            {


                $("#tablaPromedioCostoPollo").find("tr:gt(0)").remove();
                $("#tablaPromedioCostoTajado").find("tr:gt(0)").remove();
                $("#tablaPromedioPesoPollo").find("tr:gt(0)").remove();
                $("#tablaPromedioCostoBandejas").find("tr:gt(0)").remove();
                $("#tablaCantBandejas").find("tr:gt(0)").remove();
                $("#tablaPromedioCostoBandejasCerdo").find("tr:gt(0)").remove();
                $("#tablaCantBandejasCerdo").find("tr:gt(0)").remove();
                tablaPesoFilete.find("tr:gt(0)").remove();
                $.each(respuesta.promedioBandejasCerdo,function(key,value){

                    $("#tablaPromedioCostoBandejasCerdo").append("<tr><td>" + 'Bandejas de Cerdo Apanado' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.cantBandejasCerdo,function(key,value){

                    $("#tablaCantBandejasCerdo").append("<tr><td>" + 'Bandejas de Cerdo Apanado' + "</td><td>" + value + "</td></tr>");
                });
                $.each(respuesta.promedioBandejasPollo,function(key,value){

                    $("#tablaPromedioCostoBandejas").append("<tr><td>" + 'Bandejas de Pollo Apanado' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.cantBandejas,function(key,value){

                    $("#tablaCantBandejas").append("<tr><td>" + 'Bandejas de Pollo Apanado' + "</td><td>" + value + "</td></tr>");
                });
                $.each(respuesta.Promedio,function(key,value){

                    $("#tablaPromedioCostoPollo").append("<tr><td>" + 'Filete Condimetado de pollo' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ListaPesoFilete,function(key,value){

                    tablaPesoFilete.append("<tr><td>" + key + "</td><td>" + value + "</td></tr>");
                });

                $.each(respuesta.ListaCosto,function(key,value){

                    $("#tablaPromedioCostoTajado").append("<tr><td>" + key + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });

                $.each(respuesta.ListaPeso,function(key,value){

                    $("#tablaPromedioPesoPollo").append("<tr><td>" + key + "</td><td>" + value + "</td></tr>");

                });

                $( "#progressbar" ).hide();
            }

        });
}
function consultaPromedioPorFecha ()
{   $( "#progressbar" ).show();
    var inicio = $('#inicio').val();
    var fin = $('#fin').val();
    var grupo = $('#grupo').val();


    $.ajax({

            url : '/fabricacion/calcPromedio/',
            dataType : "json",
            type : "get",
            data : {'inicio':inicio,'fin':fin,'grupo':grupo},
            success : function(respuesta)
            {
                $("#tablaPesos").find("tr:gt(0)").remove();
                $("#tablaPromedio").find("tr:gt(0)").remove();

                $.each(respuesta.costos,function(key,value){

                    $("#tablaPromedio").append("<tr><td>" + key + "</td><td>" + value + "</td></tr>");
                });
                $.each(respuesta.pesos,function(key,value){

                    $("#tablaPesos").append("<tr><td>" + key + "</td><td>" + value + "</td></tr>");
                });
                $( "#progressbar" ).hide();
            }

        });
}
function CostoKiloChuleta()
{
     var produccion = $('#id_produccion').val();

    $.ajax({

            url : '/fabricacion/consultaCostoChuleta/',
            dataType : "json",
            type : "get",
            data : {'produccion':produccion},
            success : function(respuesta)
            {
                if (respuesta != '')
                {
                    $('#id_costoKiloChuleta').val(respuesta)
                }

            }

        });
}
function CostoProdListaPrecios()
{
    var producto = $('#id_productoLista').val();

    $.ajax({

            url : '/ventas/consultaCosto/',
            dataType : "json",
            type : "get",
            data : {'producto':producto},
            success : function(respuesta)
            {
                if (respuesta != '')
                {
                    $('#id_costoKilo').val(respuesta)
                }

            }

        });
}

function GuardarMolido(idMolido)
{
    var opcion = confirm('Desea guardar este Registro, recuerde que esto afectara el inventario.');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/guardarMolido/',
            dataType: "json",
            type: "get",
            data: {'idMolido': idMolido},
            success: function (respuesta) {
                if (respuesta != '') {
                   alert(respuesta);
                }

            }

        });
    }
}
function GuardarEmpaqueApanado(idEmpaque)
{
    var opcion = confirm('Desea costear este Registro ?');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/guardarEmpaque/',
            dataType: "json",
            type: "get",
            data: {'idEmpaque': idEmpaque},
            success: function (respuesta) {
                if (respuesta != '') {
                    alert(respuesta);
                }

            }

        });
    }
}
function CostearEmpaqueApanado(idEmpaque)
{
    var opcion = confirm('Desea costear este Registro ?');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/costearEmpaque/',
            dataType: "json",
            type: "get",
            data: {'idEmpaque': idEmpaque},
            success: function (respuesta) {
                if (respuesta != '') {
                    alert(respuesta);
                }

            }

        });
    }
}
function CostearMolido(idMolido)
{
    var opcion = confirm('Desea costear este Registro ?, recuerde Actualizar la tabla de costos.');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/costearMolido/',
            dataType: "json",
            type: "get",
            data: {'idMolido': idMolido},
            success: function (respuesta) {
                if (respuesta != '') {
                    alert(respuesta);
                }

            }

        });
    }
}
function existenciasCarneAMoler()
{
    var producto = $('#id_productoMolido');
    var peso = $('#id_pesoAmoler').val();
    Existencias(producto,6,peso);

}
function calculoTotalApanado()
{
    var filete = parseInt($('#id_pesoFilete').val());
    var miga = parseInt($('#id_miga').val());
    var totalApanado = filete + miga;
    $('#id_totalApanado').val(totalApanado);
}
function GuardarApanado(idApanado) {
    //Funcion que costea el apanado actual
    var opcion = confirm('Desea guardar este Registro, recuerde que esto afectara el inventario.');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/guardarApanado/',
            dataType: "json",
            type: "get",
            data: {'idApanado': idApanado},
            success: function (respuesta) {
                if (respuesta != '') {
                    $('#id_costoFilete').val(respuesta)
                }

            }

        });
    }
}
function CostearApanado(idApanado)
{
    //Funcion que costea el apanado actual
    var opcion = confirm('Desea costear este Registro ?, recuerde Actualizar la tabla de costos.');
    if (opcion == true)
    {
        $.ajax({

            url : '/fabricacion/costearApanado/',
            dataType : "json",
            type : "get",
            data : {'idApanado':idApanado},
            success : function(respuesta)
            {
                if (respuesta != '')
                {
                    $('#id_costoFilete').val(respuesta);
                }

            }

        });
    }


}
function existenciasFileteCondimentado()
{
    var producto = $('#id_productoApanado').val();
    var peso= $('#id_pesoFilete').val();
    Existencias(producto,5,peso);
}
function ExistenciasApanado()
{
    var miga = $('#id_miga').val();
    // Miga Preparada 109
    Existencias(109,6,miga);
}
function TraecostoEnsalinado()
{
    var producto = $('#id_productoEnsalinado').val();
    var peso = $('#id_pesoProducto').val();
    Existencias(producto,6,peso);
}
function GuardarEnsalinado(idEnsalinado)
{
    var opcion = confirm('Desea guardar este Registro, recuerde que esto afectara el inventario');
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
                    alert(respuesta);
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
                    alert(respuesta);

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
                    var n = noty({text: respuesta});
                    //alert(respuesta);
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
    var opcion = confirm('Desea guardar los cambios, Recuerde que esto afectara el Inventario?');
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
    var combo = $('#id_productoVenta').val();
    var idVenta = $('#codigoVenta').text();
    var peso = $('#id_peso').val();
    var lista = $('#codigoLista').text();

     $.ajax({

        url : '/ventas/consultaPrecioProducto/',
         dataType: "json",
         type: "get",
         data : {'lista':lista,'idProducto':combo,'idVenta':idVenta,'peso':peso},
         success : function(respuesta){

             if(respuesta == "No hay existencias en almacen")
             {
                 alert('No hay existencias en almacen')
             }else
             {
                 $('#id_vrUnitario').val(respuesta)
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
