$(document).on("ready", arranque);
var errores_s="";
var num_parametros=0;
function arranque(name) {
    if($("#autores1").val()){
        var string_autores=$("#autores1").val();//En la plantilla el campo autores1 tiene el array de los autores del objeto a modificar
        var autores_arr=string_autores.split(",");//como no hay comunicación con el array autores de la plantilla entonces se crea aquí el array con los autores del objeto.
    }else{
        var autores_arr=[];//si no hay nada en el campo es porque Ó no está en la página de modificación Ó porque no hay autores en el objeto a modificar
    }
    /*
        Deshabilitar / habilitar campos de texto para las busquedas avanzadas
    */
    $("#id_c_titulo").prop('disabled',true);
    $("#id_c_tipo_obj").prop('disabled',true);
    $("#id_c_idioma").prop('disabled',true);
    $("#id_c_fecha").prop('disabled',true);
    $("#id_c_tipo_rec").prop('disabled',true);

    $("#v_tit").click(function(){
        if($("#v_tit").is(':checked')){
            $("#id_c_titulo").prop('disabled',false);
        }else{
            $("#id_c_titulo").prop('disabled',true);
        }
    });

    $("#v_tob").click(function(){
        if($("#v_tob").is(':checked')){
            $("#id_c_tipo_obj").prop('disabled',false);
        }else{
            $("#id_c_tipo_obj").prop('disabled',true);
        }
    });

    $("#v_idi").click(function(){
        if($("#v_idi").is(':checked')){
            $("#id_c_idioma").prop('disabled',false);
        }else{
            $("#id_c_idioma").prop('disabled',true);
        }
    });

    $("#v_fec").click(function(){
        if($("#v_fec").is(':checked')){
            $("#id_c_fecha").prop('disabled',false);
        }else{
            $("#id_c_fecha").prop('disabled',true);
        }
    });

    $("#v_tre").click(function(){
        if($("#v_tre").is(':checked')){
            $("#id_c_tipo_rec").prop('disabled',false);
        }else{
            $("#id_c_tipo_rec").prop('disabled',true);
        }
    });

    // termina

    /* Interacciones con JQueryUI*/
    //$("#rcontenidos").accordion({ active: 2 });
    $("#id_c_fecha" ).datepicker({dateFormat:'dd/mm/yy'});
    $("#id_lc2_fecha" ).datepicker({dateFormat:'dd/mm/yy'});
    $("#id_fecha" ).datepicker({dateFormat:'dd/mm/yy'});

    /*************Interacciones con AJAX*****************/
    $('#busca').click(function(e) {
        e.defaultPrevented;//preventDefault();
        qu = $('#q').val();
        if (qu==""){
            $("#results1").empty();
        }else{
            $.getJSON("/buscar", { q:qu }, function(json){
                $("#results1").empty();
                if (json.length != 0) {
                    obj=json.slice(0,(json.length/2));
                    esp=json.slice(json.length/2,json.length);
                    $.each(obj, function(key,val){
                        if(obj[key]['fields']['proyecto']!=null){
                            $("#results1").append("<li class='resultados'><a href='/proyecto/"+val.pk+"'>"+esp[key]['fields']['lc1_titulo']+"</a></li>");
                        }
                        else{
                            $("#results1").append("<li class='resultados'><a href='/objeto/"+val.pk+"'>"+esp[key]['fields']['lc1_titulo']+"</a></li>");
                        }
                    });
                }else{
                    $("#results1").html('<h3>La búsqueda no arrojó resultados</h3>');
                }
            });
        }
    });

    $('#busqueda').click(function(e) {
        e.preventDefault();
        tit = $('#id_c_titulo').val();
        if($('#v_tit:checked').val()){v_tit = $('#v_tit:checked').val();}else{v_tit = "False";}
        tob = $('#id_c_tipo_obj').val();
        if($('#v_tob:checked').val()){v_tob = $('#v_tob:checked').val();}else{v_tob = "False";}
        idi = $('#id_c_idioma').val();
        if($('#v_idi:checked').val()){v_idi = $('#v_idi:checked').val();}else{v_idi = "False";}

        fec = $('#id_c_fecha').val();
        if($('#v_fec:checked').val()){v_fec = $('#v_fec:checked').val();}else{v_fec = "False";}

        tre = $('#id_c_tipo_rec').val();
        if($('#v_tre:checked').val()){v_tre = $('#v_tre:checked').val();}else{v_tre = "False";}

        /*******************/
        if((v_tit=="True" & tit.length>0) | (v_tob=="True" & tob.length>0) | (v_idi=="True" & idi.length>0) |(v_fec=="True" & fec.length>0) |  (v_tre=="True" & tre.length>0)  ) {
            console.log(idi);
            $.getJSON("/busqueda", { tit:tit, v_tit:v_tit, tob:tob, v_tob:v_tob, idi:idi, v_idi:v_idi, fec:fec, v_fec:v_fec, tre:tre, v_tre:v_tre }, function(json){
                $("#results2").empty();
                if (json.length != 0) {
                    obj=json.slice(0,(json.length/2));
                    esp=json.slice(json.length/2,json.length);
                    $.each(obj, function(key,val){
                        if(obj[key]['fields']['proyecto']!=null){
                            $("#results2").append("<li class='resultados'><a href='/proyecto/"+val.pk+"'>"+esp[key]['fields']['lc1_titulo']+"</a></li>");
                        }
                        else{
                            $("#results2").append("<li class='resultados'><a href='/objeto/"+val.pk+"'>"+esp[key]['fields']['lc1_titulo']+"</a></li>");
                        }
                    });
                }else{
                    $("#results2").html('<h3>La búsqueda no arrojó resultados</h3>');
                }
            });
        }else{
            $("#results2").empty();
        }
    });



/****************************************************/

    $('#btn_agr').click(function(e) {
        if($("#autores1").val()){
            string_autores=$("#autores1").val();//En la plantilla el campo autores1 tiene el array de los autores del objeto a modificar
            autores_arr=string_autores.split(",");//como no hay comunicación con el array autores de la plantilla entonces se crea aquí el array con los autores del objeto.
        }else{
            autores_arr=[];
        }
        $("#error").css('display','none');
        naut = $('#au_name').val();
        aaut = $('#au_last').val();
        raut = $('#au_rol').val();
        if(naut.length>0 & aaut.length>0 & raut.length>0){
            var flag = false;
            var flag2 = false;
            $( "#autores li #sp1" ).each(function( index ) {
                var t = $(this).text().split(" ");
                flag=validar(t,naut,aaut,raut);
                if(flag==true){
                    flag2=true;
                }
            });
            if(flag2){
                $("#error").html("Autor ya existe");
                $("#error").fadeIn();
            }else{
                _naut=naut.replace(/ /g,'-');
                _aaut=aaut.replace(/ /g,'-');
                _raut=raut.replace(/ /g,'-');
                _naut=_naut.replace(/\./g,'');
                _aaut=_aaut.replace(/\./g,'');
                _raut=_raut.replace(/\./g,'');
                var a = _naut+" "+_aaut+" "+_raut;
                autores_arr.push(a);
                $("#autores").fadeIn();
                $("#autores").append('<li id="autors'+_naut+'_'+_aaut+'_'+_raut+'"><span id="sp1">'+naut+' '+aaut+' - '+raut+'</span></li>');
                $("#autores li").last().append(function() {
                    return $('<span class="btn_peq" id="'+_naut+'_'+_aaut+'_'+_raut+'">&nbsp-&nbsp</span>').click(function() {
                       if($("#autores1").val()){
                            string_autores=$("#autores1").val();//En la plantilla el campo autores1 tiene el array de los autores del objeto a modificar
                            autores_arr=string_autores.split(",");//como no hay comunicación con el array autores de la plantilla entonces se crea aquí el array con los autores del objeto.
                        }
                        var e=$(this).context.id;
                        s=e.replace(/_/g,' ');
                        autores_arr.splice(jQuery.inArray(s,autores_arr),1);
                        $('#autores1').val(autores_arr);
                        $("#autors"+e).remove();
                        //console.log("Archivo_autores:  (al eliminar) "+$('#autores1').val());
                    });
                });
                $('#au_name').val("");
                $('#au_last').val("");
                $('#au_rol').val("Autor");
                $('#autores1').val(autores_arr);
                //console.log("Archivo_autores previos:  (al agregar) "+$('#autores1').val());
            }
        }else{
            $("#error").html("Debes digitar todos los campos del Autor");
            $("#error").fadeIn();
        }
    });

    $("#submenu1").click(function(e){
        $("#contenidosm2").fadeOut(function(e){
            $("#contenidosm1").fadeIn();
        });
        $("#submenu1").removeClass('submenu_');
        $("#submenu1").addClass('submenu');
        $("#submenu2").removeClass('submenu');
        $("#submenu2").addClass('submenu_');
    });

    $("#submenu2").click(function(e){
        $("#contenidosm1").fadeOut(function(e){
            $("#contenidosm2").fadeIn();
        });
        $("#submenu1").removeClass('submenu');
        $("#submenu1").addClass('submenu_');
        $("#submenu2").removeClass('submenu_');
        $("#submenu2").addClass('submenu');
    });

    $("#busq1").click(function(e){
        $("#contenidosm4").fadeOut(function(e){
            $("#contenidosm3").fadeIn();
        });
        $("#busq1").removeClass('submenu_');
        $("#busq1").addClass('submenu');
        $("#busq2").removeClass('submenu');
        $("#busq2").addClass('submenu_');
    });

    $("#busq2").click(function(e){
        $("#contenidosm3").fadeOut(function(e){
            $("#contenidosm4").fadeIn();
        });
        $("#busq1").removeClass('submenu');
        $("#busq1").addClass('submenu_');
        $("#busq2").removeClass('submenu_');
        $("#busq2").addClass('submenu');
    });

    /* *******Interactividad(Proyectos)******************/

    $("#sec1_btn").click(function(e){
        $("#sec1").slideToggle();
        $("#sec2").slideUp();
        $("#sec3").slideUp();
    });

    $("#sec2_btn").click(function(e){
        $("#sec1").slideUp();
        $("#sec3").slideUp();
        $("#sec2").slideToggle();
    });

    $("#sec3_btn").click(function(e){
        $("#sec1").slideUp();
        $("#sec2").slideUp();
        $("#sec3").slideToggle();
    });

    $(".sec_formV_par").click(function(e){
        //console.log("algo");
        id=e.target.id;
        s=id.replace(/sec_formV_par/g,'');
        $("#sec_formV_"+s).slideToggle();
    });

    $(".sec_formV input").click(function(e){
        id=e.target.id;
        calif=e.target.value;
        s=id.replace(/id_form-/g,'');
        s1=s.replace(/-valoracion_/g,'');
        st=s1.substr(0,s1.length-1);
        st2=calif.substr(0,calif.length-2);
        num=(Number(st)+1);
        $("#sec_formV_par"+num).removeClass('sec_formV_par_error calificacion_10 calificacion_7 calificacion_5 calificacion_2');
        $("#sec_formV_par"+num).addClass('calificacion_'+st2);
    });

    $("#aprobado_lista").click(function(e){
        $("#sprobado_listaP").slideUp();
        $("#rprobado_listaP").slideUp();
        $("#aprobado_listaP").slideToggle();
    });

    $("#rprobado_lista").click(function(e){
        $("#aprobado_listaP").slideUp();
        $("#sprobado_listaP").slideUp();
        $("#rprobado_listaP").slideToggle();
    });

    $("#sprobado_lista").click(function(e){
        $("#aprobado_listaP").slideUp();
        $("#rprobado_listaP").slideUp();
        $("#sprobado_listaP").slideToggle();
    });

    $(".ind_grados").click(function(e){
        $(this).next().slideToggle();
    });

    $(".lap_factores").click(function(e){
        $(this).next().slideToggle();
    });

    $(".lap_enunciados").click(function(e){
        $(this).next().slideToggle();
    });

    $("#lap_operaciones_l").click(function(e){
        $(this).next().slideToggle();
    });


    /***********************Errores para el formulario de validación************/
    if(errores_s.length>0){
        var errores_arr=errores_s.split(",");
        for(var i=0; i<errores_arr.length; i++){
            cadenafinal=errores_arr[i].replace(/u&#39;form-/g,'').replace(/-valoracion&#39;/g,'').replace(/\[/g,'').replace(/\]/g,'');
            num=(Number(cadenafinal)+1);
            $("#sec_formV_par"+num).addClass("sec_formV_par_error");
        }
        pintarFormularioValidar(num_parametros);
    }

    /***************************************************************/
}

function pintarFormularioValidar(np){
    num_parametros=np;
    for(var j=0; j<num_parametros; j++){
        for(var k=0; k<5; k++){
            if($("#id_form-"+j+"-valoracion_"+k).attr("checked")=="checked"){
                calif=$("#id_form-"+j+"-valoracion_"+k).attr("value");
                st2=calif.substr(0,calif.length-2);
                $("#sec_formV_par"+(j+1)).removeClass('calificacion_10 calificacion_7 calificacion_5 calificacion_2');
                $("#sec_formV_par"+(j+1)).addClass('calificacion_'+st2);
            }
        }
    }
}

function validar(ar,nam,las,rol) {
    var b1=false;
    var b2=false;
    var b3=false;
    for (var i = 0; i < ar.length; i++) {
        if(ar[i]==nam){
            b1=true;
        }
        if(ar[i]==las){
            b2=true;
        }
        if(ar[i]==rol){
            b3=true;
        }
    }
    if(b1 & b2 & b3){
        return true;
    }else{
        return false;
    }
}

$(document).ajaxStart(function() {
    $('#cargando').show();
}).ajaxStop(function() {
    $('#cargando').hide();
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');