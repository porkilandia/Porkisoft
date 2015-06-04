$(document).on('ready', inicio);

 function inicio()
 {
     /*Caracteristicas Traslados*/
     if ($('#TrasladoGuardado').text() == 'Si')
     {
         $('#Guardatraslado').hide();
         $('#nuevo').hide();
     }
     else
     {
         $('#Guardatraslado').show();
         $('#nuevo').show();
     }
     function guardarConfiguracion()
     {
         alert('')
     }

    // oculta el boton de guardado en pedido en caso de que sea contado
     /************************************************Template Venta Norte*********************************************/
    var estado = $('#guardado').text();
    var productoVenta = $('#id_productoVenta');
    var pesoVentaPunto = $('#id_pesoVentaPunto');
    var unidadesVentaPunto = $('#id_unidades');

    var total= 0;
    pesoVentaPunto.on('change',calculoTotalVentaPunto);

     function calculoTotalVentaPunto() {
        var producto = productoVenta.val();
        var vrUnitario =$('#id_vrUnitarioPunto').val();
         $.ajax({
            url: '/ventas/tipoProducto/',
            dataType: "json",
            type: "get",
            data: {'producto': producto},
            success: function (respuesta) {

                if (respuesta == 'pesable')
                {
                    total = (pesoVentaPunto.val()/1000) * vrUnitario;
                    $('#id_vrTotalPunto').val(Math.round(total));
                }
                else
                {
                    total = pesoVentaPunto.val() * vrUnitario;
                    $('#id_vrTotalPunto').val(total);
                }

            }

        });

     }
     pesoVentaPunto.on('change',calculoTotalVentaPunto);


    if (estado == 'Si')
        {
            $('#FormularioVentaPunto').hide();
            $('#cobraVenta').hide();

        }
    productoVenta.focus();

    /******************************************************************************************************************/

     $('#agregarProducto').show();
     $('#encabezado').addClass('ocultarRecibo');
     $('#pieRecibo').addClass('ocultarRecibo');
     $('#pie').hide();
     $('#Retiro').hide();
     $('#tablaMovi').hide();

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
     $('#id_vrTotalPedido').on('focus',CalculaTotalPedido);
     //productoVenta.on('blur',consultaValorProducto);
     $('#id_vrUnitario').on('focus',ExistenciasPedido);
     $('#id_vrTotal').on('focus',calculoValorProducto);
     $('#guardarVentas').on('click',GuardarVentas);
     $('#Guardatraslado').on('click',GuardarTraslado);
     $('#id_productoTraslado').on('blur',ConsultaStock);
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
     $('#id_punto').on('change',VerificarCond);
     $('#id_productoFrito').on('change',VerificarProdFrito);
     $('#id_puntoCond').on('change',VerificarCondCarne);
     $('#id_productoCond').on('change',VerificarProdCarne);
     $('#id_puntoCroq').on('change',VerificarInsCroquetas);
     $('#id_puntoReApanado').on('change',VerificarReApanados);
     $('#id_puntoConversion').on('change',VerificarConversiones);
     $('#id_puntoBodega').on('change',VerificaBolaEns);
     $('#Excel').on('click',Exportar);
     $('#ExpExcelFaltantes').on('click',ExportarFaltantes);
     $('#id_pesoEnvio').on('focus',PasaValorEnvio);
     $('#id_vrTotalPunto').on('focus',calculoTotalVenta);
     $('#id_diferencia').on('focus',calculoDiferencia);
     var vrUnitario = $('#id_vrUnitarioPunto');
     productoVenta.on('change',traeValorVenta);
     //pesoVentaPunto.on('change',existenciasVenta);
     $('#regreso').on('focus',calculoRegreso);
     $('#id_cantidadActual').on('focus',CantidadActual);
     $('#id_compra').on('change',ValorVerduras);



     //var tablaEmpacado = $('#tablaEmpacado tr');
     //tablaEmpacado.on('click',maneja);
     //$('#TablaPuntoNorte').dataTable();

     $('#tablaAjustes').dataTable();
     $('#canalPendiente').dataTable();
     $('#tablaenTajados').dataTable();
     $('#tablacostos').dataTable({ "pageLength": 13 });
     $('#tablastock').dataTable({ "pageLength": 13 });
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
     $('#tablaMovimientos').dataTable();
     $('#tablaApanados').dataTable();
     $('#tablaReApanado').dataTable();
     $('#tablaCCond').dataTable();
     $('#tablaConversiones').dataTable();
     //$('#tablaReporteMovimientos').dataTable();
     $('#tablaFritos').dataTable();
     $('#TablaCondimento').dataTable();
     $('#tablaCroquetas').dataTable();
     $('#TablaEnsBola').dataTable();
     $('#listaDePrecios').dataTable();
     $('#TablaMiga').dataTable();
     $('#tablaCaja').dataTable();
     $('#tablaMenudos').dataTable();

     $('#id_fecha').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaCompra').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaDesposte').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaTajado').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaEnsalinado').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaApanado').datepicker({ dateFormat: "dd/mm/yy" });
     var fechaVenta = $('#id_fechaVenta');
     fechaVenta.datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaRecepcion').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaSacrificio').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaFabricacion').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaMolido').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaEmpacado').datepicker({ dateFormat: "dd/mm/yy" });
     $('#inicio').datepicker({ dateFormat: "dd/mm/yy" });
     $('#fin').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaTraslado').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaMenudo').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaFrito').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaReApanado').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaConversion').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaCroqueta').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaCarCond').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaAjuste').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaBolaCondimentada').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaCaja').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaFaltante').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaPedido').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaLimpieza').datepicker({ dateFormat: "dd/mm/yy" });
     $('#id_fechaChicharron').datepicker({ dateFormat: "dd/mm/yy" });

     $( "#bodegaFaltantes" ).selectmenu({ width: 200 });

     $('#homeAccordeon').accordion({ heightStyle: "content" });
     $('#acordeon').accordion({ heightStyle: "content" });
     $( "#progressbar" ).progressbar({value: false}).hide();
     $('#FrmVenta').show();
     $('#FrmVentaPunto').show();
     $('#InicioSesion').show();

     $("label[for=id_venta],#id_venta").hide();
     $("label[for=id_productoVenta]").hide();
     $('#diagrama').hide();
     $('#totalCompra').val($('#totalVentaDet').text()).attr('disabled','-1');
     //fechaVenta.attr('disabled','-1');
     //$('#id_encargado').attr('disabled','-1');
     //$('#id_jornada').attr('disabled','-1');

}

/**************************************************** METODOS *********************************************************/
function deshidratacion() {

    var bodega = $('#bodegaFaltantes').val();

    $.ajax({
            url: '/inventario/deshidratacion/',
            dataType: "json",
            type: "get",
            data: {'bodega': bodega},
            success: function (respuesta) {
                var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
            }
        });
}
function ReporteTipoPedido() {

    var fechaInicio = $('#inicio').val();
    var fechaFin = $('#fin').val();
    var cliente = $('#cliente').val();
    var TablaPedidos = $('#TablaPedidos');
    var TablaVentasClientes = $('#TablaVentasClientes');
    var filtrpedido = '';
    var bodega = $('#bodega').val();

    if($("#porFecha").is(':checked')) {
            filtrpedido = 'fecha';
        } else {
            filtrpedido = 'total';
        }

    var credito = '';
    var contado = '';
    var vrContado= 0;
    var vrCredito= 0;

    $.ajax({

            url: '/ventas/consultaTipoPedido/',
            dataType: "json",
            type: "get",
            data: {'bodega':bodega,'inicio':fechaInicio,'fin':fechaFin,'cliente':cliente,'filtrpedido':filtrpedido},
            success: function (respuesta) {
                    TablaPedidos.find("tr:gt(0)").remove();
                    TablaVentasClientes.find("tr:gt(0)").remove();
                    //ReporteTipoPedidoContado();

                    for (var i=0;i<respuesta.length;i++) {

                        if (respuesta[i].fields.credito == true) {
                            credito = 'Si';
                            contado = 'No';
                            vrCredito += respuesta[i].fields.TotalVenta;

                        } else {
                            credito = 'No';
                            contado = 'Si';
                            vrContado += respuesta[i].fields.TotalVenta;
                        }

                        TablaPedidos.append(
                                "<tr><td>" + respuesta[i].pk +
                                "</td><td>" + respuesta[i].fields.fechaPedido +
                                "</td><td>" + respuesta[i].fields.numeroFactura +
                                "</td><td>" + respuesta[i].fields.nitCliente +
                                "</td><td>" + respuesta[i].fields.NombreCliente +
                                "</td><td>" + "$" + respuesta[i].fields.TotalVenta +
                                "</td><td>" + credito +
                                "</td><td>" + contado +
                                "</td><td>" + "<a target='_blank'' href='/ventas/detallePedido/" + respuesta[i].pk + "'>" + 'Detalles' + "</a>" +
                                "</td></tr>");

                    }
                    TablaPedidos.append("<tr><th>"+"Total Creditos"+
                                        "</th></tr><tr><th>"+"$"+vrCredito +
                                        "</th></tr><tr><th>"+"Total Contados"+
                                        "</th></tr><tr><th>"+"$"+vrContado+"</th></tr>");
                    }

        });


}
function ReporteTipoPedidoContado() {

    var fechaInicio = $('#inicio').val();
    var fechaFin = $('#fin').val();
    var cliente = $('#cliente').val();
    var TablaPedidos = $('#TablaPedidos');
    var TablaVentasClientes = $('#TablaVentasClientes');
    var filtrpedido = '';
    var bodega = $('#bodega').val();
    var vrContado = 0;

    if($("#porFecha").is(':checked')) {
            filtrpedido = 'fecha';
        } else {
            filtrpedido = 'total';
        }

    $.ajax({

            url: '/ventas/consultaTipoPedidoContado/',
            dataType: "json",
            type: "get",
            data: {'bodega':bodega,'inicio':fechaInicio,'fin':fechaFin,'cliente':cliente,'filtrpedido':filtrpedido},
            success: function (respuesta) {
                TablaVentasClientes.find("tr:gt(0)").remove();

                for (var j = 0; j < respuesta.length; j++) {


                    TablaVentasClientes.append(
                            "<tr><td>" + respuesta[j].pk +
                            "</td><td>" + respuesta[j].fields.fechaVenta +
                            "</td><td>" + respuesta[j].fields.factura +
                            "</td><td>" + respuesta[i].fields.nitCliente +
                            "</td><td>" + respuesta[j].fields.cliente +
                            "</td><td>" + "$" + respuesta[j].fields.TotalVenta +
                            "</td><td>" + "<a target='_blank'' href='/ventas/detalleVentaPunto/" + respuesta[j].pk + "'>" + 'Detalles' + "</a>" +
                            "</td></tr>");

                            vrContado += respuesta[j].fields.TotalVenta;
                }

                TablaVentasClientes.append("<tr><th>"+"Total Contado"+
                                        "</th><th>"+"$"+vrContado+"</th></tr>");

            }

        });


}
function GuardarCompra() {

    var idCompra = $('#CodigoCompra').text();

    var opcion = confirm('Desea Guardar el registro ?');
    if (opcion == true) {
        $.ajax({
            url: '/inventario/guardaCompra/',
            dataType: "json",
            type: "get",
            data: {'idCompra': idCompra},
            success: function (respuesta) {
                var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
            }
        });
    }
}
function ValorVerduras() {

    var idProducto = $('#id_productoLimpiar').val();
    var idCompra = $('#id_compra').val();

    $.ajax({
            url: '/fabricacion/ValorVerduras/',
            dataType: "json",
            type: "get",
            data: {'idProducto': idProducto,'idCompra':idCompra},
            success: function (respuesta) {
                $.each(respuesta.valorProducto,function(key,value){
                    $('#id_valorProducto').val(value);
                });
                $.each(respuesta.valorTransporte,function(key,value){
                    $('#id_valorTransporte').val(value);
                });
            }
        });

}

function CostearVerduras(idVerdura) {

    $.ajax({
            url: '/fabricacion/costearVerduras/',
            dataType: "json",
            type: "get",
            data: {'idVerdura': idVerdura},
            success: function (respuesta) {
                var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
            }
        });

}
function GuardarVerduras(idVerdura) {

   var opcion = confirm('Desea Guardar el registro ?');
    if (opcion == true) {
        $.ajax({
            url: '/fabricacion/guardarVerduras/',
            dataType: "json",
            type: "get",
            data: {'idVerdura': idVerdura},
            success: function (respuesta) {
                var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
            }
        });
    }

}


function ReporteListaDesposte() {

    var grupo = $('#grupos option:selected');
    var CodigoGrupo = grupo.val();
    var NombreGrupo = grupo.text();
     var fechaInicio = $('#inicio').val();
    var fechaFin = $('#fin').val();

    var tablaDesposte = $("#tablaListaDesposte");

        $.ajax({

            url: '/fabricacion/reporteListDesp/',
            dataType: "json",
            type: "get",
            data: {'grupo': CodigoGrupo,'inicio':fechaInicio,'fin':fechaFin},
            success: function (respuesta) {
                    tablaDesposte.find("tr:gt(0)").remove();

                    for (var i=0;i<respuesta.length;i++)
                    {
                            tablaDesposte.append(
                                "<tr><td>" + respuesta[i].pk +
                                "</td><td>" + respuesta[i].fields.fechaDesposte +
                                "</td><td>" + respuesta[i].fields.resesADespostar +
                                "</td><td>" + respuesta[i].fields.totalDespostado +
                                "</td><td>" + respuesta[i].fields.totalCanal +
                                "</td><td>" + respuesta[i].fields.difCanalADespostado +
                                "</td><td>" + respuesta[i].fields.tipoDesposte +
                                "</td><td>" + respuesta[i].fields.cif +
                                "</td><td>" + respuesta[i].fields.mod +
                                "</td><td>" + "<a target='_blank'' href='/fabricacion/detalleDesposte/"+ respuesta[i].pk + "'>"+'Detalles'+"</a>" +
                                "</td></tr>");

                    }

                    }

        });

}
function AnularFactura(idFactura,numFactura) {

    var opcion = confirm('Desea Anular la factura No.'+ numFactura +' ?');
    if (opcion == true) {
        $.ajax({
            url: '/ventas/anulaVenta/',
            dataType: "json",
            type: "get",
            data: {'idFactura': idFactura},
            success: function (respuesta) {
                var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
            }
        });
    }
}
function consultaListaVentas() {

    var bodega = $('#bodega').val();
    var fechaInicio = $('#inicio').val();
    var fechaFin = $('#fin').val();
    var jornadaVta = $('#jornada').val();
    var TotalVenta = 0;
    var estado = '';
    var TablaVenta = $("#tablaListaVenta");
    var linkAnulado = '';


        $.ajax({

            url: '/ventas/reporteListaVentaNorte/',
            dataType: "json",
            type: "get",
            data: {'inicio': fechaInicio,'fin': fechaFin,'bodega': bodega,'jornada': jornadaVta},
            success: function (respuesta) {
                    TablaVenta.find("tr:gt(0)").remove();
                    $('#total').remove();
                    for (var i=0;i<respuesta.length;i++)
                    {
                        if(respuesta[i].fields.anulado)
                        {
                            estado = 'Anulada';
                            linkAnulado = '';

                        }else
                        {
                            estado = 'Activo';
                            linkAnulado = "<a onclick='AnularFactura("+ respuesta[i].pk+","+respuesta[i].fields.factura +")' href='#'>"+'Anular'+"</a>";
                            TotalVenta += respuesta[i].fields.TotalVenta;
                        }

                        TablaVenta.append(
                                "<tr><td>" + respuesta[i].pk +
                                "</td><td>" + estado +
                                "</td><td>" + respuesta[i].fields.factura +
                                "</td><td>" + respuesta[i].fields.fechaVenta +
                                "</td><td>" + respuesta[i].fields.encargado +
                                "</td><td>" + respuesta[i].fields.jornada +
                                "</td><td>" + '$ ' + respuesta[i].fields.TotalVenta +
                                "</td><td>" + "<a target='_blank'' href='/ventas/detalleVentaPunto/"+ respuesta[i].pk + "'>"+'Detalles'+"</a>" +linkAnulado +
                                "</td></tr>");




                    }

                TablaVenta.append("<tr><th id = 'total' colspan='5' style='text-align: right'>" + 'Total :'  +"</th><th>"+ '$ ' +TotalVenta +"</th></tr>");

                //var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                    }

        });

}

function CantidadActual() {
    var producto = $('#id_productoAjuste').val();
    var bodega = $('#id_bodegaAjuste').val();

    $.ajax({
            url: '/inventario/cantidadActual/',
            dataType: "json",
            type: "get",
            data: {'producto': producto, 'bodega': bodega},
            success: function (respuesta) {

                $.each(respuesta.pesoActual,function(key,value){
                    $('#id_cantidadActual').val(value)
                });
                $.each(respuesta.undActual,function(key,value){
                    $('#id_unidadActual').val(value)
                });
            }

        });


}
function ReporteVentaDiaria()
{
        var inicio = $('#inicio').val();
        var fin = $('#fin').val();
        var bodega = $('#bodega').val();
        var tablaRepDiario =  $("#tablaRepDiario");
        var totalrango = 0;
        var tipoReporte = '';

        if($("#ventas").is(':checked')) {
               tipoReporte = 'ventas';

        }
        else if($("#pedidos").is(':checked')) {
               tipoReporte = 'pedidos';
        }


    $.ajax({
            url: '/ventas/reporteVentaDiaria/',
            dataType: "json",
            type: "get",
            data: {'inicio': inicio, 'fin': fin,'bodega':bodega,'tipoReporte':tipoReporte},
            success: function (respuesta) {

                tablaRepDiario.find("tr:gt(0)").remove();

                $.each(respuesta.totalDia,function(key,value){

                    tablaRepDiario.append("<tr><td>" + key + "</td><td style='text-align: right'>"+ value + "</td></tr>");
                    totalrango += value;
                });

            tablaRepDiario.append("<tr><th>"+'Total Rango '+"</th><th>"+ totalrango + "</th></tr>");


            $( "#progressbar" ).hide();
            }

        });


}
function ReporteVentasNorte() {
    $( "#progressbar" ).show();
    var tipoReporte = '';

    if($("#ventas").is(':checked')) {
           tipoReporte = 'ventas';

    }
    else if($("#pedidos").is(':checked')) {
           tipoReporte = 'pedidos';
        }
     else if($("#clienteDet").is(':checked')) {
           tipoReporte = 'clienteDetalle';
        }
    else
    {
        tipoReporte = 'todo';
    }

        var inicio = $('#inicio').val();
        var fin = $('#fin').val();
        var jornada = $('#jornada').val();
        var totalVentaPesables = 0;
        var totalVentaNoPesables = 0;
        var bodega = $('#bodega').val();
        var sumatoria = $('#sumasTotales');
        var cliente = $('#cliente').val();
        var iva = 0;

    $.ajax({
            url: '/ventas/reporteVentaNorte/',
            dataType: "json",
            type: "get",
            data: {'cliente':cliente,'inicio': inicio, 'fin': fin,'jornada':jornada,'bodega':bodega,'tipoReporte':tipoReporte},
            success: function (respuesta) {

                $("#tablaRepPP").find("tr:gt(0)").remove();
                $("#tablaRepVN").find("tr:gt(0)").remove();
                $("#tablaReCPP").find("tr:gt(0)").remove();
                $("#tablaRepVCP").find("tr:gt(0)").remove();
                sumatoria.find("tr:gt(0)").remove();


                $.each(respuesta.PesoProductos,function(key,value){

                    $("#tablaRepPP").append("<tr><td>" + key + "</td><td style='text-align: right'>"+ Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ValorProductos,function(key,value){

                    totalVentaPesables += Math.ceil(value);
                    $("#tablaRepVN").append("<tr><td>" + key + "</td><td style='text-align: right'>" + Math.ceil(value) + "</td></tr>");
                });

                $.each(respuesta.UdnProductos,function(key,value){

                    $("#tablaReCPP").append("<tr><td>" + key + "</td><td style='text-align: right'>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ValorUnds,function(key,value){
                    totalVentaNoPesables += Math.ceil(value);
                    $("#tablaRepVCP").append("<tr><td>" + key + "</td><td style='text-align: right'>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ValorIva,function(key,value){
                    iva = value;
                });

                var sumaTotal = totalVentaNoPesables + totalVentaPesables;
                sumatoria.append("<tr><td>" + 'Pesables' +
                                 "</td><td>"+ totalVentaPesables +
                                 "</td></tr>"+
                                 "<tr><td>" + 'No Pesables' +
                                 "</td><td>" + totalVentaNoPesables +
                                 "</td></tr>"+
                                 "<tr><td>" + 'Total Iva' +
                                 "</td><td>" +  iva +
                                 "<tr><td>" + 'Total' +
                                 "</td><td>" +  sumaTotal +
                                 "</td></tr>");
                $('#totalPesables').append(': $'+totalVentaPesables);
                $('#totalNoPesables').append(': $'+totalVentaNoPesables);

            $( "#progressbar" ).hide();
            }

        });

}
function ImprimirAZ()
{
                var encabezado = $('#encabezado');
                var pie = $('#pieRecibo');
                var tablaExcentos = $('#TablaExcentos');
                var tablaExcluidos = $('#TablaExcluidos');
                var tablaGravados = $('#TablaGravados1');
                var tablaGravados2 = $('#TablaGravados2');

                var tablaPesables = $('#TablaPesables');
                var TablaValorPesables = $('#TablaValPesables');
                var tablaNoPesables = $('#TablaNoPesables');
                var tablaValorNoPesables = $('#TablaValNoPesables');


                var inicio = $('#inicio').val();
                var jornada = $('#jornada').val();
                encabezado.show();
                pie.show();
                $('#fechaAZ').append(': '+ inicio);
                $('#jornadaAZ').append(': '+ jornada);
                var direccion = $('#direccion').text();
                var punto = $('#bodega option:selected');
                $('#lugar').append(': '+ punto.text())
                var cabecera = $('#Cabecera');

                tablaExcentos.addClass('recibo');
                tablaExcluidos.addClass('recibo');
                tablaGravados.addClass('recibo');
                tablaGravados2.addClass('recibo');
                tablaPesables.addClass('recibo');
                TablaValorPesables.addClass('recibo');
                tablaNoPesables.addClass('recibo');
                tablaValorNoPesables.addClass('recibo');

                cabecera.append(
                                    "<table id='encabezado'>"+
                                    "<tr><th>" + 'PORKILANDIA S.A.S.' + "</th></tr>"+
                                    "<tr><th>" + 'Nit: 900606687-6' + "</th></tr>"+
                                    "<tr><th>" + 'Regimen Comun' + "</th></tr>"+
                                    "<tr><th>" + 'Resolucion : 140000039353'+ "</th></tr>"+
                                    "<tr><th>" + 'Rango:000000 hasta 999999' + "</th></tr>"+
                                    "<tr><th>" + 'Expedida el : 09-04-2013'+ "</th></tr>"+
                                    "<tr><th>" + direccion +"</th></tr></table>"
                );

                $('#recibo').printArea();
                encabezado.hide();
                pie.hide();


                tablaExcentos.removeClass('recibo');
                tablaExcluidos.removeClass('recibo');
                tablaGravados.removeClass('recibo');
                tablaGravados2.removeClass('recibo');
                tablaPesables.removeClass('recibo');
                TablaValorPesables.removeClass('recibo');
                tablaNoPesables.removeClass('recibo');
                tablaValorNoPesables.removeClass('recibo');

}
function calculoDiferencia() {
    var pesoActual = $('#id_pesoActual').val();
    var undActual = $('#id_unidadActual').val();
    var pesoFisico = $('#id_pesoFisico').val();
    var undFisica = $('#id_unidadFisica').val();
    var diferencia = 0;
    if (pesoActual == 0)
    {
        diferencia = undActual - undFisica;
    }else
    {
        diferencia = pesoActual - pesoFisico;
    }

    $('#id_diferencia').val(diferencia);

}
function GenerarReportFaltantes(idFaltante) {

    var nombreBodega = $('#nombreBodega').text();
    var opcion = confirm('Desea Generar un Reporte de inventario?');
    if (opcion == true) {
        $.ajax({
            url: '/inventario/generarFaltante/',
            dataType: "json",
            type: "get",
            data: {'idFaltante': idFaltante, 'nombreBodega': nombreBodega},
            success: function (respuesta) {
                var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
            }

        });
    }
}
function consultaAZ() {

    var inicio = $('#inicio').val();
    var fechaFin = $('#fin').val();
    var bod = $('#bodega option:selected');
    var nombreBodega =bod.text();
    var bodega = $('#bodega').val();
    var jornada = $('#jornada').val();
    var gravados1= 0;
    var gravados2= 0;
    var IvaGravados1= 0;
    var IvaGravados2= 0;
    var VentaTotal = 0;

    var opcion = confirm('Se creara el reporte Z del : ' + inicio + ' en la jornada : '+ jornada +' del Punto : ' + nombreBodega +'.' );
    if (opcion == true) {

                $.ajax({
                        url: '/ventas/reporteAZ/',
                        dataType: "json",
                        type: "get",
                        data: {'bodega':bodega,'inicio': inicio,'fin':fechaFin,'jornada':jornada},
                        success: function (respuesta)
                        {
                            $("#TablaExcentos").find("tr:gt(0)").remove();
                            $("#TablaExcluidos").find("tr:gt(0)").remove();
                            $("#TablaGravados1").find("tr:gt(0)").remove();
                            $("#TablaGravados2").find("tr:gt(0)").remove();

                            $.each(respuesta.excentos,function(key,value){

                                $("#TablaExcentos").append("<tr><td>" + key + "</td><td style='text-align: right'>"+'$ '+ Math.ceil(value) + "</td></tr>");
                            });
                            $.each(respuesta.excluidos,function(key,value){

                                $("#TablaExcluidos").append("<tr><td>" + key + "</td><td style='text-align: right'>" +'$ '+ Math.ceil(value) + "</td></tr>");
                            });

                            $.each(respuesta.gravados1,function(key,value){

                                gravados1 = value;
                                $("#TablaGravados1").append("<tr><td>" + key + "</td><td style='text-align: right'>" +'$ '+ Math.ceil(value) + "</td></tr>");
                            });
                            $.each(respuesta.gravados2,function(key,value){
                                gravados2 = value;
                                $("#TablaGravados2").append("<tr><td>" + key + "</td><td style='text-align: right'>" +'$ '+ Math.ceil(value) + "</td></tr>");
                            });
                            $.each(respuesta.totalVenta,function(key,value){

                                $("#ventaTotal").append(' $ '+value);
                            });
                            /**************Reporte pesables y no pesables*******************/
                            $.each(respuesta.PesoProductos,function(key,value){

                                $("#TablaPesables").append("<tr><td>" + key + "</td><td style='text-align: right'>"+ Math.ceil(value)+' grs' + "</td></tr>");
                            });
                            $.each(respuesta.ValorProductos,function(key,value){

                                $("#TablaValPesables").append("<tr><td>" + key + "</td><td style='text-align: right'>"+'$ ' + Math.ceil(value) + "</td></tr>");
                            });
                            $.each(respuesta.UdnProductos,function(key,value){

                                $("#TablaNoPesables").append("<tr><td>" + key + "</td><td style='text-align: right'>" + Math.ceil(value)+' unds' + "</td></tr>");
                            });
                            $.each(respuesta.ValorUnds,function(key,value){

                                $("#TablaValNoPesables").append("<tr><td>" + key + "</td><td style='text-align: right'>" +'$ '+ Math.ceil(value) + "</td></tr>");
                            });
                            /**************************************************************************/

                            $.each(respuesta.inicial,function(key,value){

                                $("#inicioConsecVentas").append(' : '+ value);
                            });
                            $.each(respuesta.final,function(key,value){

                                $("#finConsecVentas").append(' : '+ value);
                            });
                            $.each(respuesta.consec,function(key,value){

                                $("#ConsecZ").append(' : '+ value);
                            });

                            var grav1 = gravados1 / 1.16;
                            var grav2 = gravados2 / 1.16;
                            IvaGravados1 = grav1 * 0.16;
                            IvaGravados2 = grav2 * 0.16;
                            $("#grav1").append(' $ '+Math.round(grav1));
                            $("#grav2").append(' $ '+Math.round(grav2));
                            $("#IvaGrav1").append(' $ '+Math.round(IvaGravados1));
                            $("#IvaGrav2").append(' $ '+Math.round(IvaGravados2));


                        }

                });

        }
}
function CalculaTotalPedido() {
    var peso = $('#id_pesoPedido').val();
    var unidades = $('#id_unidadesPedido').val();
    var vrUnitario = $('#id_vrUnitario').val();
    var total = 0;
    if (peso == 0)
    {
       total = unidades * vrUnitario;
       $('#id_vrTotalPedido').val(total);
    }else{
        total = (peso/1000) * vrUnitario;
       $('#id_vrTotalPedido').val(total);
    }
}
function ExistenciasPedido() {
    var peso = $('#id_pesoPedido').val();
    var unidades = $('#id_unidadesPedido').val();
    var bodega = $('#bodegaPedido').text();
    var producto = $('#id_producto').val();
    var Lista= $('#listaPrecios').text();

    Existencias(producto,bodega,peso);
    ExistenciasUnd(producto,bodega,unidades);
    VerificarPrecioPedido(Lista,producto)


}
function VerificarPrecioPedido(idLista,idProducto) {

        $.ajax({
            url: '/ventas/verificarPrecioPedido/',
            dataType: "json",
            type: "get",
            data: {'idLista': idLista,'idProducto':idProducto},
            success: function (respuesta)
            {
                $('#id_vrUnitario').val(respuesta);
            }

    });
}
function GuardarPedido(idPedido) {

    var opcion = confirm('Desea Guardar este Registro?, tenga en cuenta que afectara el Inventario');
    if (opcion == true)
    {
        $.ajax({
            url: '/ventas/guardarPedido/',
            dataType: "json",
            type: "get",
            data: {'idPedido': idPedido},
            success: function (respuesta)
            {
                var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
            }

    });
    }

}
function calculoRegreso() {
    var efectivo = $('#efectivo').val();
    var totalCompra= $('#totalCompra').val();

    var resultado = efectivo - totalCompra;
    $('#regreso').val(resultado);

}
function GuardarDevolucion() {
    var idDetalleDev = $('#idDetDevolucion').text();
        var opcion = confirm('Desea Imprimir este Comprobante?');
    if (opcion == true)
    {
        $.ajax({
            url: '/ventas/GuardarDevolucion/',
            dataType: "json",
            type: "get",
            data: {'idDetalleDev': idDetalleDev},
            success: function (respuesta)
            {
                var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
            }

    });
    }
}
function imprimirRetiro(idRetiro) {
    var tablaRetiro = $('#Retiro');

    var opcion = confirm('Desea Imprimir este Comprobante?');
    if (opcion == true)
    {
        $.ajax({
            url: '/ventas/ImprimirRetiro/',
            dataType: "json",
            type: "get",
            data: {'idRetiro': idRetiro},
            success: function (respuesta) {
                        tablaRetiro.find("tr:gt(0)").remove();
                        var encabezado = $('#encabezado');
                        var pie = $('#pieRecibo');
                        encabezado.show();
                        pie.show();
                        tablaRetiro.show();
                        tablaRetiro.find("th:eq(5)").hide();
                        for (var i=0;i<respuesta.length;i++)
                            {
                                $('#fechaRetiro').text('Fecha :' + respuesta[i].fields.fechaRetiro);
                                $('#EncargadoRetiro').text('Encargado :' + respuesta[i].fields.nombreEncargado);
                                tablaRetiro.append(
                                        "<tr><td>" +'$ '+ respuesta[i].fields.cantidad +
                                        "</td><td>"  + respuesta[i].fields.observacion +
                                        "</td></tr>");

                            }
                        tablaRetiro.addClass('recibo');
                        $('#ImpRetiro').printArea();
                        encabezado.hide();
                        pie.hide();
                        tablaRetiro.hide();

                        }
    });
    }


}
function GuardarChicharron(idChicharron) {

    $.ajax({
            url: '/fabricacion/guardarChicharrones/',
            dataType: "json",
            type: "get",
            data: {'idChicharron': idChicharron},
            success: function (respuesta) {
                        var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
                        }

        });

}
function CostearChicharron(idChicharron) {

    $.ajax({
            url: '/fabricacion/costearChicharrones/',
            dataType: "json",
            type: "get",
            data: {'idChicharron': idChicharron},
            success: function (respuesta) {
                        var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
                        }

        });

}
function existenciasVenta()
{
    var idProducto = $('#id_productoVenta').val();
    var peso = $('#id_pesoVentaPunto').val();

    $.ajax({
            url: '/ventas/tipoProducto/',
            dataType: "json",
            type: "get",
            data: {'producto': idProducto},
            success: function (respuesta) {

                if (respuesta == 'pesable')
                {
                    Existencias(idProducto,1,peso);
                }
                else
                {
                    ExistenciasUnd(idProducto,1,peso);
                }

            }

        });


    //ExistenciasUnd(idProducto,1,peso);
}
function traeValorVenta()
{
    var idProducto = $('#id_productoVenta').val();
    var peso = $('#id_pesoVentaPunto').val();
    var und = $('#id_unidades').val();
    var numVenta = $('#NumVenta').text();

     $.ajax({
            url: '/ventas/valorProdVenta/',
            dataType: "json",
            type: "get",
            data: {'idProducto': idProducto,'peso':peso,'und':und,'numVenta':numVenta},
            success: function (respuesta) {
                    $('#id_vrUnitarioPunto').val(respuesta);
                            }

        });

}
function calculoTotalVenta()
{
    var peso = $('#id_pesoVentaPunto').val();
    //var und = $('#id_unidades').val();
    var total = 0;
    var vrUnitario = $('#id_vrUnitarioPunto').val();
    var producto = $('#id_productoVenta').val();
    peso = parseInt(peso);

    /*if (peso == 0)
    {
        total = und * vrUnitario;
        $('#id_vrTotalPunto').val(total);
    }
    else
    {
        total = (peso/1000) * vrUnitario;
        $('#id_vrTotalPunto').val(Math.round(total));
    }*/

    $.ajax({
            url: '/ventas/tipoProducto/',
            dataType: "json",
            type: "get",
            data: {'producto': producto},
            success: function (respuesta) {

                if (respuesta == 'pesable')
                {
                    total = (peso/1000) * vrUnitario;
                    $('#id_vrTotalPunto').val(Math.round(total));
                }
                else
                {
                    total = peso * vrUnitario;
                    $('#id_vrTotalPunto').val(total);
                }

            }

        });

}
function ImprimirRecibo()
{
                var encabezado = $('#encabezado');
                var pie = $('#pieRecibo');
                var tablaDetVenta = $('#tablaDetalleVentaPunto');
                var calculadora = $('#calculaVuelto');
                var cabecera = $('#Cabecera');
                var piePagina = $('#piePagina');
                var totalGravado = $('#Totalgravado').text();
                var numFactura = $('#numFactura').text();
                var fechaVenta = $('#FechaVenta').text();
                var nomEmcargado = $('#NomEncargado').text();
                var totalCompra = $('#totalCompra').val();
                var efectivo = $('#efectivo').val();
                var regreso = $('#regreso').val();
                var direccion = $('#direccion').text();
                calculadora.hide();
                encabezado.show();
                cabecera.append(
                                    "<table id='encabezado'>"+
                                    "<tr><th>" + 'PORKILANDIA S.A.S.' + "</th></tr>"+
                                    "<tr><th>" + 'Nit: 900606687-6' + "</th></tr>"+
                                    "<tr><th>" + 'Regimen Comun' + "</th></tr>"+
                                    "<tr><th>" + 'Resolucion : 140000045556'+ "</th></tr>"+
                                    "<tr><th>" + 'Rango:000000 hasta 999999' + "</th></tr>"+
                                    "<tr><th>" + 'Expedida el : 09-04-2015'+ "</th></tr>"+
                                    "<tr><th>" + direccion +"</th></tr>"+
                                    "<tr><th style='font-size: 1.1em'>"+'__________________________________'+"</th></tr>"+
                                    "<tr><th style='text-align: left'>"+'Fecha : ' + fechaVenta + "</th></tr>"+
                                    "<tr><th style='text-align: left'>"+'Factura N°: ' + numFactura+ "</th></tr>"+
                                    "<tr><th style='text-align: left'>"+'Encargado : ' + nomEmcargado + "</th></tr>"+
                                    "<tr><th style='font-size: 1.1em'>"+'__________________________________'+"</th></tr>"+
                                    "</table>"
                );

                piePagina.append(
                                "<table id='pieRecibo'>"+
                                    "<tr>"+
                                        "<th>"+'Total Compra:...................... $ ' + totalCompra + "</th>"+
                                    "</tr>"+
                                    "<tr>"+
                                        "<th id='efectivoImp' >"+'Efectivo:......................'+ efectivo +"</th>"+
                                    "</tr>"+
                                    "<tr>"+
                                        "<th id='regresoImp' >"+'Regreso:......................'+ regreso + "</th>"+
                                    "</tr>"+
                                    "<tr>"+
                                        "<th >"+'Total Gravado:...................... $ '+totalGravado+"</th>"+
                                    "</tr>"+
                                    "<tr>"+
                                        "<th>"+'__________________________________'+"</th>"+
                                    "</tr>"+
                                    "<tr>"+
                                        "<th>"+'!! GRACIAS POR SU COMPRA !!'+"</th>"+
                                    "</tr>"+
                                    "<tr>"+
                                        "<th style='font-size: 0.8em'>"+'Generado en PORKISOFT V.1.0'+"</th>"+
                                    "</tr>"+
                                "</table>"
                );

                pie.show();
                tablaDetVenta.find("th:eq(4)").hide();
                tablaDetVenta.addClass('recibo');
                $('#recibo').printArea();
                cabecera.hide();
                piePagina.hide();
                encabezado.hide();
                pie.hide();
                tablaDetVenta.removeClass('recibo');
                calculadora.show();
                $('#imprimeRecibo').hide();

}
function Cobrar()
{
    var venta = $('#NumVenta').text();
    if($('#totalVentaDet').text() != 0)
    {
        var opcion = confirm('Desea Cobrar esta Factura, recuerde que esto afectara el inventario.');
        if (opcion == true) {
            $.ajax({
                url: '/ventas/cobrar/',
                dataType: "json",
                type: "get",
                data: {'venta': venta},
                success: function (respuesta) {
                    var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
                    location.reload();

                }

            });
        }
    }else
    {
        alert('Debe ingresar un producto primero antes de cobrar!!!');
    }

}

function imprimir()
{
    var encabezado = $('#encabezado');
    var pie = $('#pie');
    var tablaBodega = $('#tablaReporteFaltante');
    encabezado.show();
    pie.show();
    tablaBodega.addClass('tablabodegas');
    $('#areaImpresion').printArea();
    encabezado.hide();
    pie.hide();
    tablaBodega.removeClass('tablabodegas');


}

function VerificaBolaEns()
{
   var idBodega = $('#id_puntoBodega').val();
   var pesoBola = $('#id_pesoBola').val();
    var pesoSal = $('#id_sal').val();
   var pesoPapaina = $('#id_papaina').val();

    Existencias(97,idBodega,pesoBola);
    Existencias(89,6,pesoSal);
    Existencias(95,6,pesoPapaina);

}
function GuardarEnsBola(idEnsalinado)
{
    var opcion = confirm('Desea guardar este Ajuste, recuerde que esto afectara el inventario.');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/guardarEnsBola/',
            dataType: "json",
            type: "get",
            data: {'idEnsalinado': idEnsalinado},
            success: function (respuesta) {
                var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
            }

        });
    }
}
function CostearEnsBola(idEnsalinado)
{
     $.ajax({

            url: '/fabricacion/costearEnsBola/',
            dataType: "json",
            type: "get",
            data: {'idEnsalinado': idEnsalinado},
            success: function (respuesta) {
                var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
            }

        });

}
function GuardarAjuste(idAjuste)
{
    var opcion = confirm('Desea guardar este Ajuste, recuerde que esto afectara el inventario.');
    if (opcion == true) {
        $.ajax({

            url: '/inventario/guardarAjustes/',
            dataType: "json",
            type: "get",
            data: {'idAjuste': idAjuste},
            success: function (respuesta) {
                var n = noty({text: respuesta, type: 'success', layout: 'bottom'});
            }

        });
    }
}

function ImprimirMovimientos() {

                var encabezado = $('#encabezado');
                var pie = $('#pieRecibo');
                var tablaRepoMovimientos = $('#tablaReporteMovimientos');
                var tablaMovimientos = $('#tablaMovi');
                var calculadora = $('#calculaVuelto');
                calculadora.hide();
                encabezado.show();
                pie.show();
                tablaRepoMovimientos.hide();
                tablaMovimientos.show();

                tablaRepoMovimientos.addClass('recibo');
                tablaMovimientos.addClass('recibo');

                $('#recibo').printArea();
                encabezado.hide();
                pie.hide();
                tablaMovimientos.removeClass('recibo');
                tablaRepoMovimientos.removeClass    ('recibo');
                calculadora.show();
                $('#imprimeRecibo').hide();
}

function consultaMovimientos()
{

    if($("#porBodega").is(':checked')) {
            var bodega = $('#bodega').val();
            //var NombreBodega = bodega.text();
        } else {
            var producto = $('#productoMovimiento').val();
            //var NombreProducto = producto.text();
        }
    var fechaInicio = $('#inicio').val();
    var fechaFin = $('#fin').val();
    var TablaRepoMovimientos = $('#tablaReporteMovimientos');
    var TablaMovimientos = $('#tablaMovi');
    var NombreBodega = '';
    var Fecha = '';
    $.ajax({

            url: '/inventario/reporteMovimientos/',
            dataType: "json",
            type: "get",
            data: {'inicio': fechaInicio,'fin': fechaFin,'producto': producto,'bodega':bodega},
            success: function (respuesta) {
                    TablaRepoMovimientos.find("tr:gt(0)").remove();

                    for (var i=0;i<respuesta.length;i++)
                    {
                        TablaRepoMovimientos.append(
                                "<tr><td>" + respuesta[i].fields.tipo +
                                "</td><td>" + respuesta[i].fields.fechaMov +
                                "</td><td>" + respuesta[i].fields.nombreProd +
                                "</td><td>"  + respuesta[i].fields.desde +
                                "</td><td>"  + respuesta[i].fields.Hasta +
                                "</td><td>"  + respuesta[i].fields.entrada +
                                "</td><td>"  + respuesta[i].fields.salida +
                                "</td></tr>");

                        TablaMovimientos.append(
                                "<tr><td>" + respuesta[i].fields.tipo +
                                "</td><td>" + respuesta[i].fields.nombreProd +
                                "</td><td>"  + Math.round(respuesta[i].fields.entrada) +
                                "</td><td>"  + Math.round(respuesta[i].fields.salida) +
                                "</td></tr>");

                         NombreBodega = respuesta[i].fields.Hasta;
                         Fecha = respuesta[i].fields.fechaMov;


                    }
                $('#fechaMov').append(' : '+Fecha);
                $('#bodegaMov').append(' : '+NombreBodega);
             }

        });
}
function PasaValorEnvio()
{
    var peso = $('#id_pesoTraslado').val();
    $('#id_pesoEnvio').val(peso);

}

function ExportarFaltantes()
{
    $('#tablaReporteFaltante').tableExport({type:'excel',escape:'false',pdfFontSize:8});
}
function Exportar()
{
    $('#tablaApanados').tableExport({type:'pdf',escape:'false',pdfFontSize:8,ignoreColumn: [3,9,10]});
}
function conciliarFaltantes() {

     var table = $('#tablaReporteFaltante').tableToJSON({
         onlyColumns:[0,7]
     });
    var datos = JSON.stringify(table);
    var bodega = $('#bodegaFaltantes option:selected');
    var CodigoBodega = bodega.val();

     //alert(JSON.stringify(table));
    var opcion = confirm('Desea ajustar los productos Seleccionados?');
    if (opcion == true) {
        $.ajax({

            url: '/inventario/conciliaInventario/',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            type: "get",
            data: {'datos': datos,'CodigoBodega':CodigoBodega},
            success: function (respuesta) {
                alert(respuesta);
            }

        });
    }

}
$('#tablaReporteFaltante').delegate('tr.pesos','change', function(){

    var fisico = $(".actual",this).val();

    if ($(".conciliar",this).attr('checked')){}//$(this).find("td").eq(7).html(fisico);
    else $(this).find("td").eq(7).html(0);

    var invSistema = parseInt($(this).find("td").eq(3).html());
    var undSistema = parseInt($(this).find("td").eq(4).html());

    if (invSistema < 0)invSistema = invSistema * (-1);
    if (undSistema < 0)undSistema = undSistema * (-1);

    var faltante = 0;
    if (invSistema != 0)faltante = fisico - invSistema;
    else faltante = fisico - undSistema;

    $(this).find("td").eq(7).html(faltante);
});


function ReporteFaltantes() {

    var bodega = $('#bodegaFaltantes option:selected');
    var CodigoBodega = bodega.val();
    var NombreBodega = bodega.text();
    var color = '';
    var colorund = '';

   var tablaFaltante = $("#tablaReporteFaltante");

        $.ajax({

            url: '/inventario/reporteFaltantes/',
            dataType: "json",
            type: "get",
            data: {'bodega': CodigoBodega},
            success: function (respuesta) {
                    tablaFaltante.find("tr:gt(0)").remove();

                    for (var i=0;i<respuesta.length;i++)
                    {


                        if((respuesta[i].fields.pesoProductoStock >= 1)&&(respuesta[i].fields.pesoProductoStock <= 1999))
                             {
                                    color = 'red';
                             }
                        else if((respuesta[i].fields.pesoProductoStock >= 2000)&&(respuesta[i].fields.pesoProductoStock <= 20000))
                            {
                                    color = 'green';
                            }
                        else if((respuesta[i].fields.pesoProductoStock > 20000))
                            {
                                    color = 'orange';
                            }
                        else if(respuesta[i].fields.pesoProductoStock == 0)
                        {
                            color = 'white';
                        }


                        if((respuesta[i].fields.unidadesStock >= 1)&&(respuesta[i].fields.unidadesStock <= 5))
                             {
                                    colorund = 'red';
                             }
                        else if((respuesta[i].fields.unidadesStock >= 6)&&(respuesta[i].fields.unidadesStock <= 15))
                            {
                                    colorund = 'green';
                            }
                        else if((respuesta[i].fields.unidadesStock > 16))
                            {
                                    colorund = 'orange';
                            }
                        else if(respuesta[i].fields.pesoProductoStock == 0)
                        {
                            colorund = 'white';
                        }


                            if ((parseInt(respuesta[i].fields.pesoProductoStock)!= 0) || (parseInt(respuesta[i].fields.unidadesStock)))
                            {

                                tablaFaltante.append(
                                "<tr style= 'color: black' class = 'pesos'><td>" + respuesta[i].fields.producto +
                                "</td><td>" + respuesta[i].fields.nombreProducto +
                                "</td><td>" + NombreBodega +
                                "</td><td style= 'background:"+ color +" ; font-weight: bold'>" +parseInt(respuesta[i].fields.pesoProductoStock) +
                                "</td><td style= 'background:"+ colorund +" ; font-weight: bold ' >" + parseInt(respuesta[i].fields.unidadesStock) +
                                "</td><td><input  class='actual' type = 'text' style='text-align: center'>"+
                                 "</td><td>"+ '0' +
                                "</td><td>"+ '0' +
                                "</td><td><input type = 'checkbox' class = 'conciliar' checked = 'checked'>"+
                                "</td></tr>");
                            }
                    }

                    }

        });

}

function ReportePesosLote()
{
    $( "#progressbar" ).show();
    var idCompra = $('#compras').val();
    var idLista = $('#listaP').val();
    var TotalCosto = 0;
    var TotalCompra = 0;
    var perdida = 0;
    var TotalVenta = 0;
    var modCif = 0;
    var tablaCosto = $("#tablaCostoLote");


    $.ajax({

            url: '/fabricacion/utilidadReses/',
            dataType: "json",
            type: "get",
            data: {'idCompra': idCompra,'idLista':idLista},
            success: function (respuesta)
            {
                    $("#tablaPesoLote").find("tr:gt(0)").remove();
                    $("#tablaPesoCarne").find("tr:gt(0)").remove();
                    $("#tablaPorcentaje").find("tr:gt(0)").remove();
                    tablaCosto.find("tr:gt(0)").remove();

                    $.each(respuesta.Pesos,function(key,value){
                    if(value != 0)
                    {
                        $("#tablaPesoLote").append("<tr><td>" + key + "</td><td>" + Math.ceil(value) + "</td></tr>");

                    }
                    });

                    var SubProducto =  $('#SubProducto');
                    var Grasa =  $('#Grasa');
                    var carne =  $('#carne');
                    var Desecho =  $('#Desecho');
                    var Costilla =  $('#Costilla');
                    var Hueso =  $('#Hueso');

                    $.each(respuesta.adicionales,function(key,value){

                        $("#tablaPesoCarne").append("<tr><td>" + key + "</td><td>" + Math.ceil(value) +' %'+ "</td></tr>");
                        $('#diagrama').show();
                        var  alto = Math.ceil(value) * 4;

                        if (key == 'SubProducto')
                        {
                           SubProducto.height(alto);
                        }
                        if (key == 'Grasa')
                        {
                           Grasa.height(alto);
                        }
                        if (key == 'Carne')
                        {
                           carne.height(alto);
                        }
                        if (key == 'Desecho')
                        {
                           Desecho.height(alto);
                        }

                        if (key == 'Costilla')
                        {
                           Costilla.height(alto);
                        }
                        if (key == 'Hueso')
                        {
                           Hueso.height(alto);
                        }


                    });
                    $.each(respuesta.perdida,function(key,value){

                       perdida = value;
                    });
                    $.each(respuesta.ListaVenta,function(key,value){

                       TotalVenta += value;
                    });

                    $.each(respuesta.costo,function(key,value){
                        TotalCosto += Math.ceil(value);
                    });
                    $.each(respuesta.compras,function(key,value){
                        TotalCompra = value;
                    });
                    $.each(respuesta.costoOperativo,function(key,value){
                        modCif = value;
                    });

                    var costo = TotalCompra + modCif;
                    var gananciaEstimada = TotalVenta - costo;
                    var utilidad = (gananciaEstimada * 100)/TotalVenta;

                    tablaCosto.append("<tr><td>" + 'Total Compra' + "</td><td style='text-align: right' >" +'$ '+ TotalCompra + "</td></tr>");
                    tablaCosto.append("<tr><td>" + 'Costo Operacion' + "</td><td style='text-align: right' >"+'$ ' + modCif + "</td></tr>");
                    tablaCosto.append("<tr><td>" + 'Total Operacion' + "</td><td style='text-align: right' >"+'$ ' + costo + "</td></tr>");


                    tablaCosto.append("<tr><td>" + 'Total Venta Estimada' + "</td><td style='text-align: right' >" +'$ '+ Math.round(TotalVenta) + "</td></tr>");
                    tablaCosto.append("<tr><td>" + 'Utilidad Estimada' + "</td><td style='text-align: right' >" +'$ '+ Math.round(gananciaEstimada) + "</td></tr>");
                    tablaCosto.append("<tr><td>" + 'Utilidad' + "</td><td style='text-align: right' >" + Math.round(utilidad) +' %'+ "</td></tr>");
                    tablaCosto.append("<tr><td>" + 'perdida de Pie a Canal' + "</td><td style='text-align: right' >" + perdida +' %'+ "</td></tr>");

                /*******************************************************************************************************/

                $( "#progressbar" ).hide();
            }

        });

}
function RepoConversiones() {

    var bodega = $('#bodegas option:selected');
    //var producto = $('#productoTraslado option:selected');
    var fechaInicio = $('#inicio').val();
    var fechaFin = $('#fin').val();
    var CodigoBodega = bodega.val();
    var estadoConversion = '';
    var color = '';

    /*var CodigoProducto = producto.val();

    var NombreBodega = bodega.text();
    var NombreProducto = producto.text();

    var TotalCompra = 0;
    var TotalUnds = 0;*/

    var TablaRepoConversiones = $("#TablaRepoConversiones");

        $.ajax({

            url: '/fabricacion/RepoConv/',
            dataType: "json",
            type: "get",
            data: {'inicio': fechaInicio,'fin': fechaFin,'bodega': CodigoBodega},
            success: function (respuesta) {
                    TablaRepoConversiones.find("tr:gt(0)").remove();
                    //$('#total').remove();
                    for (var i=0;i<respuesta.length;i++)
                    {
                        if(respuesta[i].fields.costoP1 < respuesta[i].fields.costoP2)
                        {
                            estadoConversion = 'Ganancia';
                            color = 'blue';
                        }
                        else
                        {
                             estadoConversion = 'Perdida';
                             color = 'red';
                        }
                        TablaRepoConversiones.append(
                                "<tr  style='color:" + color + "' ><td>" + respuesta[i].fields.fechaConversion +
                                "</td><td>" + respuesta[i].fields.pesoConversion +
                                "</td><td>" + respuesta[i].fields.productoUno +
                                "</td><td>" + respuesta[i].fields.costoP1 +
                                "</td><td>" + respuesta[i].fields.productoDos +
                                "</td><td>" + respuesta[i].fields.costoP2 +
                                "</td><td>" + estadoConversion +
                                "</td></tr>");

                    }
                /*
                * pesoConversion
                * costoP1
                * costoP2
                * */

                //var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                //"</td><td>" + "<a target='_blank'' href='/inventario/dettraslado/"+ respuesta[i].fields.traslado + "'>"+'Detalles'+"</a>" +
                    }

        });

}
function ReporteTelleresPuntos ()
{
    $( "#progressbar" ).show();
    var inicio = $('#inicio').val();
    var fin = $('#fin').val();
    var bodega = $('#bodega').val();

    $.ajax({

            url : '/fabricacion/reporteTallerPunto/',
            dataType : "json",
            type : "get",
            data : {'inicio':inicio,'fin':fin,'bodega':bodega},
            success : function(respuesta)
            {
                $("#tablaCostoFrito").find("tr:gt(0)").remove();
                $("#tablaPesoFrito").find("tr:gt(0)").remove();
                $("#tablaCostoCroqueta").find("tr:gt(0)").remove();
                $("#tablaPesoCroqueta").find("tr:gt(0)").remove();
                $("#tablaCostoCarne").find("tr:gt(0)").remove();
                $("#tablaPesoCarne").find("tr:gt(0)").remove();
                $("#tablaCostoBola").find("tr:gt(0)").remove();
                $("#tablaPesoBola").find("tr:gt(0)").remove();
                $("#tablaCostoMolida").find("tr:gt(0)").remove();

                $.each(respuesta.promedioFrito,function(key,value){

                    $("#tablaCostoFrito").append("<tr><td>" + 'Frito Condimentado' + "</td><td style='text-align: right'>"+'$ '+ Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.pesoFrito,function(key,value){

                    $("#tablaPesoFrito").append("<tr><td>" + key + "</td><td style='text-align: right'>" + Math.ceil(value) +' grs'+ "</td></tr>");
                });

                /*******************************************************************************************************/
                $.each(respuesta.promedioCroqueta,function(key,value){

                    $("#tablaCostoCroqueta").append("<tr><td>" + 'Croqueta Apanada' + "</td><td style='text-align: right'>"+'$ '+ Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.pesoCroqueta,function(key,value){

                    $("#tablaPesoCroqueta").append("<tr><td>" + key + "</td><td style='text-align: right'>" + Math.ceil(value) +' grs'+ "</td></tr>");
                });

                /*******************************************************************************************************/
                $.each(respuesta.promedioCarneCond,function(key,value){

                    $("#tablaCostoCarne").append("<tr><td>" + 'Carne Condimentada' + "</td><td style='text-align: right'>"+'$ '+ Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.pesoCarneCond,function(key,value){

                    $("#tablaPesoCarne").append("<tr><td>" + key + "</td><td style='text-align: right'>" + Math.ceil(value) +' grs'+ "</td></tr>");
                });

                /*******************************************************************************************************/
                $.each(respuesta.promedioBolaEns,function(key,value){

                    $("#tablaCostoBola").append("<tr><td>" + 'Carne Ensalinada' + "</td><td style='text-align: right'>"+'$ '+ Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.pesoBolaEns,function(key,value){

                    $("#tablaPesoBola").append("<tr><td>" + key + "</td><td style='text-align: right'>" + Math.ceil(value) +' grs'+ "</td></tr>");
                });
                /*******************************************************************************************************/
                $.each(respuesta.promedioMolida,function(key,value){

                    $("#tablaCostoMolida").append("<tr><td>" + 'Carne Molida' + "</td><td style='text-align: right'>"+'$ '+ Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.pesoMolida,function(key,value){

                    $("#tablaPesoMolida").append("<tr><td>" + key + "</td><td style='text-align: right'>" + Math.ceil(value) +' grs'+ "</td></tr>");
                });

            $( "#progressbar" ).hide();
            }

        });
}
function consultaTrasladosBodega ()
{
    $( "#progressbar" ).show();
    var inicio = $('#inicio').val();
    var fin = $('#fin').val();
    var bodega = $('#bodega').val();

    $.ajax({

            url : '/fabricacion/reporteTrasladoBodega/',
            dataType : "json",
            type : "get",
            data : {'inicio':inicio,'fin':fin,'bodega':bodega},
            success : function(respuesta)
            {
                $("#tablaTrasladoBodega").find("tr:gt(0)").remove();

                $.each(respuesta.traslado,function(key,value){

                    $("#tablaTrasladoBodega").append("<tr><td>" + key + "</td><td style='text-align: right'>" + Math.ceil(value) + "</td></tr>");
                });

            $( "#progressbar" ).hide();
            }

        });
}
function consultaTraslados() {

    var bodega = $('#bodega option:selected');
    var producto = $('#productoTraslado option:selected');

    var fechaInicio = $('#inicio').val();
    var fechaFin = $('#fin').val();
    var CodigoBodega = bodega.val();
    var CodigoProducto = producto.val();

    var NombreBodega = bodega.text();
    var NombreProducto = producto.text();

    var TotalCompra = 0;
    var TotalUnds = 0;

    var tablaReporteTraslado = $("#tablaReporteTraslado");

        $.ajax({

            url: '/fabricacion/reporteTraslado/',
            dataType: "json",
            type: "get",
            data: {'inicio': fechaInicio,'fin': fechaFin,'bodega': CodigoBodega,'producto': CodigoProducto},
            success: function (respuesta) {
                    tablaReporteTraslado.find("tr:gt(0)").remove();
                    $('#total').remove();
                    for (var i=0;i<respuesta.length;i++)
                    {
                        tablaReporteTraslado.append(
                                "<tr><td>" + respuesta[i].fields.traslado +
                                "</td><td>" + NombreBodega +
                                "</td><td>" + NombreProducto +
                                "</td><td>" + respuesta[i].fields.pesoTraslado +
                                "</td><td>" + respuesta[i].fields.unidadesTraslado +
                                "</td><td>" + "<a target='_blank'' href='/inventario/dettraslado/"+ respuesta[i].fields.traslado + "'>"+'Detalles'+"</a>" +
                                "</td></tr>");
                        TotalCompra += parseInt(respuesta[i].fields.pesoTraslado);
                        TotalUnds += parseInt(respuesta[i].fields.unidadesTraslado);
                    }

                tablaReporteTraslado.append("<tr><th id = 'total' colspan='3' style='text-align: right'>" +
                    'Totales:'  +"</th><th>"+  +TotalCompra +"</th><th>"+ TotalUnds +"</th></tr>");

                //var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                    }

        });

}

function consultaCompras() {

    var bodega = $('#bodega option:selected');
    var provedor = $('#provedor option:selected');

    var fechaInicio = $('#inicio').val();
    var fechaFin = $('#fin').val();
    var CodigoBodega = bodega.val();
    var CodigoProvedor = provedor.val();

    var NombreBodega = bodega.text();
    var NombreProvedor = provedor.text();

    var TotalCompra = 0;

    var tablaCompra = $("#tablaReporteCompra");

        $.ajax({

            url: '/inventario/jsonCompras/',
            dataType: "json",
            type: "get",
            data: {'inicio': fechaInicio,'fin': fechaFin,'bodega': CodigoBodega,'provedor': CodigoProvedor},
            success: function (respuesta) {
                    tablaCompra.find("tr:gt(0)").remove();
                    $('#total').remove();
                    for (var i=0;i<respuesta.length;i++)
                    {
                        if( (respuesta[i].fields.tipo == 2)||(respuesta[i].fields.tipo == 3) )
                            {
                               tablaCompra.append(

                                "<tr><td>" + respuesta[i].pk +
                                "</td><td>" + respuesta[i].fields.fechaCompra +
                                "</td><td>" + NombreProvedor +
                                "</td><td>" + NombreBodega +
                                "</td><td>" + respuesta[i].fields.cantCabezas +
                                "</td><td>" + '$ ' + respuesta[i].fields.vrCompra +
                                "</td><td>" +"<a target='_blank'' href='/inventario/recepcion/"+ respuesta[i].pk + "'>"+'Recepcion'+"</a>" +
                                "</td></tr>");
                            }else
                                {
                                    tablaCompra.append(

                                "<tr><td>" + respuesta[i].pk +
                                "</td><td>" + respuesta[i].fields.fechaCompra +
                                "</td><td>" + NombreProvedor +
                                "</td><td>" + NombreBodega +
                                "</td><td>" + respuesta[i].fields.cantCabezas +
                                "</td><td>" + '$ ' + respuesta[i].fields.vrCompra +
                                "</td><td>" + "<a target='_blank'' href='/inventario/detcompra/"+ respuesta[i].pk + "'>"+'Detalles'+"</a>"
                                    +"<a target='_blank'' href='/inventario/recepcion/"+ respuesta[i].pk + "'>"+'Recepcion'+"</a>" +
                                "</td></tr>");

                                }
                        //

                        TotalCompra += respuesta[i].fields.vrCompra;
                    }

                tablaCompra.append("<tr><th id = 'total' colspan='4' style='text-align: right'>" + 'Total :'  +"</th><th>"+ '$ ' +TotalCompra +"</th></tr>");

                //var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                    }

        });

}
function VerificarConversiones () {
   var idBodega = $('#id_puntoConversion').val();
   var peso = $('#id_pesoConversion').val();
   var prod1 = $('#id_productoUno').val();

   Existencias(prod1,idBodega,peso);

}
function GuardarConversion(idConversion) {
    //Funcion que costea el apanado actual

    //var producto1 = $('#id_productoUno').val();
    //var producto2 = $('#id_productoDos').val();


    var opcion = confirm('Desea guardar este Registro, recuerde que esto afectara el inventario.');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/Guardaconversiones/',
            dataType: "json",
            type: "get",
            data: {'idConversion': idConversion},
            success: function (respuesta) {
                if (respuesta != '') {
                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                }

            }

        });
    }
}
function GuardarMiga(IdMiga) {
    //Funcion que costea el apanado actual

    var opcion = confirm('Desea guardar este Registro, recuerde que esto afectara el inventario.');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/guardarMiga/',
            dataType: "json",
            type: "get",
            data: {'IdMiga': IdMiga},
            success: function (respuesta) {
                if (respuesta != '') {

                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                }

            }

        });
    }
}
function VerificarReApanados () {
   var idBodega = $('#id_puntoReApanado').val();
   var pesoMiga = $('#id_miga').val();
   var pesoChuleta = $('#id_pesoChuleta').val();
   var chuleta = $('#id_chuelta').val();

    Existencias(109,idBodega,pesoMiga);
    Existencias(chuleta,idBodega,pesoChuleta);
}
function GuardarreApanado(idReApanado) {
    //Funcion que costea el apanado actual
    var opcion = confirm('Desea guardar este Registro, recuerde que esto afectara el inventario.');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/guardarReApanado/',
            dataType: "json",
            type: "get",
            data: {'idReApanado': idReApanado},
            success: function (respuesta) {
                if (respuesta != '') {
                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                }

            }

        });
    }
}
function VerificarInsCroquetas () {
    var idBodega = $('#id_puntoCroq').val();
    var pesoCroqueta = $('#id_croqueta').val();
    var pesoCond = $('#id_condimento').val();
    var pesoMiga = $('#id_miga').val();
    Existencias(109, idBodega, pesoMiga);
    Existencias(111, idBodega, pesoCond);
    Existencias(175, idBodega, pesoCroqueta);

}

function GuardarCroqueta(idCroqueta) {
    //Funcion que costea el apanado actual
    var opcion = confirm('Desea guardar este Registro, recuerde que esto afectara el inventario.');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/guardarCroquetas/',
            dataType: "json",
            type: "get",
            data: {'idCroqueta': idCroqueta},
            success: function (respuesta) {
                if (respuesta != '') {
                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                }

            }

        });
    }
}
function CostearCroqueta(idCroqueta)
{
    //Funcion que costea el apanado actual
    var opcion = confirm('Desea costear este Registro ?');
    if (opcion == true)
    {
        $.ajax({

            url : '/fabricacion/costearCroquetas/',
            dataType : "json",
            type : "get",
            data : {'idCroqueta':idCroqueta},
            success : function(respuesta)
            {
                if (respuesta != '')
                {
                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                }

            }

        });
    }

}
function VerificarCondCarne () {
   var idBodega = $('#id_puntoCond').val();
   var pesoCond = $('#id_condimento').val();

    Existencias(111,idBodega,pesoCond);
}
function VerificarProdCarne () {
   var idBodega = $('#id_puntoCond').val();
   var pesoCarne = $('#id_pesoProducto').val();
   var producto = $('#id_productoCond').val();

    Existencias(producto,idBodega,pesoCarne);
}
function VerificarCond () {
   var idBodega = $('#id_punto').val();
   var pesoCond = $('#id_condimento').val();

    Existencias(111,idBodega,pesoCond);
}
function VerificarProdFrito () {
   var idBodega = $('#id_punto').val();
   var pesoCarne = $('#id_pesoProducto').val();
   var producto = $('#id_productoFrito').val();

    Existencias(producto,idBodega,pesoCarne);
}
function CostearCarneCond(idCarne)
{
    var opcion = confirm('Desea costear este Registro.');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/costearCarneCond/',
            dataType: "json",
            type: "get",
            data: {'idCarne': idCarne},
            success: function (respuesta) {
                if (respuesta != '') {
                   var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                }

            }

        });
    }
}
function GuardarCarneCond(idCarne)
{
    var opcion = confirm('Desea costear este Registro.');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/guardarCarneCond/',
            dataType: "json",
            type: "get",
            data: {'idCarne': idCarne},
            success: function (respuesta) {
                if (respuesta != '') {
                   var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                }

            }

        });
    }
}
function CostearFrito(idFrito)
{
    var opcion = confirm('Desea costear este Registro.');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/costearFritos/',
            dataType: "json",
            type: "get",
            data: {'idFrito': idFrito},
            success: function (respuesta) {
                if (respuesta != '') {
                   var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                }

            }

        });
    }
}
function GuardarFrito(idFrito)
{
    var opcion = confirm('Desea guardar este Registro, recuerde que esto afectara el inventario.');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/guardarFritos/',
            dataType: "json",
            type: "get",
            data: {'idFrito': idFrito},
            success: function (respuesta) {
                if (respuesta != '') {
                   var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                }

            }

        });
    }
}
function GuardarPicadillo(idMenudo)
{
    var opcion = confirm('Desea guardar este Registro, recuerde que esto afectara el inventario.');
    if (opcion == true) {
        $.ajax({

            url: '/fabricacion/guardarMenudo/',
            dataType: "json",
            type: "get",
            data: {'idMenudo': idMenudo},
            success: function (respuesta) {
                if (respuesta != '') {
                   var n = noty({text: respuesta, type:'success',layout: 'bottom'});
                }

            }

        });
    }
}

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

function consultaMenChicha ()
{   $( "#progressbar" ).show();
    var inicio = $('#inicio').val();
    var fin = $('#fin').val();
    var grupo = $('#grupo').val();


    $.ajax({

            url : '/fabricacion/reporteMenChich/',
            dataType : "json",
            type : "get",
            data : {'inicio':inicio,'fin':fin,'grupo':grupo},
            success : function(respuesta)
            {

                $("#tablaPromedioCostoMenudos").find("tr:gt(0)").remove();
                $("#tablaPesoMenudos").find("tr:gt(0)").remove();
                $("#tablaPromedioCostoChicharrones").find("tr:gt(0)").remove();
                $("#tablaPesoChicharrones").find("tr:gt(0)").remove();
                $("#tablaPromedioCostoGrasa").find("tr:gt(0)").remove();
                $("#tablaPesoGrasa").find("tr:gt(0)").remove();

                $.each(respuesta.promedioMiga,function(key,value){

                    $("#tablaPromedioCostoMenudos").append("<tr><td>" + 'Menudo' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ListaCantMiga,function(key,value){

                    $("#tablaPesoMenudos").append("<tr><td>" + key + "</td><td>" + value + "</td></tr>");
                });
                $.each(respuesta.promedioCondimento,function(key,value){

                    $("#tablaPromedioCostoChicharrones").append("<tr><td>" + 'Chicharrones' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ListaCantCond,function(key,value){

                    $("#tablaPesoChicharrones").append("<tr><td>" + key + "</td><td>" + value + "</td></tr>");
                });

                $.each(respuesta.promedioMolidas,function(key,value){

                    $("#tablaPromedioCostoGrasa").append("<tr><td>" + 'Grasa' + "</td><td>" + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ListaCantMolida,function(key,value){

                    $("#tablaPesoGrasa").append("<tr><td>" + key + "</td><td>" + value + "</td></tr>");
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
                $("#tablaPesoPolloCond").find("tr:gt(0)").remove();
                $("#tablaChuletaPollo").find("tr:gt(0)").remove();
                $("#tablaPesoChuletaPollo").find("tr:gt(0)").remove();
                $("#tablaChuletasCerdo").find("tr:gt(0)").remove();
                $("#tablaPesoChuletaCerdo").find("tr:gt(0)").remove();



                $.each(respuesta.promedioBandejasCerdo,function(key,value){

                    $("#tablaPromedioCostoBandejasCerdo").append("<tr><td>" + 'Bandejas de Cerdo Apanado' + "</td><td>"+ '$ ' + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.cantBandejasCerdo,function(key,value){

                    $("#tablaCantBandejasCerdo").append("<tr><td>" + 'Bandejas de Cerdo Apanado' + "</td><td>" + value +' unds'+ "</td></tr>");
                });
                $.each(respuesta.promedioBandejasPollo,function(key,value){

                    $("#tablaPromedioCostoBandejas").append("<tr><td>" + 'Bandejas de Pollo Apanado' + "</td><td>"+ '$ ' + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.cantBandejas,function(key,value){

                    $("#tablaCantBandejas").append("<tr><td>" + 'Bandejas de Pollo Apanado' + "</td><td>" + value +' unds'+ "</td></tr>");
                });
                $.each(respuesta.Promedio,function(key,value){

                    $("#tablaPromedioCostoPollo").append("<tr><td>" + 'Filete Condimetado de pollo' + "</td><td>" + '$ '+ Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.ListaPesoFilete,function(key,value){

                    $("#tablaPesoPolloCond").append("<tr><td>" + key + "</td><td>" + value +' grs'+ "</td></tr>");
                });

                $.each(respuesta.ListaCosto,function(key,value){

                    $("#tablaPromedioCostoTajado").append("<tr><td>" + key + "</td><td>" + '$ '+ Math.ceil(value) + "</td></tr>");
                });

                $.each(respuesta.ListaPeso,function(key,value){
                    $("#tablaPromedioPesoPollo").append("<tr><td>" + key + "</td><td>" + value +' grs'+ "</td></tr>");
                });

                $.each(respuesta.promedioChuletasPollo,function(key,value){

                    $("#tablaChuletaPollo").append("<tr><td>" + 'Chuletas de Pollo' + "</td><td>"+ '$ ' + Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.pesoChuletaPollo,function(key,value){

                    $("#tablaPesoChuletaPollo").append("<tr><td>" + 'Chuletas de Pollo' + "</td><td>" + value +' grs'+ "</td></tr>");
                });
                $.each(respuesta.promedioChuletasCerdo,function(key,value){

                    $("#tablaChuletasCerdo").append("<tr><td>" + 'Chuletas de Cerdo' + "</td><td>" + '$ '+ Math.ceil(value) + "</td></tr>");
                });
                $.each(respuesta.pesoChuletaCerdo,function(key,value){


                    $("#tablaPesoChuletaCerdo").append("<tr><td>" + 'Chuletas de Cerdo' + "</td><td>" + value +' grs'+ "</td></tr>");
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
                $("#tablaPromedioPerdida").find("tr:gt(0)").remove();
                 $("#tablaPesoDespostado").find("tr:gt(0)").remove();

                $.each(respuesta.costos,function(key,value){

                    $("#tablaPromedio").append("<tr><td>" + key + "</td><td>" +'$ '+ value + "</td></tr>");
                });
                $.each(respuesta.pesos,function(key,value){

                    $("#tablaPesos").append("<tr><td>" + key + "</td><td>" + value +' grs.'+ "</td></tr>");
                });
                $.each(respuesta.promedioPerdida,function(key,value){

                    $("#tablaPromedioPerdida").append("<tr><td>" + Math.ceil(value) +' grs.'+ "</td></tr>");
                });
                $.each(respuesta.totalDespostado,function(key,value){

                    $("#tablaPesoDespostado").append("<tr><td>" + Math.ceil(value) +' Kg.'+ "</td></tr>");
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
                   var n = noty({text: respuesta, type:'success',layout: 'bottom'});
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
                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});
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
                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});
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
                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});
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
                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});
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
                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});
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
    Existencias(109,5,miga);
}
function TraecostoEnsalinado()
{
    var producto = $('#id_productoEnsalinado').val();
    var peso = $('#id_pesoProducto').val();
    Existencias(producto,5,peso);
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
                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});
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
                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});

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
                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});
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
                    var n = noty({text: respuesta, type:'error',layout: 'bottom'});
                    //alert(respuesta);
                }

            }

        });
}
function ExistenciasUnd(idProducto,idBodega,unidades)
{
    /*Metodo para verificar el stock del producto seleccionado*/

    $.ajax({

            url : '/fabricacion/existenciasund/',
            dataType : "json",
            type : "get",
            data : {'producto':idProducto,'bodega':idBodega,'unidades':unidades},
            success : function(respuesta)
            {
                if (respuesta != '')
                {
                    var n = noty({text: respuesta, type:'error',layout: 'bottom'});
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
                    var n = noty({text: respuesta, type:'success',layout: 'bottom'});
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
             var n = noty({text: respuesta, type:'success',layout: 'bottom'});
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
             var n = noty({text: respuesta, type:'success',layout: 'bottom'});
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
             var n = noty({text: respuesta, type:'success',layout: 'bottom'});
         }

     });
    }
}
function calculoValorProducto()
{
    var peso = $('#id_peso').val();
    var vrKilo = $('#id_vrUnitario').val();
    var unidades = $('#id_unidades').val();
    var total = 0;
    if (unidades == 0)
    {
        total = Math.round((vrKilo * peso)/1000);
        $('#id_vrTotal').val(total);
    }else
    {
        total = vrKilo * unidades;
        $('#id_vrTotal').val(total);
    }


}

function consultaValorProducto()
{
    var combo = $('#id_productoVenta').val();
    var idVenta = $('#codigoVenta').text();
    var peso = $('#id_peso').val();
    var lista = $('#codigoLista').text();
    var unidades = $('#id_unidades').val();

     $.ajax({

        url : '/ventas/consultaPrecioProducto/',
         dataType: "json",
         type: "get",
         data : {'unidades':unidades,'lista':lista,'idProducto':combo,'idVenta':idVenta,'peso':peso},
         success : function(respuesta){

             if(respuesta == "No hay existencias en almacen")
             {
                 var n = noty({text: 'No hay existencias en almacen', type:'error',layout: 'bottom'});

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
             var n = noty({text: respuesta, type:'success',layout: 'bottom'});
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
             var n = noty({text: respuesta, type:'success',layout: 'bottom'});
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
            var n = noty({text: respuesta, type:'success',layout: 'bottom'});
         }
    });
    }

}
