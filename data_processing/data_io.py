from nba_api.stats.endpoints import playercareerstats, commonallplayers
import pandas as pd
import data_processing.constants as ct


def list_players_with_ids(search_term):
    """
    Args:
        search_term (str): Last name or part of last name of player. Not case sensitive.

    Returns:
        list: List containing dictionaries with key player name and value player id.
    """
    all_players = commonallplayers.CommonAllPlayers().get_data_frames()[0][['PERSON_ID', 'DISPLAY_LAST_COMMA_FIRST']]
    all_players["LAST_NAME"] = list(map(lambda x: x.split(",")[0].lower(), all_players["DISPLAY_LAST_COMMA_FIRST"]))
    result_list = []
    for _, row in all_players[all_players['LAST_NAME'].str.contains(search_term.lower())].iterrows():
        result_list.append({'label':row['DISPLAY_LAST_COMMA_FIRST'],'value':row['PERSON_ID']})
    return result_list


def get_player_stats(player_id):
    """
    Args:
        player_id (str): String of a player id.

    Returns:
        dict: Data frames containing a player's career stats.
    """
    Career = playercareerstats.PlayerCareerStats(player_id)
    career_dict = Career.get_dict()
    return {i["name"]:pd.DataFrame(i["rowSet"],columns=i["headers"]) for i in career_dict["resultSets"]}


def aggregate_seasons_for_plotting(df):
    agg_df = df[ct.aggregations["sum"]+["SEASON_ID"]].groupby("SEASON_ID").agg("sum").reset_index()
    for i in ct.aggregations["calculate"]:
        try:
            agg_df[i] = round(agg_df[i.split("_")[0]+"M"] / agg_df[i.split("_")[0]+"A"],3)
        except Exception as e:
            print(f"column not generated in aggregation because of exception: {e}")
    agg_df["SEASON"] = [int(i.split("-")[0]) for i in agg_df["SEASON_ID"]]
    agg_df = agg_df.fillna(0).drop("SEASON_ID", axis=1)
    agg_df = pd.melt(agg_df, id_vars=['SEASON'])
    return agg_df
