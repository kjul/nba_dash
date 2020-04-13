import data_processing.data_io as data_io
import plotly.express as px


def plot_career_stats(selected_player, selected_data_set, selected_columns):
    """
    Args:
        selected_player (str): player_id
        selected_data_set (str): name of the type of data, either 'SeasonTotalsRegularSeason' or 'SeasonTotalsPostSeason'
        selected_columns (list): list of strings with column names that should be plotted
    Returns:
        plotly plot: for career stats of the selected player
    """
    player_stats = data_io.get_player_stats(str(selected_player))[selected_data_set]
    agg_player_stats = data_io.aggregate_seasons_for_plotting(player_stats)
    agg_player_stats = agg_player_stats[agg_player_stats["variable"].isin(selected_columns)]
    if len(agg_player_stats["value"]) > 0:
        y_upper_bound = max(agg_player_stats["value"])
    else: 
        y_upper_bound = 1
    if y_upper_bound > 1:
        y_upper_bound +=100
    else:
        y_upper_bound += 0.1
    return px.line(agg_player_stats,
                   "season", 
                   "value", 
                   color="variable", 
                   render_mode="svg", 
                   range_y=(0, y_upper_bound), 
                   template="plotly+presentation+xgridoff")
