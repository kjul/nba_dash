import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_table
import plotly.express as px
import pandas
from nba_api.stats.endpoints import playercareerstats, commonallplayers
import data_io
import constants as ct

external_stylesheets = ['https://codepen.io/ericthayer/pen/1b88027d0220b52e07214fff4610e7ba.scss']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

table_cols_values = ct.table_cols_values

app.layout = html.Div([
    
    dcc.Markdown('''
                 ### NBA Player Data
                 Enter player's name and select player from drop down:
                 '''),
    
    dcc.Dropdown(
                id='chosen-player', 
                options=data_io.list_players_with_ids("")
                ),

    html.Hr(),
    
    dcc.Graph(id='result-graph'),
    
    dash_table.DataTable(id='player_table',
                         columns=[{"name": i, "id": i, "selectable": True} for i in table_cols_values],
                         data=[],
                         filter_action='native',
                         sort_action='native',
                         sort_mode='single',
                         column_selectable='multi',
                         selected_columns=['AST','PTS','MIN','REB'],
                         selected_rows=[],
                         tooltip=ct.tooltip                         
                        )
])


@app.callback(
    Output('player_table', 'data'),
    [Input('chosen-player', 'value')])
def update_table(selected_player):
        if selected_player is None:
            raise PreventUpdate
        else:
            return data_io.get_player_stats(str(selected_player))["SeasonTotalsRegularSeason"][table_cols_values].to_dict(orient="records")


@app.callback(
    Output('result-graph', 'figure'),
    [Input('player_table', 'selected_columns'), Input('chosen-player', 'value')])
def update_figure2(selected_columns, selected_player):
    if selected_player is None or selected_columns is None:
        raise PreventUpdate
    else:
        player_stats = data_io.get_player_stats(str(selected_player))["SeasonTotalsRegularSeason"]
        agg_player_stats = data_io.aggregate_seasons_for_plotting(player_stats)
        agg_player_stats = agg_player_stats[agg_player_stats["variable"].isin(selected_columns)]
        return px.line(agg_player_stats,'SEASON', "value", color="variable")


if __name__ == '__main__':
    app.run_server(debug=True)
