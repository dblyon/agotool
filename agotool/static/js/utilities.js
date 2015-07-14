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
        $(placeholder_tag).show();
    } else {
        $(tag).show();
        $(placeholder_tag).hide();
    }

};





