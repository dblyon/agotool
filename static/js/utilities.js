// ENRICHMENT PAGE
var enrichment_page = (function() {
// hide GO-term specific options if UniProt-keywords selected
    $("#copy_paste_field textarea").keypress(function (event) {
        $("#userinput_file").filestyle('clear');
    });

    $("#clear_button").click(function (event) {
        $('#foreground_textarea').val('');
        $('#background_textarea').val('');
        $("#userinput_file").filestyle('clear');
    });

    $('#gocat_upk').change(function() {
        var gocat_upk = $('#gocat_upk').val();
        var choice = gocat_upk == "UPK";
        toggle_if(choice, ".GOT", ".GOT_placeholder");


        //// hide organimss
        //if (choice) { // UPK selected
        //    $('.go_term').hide();
        //    $('.up_keyword').show();
        //} else {
        //    var selected = $('#organism').val();
        //    var selected_cass = $('#organism option[value="' + selected + '"]').prop('class');
        //    if (selected_cass == "up_keyword") {
        //         $('#organism').val('');
        //    }
        //    $('.up_keyword').hide();
        //    $('.go_term').show();
        //}

    });
    $("#gocat_upk").change(); // fire event to hide stuff

// hide 'alpha' parameter if BH selected
    $('#multitest_method').change(function() {
        var multitest_method = $('#multitest_method').val();
        var choice = multitest_method == "benjamini_hochberg" || multitest_method == "bonferroni";
        toggle_if(choice, ".alpha", ".alpha_placeholder");
    });
    $("#multitest_method").change();

// show 'foreground_n and background_n boxes' if "compare_groups" selected
    $('#enrichment_method').change(function() {
        var enrichment_method = $('#enrichment_method').val();
        var choice = enrichment_method != "compare_groups";
        toggle_if(choice, ".foreground_n_background_n", "");
    });
    $("#enrichment_method").change();


// hide decimal delimiter and number of bins if abcorr deselected
    $("#abcorr").change(function() {
        var abcorr = $("#abcorr:checked").val();
        var choice = abcorr != "y";
        toggle_if(choice, ".number", ".number_placeholder");
    });
    $("#abcorr").change();
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
// hide Filter button if "UPK" == "GOT"
    var gocat_upk = $('input[name=gocat_upk]').val();
    if (gocat_upk == "UPK") {
        $('#submit_filter').parents(".row").hide();
    }

    $('#table_id').DataTable({
        paging: true
    });

    $("tbody > tr").hover(
        // hover over
        function () {
            $(this).children().css("background-color", "#FFA500");
        },
        // hover out
        function () {
            $(this).children().css("background-color", "");
        }

    );


});

//var function_name = (function () {
//
//});

var toggle_ellipsis = (function(element) {
        $(element).toggleClass("ellipsis")
});


var submit_form = (function(form_id, action) {
    var form = $("#" + form_id);
    form.attr("action", action);
    form.submit();
});



