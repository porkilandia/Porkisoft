$(document).on('ready', inicio);

function inicio()
{
    // oculta el boton de guardado en pedido en caso de que sea contado
     /************************************************Template Venta Norte*********************************************/
    var estado = $('#guardado').text();
    var productoVenta = $('#id_productoVenta');
    var pesoVentaPunto = $('#id_pesoVentaPunto');
    var unidadesVentaPunto = $('#id_unidades');
    var total= 0;
    pesoVentaPunto.on('change',calculoTotalVentaPunto);

    if (estado == 'Si')
        {
            $('#FormularioVentaPunto').hide();
            $('#cobraVenta').hide();

        }

/*********************************************CONFIGURACIONES VARIAS **********************************************/

         productoVenta.focus();
         $('#InicioSesion').show();
         productoVenta.on('change',traeValorVenta);
         $('#regreso').on('focus',calculoRegreso);
         var fechaVenta = $('#id_fechaVenta');
         fechaVenta.datepicker({ dateFormat: "dd/mm/yy" });
         $('#id_vrTotalPunto').on('focus',calculoTotalVenta);
         $('#FrmVenta').show();
         $('#FrmVentaPunto').show();
         $("label[for=id_venta],#id_venta").hide();
         $("label[for=id_productoVenta]").hide();
         $('#totalCompra').val($('#totalVentaDet').text()).attr('disabled','-1');

/****************************************************** METODOS ***************************************************/
function Cobrar()
    {
        var venta = $('#NumVenta').text();

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

    }

   function ImprimirRecibo(telefono)
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
                                    "<tr><th>" + 'Resolucion : 140000039353'+ "</th></tr>"+
                                    "<tr><th>" + 'Rango:000000 hasta 999999' + "</th></tr>"+
                                    "<tr><th>" + 'Expedida el : 09-04-2013'+ "</th></tr>"+
                                    "<tr><th>" + direccion +"</th></tr>"+
                                    "<tr><th>" + telefono +"</th></tr>"+
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

    function calculoTotalVenta()
        {
            var peso = $('#id_pesoVentaPunto').val();
            var total = 0;
            var vrUnitario = $('#id_vrUnitarioPunto').val();
            var producto = $('#id_productoVenta').val();
            peso = parseInt(peso);

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

    function calculoRegreso()
    {
        var efectivo = $('#efectivo').val();
        var totalCompra= $('#totalCompra').val();

        var resultado = efectivo - totalCompra;
        $('#regreso').val(resultado);

    }

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

}
