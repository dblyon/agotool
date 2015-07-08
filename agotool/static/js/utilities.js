///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
var enrichment_page = (function() {

// hide GO-term specific options if UniProt-keywords selected
    $('#gocat_upk').change(function() {
        var gocat_upk = $('#gocat_upk').val();
        if (gocat_upk == "UPK"){
            $(".GOT").hide(".GOT");
        }

        else {
            $(".GOT").show(".GOT");
        }
    });
    $("#gocat_upk").change();

// hide 'alpha' parameter if BH selected
    $('#multitest_method').change(function() {
        var multitest_method = $('#multitest_method').val();
        choice = multitest_method == "benjamini_hochberg" || multitest_method == "bonferroni" ;
        toggle_if(".alpha", choice);
        //if (multitest_method == "benjamini_hochberg" || multitest_method == "bonferroni" ){
        //    $(".alpha").hide(".alpha");
        //}
        //else {
        //    $(".alpha").show(".alpha");
        //}
    });
    $("#multitest_method").change();

// hide decimal delimiter and number of bins if abcorr deselected
    $("#abcorr").change(function() {
        var abcorr = $("#abcorr").val();
        if (abcorr == false){
            $(".number").hide(".number");
        }
        else {
            $(".number").show(".number");
        }
    });
    $("#abcorr").change();

});
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////


var toggle_if = function(select, choice){
    if (choice == true) {
        $(select).hide();
    } else {
        $(select).show();
    }
x}






///////////////////////////////////////////////////////////////////////////////
// global variables
///////////////////////////////////////////////////////////////////////////////

//var model_organism_name_to_id;
//var model_organism_id_to_name = {};
//
//var level_to_ids;
//
//var organism_levels_name_to_id;
//var levels_id_to_name = {};
//
//var default_organism;
//var default_level;
//var default_levels;
//
//var is_selected = {};

///////////////////////////////////////////////////////////////////////////////
// EVERYTHING
///////////////////////////////////////////////////////////////////////////////
var load_activation_loop_page = (function(page_type) {
    ///////////////////////////////////////////////////////////////////////////////
    // EVENTS
    ///////////////////////////////////////////////////////////////////////////////
    // enter sites -> clear file
    $("#sites").keypress(function (event) {
        $("#input_file").filestyle('clear')
    });

    // upload file -> clear site text area
    $('site_file').click(function (event) {
        $("input_textarea").val('')
    });

    $("#clear_button").click(function (event) {
        $('#input_textarea').val('');
    });

    $("#example_button").click( function() {
        $('#input_textarea').val($('#example_data').val());
    });
    if (page_type == "peptides") {

    }
});


//var reverse_dict = function (dict) {
//    var new_dict = {};
//    $.each(dict, function(key, value) {
//        new_dict[value] = key
//    });
//   return new_dict;
//};
//
//var parse_organism_json = function(data) {
//    // load data from json
//    level_to_ids = data.level_to_ids;
//
//    model_organism_name_to_id = data.model_organism_name_to_ids;
//    model_organism_id_to_name = reverse_dict(model_organism_name_to_id);
//
//    organism_levels_name_to_id = data.organism_levels;
//    // Jans suggestion
//    /*
//    $.each(organism_levels_name_to_id, function(organism, tax_dict) {
//        organism_levels_id_to_name[organism] = reverse_dict(tax_dict);
//    });
//    */
//    // XiaoYongs suggestion
//    $.each(organism_levels_name_to_id, function(organism, tax_dict) {
//        $.each(tax_dict, function(key, value) {
//            levels_id_to_name[value] = key;
//        });
//    });
//};
//
//var update_select_options = function(all_options, default_option, target) {
//    target.empty();
//    $.each(all_options, function(text, key) {
//        if (text == default_option){
//            var option = new Option(text, key, true, true);
//        }
//        else {
//            var option = new Option(text, key);
//        }
//        target.append($(option));
//    });
//};
//
//var update_multiselect_options = function() {
//
//    //var species = level_to_ids[level];
//    var species = level_to_ids[$("#select_taxlevel option:selected").text()];
//    //$("#select_taxlevel").val()
//
//    var right_organisms = $("select.right_organisms").empty();
//    var left_organisms = $("select.left_organisms").empty();
//    var model_organism = $("#select_organism").val() //needs fixed
//    var i = 0;
//    $.each(species, function(key, text) {
//        // str is equal to int when using '==' but not when using '==='
//        if (model_organism != text[0]) {
//            var option = '<option value="'+ text[0] + '" name="'+ i + '">' + text[1] +'</option>'
//            if (is_selected[i]) {
//                left_organisms.append(option);
//            } else {
//                right_organisms.append(option);
//
//            }
//        }
//        i += 1;
//    });
//};
//
//var get_new_is_selected = function(level) {
//    //var ids = level_to_ids[level];
//    var l = level_to_ids[level].length;
//    is_selected = new Array(l);
//    for (var i=0; i < l; i++) {
//        is_selected[i] = true;
//    }
//    return is_selected
//};
//
//// event functions
//var change_organism = function() {
//    organism = model_organism_id_to_name[$("#select_organism").val()];
//    update_select_options(organism_levels_name_to_id[organism], default_level, $("#select_taxlevel"));
//    change_taxlevel();
//};
//
//
//var change_taxlevel = function() {
//    level_name = levels_id_to_name[$("#select_taxlevel").val()];
//    is_selected = get_new_is_selected(level_name);
//    update_multiselect_options();
//};
//
//
//var move_organism_left = function() {
//    var selectedItem = $("select.right_organisms option:selected");
//    for (var i = 0; i < selectedItem.length; i++) {
//        is_selected[selectedItem[i].attributes.name.value] = true;
//    }
//    update_multiselect_options();
//};
//
//var move_organism_right = function() {
//    var selectedItem = $("select.left_organisms option:selected");
//    for (var i = 0; i < selectedItem.length; i++) {
//        is_selected[selectedItem[i].attributes.name.value] = false;
//    }
//    update_multiselect_options();
//};
//
//var submit_species = function() {
//    var species = level_to_ids[$("#select_taxlevel option:selected").text()];
//    var hidden_tags = $("#hidden_tag");
//    var model_organism = $("#select_organism").val() //needs fixed
//    var i = 0;
//    var selected = [];
//    var n_unselected = 0;
//    $.each(species, function(key, text) {
//        if (model_organism != text[0]) {
//            if (is_selected[i]) {
//                selected.push(text[0]);
//            } else {
//                n_unselected += 1;
//            }
//        }
//        i += 1;
//    });
//    if (n_unselected !== 0) {
//        hidden_tags.append('<input type="hidden" name="--compare_tax_ids"' + 'value="' + selected.join(',') + '"><input>');
//    }
//    hidden_tags.hide();
//};

var check_position = function(position, position_file, comparison){
        alert_str = "";
        position = position.trim();
	if (position == "" && position_file == ""){
		alert_str = alert_str + "Insert or upload a tab separated list of sequence IDs and positions for the PTMs" + comparison + "!\n";
	    }
	    if (position != ""){
	       var split_res = position.split(/\s+/);
	       if (split_res.length <2){
		   alert_str = alert_str + "Input position at least have protein ID and residue position" + comparison + "!\n";
		}
	    }
	    if (position != "" && position_file != ""){
		alert_str = alert_str + "cannot input position and upload position file together, please remove one of them!" + comparison + "!\n";

	    } 
         if (position != "" && position_file != ""){
                alert_str = alert_str + "Cannot input position and upload position file together, please remove one of them" + comparison + "!\n"; 
	 }  
         return alert_str;

};

var check_sequence = function(sequence, sequence_file){
    var alert_str = "";
    sequence = sequence.trim();
    if (sequence != ""){
        /*split_seq = sequence.split('\n');
        if (split_seq.length < 2){
           alert_str = alert_str + "Input sequence should be fasta format!\n";
        } else if (split_seq[0][0] != '>'){
            alert_str = alert_str + "Input sequence must be fasta format with prefix >\n";
        } else if (split_seq[0] <2) {
            alert_str = alert_str + "Input sequence must have protein ID after prefix >\n";
        }*/
        var split_seq = sequence.match(/>[\w\d]+.*\n\w+/);
        if (split_seq == null){
	    alert_str = alert_str + "Input sequence should be fasta format!\n";
        }
    } else {
    	if (sequence_file == ""){
	    alert_str = alert_str + "Please Insert or upload FASTA sequences!\n";
	}
    }
    
    if (sequence != "" && sequence_file != ""){
        alert_str = alert_str + "Cannot input sequence and upload sequence file together, please remove one of them!\n";
    }
    return alert_str;
};

var check_input = function() {
    var alert_str = "";
    var sequence =  $("#sequence_row textarea").val();
    var sequence_file = $("#sequence_row :file").val();
    alert_str = alert_str + check_sequence(sequence, sequence_file);

    var position =  $("#position_original textarea").val();
    var position_file = $("#position_original :file").val();
    alert_str = alert_str + check_position(position, position_file, "");

    var compared_position =  $("#positions_compared textarea").val();
    //console.log(compared_position != null);
    if (compared_position != null){
        //console.log("comparison");
        var compared_position_file = $("#positions_compared :file").val();
        alert_str = alert_str + check_position(compared_position, compared_position_file, " in comparison");
    }

    if (alert_str !== "") {
        alert(alert_str); 
        return false;
    }
   
    return true;
};

//var reset_input = function() {
//    default_organism = "Homo sapiens";
//    // Eukaryotes should be default!, but some anonomus guy has the worlds oldest computer
//    // so he cannot generate or store this file :D
//    //default_level = "Eukaryotes";
//    default_level = "Mammals";
//    default_levels = organism_levels_name_to_id[default_organism];
//
//    update_select_options(model_organism_name_to_id, default_organism, $("#select_organism"));
//    update_select_options(default_levels, default_level, $("#select_taxlevel"));
//
//    is_selected = get_new_is_selected(default_level);
//    update_multiselect_options();
//
//}
///////////////////////////////////////////////////////////////////////////////
// load everythin
///////////////////////////////////////////////////////////////////////////////
//var load_input_page_data = (function() {
//    // load organism json
//    $.getJSON('static/data/organisms.json', function (data) {
//        parse_organism_json(data);
//        reset_input();
//    });
//    ///////////////////////////////////////////////////////////////////////////////
//    // bind functions
//    ///////////////////////////////////////////////////////////////////////////////
//    // taxonomy events
//    $('#select_organism').change(function() {
//        change_organism();
//    });
//
//    $('#select_taxlevel').change(function() {
//        change_taxlevel();
//    });
//
//
//    $("input.right_organisms").click(function () {
//        move_organism_right();
//    });
//
//    $("input.left_organisms").click(function () {
//        move_organism_left();
//    });
//
//    // binds click events to all clear and upload file buttons
//    var tmp_items = ["#sequence_row", "#position_original", "#positions_compared"];
//    var textareas = [];
//    var files = [];
//    for (var i = 0; i < tmp_items.length; i++) {
//        var _button = $(tmp_items[i] + " button");
//        var _file = $(tmp_items[i] + " :file");
//        var _textarea = $(tmp_items[i] + " textarea");
//        files.push(_file);
//        textareas.push(_textarea);
//        // clear file and insert fasta when clear is pressed
////        _button.click({_file : _file, _textarea : _textarea}, function (event) {
////            event.data._file.filestyle('clear');
////            event.data._textarea.val('');
////        });
//        // clear text area when the user selects a file
//        _file.click({_textarea : _textarea }, function(event) {
//            event.data._textarea.val('');
//        });
//        _textarea.keypress({_file : _file }, function(event) {
//            //event.data._textarea.val('');
//            event.data._file.filestyle('clear');
//            //event.data._input_field.val('');
//
//        });
//
//    }

    // submit clear and examples
//    $("#submit_button").click(function () {
//        submit_species();
//        var validate = check_input();
//        if (validate){
//            $("#main_form").submit();
//        }
//    });
//
//    $("#clear_button").click({textareas : textareas, files : files}, function (event) {
//        reset_input();
//        for (var i=0; event.data.textareas.length; i++) {
////            console.log(event.data.textareas[i]);
//            event.data.textareas[i].val('');
//            event.data.files[i].filestyle('clear');
//        }
//    });
//
//    $("#sample_data").click( function() {
//        reset_input();
//        $("#sequence_row textarea").val($("#example_seq").text());
//        $("#position_original textarea").val($("#example_original_sites").text());
//        $("#positions_compared textarea").val($("#example_comparison_sites").text());
//    });
//
//    $("#motif_choice select").change( function() {
//        $("#motif_choice input").val($("#motif_choice option:selected").val())
//    });
//
//    $("#advanced_header").click(function () {
//        toggle($("#advanced_header"), $("#advanced_options"));
//    });
//
//});

var toggle = function(button, target) {
    if (button.hasClass("glyphicon-chevron-down")) {
        button.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-right");
    } else if (button.hasClass("glyphicon-chevron-right")) {
        button.removeClass("glyphicon-chevron-right").addClass("glyphicon-chevron-down");
    }
    target.toggle();
};

//$(this).find(".toggle_arrow").removeClass("glyphicon text-primary glyphicon-chevron-right");

