import os, sys
import pandas as pd
pd.set_option('display.max_colwidth', 300) # in order to prevent 50 character cutoff of to_html export / ellipsis
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objects as go
sys.path.insert(0, os.path.abspath(os.path.realpath('python')))


def init_callbacks(dash_app):
    ### backend filtering for datatable ("filter data ...")
    operators = [['ge ', '>='], ['le ', '<='], ['lt ', '<'], ['gt ', '>'], ['ne ', '!='], ['eq ', '='], ['contains '], ['datestartswith ']]

    def split_filter_part(filter_part):
        for operator_type in operators:
            for operator in operator_type:
                if operator in filter_part:
                    name_part, value_part = filter_part.split(operator, 1)
                    name = name_part[name_part.find('{') + 1: name_part.rfind('}')]
                    value_part = value_part.strip()
                    v0 = value_part[0]
                    if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                        value = value_part[1: -1].replace('\\' + v0, v0)
                    else:
                        try:
                            value = float(value_part)
                        except ValueError:
                            value = value_part
                    # word operators need spaces after them in the filter string,
                    # but we don't want these later
                    return name, operator_type[0].strip(), value
        return [None] * 3

    @dash_app.callback(Output('main_datatable', "data"), [Input('main_datatable', "filter_query")])
    def filter_data_in_data_table(filter_):
        filtering_expressions = filter_.split(' && ')
        dff = df
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)
            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                # dff = dff.loc[dff[col_name].str.contains(filter_value)]
                dff = dff.loc[dff[col_name].str.contains(f'(?i){filter_value}')]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]
        return dff.to_dict('records')

    @dash_app.callback([Output(component_id="main_datatable", component_property="selected_rows"), Output(component_id="main_datatable", component_property="sort_by"), Output(component_id="main_datatable", component_property="hidden_columns"), ], [Input(component_id="button_reset_plot", component_property="n_clicks"), ], )
    def select_deselect(button_reset_plot_n_clicks):
        """
        https://community.plotly.com/t/select-all-rows-in-dash-datatable/41466 # for de-selecting everything
        """
        ctx = dash.callback_context
        if ctx.triggered:
            trigger = ctx.triggered[0]["prop_id"].split(".")[0]
            if trigger == "button_reset_plot":
                return [], [], hidden_columns

    @dash_app.callback([Output(component_id="main_datatable", component_property="style_data_conditional"), Output(component_id="scatter_container", component_property="children")], [Input(component_id="main_datatable", component_property="derived_virtual_data"), Input(component_id="main_datatable", component_property="derived_virtual_selected_row_ids"), Input(component_id="toggle_point_labels", component_property="value"), Input(component_id="toggle_point_edges", component_property="value")])
    def highlight_dataTableRows_and_pointsInScatter_on_selectInDataTable(derived_virtual_data, derived_virtual_selected_row_ids, toggle_point_labels_value, toggle_point_edges_value):
        # active_cell not used BUT without it the filter_data cell doesn't get highlighted at the bottom
        if derived_virtual_data is None or len(derived_virtual_data) == 0:
            dff = df
        else:
            dff = pd.DataFrame(derived_virtual_data)

        ### original unmodified plot
        if derived_virtual_selected_row_ids is None or len(derived_virtual_selected_row_ids) == 0:
            fig = go.Figure()
            for category_name, group in dff.groupby(category):
                fig.add_trace(go.Scatter(name=category_name, x=group[logFDR].tolist(), y=group[effectSize].tolist(), ids=group[term].tolist(), legendgroup=category_name, mode="markers", marker_symbol="circle", marker_color=group[color].iloc[0], marker_size=group[FG_count], marker_opacity=group[opacity], marker_sizemin=min_marker_size, marker_sizemode="area", marker_sizeref=sizeref, marker_line_width=group[marker_line_width], marker_line_color=group[marker_line_color], customdata=[list(ele) for ele in zip(group[term], group[description], group[FG_count])], hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>", ))
            fig.update_layout(hoverlabel=dict(font_size=12), template=layout_template_DBL_v2, title=None, xaxis_title="-log(FDR)", yaxis_title="effect size", legend=dict(title=None, font_size=12, orientation="h", yanchor="bottom", y=legend_y, xanchor="left", x=0, itemclick="toggleothers", itemdoubleclick="toggle", ), )
            fig.update_layout(autosize=False, width=scatter_plot_width, height=scatter_plot_height, )
            scatter_plot_fig = dcc.Graph(id='scatter_plot', figure=fig, config=config_scatter_plot)
            return style_data_conditional_basic, scatter_plot_fig

        ### modified plot
        else:
            cond_selected_terms = dff[term].isin(derived_virtual_selected_row_ids)
            dff[marker_line_width] = marker_line_width_default
            dff[marker_line_color] = marker_line_color_default
            dff[opacity] = opacity_default
            dff.loc[cond_selected_terms, marker_line_width] = marker_line_width_highlight
            dff.loc[cond_selected_terms, marker_line_color] = hover_label_color
            dff.loc[cond_selected_terms, opacity] = opacity_highlight
            style_data_conditional_extension = [{'if': {'filter_query': '{term}=' + "{}".format(term_)}, 'backgroundColor': table_highlight_color} for term_ in derived_virtual_selected_row_ids]

            fig = go.Figure()

            ### edges
            if toggle_point_edges_value:
                X_points, Y_points, Weights, Connected_node_terms = [], [], [], []
                for term_ in derived_virtual_selected_row_ids:
                    edges_dict = term_2_edges_dict[term_]
                    X_points += edges_dict["X_points"]
                    Y_points += edges_dict["Y_points"]
                    Weights += edges_dict["Weights"]
                    Connected_node_terms += edges_dict["Nodes"]
                Connected_node_terms += derived_virtual_selected_row_ids
                cond_connected_node_terms = dff[term].isin(Connected_node_terms)
                dff.loc[cond_connected_node_terms, opacity] = opacity_highlight
                fig.add_trace(go.Scatter(x=X_points, y=Y_points, mode='lines', showlegend=False, line=dict(color=color_edge_line, width=width_edges_line), hoverinfo='none'))

            ### labels
            if toggle_point_labels_value:
                dff["label"] = ""
                dff.loc[cond_selected_terms, "label"] = dff.loc[cond_selected_terms, term]
                x_min, x_max, y_min, y_max = dff[logFDR].min(), dff[logFDR].max(), dff[effectSize].min(), dff[effectSize].max()
                for category_name, group in dff.groupby(category):
                    fig.add_trace(go.Scatter(name=category_name, x=group[logFDR].tolist(), y=group[effectSize].tolist(), ids=group[term].tolist(), legendgroup=category_name, mode="markers+text", marker_symbol="circle", marker_color=group[color].iloc[0], marker_size=group[FG_count], marker_opacity=group[opacity], marker_sizemin=min_marker_size, marker_sizemode="area", marker_sizeref=sizeref, marker_line_width=group[marker_line_width], marker_line_color=group[marker_line_color], customdata=[list(ele) for ele in zip(group[term], group[description], group[FG_count])], hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>", text=group["label"].tolist(), textposition="top right", textfont_size=10))
                fig.update_layout(hoverlabel=dict(font_size=12), template=layout_template_DBL_v2, title=None, xaxis_title="-log(FDR)", yaxis_title="effect size", legend=dict(title=None, font_size=12, orientation="h", yanchor="bottom", y=legend_y, xanchor="left", x=0, itemclick="toggleothers", itemdoubleclick="toggle", ), xaxis_range=[x_min * 0.93, x_max * 1.07], yaxis_range=[y_min * 1.25, y_max * 1.25])

            else:
                for category_name, group in dff.groupby(category):
                    fig.add_trace(go.Scatter(name=category_name, x=group[logFDR].tolist(), y=group[effectSize].tolist(), ids=group[term].tolist(), legendgroup=category_name, mode="markers", marker_symbol="circle", marker_color=group[color].iloc[0], marker_size=group[FG_count], marker_opacity=group[opacity], marker_sizemin=min_marker_size, marker_sizemode="area", marker_sizeref=sizeref, marker_line_width=group[marker_line_width], marker_line_color=group[marker_line_color], customdata=[list(ele) for ele in zip(group[term], group[description], group[FG_count])], hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>"))
                fig.update_layout(hoverlabel=dict(font_size=12), template=layout_template_DBL_v2, title=None, xaxis_title="-log(FDR)", yaxis_title="effect size", legend=dict(title=None, font_size=12, orientation="h", yanchor="bottom", y=legend_y, xanchor="left", x=0, itemclick="toggleothers", itemdoubleclick="toggle", ), )

            fig.update_layout(autosize=False, width=scatter_plot_width, height=scatter_plot_height, )  # 800 x 520
            scatter_plot_fig = dcc.Graph(id='scatter_plot', figure=fig, config=config_scatter_plot)
            return style_data_conditional_extension + style_data_conditional_basic, scatter_plot_fig
