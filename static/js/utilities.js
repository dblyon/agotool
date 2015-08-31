// ENRICHMENT PAGE
var enrichment_page = (function() {
// hide GO-term specific options if UniProt-keywords selected
    $('#gocat_upk').change(function() {
        var gocat_upk = $('#gocat_upk').val();
        var choice = gocat_upk == "UPK";
        toggle_if(choice, ".GOT", ".GOT_placeholder");
    });
    $("#gocat_upk").change();

// hide 'alpha' parameter if BH selected
    $('#multitest_method').change(function() {
        var multitest_method = $('#multitest_method').val();
        var choice = multitest_method == "benjamini_hochberg" || multitest_method == "bonferroni";
        toggle_if(choice, ".alpha", ".alpha_placeholder");
    });
    $("#multitest_method").change();

// hide decimal delimiter and number of bins if abcorr deselected
    $("#abcorr").change(function() {
        var abcorr = $("#abcorr:checked").val();
        var choice = abcorr != "y";
        toggle_if(choice, ".number", ".number_placeholder");
    });
    $("#abcorr").change();
});


// show or hide selectors/tags depending on choice
var toggle_if = function(choice, tag, placeholder_tag){
    if (choice == true) {
        $(tag).hide();
        //$(placeholder_tag).show();
    } else {
        $(tag).show();
        //$(placeholder_tag).hide();
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
        paging: false
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



