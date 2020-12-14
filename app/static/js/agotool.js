// ENRICHMENT PAGE
var enrichment_page = (function() {
// hide GO-term specific options if UniProt-keywords selected
//     $("#copy_paste_field textarea").keypress(function (event) {
//         $("#userinput_file").filestyle('clear');
//     });
//
//     $("#clear_button").click(function (event) {
//         $('#foreground_textarea').val('');
//         $('#background_textarea').val('');
//         $("#userinput_file").filestyle('clear');
//         $("#p_value_cutoff").value("0.999");
//         $("#p_value_cutoff").val("0.01");
//     });
        // $("#enrichment_method").val("compare_samples");
        // SelectElement("enrichment_method", "compare_samples");

// $('#gocat_upk').change(function() {
    //     var gocat_upk = $('#gocat_upk').val();
    //     var choice = gocat_upk == "UPK";
    //     toggle_if(choice, ".GOT", ".GOT_placeholder");
    // });
    // $("#gocat_upk").change(); // fire event to hide stuff

// // show 'foreground_n and background_n boxes' if "compare_groups" selected
//     $('#enrichment_method').change(function() {
//         var enrichment_method = $('#enrichment_method').val();
//         var choice = enrichment_method != "compare_groups";
//         toggle_if(choice, ".foreground_n_background_n", "");
//     });
//     $("#enrichment_method").change();

// show foreground_replicates and background_n only when "compare_groups" is selected  --> deprecated method
//     $('#enrichment_method').change(function() {
//         var enrichment_method = $('#enrichment_method').val();
//         var choice = enrichment_method != "compare_groups";
//         toggle_if(choice, ".foreground_replicates", "");
//     });
//     $("#enrichment_method").change();


// hide NCBI TaxID if "genome" deselected
// $('#enrichment_method').change(function() {
//     let enrichment_method = $('#enrichment_method').val();
//     let choice = enrichment_method != "genome";
//     toggle_if(choice, ".taxid", "");
// });
// $("#enrichment_method").change();

// hide "Filter redundant parent terms" if characterize_foreground is selected
// hide p_values if "characterize_foreground" selected
// $('#enrichment_method').change(function() {
//     let enrichment_method = $('#enrichment_method').val();
//     let choice = enrichment_method == "characterize_foreground";
//     if (choice === true) {
//         document.getElementById("filter_foreground_count_one").checked = false;
//     };
//     toggle_if(choice, ".filter_parents", "");
//     toggle_if(choice, ".p_value", "");
// });
// $("#enrichment_method").change();

// try single method to change everything dependent on enrichment_method
$('#enrichment_method').change(function() {
        let enrichment_method = $('#enrichment_method').val();
        let choice = enrichment_method !== "genome";
        toggle_if(choice, ".taxid", "");

        choice = enrichment_method === "characterize_foreground";
        // if (choice === true) {
        //     document.getElementById("filter_foreground_count_one").checked = false;
        // }

        toggle_if(choice, ".filter_parents", "");
        toggle_if(choice, ".p_value", "");
    });
$("#enrichment_method").change();

// old code pertinent for "characterize_foreground
// // show score_cutoff only when "characterize_foreground" is selected
//     $('#enrichment_method').change(function() {
//         var enrichment_method = $('#enrichment_method').val();
//         var choice = enrichment_method !== "characterize_foreground";
//         toggle_if(choice, ".score_cutoff", "");
//     });
//     $("#enrichment_method").change();
//
// // deselect "Filter foreground count one" when characterize foreground is selected
//     var enrichment_method = $('#enrichment_method').val();
//     var choice = enrichment_method === "characterize_foreground";
//     if (choice === true) {
//       document.getElementById("filter_foreground_count_one").checked = false;
//     };
//
// // hide "Filter redundant parent terms" if characterize_foreground is selected
//     $('#enrichment_method').change(function() {
//         var enrichment_method = $('#enrichment_method').val();
//         var choice = enrichment_method == "characterize_foreground";
//         toggle_if(choice, ".filter_parents", "");
//     });
//     $("#enrichment_method").change();
//
//
// // hide p_values if "characterize_foreground" selected
//     $('#enrichment_method').change(function() {
//         var enrichment_method = $('#enrichment_method').val();
//         var choice = enrichment_method === "characterize_foreground";
//         toggle_if(choice, ".p_value", "");
//     });
//     $("#enrichment_method").change();



// show score_cutoff only when "characterize_foreground" is selected --> deprecated
//     $('#enrichment_method').change(function() {
//         var enrichment_method = $('#enrichment_method').val();
//         var choice = enrichment_method !== "characterize_foreground";
//         toggle_if(choice, ".score_cutoff", "");
//     });
//     $("#enrichment_method").change();

// deselect "Filter foreground count one" when characterize foreground is selected
//     var enrichment_method = $('#enrichment_method').val();
//     var choice = enrichment_method === "characterize_foreground";
//     if (choice === true) {
//       document.getElementById("filter_foreground_count_one").checked = false;
//     };

// Hide example_description, show only when an example is selected
let example_status = document.getElementsByClassName('example_status')[0].getAttribute("value");
let hide_true = example_status === "example_None";
if (hide_true === true) {
    document.getElementsByClassName('example_status')[0].setAttribute("style", "display: none;");
}
//     document.getElementsByClassName('example_status').value="newValue_DBL"; --> where can I see this value in the HMTL ???
//     document.getElementsByClassName('example_status').bubu="this doesn't make sense";
});

// show or hide selectors/tags depending on choice
let toggle_if = function(choice, tag){
    if (choice === true) {
        $(tag).hide();
    } else {
        $(tag).show();
    }
};

// enrichment page
let submit_form = (function(form_id, action) {
    let form = $("#" + form_id);
    form.attr("action", action);
    form.submit();
});

// RESTULS PAGE
var results_page = (function () {

    // // Hide table if number of number of rows == 0
    // var tables = document.getElementsByClassName('div_table_etype');
    // for (i=0; i< tables.length; i++) {
    //     var table = tables[i];
    //     var attr = table.getAttribute('data-value');
    //     if (attr == 0) {
    //         table.style.display = 'none';
    //     }
    // }

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

// RESULTS PAGE COMPACT
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
                { "width": "10%" }]
      } );
    } );
});

// RESULTS PAGE COMPREHENSIVE
var results_page_comprehensive = (function () {
    // add classes to specific columns
    $(document).ready(function() {
        $('table.display').DataTable({
            "autoWidth": true,
            dom: 'Bfrtip',
            buttons: ['colvis'],
            "columnDefs": [
                { targets: '_all', render: $.fn.dataTable.render.ellipsis( 60, true ) }]
      });
    });
});

// RESULTS PAGE PLOTLY
let results_page_plotly = (function () {

    $(function () {
        $("[data-toggle='tooltip']").tooltip();
    });

    function get_individual_trace(category_name, dict_of_category) {
            return {'customdata': _.zip(dict_of_category["term"], dict_of_category["description"], dict_of_category["foreground_count"]),
                    'hovertemplate': '<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>',
                    'ids': dict_of_category["term"],
                    'legendgroup': category_name,
                    'marker': {'color': dict_of_category["color"][0],
                        'line': {
                            'color': dict_of_category["marker_line_color"],
                            'width': dict_of_category["marker_line_width"]
                        },
                        'opacity': dict_of_category["opacity"],
                        'size': dict_of_category["foreground_count"],
                        'sizemin': min_marker_size, 'sizemode': 'area', 'sizeref': sizeref, 'symbol': 'circle'
                    },
                    'mode': 'markers+text', 'name': category_name,
                    'text': dict_of_category["text_label"],
                    'textfont': {'size': text_font_size}, 'textposition': 'top right',
                    'x': dict_of_category["logFDR"],
                    'y': dict_of_category["effect_size"],
                    'type': 'scatter'}
        }

    function get_all_traces(dict_per_category) {
        let traces_list_of_arr = [];
        let trace_temp = {};
        for (let category_name in dict_per_category) {
            let dict_of_category = dict_per_category[category_name];
            trace_temp = get_individual_trace(category_name, dict_of_category)
            traces_list_of_arr.push(trace_temp);
        }
        return traces_list_of_arr;
    }

    function get_columns_visible_and_width_formatting(enrichment_method) {
        let cols;
        switch (enrichment_method) {
            case "genome":
            case "abundance_correction":
                //[s_value, term, description, FDR, effect_size, category, over_under, hierarchical_level, year, FG_IDs, FG_count, FG_n, BG_count, BG_n, ratio_in_FG, ratio_in_BG, p_value, logFDR, rank]
                cols = [
                    {"visible": true, "width": "80px"}, // s value
                    {"visible": true, "width": "100px"}, // term
                    {"visible": true, "width": "200px"}, // description
                    {"visible": true}, // FDR
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},];
                break;
            case "compare_samples":
                //[s_value, term, description, FDR, effect_size, category, over_under, hierarchical_level, year, FG_IDs, BG_IDs, FG_count, FG_n, BG_count, BG_n, ratio_in_FG, ratio_in_BG, p_value, logFDR, rank]
                cols = [
                    {"visible": true, "width": "80px"}, // s value
                    {"visible": true, "width": "100px"}, // term
                    {"visible": true, "width": "200px"}, // description
                    {"visible": true}, // FDR
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},];
                break;
            case "characterize_foreground":
                // [ratio_in_FG, term, description, category, hierarchical_level, year, FG_IDs, FG_count, FG_n, rank]
                cols = [
                    {"visible": true, "width": "80px"}, // ratio_in_FG
                    {"visible": true, "width": "100px"}, // term
                    {"visible": true, "width": "200px"}, // description
                    {"visible": true}, // category
                    {"visible": false},
                    {"visible": false},
                    {"visible": false},
                    {"visible": true},
                    {"visible": false},
                    {"visible": false},];
                break;
            default:
                cols = [];
        }
        return cols
    }

    function get_order_formatting(enrichment_method) {
        let order;
        switch (enrichment_method) {
            case "genome":
            case "abundance_correction":
                order = [[5, "desc"], [18, "asc"]]; // ["category", "rank"]
                break;
            case "compare_samples":
                order = [[5, "desc"], [19, "asc"]]; // ["category", "rank"]
                break;
            case "characterize_foreground":
                order = [[3, "desc"], [0, "desc"]]; // ["category", "ratio_in_FG"]
                break;
            default:
                order = [];
        }
        return order
    }




    // add classes to specific columns
    $(document).ready(function() {
        let table_dbl = $('table.display').DataTable({
            /* SCROLLING */
            scrollY: "500px",
            scrollCollapse: true,
            paging: false,
            scrollX: true,
            "language": {
                "info": "Showing _TOTAL_ entries",
                "infoFiltered": "(filtered from _MAX_ total entries)",
            },
            dom: 'Bfrtip',
            buttons: ['colvis'],
            // buttons: ['colvis', 'copy', 'excel', 'pdf'],
            "columnDefs": [{targets: '_all', render: $.fn.dataTable.render.ellipsis(80, true)}],
            responsive: true,
            select: {style: 'multi'},
            "order": get_order_formatting(enrichment_method),
            "autoWidth": false,
            "columns": get_columns_visible_and_width_formatting(enrichment_method),
        });

        let selected_indices_set = new Set();
        table_dbl.on('select', function (e, dt, type, indexes) {
            if (type === 'row') {
                let selected_term = table_dbl.rows(indexes).data()[0][1];
                selected_indices_set.add(selected_term);
                update_scatter_plot(); }
        });
        table_dbl.on('deselect', function (e, dt, type, indexes) {
            if (type === 'row') {
                let deselected_term = table_dbl.rows(indexes).data()[0][1];
                selected_indices_set.delete(deselected_term);
                update_scatter_plot(); }
        });


        function reset_data_dict_per_category(dict_per_category) {
            for (let category_name in dict_per_category) {
                    dict_of_category = dict_per_category[category_name];
                    num_vals = dict_of_category["logFDR"].length;
                    dict_of_category["text_label"] = Array(num_vals).fill("");
                    dict_of_category["marker_line_color"] = Array(num_vals).fill(marker_line_color_default);
                    dict_of_category["marker_line_width"] = Array(num_vals).fill(marker_line_width_default);
                    dict_of_category["opacity"] = Array(num_vals).fill(opacity_default);
                }
        }

        function redraw_original_plot() {
            reset_data_dict_per_category(dict_per_category);
            Plotly.newPlot('plotly_scatter_plot', get_all_traces(dict_per_category), plot_layout_orig, plot_config);
        }

        let toggle_point_edges_button = $("#toggle_point_edges_id")

        let toggle_point_labels_button = $("#toggle_point_labels_id")

        toggle_point_edges_button.on('change', function () {
            if (toggle_point_edges_button.is(':checked')) {
                update_scatter_plot();
            } else {
                update_scatter_plot();
            }
        });

        toggle_point_labels_button.on('change', function () {
            if (toggle_point_labels_button.is(':checked')) {
                update_scatter_plot();
            } else {
                update_scatter_plot();
            }
        });

        $("#dbl_reset_button_id").click(function () {

            if (toggle_point_edges_button.is(':checked')) {
            } else {
                toggle_point_edges_button.bootstrapToggle('on');
            }

            if (toggle_point_labels_button.is(':checked')) {
            } else {
                toggle_point_labels_button.bootstrapToggle('on');
            }

            selected_indices_set.clear();
            table_dbl.$('tr.selected').removeClass('selected');
            redraw_original_plot();
        });

        let edges_plotted = false;
        let traces_for_modified_plot = [];
        let index_position = undefined;
        let trace_temp = {};
        let category_name;
        let dict_of_category;
        let num_vals;
        let edges;
        let edge_name;

        // DIY plot everything from scratch
        function update_scatter_plot() {
            if (selected_indices_set.size > 0) {
                // clear all traces
                traces_for_modified_plot = [];
                edges_plotted = false;
                reset_data_dict_per_category(dict_per_category);
                // add edges
                if (toggle_point_edges_button.is(':checked')) {
                    trace_for_edges_template["x"] = [];
                    trace_for_edges_template["y"] = [];
                    // trace_for_edges_template["marker"]["line"]["width"] = [];
                    for (let term_name of selected_indices_set) {
                        edges = term_2_edges_dict_json[term_name];
                        category_name = term_2_category_dict[term_name];
                        dict_of_category = dict_per_category[category_name];
                        index_position = term_2_positionInArr_dict[term_name];
                        dict_of_category["opacity"][index_position] = opacity_highlight;
                        // if edges exists
                        if (typeof edges !== "undefined") {
                            trace_for_edges_template["x"] = trace_for_edges_template["x"].concat(edges["X_points"]);
                            trace_for_edges_template["y"] = trace_for_edges_template["y"].concat(edges["Y_points"]);
                            // trace_for_edges_template["marker"]["line"]["width"] = trace_for_edges_template["marker"]["line"]["width"].concat(edges["Weights"]);
                            let i=0;
                            while (edges["Nodes"].length > i) {
                                edge_name = edges["Nodes"][i];
                                index_position = term_2_positionInArr_dict[edge_name];
                                dict_of_category["opacity"][index_position] = opacity_highlight;
                                i++;
                            }

                        } else {
                            // pass if no edges
                        }
                    }

                    if (trace_for_edges_template["x"].length > 0) {
                        edges_plotted = true;
                        traces_for_modified_plot.push(trace_for_edges_template)
                    } else {
                        // edges ON but empty (no edges available)
                    }

                } else {
                    // edges OFF, pass
                    // reset to default values
                    for (let category_name in dict_per_category) {
                        dict_of_category = dict_per_category[category_name];
                        num_vals = dict_of_category["logFDR"].length;
                        dict_of_category["opacity"] = Array(num_vals).fill(opacity_default);
                    }
                }

                if (toggle_point_labels_button.is(':checked')) {
                    for (let term_name of selected_indices_set) {
                        category_name = term_2_category_dict[term_name];
                        dict_of_category = dict_per_category[category_name];
                        num_vals = dict_of_category["logFDR"].length;
                        index_position = term_2_positionInArr_dict[term_name];
                        dict_of_category["text_label"][index_position] = term_name;
                        dict_of_category["marker_line_color"][index_position] = marker_line_color_highlight;
                        dict_of_category["marker_line_width"][index_position] = marker_line_width_highlight;
                        dict_of_category["opacity"][index_position] = opacity_highlight;
                    }

                    // xaxis_range=[x_min * 0.93, x_max * 1.07], yaxis_range=[y_min * 1.25, y_max * 1.25]

                } else {
                    // reset labels, but highlight with less opacity and line around point
                    for (let term_name of selected_indices_set) {
                        category_name = term_2_category_dict[term_name];
                        dict_of_category = dict_per_category[category_name];
                        index_position = term_2_positionInArr_dict[term_name];
                        dict_of_category["marker_line_color"][index_position] = marker_line_color_highlight;
                        dict_of_category["marker_line_width"][index_position] = marker_line_width_highlight;
                        dict_of_category["opacity"][index_position] = opacity_highlight;
                    }
                }

                for (let category_name in dict_per_category) {
                    dict_of_category = dict_per_category[category_name];
                    trace_temp = get_individual_trace(category_name, dict_of_category)
                    traces_for_modified_plot.push(trace_temp);
                }
                Plotly.newPlot('plotly_scatter_plot', traces_for_modified_plot, plot_layout_orig, plot_config);
            } else {
                redraw_original_plot();
            }
        }

    })
});

// Bugs
// - draw edges then hide a trace --> edges persist

// ToDo
// - Plot deselect trace in legend --> filter in table ?
// - select point in plot --> highlight in table
// - reset --> activate buttons

