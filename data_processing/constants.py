table_cols_values = ["SEASON_ID", "TEAM_ABBREVIATION",
                     "PLAYER_AGE", "GP", "GS", "MIN", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A",
                     "FG3_PCT", "FTM", "FTA", "FT_PCT", "OREB", "DREB", "REB", "AST", "STL",
                     "BLK", "TOV", "PF", "PTS"]

tooltip = {"GP":{"value":"games played"},
           "GS":{"value":"games started"},
           "MIN":{"value":"minutes"},
           "FGM":{"value":"field goals made"},       
           "FGA":{"value":"field goals attempted"},
           "FG_PCT":{"value":"field goals percentage"},
           "FG3M":{"value":"three-point field goals made"},
           "FG3A":{"value":"three-point field goals attempted"},
           "FG3_PCT":{"value":"three-point field goals percentage"},
           "FTM":{"value":"free throws made"},
           "FTA":{"value":"free throws attempted"},
           "FT_PCT":{"value":"free throws percentage"},
           "OREB":{"value":"offensive rebounds"},
           "DREB":{"value":"defensive rebounds"},
           "REB":{"value":"rebounds"},
           "AST":{"value":"assists"},
           "STL":{"value":"steals"},
           "BLK":{"value":"blocks"},
           "TOV":{"value":"turnovers"},
           "PF":{"value":"personal fouls"},
           "PTS":{"value":"points"}
          }

aggregations = {"sum":[i for i in tooltip.keys() if "PCT" not in i],
                "calculate":[i for i in tooltip.keys() if "PCT" in i]}
