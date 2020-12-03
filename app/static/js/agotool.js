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



// show score_cutoff only when "characterize_foreground" is selected
    $('#enrichment_method').change(function() {
        var enrichment_method = $('#enrichment_method').val();
        var choice = enrichment_method !== "characterize_foreground";
        toggle_if(choice, ".score_cutoff", "");
    });
    $("#enrichment_method").change();

// deselect "Filter foreground count one" when characterize foreground is selected
//     var enrichment_method = $('#enrichment_method').val();
//     var choice = enrichment_method === "characterize_foreground";
//     if (choice === true) {
//       document.getElementById("filter_foreground_count_one").checked = false;
//     };

// hide "Filter redundant parent terms" if characterize_foreground is selected
// hide p_values if "characterize_foreground" selected
    $('#enrichment_method').change(function() {
        var enrichment_method = $('#enrichment_method').val();
        var choice = enrichment_method == "characterize_foreground";
        if (choice === true) {
            document.getElementById("filter_foreground_count_one").checked = false;
        };
        toggle_if(choice, ".filter_parents", "");
        toggle_if(choice, ".p_value", "");
    });
    $("#enrichment_method").change();

// Hide example_description, show only when an example is selected
    var example_status = document.getElementsByClassName('example_status')[0].getAttribute("value");
    var hide_true = example_status == "example_None";
    if (hide_true == true) {
        document.getElementsByClassName('example_status')[0].setAttribute("style", "display: none;");
    };
//     document.getElementsByClassName('example_status').value="newValue_DBL"; --> where can I see this value in the HMTL ???
//     document.getElementsByClassName('example_status').bubu="this doesn't make sense";
});

// show or hide selectors/tags depending on choice
var toggle_if = function(choice, tag){
    if (choice === true) {
        $(tag).hide();
    } else {
        $(tag).show();
    }
};
// enrichment page
var submit_form = (function(form_id, action) {
    var form = $("#" + form_id);
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
            // select: true,
            buttons: ['colvis'],
            // buttons: ['colvis', 'copy', 'excel', 'pdf'],
            "columnDefs": [{targets: '_all', render: $.fn.dataTable.render.ellipsis(80, true)}],
            responsive: true,

            // select multiple rows (via dataTables.select.min.js
            select: {style: 'multi'},
            "order": [[7, "desc"], [18, "asc"]], // ["category", "rank"]
            "autoWidth": false,
            "columns": [
                {"visible": true, "width": "80px"}, // s value
                {"visible": true, "width": "100px"}, // term
                {"visible": true, "width": "200px"}, // description
                {"visible": true}, // FDR
                {"visible": false}, // p value
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
                {"visible": false},
                {"visible": false},
                {"visible": false},
                {"visible": false},
                {"visible": false}, ],
        });


        let selected_indices_set = new Set();

        table_dbl.on('select', function (e, dt, type, indexes) {
            if (type === 'row') {
                // console.log("on select")
                // console.log(table_dbl.rows());
                // console.log(indexes);
                // let row_ids = table_dbl.rows( indexes ).data().pluck( 'id' );

                // do something with the ID of the selected items
                // console.log("row_ids will be printed to console.log");
                // console.log(table_dbl.rows( indexes ).data()[0]);
                let selected_term = table_dbl.rows(indexes).data()[0][1];
                selected_indices_set.add(selected_term);
                // console.log("select: ", selected_term);
                // console.log("selected_indices_set: ", selected_indices_set);
                // update_scatter_plot(selected_indices_set);
                update_scatter_plot();
            }
        });

        table_dbl.on('deselect', function (e, dt, type, indexes) {
            if (type === 'row') {
                let deselected_term = table_dbl.rows(indexes).data()[0][1];
                selected_indices_set.delete(deselected_term);
                // console.log("deselected: ", deselected_term);
                // console.log("selected_indices_set: ", selected_indices_set);
                // update_scatter_plot(selected_indices_set);
                update_scatter_plot();
            }
        });

        function df_2_traces_orig(dict_per_category) {
            let traces_list_of_arr = [];
            for (let category_name in dict_per_category) {
                let dict_of_category = dict_per_category[category_name];
                // let num_vals = dict_of_category["logFDR"].length;
                let trace_temp = {
                    'customdata': _.zip(dict_of_category["term"], dict_of_category["description"], dict_of_category["FG_count"]),
                    'hovertemplate': '<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>',
                    'ids': dict_of_category["term"],
                    'legendgroup': category_name,
                    'marker': {
                        'color': dict_of_category["color"][0],
                        'line': {
                            'color': dict_of_category["marker_line_color"],
                            'width': dict_of_category["marker_line_width"]
                        },
                        'opacity': dict_of_category["opacity"],
                        'size': dict_of_category["FG_count"],
                        'sizemin': min_marker_size, 'sizemode': 'area', 'sizeref': sizeref, 'symbol': 'circle'
                    },
                    'mode': 'markers+text', 'name': category_name,
                    'text': dict_of_category["text_label"],
                    'textfont': {'size': text_font_size}, 'textposition': 'top right',
                    'x': dict_of_category["logFDR"],
                    'y': dict_of_category["effectSize"],
                    'type': 'scatter'
                }
                traces_list_of_arr.push(trace_temp);
            }
            return traces_list_of_arr;
        }

        function redraw_original_plot() {
            console.log("redrawing the original plot");
            // Plotly.purge("plotly_scatter_plot");
            // Plotly.newPlot('plotly_scatter_plot', get_traces_orig(), plot_layout_orig, plot_config);
            // edges_plotted = false;
            Plotly.newPlot('plotly_scatter_plot', df_2_traces_orig(dict_per_category), plot_layout_orig, plot_config);
        }

        $("#dbl_reset_button_id").click(function (event) {
            redraw_original_plot();
        });

        $("#toggle_point_edges_id").on('change', function () {
            if ($("#toggle_point_edges_id").is(':checked')) {
                // console.log("toggle_point_edges_id checked");
                update_scatter_plot();
            } else {
                // console.log("toggle_point_edges_id UNchecked");
                if (edges_plotted === true) {
                    Plotly.deleteTraces("plotly_scatter_plot", 0);
                    edges_plotted = false;
                }
            }
        });

        $("#toggle_point_labels_id").on('change', function () {
            if ($("#toggle_point_labels_id").is(':checked')) {
                console.log("toggle_point_labels_id checked");
                update_scatter_plot();
            } else {
                console.log("toggle_point_labels_id UNchecked");
                update_scatter_plot();
            }
        });

        let edges_plotted = false;
        let traces_for_modified_plot = [];
        let trace_for_edges = {};
        let line_color_arr = [];
        let line_width_arr = [];
        let text_label_arr = [];
        let index_position = undefined;

        // DIY plot everything from scratch
        function update_scatter_plot() {
            if (selected_indices_set.size > 0) {
                let toggle_point_edges = document.getElementById("toggle_point_edges_id");
                let toggle_point_labels = document.getElementById("toggle_point_labels_id");

                // add edges
                if (toggle_point_edges.checked === true) {
                    let tra
                    trace_for_edges["x"] = [];
                    trace_for_edges["y"] = [];
                    for (let term_name of selected_indices_set) {
                        let edges = term_2_edges_dict_json[term_name];
                        // if edges exists
                        if (typeof edges !== "undefined") {
                            trace_for_edges["x"] = trace_for_edges["x"].concat(edges["X_points"]);
                            trace_for_edges["y"] = trace_for_edges["y"].concat(edges["Y_points"]);
                        } else {
                            // pass
                        }
                    }
                    if (trace_for_edges["x"].length > 0) {
                        traces_for_modified_plot.push(trace_for_edges)
                    } else {
                        // edges ON but empty (no edges available)
                        traces_for_modified_plot = [];
                    }

                } else {
                    // edges OFF, pass
                    traces_for_modified_plot = [];
                }

                for (let category_name in dict_per_category) {
                    let dict_of_category = dict_per_category[category_name];
                    let num_vals = dict_of_category["logFDR"].length;

                    // labels ON
                    // add text label, change color and width of line surrounding points in scatter
                    text_label_arr = Array(num_vals).fill('');
                    line_color_arr = Array(num_vals).fill('white');
                    line_width_arr = Array(num_vals).fill(marker_line_width_default);
                    if (toggle_point_labels.checked === true) {
                        for (let term_name of selected_indices_set) {
                            index_position = term_2_positionInArr_dict[term_name];
                            // if index_position not not definded ?
                            text_label_arr[index_position] = term_name;
                            line_color_arr[index_position] = marker_line_color_highlight;
                            line_width_arr[index_position] = marker_line_width_highlight;
                        }
                    } else {
                        // label OFF, use default values
                    }
                    dict_of_category["text_label"] = text_label_arr;
                    dict_of_category["marker_line_color"] = line_color_arr;
                    dict_of_category["marker_line_width"] = line_width_arr;

                    let trace_temp = {
                        'customdata': _.zip(dict_of_category["term"], dict_of_category["description"], dict_of_category["FG_count"]),
                        'hovertemplate': '<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>',
                        'ids': dict_of_category["term"],
                        'legendgroup': category_name,
                        'marker': {
                            'color': dict_of_category["color"][0],
                            'line': {
                                'color': dict_of_category["marker_line_color"],
                                'width': dict_of_category["marker_line_width"]
                            },
                            'opacity': dict_of_category["opacity"],
                            'size': dict_of_category["FG_count"],
                            'sizemin': min_marker_size, 'sizemode': 'area', 'sizeref': sizeref, 'symbol': 'circle'
                        },
                        'mode': 'markers+text', 'name': category_name,
                        'text': dict_of_category["text_label"],
                        'textfont': {'size': text_font_size}, 'textposition': 'top right',
                        'x': dict_of_category["logFDR"],
                        'y': dict_of_category["effectSize"],
                        'type': 'scatter'
                    }
                    traces_for_modified_plot.push(trace_temp);

                }
                Plotly.newPlot('plotly_scatter_plot', traces_for_modified_plot, plot_layout_orig, plot_config);
            } else {
                // redraw original plot
                console.log("calling redraw_original_plot");
                redraw_original_plot();
            }
        }

    })
});


// function update_scatter_plot_old() {
//             if (selected_indices_set.size > 0) {
//
//                 // add edges
//                 let toggle_point_edges = document.getElementById("toggle_point_edges_id");
//                 if (toggle_point_edges.checked === true) {
//                     // console.log("adding edges");
//                     trace_for_edges["x"] = [];
//                     trace_for_edges["y"] = [];
//                     // remove existing trace
//                     if (edges_plotted === true) {
//                         Plotly.deleteTraces("plotly_scatter_plot", 0);
//                         edges_plotted = false;
//                     }
//                     for (let term_name of selected_indices_set) {
//                         let edges = term_2_edges_dict_json[term_name];
//                         // if edges exists
//                         if (typeof edges !== "undefined") {
//                             trace_for_edges["x"] = trace_for_edges["x"].concat(edges["X_points"]);
//                             trace_for_edges["y"] = trace_for_edges["y"].concat(edges["Y_points"]);
//                         } else {
//                             // pass
//                         }
//                     }
//                     // add one additional trace for all edges and move to the back of the plot
//                     edges_plotted = true;
//                     Plotly.addTraces("plotly_scatter_plot", trace_for_edges);
//                     Plotly.moveTraces("plotly_scatter_plot", -1, 0);
//                 } else {
//                     // edges OFF: remove edges trace if exists
//                     if (edges_plotted === true) {
//                         Plotly.deleteTraces("plotly_scatter_plot", 0);
//                         edges_plotted = false;
//                     }
//                 }
//
//                 // add labels
//                 let toggle_point_labels = document.getElementById("toggle_point_labels_id");
//                 if (toggle_point_labels.checked === true) {
//                     console.log("adding labels");
//                     for (let term_name of selected_indices_set) {
//                         // console.log("label pseudo info: ", term_name);
//                     }
//                     //
//                     // 'text': [ '', 'KW-0472', ''] --> update
//                     // need to remember order of term, term 2 position (in array) mapping
//                     // term_2_trace_dict
//                     // term_2_positionInArr_dict
//
//                     // mode="markers+text",
//
//                     // Plotly.update("plotly_scatter_plot", data_update, layout_update, [trace_index_1, trace_index_2]);
//                 } else {
//                     // only change outer circle highlighting
//                     console.log("add circle to highlight")
//                     for (let term_name of selected_indices_set) {
//                         // group terms by category --> ?
//                         // for every term get index of arr (term_2_positionInArr_dict)
//                         // set values for color and width
//                         // update plot
//                     }
//                     //marker_line_width=group[marker_line_width], marker_line_color=group[marker_line_color]
//                     let data_update = {
//                         'line': {
//                             'color': ['white', '#43464B', 'white'],
//                             'width': [1, 3, 1]
//                         }
//                     }
//                     // Plotly.update("plotly_scatter_plot", data_update, [trace_index_1, trace_index_2]);
//
//                 }
//
//             } else {
//                 // redraw original plot
//                 console.log("calling redraw_original_plot");
//                 redraw_original_plot();
//             }
//         }