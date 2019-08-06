// ENRICHMENT PAGE
var enrichment_page = (function() {
// hide GO-term specific options if UniProt-keywords selected
    $("#copy_paste_field textarea").keypress(function (event) {
        $("#userinput_file").filestyle('clear');
    });

    $("#clear_button").click(function (event) {
        $('#foreground_textarea').val('');
        $('#background_textarea').val('');
        // $("#userinput_file").filestyle('clear');
        // $("#p_value_cutoff").value("0.01");
        // $("#p_value_cutoff").val("0.01");
    });
        // $("#enrichment_method").val("compare_samples");
        // SelectElement("enrichment_method", "compare_samples");


    $('#gocat_upk').change(function() {
        var gocat_upk = $('#gocat_upk').val();
        var choice = gocat_upk == "UPK";
        toggle_if(choice, ".GOT", ".GOT_placeholder");
    });
    $("#gocat_upk").change(); // fire event to hide stuff

// // show 'foreground_n and background_n boxes' if "compare_groups" selected
//     $('#enrichment_method').change(function() {
//         var enrichment_method = $('#enrichment_method').val();
//         var choice = enrichment_method != "compare_groups";
//         toggle_if(choice, ".foreground_n_background_n", "");
//     });
//     $("#enrichment_method").change();

// hide NCBI TaxID if "genome" deselected
    $('#enrichment_method').change(function() {
        var enrichment_method = $('#enrichment_method').val();
        var choice = enrichment_method != "genome";
        toggle_if(choice, ".taxid", "");
    });
    $("#enrichment_method").change();

// show foreground_replicates and background_n only when "compare_groups" is selected
    $('#enrichment_method').change(function() {
        var enrichment_method = $('#enrichment_method').val();
        var choice = enrichment_method != "compare_groups";
        toggle_if(choice, ".foreground_replicates", "");
    });
    $("#enrichment_method").change();

// show score_cutoff only when "characterize_foreground" is selected
    $('#enrichment_method').change(function() {
        var enrichment_method = $('#enrichment_method').val();
        var choice = enrichment_method != "characterize_foreground";
        toggle_if(choice, ".characterize_foreground", "");
    });
    $("#enrichment_method").change();




    // $('.nav-item li').click(function(){
    //     $('.nav-item li').removeClass('active');
    //     $(this).addClass('active');
    // });

    // $(":file").filestyle({dragdrop: true});

});



// show or hide selectors/tags depending on choice
var toggle_if = function(choice, tag){
    if (choice == true) {
        $(tag).hide();
    } else {
        $(tag).show();
    }
};

// RESTULS PAGE
var results_page = (function () {

    // Hide table if number of number of rows == 0
    var tables = document.getElementsByClassName('div_table_etype');
    for (i=0; i< tables.length; i++) {
        var table = tables[i];
        var attr = table.getAttribute('data-value');
        if (attr == 0) {
            table.style.display = 'none';
        }
    }


    jQuery.fn.dataTable.render.ellipsis = function ( cutoff, wordbreak, escapeHtml ) {
    var esc = function ( t ) {
        return t
            .replace( /&/g, '&amp;' )
            .replace( /</g, '&lt;' )
            .replace( />/g, '&gt;' )
            .replace( /"/g, '&quot;' );
    };
    return function ( d, type, row ) {
        // Order, search and type get the original data
        if ( type !== 'display' ) {
            return d;
        }
        if ( typeof d !== 'number' && typeof d !== 'string' ) {
            return d;
        }
        d = d.toString(); // cast numbers
        if ( d.length <= cutoff ) {
            return d;
        }
        var shortened = d.substr(0, cutoff-1);
        // Find the last white space character in the string
        if ( wordbreak ) {
            shortened = shortened.replace(/\s([^\s]*)$/, '');
        }
        // Protect against uncontrolled HTML input
        if ( escapeHtml ) {
            shortened = esc( shortened );
        }
        return '<span class="ellipsis" title="'+esc(d)+'">'+shortened+'&#8230;</span>';
    };
    };
});

// RESTULS PAGE COMPACT
var results_page_compact = (function () {

    // add classes to specific columns
    $(document).ready(function() {
        $('table.display').DataTable({
            "columnDefs": [{ className: "dt-nowrap", "targets": [ 1 ] }],
            "autoWidth": false,
            "columns": [
                { "width": "5%" },
                { "width": "10%" },
                { "width": "65%" },
                { "width": "10%" },
                { "width": "10%" }
          ]
      } );
    } );
});


// RESTULS PAGE COMPREHENSIVE
var results_page_comprehensive = (function () {

    // add classes to specific columns
    $(document).ready(function() {
        $('table.display').DataTable({
            "autoWidth": true,
            dom: 'Bfrtip',
            buttons: ['colvis'],
            "columnDefs": [
                { targets: '_all', render: $.fn.dataTable.render.ellipsis( 30, true ) }]
      } );
    } );
});





// var toggle_ellipsis = (function(element) {
//         $(element).toggleClass("ellipsis")
// });

var submit_form = (function(form_id, action) {
    var form = $("#" + form_id);
    form.attr("action", action);
    form.submit();
});

//
// function SelectElement(id, valueToSelect)
// {
//     var element = document.getElementById(id);
//     element.value = valueToSelect;
// }

//// for debug purposes to see stuff in "console" when inspecting in browser
// alert('WOW!');
// console.log(tables);


    // $('#table_etype').dataTable( {
    //   "columnDefs": [
    //     { "width": "80%", "targets": 0 }
    //   ]
    // } );
//     var table = $('#display').DataTable({
//     autoWidth: false,
//     columns : [
//         { width : '50px' },
//         { width : '50px' },
//         { width : '50px' },
//         { width : '50px' },
//         { width : '50px' },
//         { width : '50px' }
//     ]
// });

