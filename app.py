import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import data_processing.data_io as data_io
import data_processing.constants as ct
import data_processing.plotting as plotting

external_stylesheets = ["https://codepen.io/ericthayer/pen/1b88027d0220b52e07214fff4610e7ba.scss"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

table_cols_values = ct.table_cols_values
colors = {"text": "#0c0540"}

app.layout = html.Div([
    html.H1("NBA Player Stats",
            style={
                   "textAlign": "center",
                   "color": colors["text"]
            }
    ),
    
    html.Div(f"Collected career data of {len(data_io.list_players_with_ids(str()))} players.", 
             style={
                    "textAlign": "center", 
                    "color": colors["text"]
             }
    ),
    
    html.Label("Enter player name or select from drop down:"),

    dcc.Dropdown(
                id="selected-player", 
                options=data_io.list_players_with_ids("")
    ),

    html.Label("Select regular season or playoffs:"),

    dcc.Dropdown(
                id="selected-data-set", 
                options=[{"label": "Regular Season", "value": "SeasonTotalsRegularSeason"},
                         {"label": "Playoffs", "value": "SeasonTotalsPostSeason"}]
    ),

    html.Hr(),
    
    dcc.Graph(id="result-graph"),
    
    html.Hr(),
    
    html.Label("Select columns to plot:"),
    
    dash_table.DataTable(id="player_table",
                         columns=[{"name": i, "id": i, "selectable": True} for i in table_cols_values],
                         data=[],
                         filter_action="native",
                         sort_action="native",
                         sort_mode="single",
                         column_selectable="multi",
                         selected_columns=["AST", "PTS", "MIN", "REB"],
                         selected_rows=[],
                         tooltip=ct.tooltip
    ),
    
    dcc.Markdown("apis provided by https://github.com/swar/nba_api")
])


@app.callback(
    Output("player_table", "data"),
    [Input("selected-player", "value"), 
     Input("selected-data-set", "value")]) 
def update_table(selected_player, selected_data_set):
        if selected_player is None or selected_data_set is None:
            raise PreventUpdate
        else:
            return data_io.get_player_stats(str(selected_player))[selected_data_set][table_cols_values].to_dict(orient="records")


@app.callback(
    Output("result-graph", "figure"),
    [Input("player_table", "selected_columns"), 
     Input("selected-player", "value"), 
     Input("selected-data-set", "value")])
def update_figure(selected_columns, selected_player, selected_data_set):
    if selected_player is None or selected_columns is None or selected_data_set is None:
        raise PreventUpdate
    else:
        return plotting.plot_career_stats(selected_player, selected_data_set, selected_columns)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0")
