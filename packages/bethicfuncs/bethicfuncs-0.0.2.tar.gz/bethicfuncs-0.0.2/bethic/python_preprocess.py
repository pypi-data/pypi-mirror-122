import pandas as pd
import numpy as np

def clean_and_rename_df(df):

    df.drop([
            "0_league_season_eventType_0_events_0_startDate_1", "0_league_season_eventType_0_events_0_boxscores_0_players", "0_league_season_eventType_0_events_0_boxscores_1_players",
            "0_league_season_eventType_0_events_0_boxscores_0_teamStats_groundDuels_percentage", "0_league_season_eventType_0_events_0_boxscores_1_teamStats_groundDuels_percentage",
            "0_league_season_eventType_0_events_0_boxscores_0_teamStats_aerialDuels_percentage", "0_league_season_eventType_0_events_0_boxscores_1_teamStats_aerialDuels_percentage",
            "0_league_season_eventType_0_events_0_boxscores_0_teamStats_aerialDuels_total", "0_league_season_eventType_0_events_0_boxscores_0_teamStats_aerialDuels_won",
            "0_league_season_eventType_0_events_0_boxscores_0_teamStats_groundDuels_total", "0_league_season_eventType_0_events_0_boxscores_0_teamStats_groundDuels_won",
            "0_league_season_eventType_0_events_0_boxscores_1_teamStats_aerialDuels_total", "0_league_season_eventType_0_events_0_boxscores_1_teamStats_aerialDuels_won",
            "0_league_season_eventType_0_events_0_boxscores_1_teamStats_groundDuels_total", "0_league_season_eventType_0_events_0_boxscores_1_teamStats_groundDuels_won",
            "0_league_season_eventType_0_events_0_boxscores_0_teamStats_tackles", "0_league_season_eventType_0_events_0_boxscores_1_teamStats_tackles",
            "0_league_season_eventType_0_events_0_boxscores_0_teamStats_shots_insideBox", "0_league_season_eventType_0_events_0_boxscores_0_teamStats_shots_outsideBox",
            "0_league_season_eventType_0_events_0_boxscores_1_teamStats_shots_insideBox", "0_league_season_eventType_0_events_0_boxscores_1_teamStats_shots_outsideBox"
    ], inplace=True, axis=1)

    df.columns = ["season","eventId","year","month","day","full_date","dateType","stadi","city","hm_t_n","hm_t_id","hm_t_win",
                 "hm_t_los","hm_t_tie","hm_t_points","hm_t_sco","hm_t_isw","aw_t_n","aw_t_id","aw_t_win","aw_t_los","aw_t_tie",
                 "aw_t_points","aw_t_sco","aw_t_isw","week_0","week_1","t1_id","t1_gol","t1_autogol","t1_assis","t1_shot",
                 "t1_shot_gol","t1_xtg_gol","t1_save","t1_cross","t1_pty","t1_pty_gol","t1_fouls_do","t1_fouls_re","t1_yel_card",
                 "t1_red_card","t1_offsid","t1_corner","t1_catch","t1_punch","t1_xtg_poss","t2_id","t2_gol","t2_autogol","t2_assis",
                 "t2_shot","t2_shot_gol","t2_xtg_gol","t2_save","t2_cross","t2_pty","t2_pty_gol","t2_fouls_do","t2_fouls_re",
                 "t2_yel_card","t2_red_card","t2_offsid","t2_corner","t2_catch","t2_punch","t2_xtg_poss","arbitr_n","hour","minute",
                 "Attend","t1plyr0_Id","t1plyr0_n","t1plyr0_posId","t1plyr0_started","t1plyr0_minutes","t1plyr0_gol",
                 "t1plyr0_shots","t1plyr0_shGoal","t1plyr0_fouls_do","t1plyr0_yellow_do","t1plyr1_Id","t1plyr1_n","t1plyr1_posId",
                 "t1plyr1_started","t1plyr1_minutes","t1plyr1_gol","t1plyr1_shots","t1plyr1_shGoal","t1plyr1_fouls_do",
                 "t1plyr1_yellow_do","t1plyr2_Id","t1plyr2_n","t1plyr2_posId","t1plyr2_started","t1plyr2_minutes","t1plyr2_gol",
                 "t1plyr2_shots","t1plyr2_shGoal","t1plyr2_fouls_do","t1plyr2_yellow_do","t1plyr3_Id","t1plyr3_n","t1plyr3_posId",
                 "t1plyr3_started","t1plyr3_minutes","t1plyr3_gol","t1plyr3_shots","t1plyr3_shGoal","t1plyr3_fouls_do",
                 "t1plyr3_yellow_do","t1plyr4_Id","t1plyr4_n","t1plyr4_posId","t1plyr4_started","t1plyr4_minutes","t1plyr4_gol",
                 "t1plyr4_shots","t1plyr4_shGoal","t1plyr4_fouls_do","t1plyr4_yellow_do","t1plyr5_Id","t1plyr5_n","t1plyr5_posId",
                 "t1plyr5_started","t1plyr5_minutes","t1plyr5_gol","t1plyr5_shots","t1plyr5_shGoal","t1plyr5_fouls_do",
                 "t1plyr5_yellow_do","t1plyr6_Id","t1plyr6_n","t1plyr6_posId","t1plyr6_started","t1plyr6_minutes","t1plyr6_gol",
                 "t1plyr6_shots","t1plyr6_shGoal","t1plyr6_fouls_do","t1plyr6_yellow_do","t1plyr7_Id","t1plyr7_n","t1plyr7_posId",
                 "t1plyr7_started","t1plyr7_minutes","t1plyr7_gol","t1plyr7_shots","t1plyr7_shGoal","t1plyr7_fouls_do",
                 "t1plyr7_yellow_do","t1plyr8_Id","t1plyr8_n","t1plyr8_posId","t1plyr8_started","t1plyr8_minutes","t1plyr8_gol",
                 "t1plyr8_shots","t1plyr8_shGoal","t1plyr8_fouls_do","t1plyr8_yellow_do","t1plyr9_Id","t1plyr9_n","t1plyr9_posId",
                 "t1plyr9_started","t1plyr9_minutes","t1plyr9_gol","t1plyr9_shots","t1plyr9_shGoal","t1plyr9_fouls_do",
                 "t1plyr9_yellow_do","t1plyr10_Id","t1plyr10_n","t1plyr10_posId","t1plyr10_started","t1plyr10_minutes",
                 "t1plyr10_gol","t1plyr10_shots","t1plyr10_shGoal","t1plyr10_fouls_do","t1plyr10_yellow_do","t1plyr11_Id",
                 "t1plyr11_n","t1plyr11_posId","t1plyr11_started","t1plyr11_minutes","t1plyr11_gol","t1plyr11_shots",
                 "t1plyr11_shGoal","t1plyr11_fouls_do","t1plyr11_yellow_do","t1plyr12_Id","t1plyr12_n","t1plyr12_posId",
                 "t1plyr12_started","t1plyr12_minutes","t1plyr12_gol","t1plyr12_shots","t1plyr12_shGoal","t1plyr12_fouls_do",
                 "t1plyr12_yellow_do","t2plyr0_Id","t2plyr0_n","t2plyr0_posId","t2plyr0_started","t2plyr0_minutes","t2plyr0_gol",
                 "t2plyr0_shots","t2plyr0_shGoal","t2plyr0_fouls_do","t2plyr0_yellow_do","t2plyr1_Id","t2plyr1_n","t2plyr1_posId",
                 "t2plyr1_started","t2plyr1_minutes","t2plyr1_gol","t2plyr1_shots","t2plyr1_shGoal","t2plyr1_fouls_do",
                 "t2plyr1_yellow_do","t2plyr2_Id","t2plyr2_n","t2plyr2_posId","t2plyr2_started","t2plyr2_minutes","t2plyr2_gol",
                 "t2plyr2_shots","t2plyr2_shGoal","t2plyr2_fouls_do","t2plyr2_yellow_do","t2plyr3_Id","t2plyr3_n","t2plyr3_posId",
                 "t2plyr3_started","t2plyr3_minutes","t2plyr3_gol","t2plyr3_shots","t2plyr3_shGoal","t2plyr3_fouls_do",
                 "t2plyr3_yellow_do","t2plyr4_Id","t2plyr4_n","t2plyr4_posId","t2plyr4_started","t2plyr4_minutes","t2plyr4_gol",
                 "t2plyr4_shots","t2plyr4_shGoal","t2plyr4_fouls_do","t2plyr4_yellow_do","t2plyr5_Id","t2plyr5_n","t2plyr5_posId",
                 "t2plyr5_started","t2plyr5_minutes","t2plyr5_gol","t2plyr5_shots","t2plyr5_shGoal","t2plyr5_fouls_do",
                 "t2plyr5_yellow_do","t2plyr6_Id","t2plyr6_n","t2plyr6_posId","t2plyr6_started","t2plyr6_minutes","t2plyr6_gol",
                 "t2plyr6_shots","t2plyr6_shGoal","t2plyr6_fouls_do","t2plyr6_yellow_do","t2plyr7_Id","t2plyr7_n","t2plyr7_posId",
                 "t2plyr7_started","t2plyr7_minutes","t2plyr7_gol","t2plyr7_shots","t2plyr7_shGoal","t2plyr7_fouls_do",
                 "t2plyr7_yellow_do","t2plyr8_Id","t2plyr8_n","t2plyr8_posId","t2plyr8_started","t2plyr8_minutes","t2plyr8_gol",
                 "t2plyr8_shots","t2plyr8_shGoal","t2plyr8_fouls_do","t2plyr8_yellow_do","t2plyr9_Id","t2plyr9_n","t2plyr9_posId",
                 "t2plyr9_started","t2plyr9_minutes","t2plyr9_gol","t2plyr9_shots","t2plyr9_shGoal","t2plyr9_fouls_do",
                 "t2plyr9_yellow_do","t2plyr10_Id","t2plyr10_n","t2plyr10_posId","t2plyr10_started","t2plyr10_minutes",
                 "t2plyr10_gol","t2plyr10_shots","t2plyr10_shGoal","t2plyr10_fouls_do","t2plyr10_yellow_do","t2plyr11_Id",
                 "t2plyr11_n","t2plyr11_posId","t2plyr11_started","t2plyr11_minutes","t2plyr11_gol","t2plyr11_shots",
                 "t2plyr11_shGoal","t2plyr11_fouls_do","t2plyr11_yellow_do","t2plyr12_Id","t2plyr12_n","t2plyr12_posId",
                 "t2plyr12_started","t2plyr12_minutes","t2plyr12_gol","t2plyr12_shots","t2plyr12_shGoal","t2plyr12_fouls_do",
                 "t2plyr12_yellow_do","t2plyr13_Id","t2plyr13_n","t2plyr13_posId","t2plyr13_started","t2plyr13_minutes",
                 "t2plyr13_gol","t2plyr13_shots","t2plyr13_shGoal","t2plyr13_fouls_do","t2plyr13_yellow_do","arbitr_id",
                 "t1plyr13_Id","t1plyr13_n","t1plyr13_posId","t1plyr13_started","t1plyr13_minutes","t1plyr13_gol","t1plyr13_shots",
                 "t1plyr13_shGoal","t1plyr13_fouls_do","t1plyr13_yellow_do","hm_t_shot","aw_t_shot","t2plyr14_Id","t2plyr14_n",
                 "t2plyr14_posId","t2plyr14_started","t2plyr14_minutes","t2plyr14_gol","t2plyr14_shots","t2plyr14_shGoal",
                 "t2plyr14_fouls_do","t2plyr14_yellow_do","t1plyr14_Id","t1plyr14_n","t1plyr14_posId","t1plyr14_started",
                 "t1plyr14_minutes","t1plyr14_gol","t1plyr14_shots","t1plyr14_shGoal","t1plyr14_fouls_do","t1plyr14_yellow_do",
                 "hm_t_format","aw_t_format"]

    return (df)

def define_hm_aw(df):
    columns = ["assis", "autogol", "catch", "corner", "cross", "fouls_do", "fouls_re", "gol", "id", "offsid", "pty",
                  "pty_gol", "punch", "red_card", "save", "shot", "shot_gol", "xtg_gol", "xtg_poss", "yel_card"]

    for column in columns:
        df.loc[df['hm_t_id'] == df['t1_id'], 'hm_t_' + column] = df['t1_' + column]
        df.loc[df['hm_t_id'] == df['t2_id'], 'hm_t_' + column] = df['t2_' + column]
        df.loc[df['aw_t_id'] == df['t1_id'], 'aw_t_' + column] = df['t1_' + column]
        df.loc[df['aw_t_id'] == df['t2_id'], 'aw_t_' + column] = df['t2_' + column]

    player_variables = ["plyr0_fouls_do","plyr0_gol","plyr0_Id","plyr0_minutes","plyr0_n","plyr0_posId","plyr0_shGoal","plyr0_shots",
                  "plyr0_started","plyr0_yellow_do","plyr1_fouls_do","plyr1_gol","plyr1_Id","plyr1_minutes","plyr1_n","plyr1_posId",
                  "plyr1_shGoal","plyr1_shots","plyr1_started","plyr1_yellow_do","plyr10_fouls_do","plyr10_gol","plyr10_Id",
                  "plyr10_minutes","plyr10_n","plyr10_posId","plyr10_shGoal","plyr10_shots","plyr10_started","plyr10_yellow_do",
                  "plyr11_fouls_do","plyr11_gol","plyr11_Id","plyr11_minutes","plyr11_n","plyr11_posId","plyr11_shGoal",
                  "plyr11_shots","plyr11_started","plyr11_yellow_do","plyr12_fouls_do","plyr12_gol","plyr12_Id","plyr12_minutes",
                  "plyr12_n","plyr12_posId","plyr12_shGoal","plyr12_shots","plyr12_started","plyr12_yellow_do","plyr13_fouls_do",
                  "plyr13_gol","plyr13_Id","plyr13_minutes","plyr13_n","plyr13_posId","plyr13_shGoal","plyr13_shots",
                  "plyr13_started","plyr13_yellow_do","plyr14_fouls_do","plyr14_gol","plyr14_Id","plyr14_minutes","plyr14_n",
                  "plyr14_posId","plyr14_shGoal","plyr14_shots","plyr14_started","plyr14_yellow_do","plyr2_fouls_do","plyr2_gol",
                  "plyr2_Id","plyr2_minutes","plyr2_n","plyr2_posId","plyr2_shGoal","plyr2_shots","plyr2_started","plyr2_yellow_do",
                  "plyr3_fouls_do","plyr3_gol","plyr3_Id","plyr3_minutes","plyr3_n","plyr3_posId","plyr3_shGoal","plyr3_shots",
                  "plyr3_started","plyr3_yellow_do","plyr4_fouls_do","plyr4_gol","plyr4_Id","plyr4_minutes","plyr4_n","plyr4_posId",
                  "plyr4_shGoal","plyr4_shots","plyr4_started","plyr4_yellow_do","plyr5_fouls_do","plyr5_gol","plyr5_Id",
                  "plyr5_minutes","plyr5_n","plyr5_posId","plyr5_shGoal","plyr5_shots","plyr5_started","plyr5_yellow_do",
                  "plyr6_fouls_do","plyr6_gol","plyr6_Id","plyr6_minutes","plyr6_n","plyr6_posId","plyr6_shGoal","plyr6_shots",
                  "plyr6_started","plyr6_yellow_do","plyr7_fouls_do","plyr7_gol","plyr7_Id","plyr7_minutes","plyr7_n","plyr7_posId",
                  "plyr7_shGoal","plyr7_shots","plyr7_started","plyr7_yellow_do","plyr8_fouls_do","plyr8_gol","plyr8_Id",
                  "plyr8_minutes","plyr8_n","plyr8_posId","plyr8_shGoal","plyr8_shots","plyr8_started","plyr8_yellow_do",
                  "plyr9_fouls_do","plyr9_gol","plyr9_Id","plyr9_minutes","plyr9_n","plyr9_posId","plyr9_shGoal","plyr9_shots",
                  "plyr9_started","plyr9_yellow_do"
    ]

    for player_variable in player_variables:
        df.loc[df['hm_t_id'] == df['t1_id'], 'hm_t_' + player_variable] = df['t1' + player_variable]
        df.loc[df['hm_t_id'] == df['t2_id'], 'hm_t_' + player_variable] = df['t2' + player_variable]
        df.loc[df['aw_t_id'] == df['t1_id'], 'aw_t_' + player_variable] = df['t1' + player_variable]
        df.loc[df['aw_t_id'] == df['t2_id'], 'aw_t_' + player_variable] = df['t2' + player_variable]

    df.drop(["t1_id", "t1_gol", "t1_autogol", "t1_assis", "t1_shot", "t1_shot_gol", "t1_xtg_gol", "t1_save", "t1_cross",
            "t1_pty", "t1_pty_gol", "t1_fouls_do", "t1_fouls_re", "t1_yel_card", "t1_red_card", "t1_offsid", "t1_corner",
            "t1_catch", "t1_punch", "t1_xtg_poss", "t2_id", "t2_gol", "t2_autogol", "t2_assis", "t2_shot", "t2_shot_gol", "t2_xtg_gol",
            "t2_save", "t2_cross", "t2_pty", "t2_pty_gol", "t2_fouls_do", "t2_fouls_re", "t2_yel_card", "t2_red_card", "t2_offsid",
            "t2_corner", "t2_catch", "t2_punch", "t2_xtg_poss", "t1plyr0_Id", "t1plyr0_n", "t1plyr0_posId", "t1plyr0_started", "t1plyr0_minutes",
            "t1plyr0_gol", "t1plyr0_shots", "t1plyr0_shGoal", "t1plyr0_fouls_do", "t1plyr0_yellow_do", "t1plyr1_Id", "t1plyr1_n",
            "t1plyr1_posId", "t1plyr1_started", "t1plyr1_minutes", "t1plyr1_gol", "t1plyr1_shots", "t1plyr1_shGoal", "t1plyr1_fouls_do",
            "t1plyr1_yellow_do", "t1plyr2_Id", "t1plyr2_n", "t1plyr2_posId", "t1plyr2_started", "t1plyr2_minutes",
            "t1plyr2_gol", "t1plyr2_shots", "t1plyr2_shGoal", "t1plyr2_fouls_do", "t1plyr2_yellow_do", "t1plyr3_Id", "t1plyr3_n",
            "t1plyr3_posId", "t1plyr3_started", "t1plyr3_minutes", "t1plyr3_gol", "t1plyr3_shots", "t1plyr3_shGoal", "t1plyr3_fouls_do",
            "t1plyr3_yellow_do", "t1plyr4_Id", "t1plyr4_n", "t1plyr4_posId", "t1plyr4_started", "t1plyr4_minutes",
            "t1plyr4_gol", "t1plyr4_shots", "t1plyr4_shGoal", "t1plyr4_fouls_do", "t1plyr4_yellow_do", "t1plyr5_Id", "t1plyr5_n",
            "t1plyr5_posId", "t1plyr5_started", "t1plyr5_minutes", "t1plyr5_gol", "t1plyr5_shots", "t1plyr5_shGoal", "t1plyr5_fouls_do",
            "t1plyr5_yellow_do", "t1plyr6_Id", "t1plyr6_n", "t1plyr6_posId", "t1plyr6_started", "t1plyr6_minutes",
            "t1plyr6_gol", "t1plyr6_shots", "t1plyr6_shGoal", "t1plyr6_fouls_do", "t1plyr6_yellow_do", "t1plyr7_Id", "t1plyr7_n",
            "t1plyr7_posId", "t1plyr7_started", "t1plyr7_minutes", "t1plyr7_gol", "t1plyr7_shots", "t1plyr7_shGoal", "t1plyr7_fouls_do",
            "t1plyr7_yellow_do", "t1plyr8_Id", "t1plyr8_n", "t1plyr8_posId", "t1plyr8_started", "t1plyr8_minutes",
            "t1plyr8_gol", "t1plyr8_shots", "t1plyr8_shGoal", "t1plyr8_fouls_do", "t1plyr8_yellow_do", "t1plyr9_Id", "t1plyr9_n",
            "t1plyr9_posId", "t1plyr9_started", "t1plyr9_minutes", "t1plyr9_gol", "t1plyr9_shots", "t1plyr9_shGoal", "t1plyr9_fouls_do",
            "t1plyr9_yellow_do", "t1plyr10_Id", "t1plyr10_n", "t1plyr10_posId", "t1plyr10_started", "t1plyr10_minutes",
            "t1plyr10_gol", "t1plyr10_shots", "t1plyr10_shGoal", "t1plyr10_fouls_do", "t1plyr10_yellow_do", "t1plyr11_Id", "t1plyr11_n",
            "t1plyr11_posId", "t1plyr11_started", "t1plyr11_minutes", "t1plyr11_gol", "t1plyr11_shots", "t1plyr11_shGoal",
            "t1plyr11_fouls_do", "t1plyr11_yellow_do", "t1plyr12_Id", "t1plyr12_n", "t1plyr12_posId", "t1plyr12_started", "t1plyr12_minutes",
            "t1plyr12_gol", "t1plyr12_shots", "t1plyr12_shGoal", "t1plyr12_fouls_do", "t1plyr12_yellow_do", "t2plyr0_Id", "t2plyr0_n",
            "t2plyr0_posId", "t2plyr0_started", "t2plyr0_minutes", "t2plyr0_gol", "t2plyr0_shots", "t2plyr0_shGoal", "t2plyr0_fouls_do",
            "t2plyr0_yellow_do", "t2plyr1_Id", "t2plyr1_n", "t2plyr1_posId", "t2plyr1_started", "t2plyr1_minutes",
            "t2plyr1_gol", "t2plyr1_shots", "t2plyr1_shGoal", "t2plyr1_fouls_do", "t2plyr1_yellow_do", "t2plyr2_Id", "t2plyr2_n",
            "t2plyr2_posId", "t2plyr2_started", "t2plyr2_minutes", "t2plyr2_gol", "t2plyr2_shots", "t2plyr2_shGoal", "t2plyr2_fouls_do",
            "t2plyr2_yellow_do", "t2plyr3_Id", "t2plyr3_n", "t2plyr3_posId", "t2plyr3_started", "t2plyr3_minutes",
            "t2plyr3_gol", "t2plyr3_shots", "t2plyr3_shGoal", "t2plyr3_fouls_do", "t2plyr3_yellow_do", "t2plyr4_Id", "t2plyr4_n",
            "t2plyr4_posId", "t2plyr4_started", "t2plyr4_minutes", "t2plyr4_gol", "t2plyr4_shots", "t2plyr4_shGoal", "t2plyr4_fouls_do",
            "t2plyr4_yellow_do", "t2plyr5_Id", "t2plyr5_n", "t2plyr5_posId", "t2plyr5_started", "t2plyr5_minutes",
            "t2plyr5_gol", "t2plyr5_shots", "t2plyr5_shGoal", "t2plyr5_fouls_do", "t2plyr5_yellow_do", "t2plyr6_Id", "t2plyr6_n",
            "t2plyr6_posId", "t2plyr6_started", "t2plyr6_minutes", "t2plyr6_gol", "t2plyr6_shots", "t2plyr6_shGoal", "t2plyr6_fouls_do",
            "t2plyr6_yellow_do", "t2plyr7_Id", "t2plyr7_n", "t2plyr7_posId", "t2plyr7_started", "t2plyr7_minutes",
            "t2plyr7_gol", "t2plyr7_shots", "t2plyr7_shGoal", "t2plyr7_fouls_do", "t2plyr7_yellow_do", "t2plyr8_Id", "t2plyr8_n",
            "t2plyr8_posId", "t2plyr8_started", "t2plyr8_minutes", "t2plyr8_gol", "t2plyr8_shots", "t2plyr8_shGoal", "t2plyr8_fouls_do",
            "t2plyr8_yellow_do", "t2plyr9_Id", "t2plyr9_n", "t2plyr9_posId", "t2plyr9_started", "t2plyr9_minutes",
            "t2plyr9_gol", "t2plyr9_shots", "t2plyr9_shGoal", "t2plyr9_fouls_do", "t2plyr9_yellow_do", "t2plyr10_Id", "t2plyr10_n",
            "t2plyr10_posId", "t2plyr10_started", "t2plyr10_minutes", "t2plyr10_gol", "t2plyr10_shots", "t2plyr10_shGoal",
            "t2plyr10_fouls_do", "t2plyr10_yellow_do", "t2plyr11_Id", "t2plyr11_n", "t2plyr11_posId", "t2plyr11_started", "t2plyr11_minutes",
            "t2plyr11_gol", "t2plyr11_shots", "t2plyr11_shGoal", "t2plyr11_fouls_do", "t2plyr11_yellow_do", "t2plyr12_Id", "t2plyr12_n",
            "t2plyr12_posId", "t2plyr12_started", "t2plyr12_minutes", "t2plyr12_gol", "t2plyr12_shots",
            "t2plyr12_shGoal", "t2plyr12_fouls_do", "t2plyr12_yellow_do", "t2plyr13_Id", "t2plyr13_n", "t2plyr13_posId",
            "t2plyr13_started", "t2plyr13_minutes", "t2plyr13_gol", "t2plyr13_shots", "t2plyr13_shGoal", "t2plyr13_fouls_do",
            "t2plyr13_yellow_do", "t1plyr13_Id", "t1plyr13_n", "t1plyr13_posId", "t1plyr13_started", "t1plyr13_minutes", "t1plyr13_gol",
            "t1plyr13_shots", "t1plyr13_shGoal", "t1plyr13_fouls_do", "t1plyr13_yellow_do", "t2plyr14_Id", "t2plyr14_n", "t2plyr14_posId",
            "t2plyr14_started", "t2plyr14_minutes", "t2plyr14_gol", "t2plyr14_shots", "t2plyr14_shGoal",
            "t2plyr14_fouls_do", "t2plyr14_yellow_do", "t1plyr14_Id", "t1plyr14_n", "t1plyr14_posId", "t1plyr14_started", "t1plyr14_minutes",
            "t1plyr14_gol", "t1plyr14_shots", "t1plyr14_shGoal", "t1plyr14_fouls_do", "t1plyr14_yellow_do"
            ], inplace=True, axis=1)

    return (df)

def change_wrong_team_names(df):
    df.loc[df['hm_t_id'] == 8197, 'hm_t_n'] = 'Almeria'
    df.loc[df['aw_t_id'] == 8197, 'aw_t_n'] = 'Almeria'

    df.loc[df['hm_t_id'] == 6172, 'hm_t_n'] = 'Atletico Madrid'
    df.loc[df['aw_t_id'] == 6172, 'aw_t_n'] = 'Atletico Madrid'

    df.loc[df['hm_t_id'] == 6165, 'hm_t_n'] = 'Deportivo La Coruna'
    df.loc[df['aw_t_id'] == 6165, 'aw_t_n'] = 'Deportivo La Coruna'

    df.loc[df['hm_t_id'] == 7185, 'hm_t_n'] = 'Malaga'
    df.loc[df['aw_t_id'] == 7185, 'aw_t_n'] = 'Malaga'

    df.loc[df['hm_t_id'] == 8312, 'hm_t_n'] = 'Sporting de Gijon'
    df.loc[df['aw_t_id'] == 8312, 'aw_t_n'] = 'Sporting de Gijon'

    df.loc[df['hm_t_id'] == 6164, 'hm_t_n'] = 'Real Zaragoza'
    df.loc[df['aw_t_id'] == 6164, 'aw_t_n'] = 'Real Zaragoza'

    df.loc[df['hm_t_id'] == 7185, 'hm_t_n'] = 'Malaga'
    df.loc[df['aw_t_id'] == 7185, 'aw_t_n'] = 'Malaga'

    df.loc[df['hm_t_id'] == 23420, 'hm_t_n'] = 'Granada'
    df.loc[df['aw_t_id'] == 23420, 'aw_t_n'] = 'Granada'

    return(df)

def fill_missings(df):

    index_update = df[df['eventId'] == 832016].index
    df.loc[index_update, 'arbitr_id'] = 565985
    del index_update

    index_update = df[df['eventId'] == 832031].index
    df.loc[index_update, 'arbitr_id'] = 565989
    del index_update

    index_update = df[df['eventId'] == 832090].index
    df.loc[index_update, 'arbitr_id'] = 565989
    del index_update

    index_update = df[df['eventId'] == 832200].index
    df.loc[index_update, 'arbitr_id'] = 565989
    del index_update

    index_update = df[df['eventId'] == 832210].index
    df.loc[index_update, 'arbitr_id'] = 565985
    del index_update

    index_update = df[df['eventId'] == 832297].index
    df.loc[index_update, 'arbitr_id'] = 383057
    del index_update

    index_update = df[df['eventId'] == 909496].index
    df.loc[index_update, 'arbitr_id'] = 565957
    del index_update

    index_update = df[df['eventId'] == 909547].index
    df.loc[index_update, 'arbitr_id'] = 473833
    del index_update

    index_update = df[df['eventId'] == 910321].index
    df.loc[index_update, 'arbitr_id'] = 383061
    del index_update

    index_update = df[df['eventId'] == 995405].index
    df.loc[index_update, 'arbitr_id'] = 383133
    del index_update

    index_update = df[df['eventId'] == 995476].index
    df.loc[index_update, 'arbitr_id'] = 575418
    del index_update

    index_update = df[df['eventId'] == 995479].index
    df.loc[index_update, 'arbitr_id'] = 475324
    del index_update

    index_update = df[df['eventId'] == 995491].index
    df.loc[index_update, 'arbitr_id'] = 475324
    del index_update

    index_update = df[df['eventId'] == 995542].index
    df.loc[index_update, 'arbitr_id'] = 475324
    del index_update

    index_update = df[df['eventId'] == 995562].index
    df.loc[index_update, 'arbitr_id'] = 477005
    del index_update

    index_update = df[df['eventId'] == 1070022].index
    df.loc[index_update, 'arbitr_id'] = 473833
    df.loc[index_update, 'hm_t_sco'] = 3.0
    df.loc[index_update, 'aw_t_sco'] = 0.0
    del index_update

    index_update = df[df['eventId'] == 1069750].index
    df.loc[index_update, 'arbitr_id'] = 382878
    df.loc[index_update, 'hm_t_sco'] = 0.0
    df.loc[index_update, 'aw_t_sco'] = 1.0
    del index_update

    index_update = df[df['eventId'] == 1069746].index
    df.loc[index_update, 'arbitr_id'] = 382820
    df.loc[index_update, 'hm_t_sco'] = 0.0
    df.loc[index_update, 'aw_t_sco'] = 0.0
    del index_update

    index_update = df[df['eventId'] == 1069743].index
    df.loc[index_update, 'arbitr_id'] = 473550
    df.loc[index_update, 'hm_t_sco'] = 3.0
    df.loc[index_update, 'aw_t_sco'] = 0.0
    del index_update

    index_update = df[df['eventId'] == 1069738].index
    df.loc[index_update, 'arbitr_id'] = 455385
    df.loc[index_update, 'hm_t_sco'] = 1.0
    df.loc[index_update, 'aw_t_sco'] = 2.0
    del index_update

    index_update = df[df['eventId'] == 1069692].index
    df.loc[index_update, 'arbitr_id'] = 565985
    df.loc[index_update, 'hm_t_sco'] = 4.0
    df.loc[index_update, 'aw_t_sco'] = 1.0
    del index_update

    index_update = df[df['eventId'] == 1069729].index
    df.loc[index_update, 'arbitr_id'] = 383346
    df.loc[index_update, 'hm_t_sco'] = 1.0
    df.loc[index_update, 'aw_t_sco'] = 1.0
    del index_update

    index_update = df[df['eventId'] == 1069694].index
    df.loc[index_update, 'arbitr_id'] = 383319
    df.loc[index_update, 'hm_t_sco'] = 1.0
    df.loc[index_update, 'aw_t_sco'] = 4.0
    del index_update

    index_update = df[df['eventId'] == 1069688].index
    df.loc[index_update, 'arbitr_id'] = 382822
    df.loc[index_update, 'hm_t_sco'] = 0.0
    df.loc[index_update, 'aw_t_sco'] = 4.0
    del index_update

    index_update = df[df['eventId'] == 1069734].index
    df.loc[index_update, 'arbitr_id'] = 383291
    df.loc[index_update, 'hm_t_sco'] = 1.0
    df.loc[index_update, 'aw_t_sco'] = 1.0
    del index_update

    index_update = df[df['eventId'] == 1226429].index
    df.loc[index_update, 'arbitr_id'] = 382820
    df.loc[index_update, 'hm_t_sco'] = 0.0
    df.loc[index_update, 'aw_t_sco'] = 2.0
    del index_update

    index_update = df[df['eventId'] == 1340634].index
    df.loc[index_update, 'arbitr_id'] = 520113
    del index_update

    index_update = df[df['eventId'] == 1340662].index
    df.loc[index_update, 'arbitr_id'] = 473550
    del index_update
    index_update = df[df.hm_t_punch.isna() == True].index
    df.loc[index_update, 'hm_t_punch'] = 0
    del index_update

    index_update = df[df.aw_t_punch.isna() == True].index
    df.loc[index_update, 'aw_t_punch'] = 0
    del index_update

    index_update = df[df.hm_t_catch.isna() == True].index
    df.loc[index_update, 'hm_t_catch'] = 0
    del index_update

    index_update = df[df.aw_t_catch.isna() == True].index
    df.loc[index_update, 'aw_t_catch'] = 0
    del index_update

    index_update = df[df['eventId'] == 995621].index
    df.loc[index_update, 'Attend'] = 13105
    del index_update

    index_update = df[df['eventId'] == 995721].index
    df.loc[index_update, 'Attend'] = 12848
    del index_update

    index_update = df[df['eventId'] == 1340760].index
    df.loc[index_update, 'Attend'] = 35650
    del index_update

    index_update = df[df['eventId'] == 1340910].index
    df.loc[index_update, 'Attend'] = 12100
    del index_update

    index_update = df[df['eventId'] == 832159].index
    df.loc[index_update, 'hm_t_format'] = 4231
    del index_update

    index_update = df[df['eventId'] == 832170].index
    df.loc[index_update, 'hm_t_format'] = 4231
    del index_update

    index_update = df[df['eventId'] == 832172].index
    df.loc[index_update, 'hm_t_format'] = 442
    del index_update

    index_update = df[df['eventId'] == 832193].index
    df.loc[index_update, 'hm_t_format'] = 442
    del index_update

    index_update = df[df['eventId'] == 832360].index
    df.loc[index_update, 'hm_t_format'] = 4231
    del index_update

    index_update = df[df['eventId'] == 909448].index
    df.loc[index_update, 'hm_t_format'] = 442
    del index_update

    index_update = df[df['eventId'] == 909594].index
    df.loc[index_update, 'hm_t_format'] = 4231
    del index_update

    index_update = df[df['eventId'] == 995403].index
    df.loc[index_update, 'hm_t_format'] = 4231
    del index_update

    index_update = df[df['eventId'] == 995405].index
    df.loc[index_update, 'hm_t_format'] = 4231
    del index_update

    index_update = df[df['eventId'] == 995421].index
    df.loc[index_update, 'hm_t_format'] = 442
    del index_update

    index_update = df[df['eventId'] == 832159].index
    df.loc[index_update, 'aw_t_format'] = 4231
    del index_update

    index_update = df[df['eventId'] == 832170].index
    df.loc[index_update, 'aw_t_format'] = 4231
    del index_update

    index_update = df[df['eventId'] == 832172].index
    df.loc[index_update, 'aw_t_format'] = 4231
    del index_update

    index_update = df[df['eventId'] == 832193].index
    df.loc[index_update, 'aw_t_format'] = 4231
    del index_update

    index_update = df[df['eventId'] == 832360].index
    df.loc[index_update, 'aw_t_format'] = 442
    del index_update

    index_update = df[df['eventId'] == 909448].index
    df.loc[index_update, 'aw_t_format'] = 4231
    del index_update

    index_update = df[df['eventId'] == 909594].index
    df.loc[index_update, 'aw_t_format'] = 442
    del index_update

    index_update = df[df['eventId'] == 995403].index
    df.loc[index_update, 'aw_t_format'] = 4231
    del index_update

    index_update = df[df['eventId'] == 995405].index
    df.loc[index_update, 'aw_t_format'] = 4231
    del index_update

    index_update = df[df['eventId'] == 995421].index
    df.loc[index_update, 'aw_t_format'] = 4411
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'hm_t_fouls_do'] = 34
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'hm_t_fouls_do'] = 16
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'hm_t_fouls_do'] = 18
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'hm_t_fouls_do'] = 19
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'hm_t_fouls_do'] = 20
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'hm_t_fouls_do'] = 17
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'hm_t_fouls_do'] = 19
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'hm_t_fouls_do'] = 13
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'aw_t_fouls_do'] = 20
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'aw_t_fouls_do'] = 13
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'aw_t_fouls_do'] = 17
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'aw_t_fouls_do'] = 9
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'aw_t_fouls_do'] = 9
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'aw_t_fouls_do'] = 14
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'aw_t_fouls_do'] = 14
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'aw_t_fouls_do'] = 9
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'hm_t_fouls_re'] = 20
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'hm_t_fouls_re'] = 13
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'hm_t_fouls_re'] = 17
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'hm_t_fouls_re'] = 9
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'hm_t_fouls_re'] = 9
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'hm_t_fouls_re'] = 14
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'hm_t_fouls_re'] = 14
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'hm_t_fouls_re'] = 9
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'aw_t_fouls_re'] = 34
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'aw_t_fouls_re'] = 16
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'aw_t_fouls_re'] = 18
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'aw_t_fouls_re'] = 19
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'aw_t_fouls_re'] = 20
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'aw_t_fouls_re'] = 17
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'aw_t_fouls_re'] = 19
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'aw_t_fouls_re'] = 13
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'hm_t_offsid'] = 4
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'hm_t_offsid'] = 3
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'hm_t_offsid'] = 2
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'hm_t_offsid'] = 1
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'hm_t_offsid'] = 2
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'hm_t_offsid'] = 4
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'hm_t_offsid'] = 5
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'hm_t_offsid'] = 4
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'aw_t_offsid'] = 0
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'aw_t_offsid'] = 1
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'aw_t_offsid'] = 2
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'aw_t_offsid'] = 3
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'aw_t_offsid'] = 1
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'aw_t_offsid'] = 2
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'aw_t_offsid'] = 3
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'aw_t_offsid'] = 1
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'hm_t_save'] = 2
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'hm_t_save'] = 3
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'hm_t_save'] = 3
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'hm_t_save'] = 1
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'hm_t_save'] = 3
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'hm_t_save'] = 6
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'hm_t_save'] = 2
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'hm_t_save'] = 6
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'aw_t_save'] = 3
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'aw_t_save'] = 6
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'aw_t_save'] = 1
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'aw_t_save'] = 0
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'aw_t_save'] = 1
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'aw_t_save'] = 0
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'aw_t_save'] = 2
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'aw_t_save'] = 2
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'hm_t_xtg_poss'] = 48
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'hm_t_xtg_poss'] = 59
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'hm_t_xtg_poss'] = 45
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'hm_t_xtg_poss'] = 46
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'hm_t_xtg_poss'] = 41
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'hm_t_xtg_poss'] = 43
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'hm_t_xtg_poss'] = 51
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'hm_t_xtg_poss'] = 31
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'aw_t_xtg_poss'] = 52
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'aw_t_xtg_poss'] = 41
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'aw_t_xtg_poss'] = 55
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'aw_t_xtg_poss'] = 54
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'aw_t_xtg_poss'] = 59
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'aw_t_xtg_poss'] = 57
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'aw_t_xtg_poss'] = 49
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'aw_t_xtg_poss'] = 69
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'hm_t_corner'] = 2
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'hm_t_corner'] = 11
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'hm_t_corner'] = 1
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'hm_t_corner'] = 10
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'hm_t_corner'] = 4
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'hm_t_corner'] = 2
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'hm_t_corner'] = 5
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'hm_t_corner'] = 2
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'aw_t_corner'] = 6
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'aw_t_corner'] = 7
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'aw_t_corner'] = 9
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'aw_t_corner'] = 2
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'aw_t_corner'] = 6
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'aw_t_corner'] = 7
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'aw_t_corner'] = 6
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'aw_t_corner'] = 7
    del index_update

    index_update = df[df['eventId'] == 832074].index
    df.loc[index_update, 'hm_t_shot'] = 7
    del index_update

    index_update = df[df['eventId'] == 832077].index
    df.loc[index_update, 'hm_t_shot'] = 9
    del index_update

    index_update = df[df['eventId'] == 832105].index
    df.loc[index_update, 'hm_t_shot'] = 12
    del index_update

    index_update = df[df['eventId'] == 832005].index
    df.loc[index_update, 'hm_t_shot'] = 17
    del index_update

    index_update = df[df['eventId'] == 832073].index
    df.loc[index_update, 'hm_t_shot'] = 9
    del index_update

    index_update = df[df['eventId'] == 832078].index
    df.loc[index_update, 'hm_t_shot'] = 6
    del index_update

    index_update = df[df['eventId'] == 832080].index
    df.loc[index_update, 'hm_t_shot'] = 9
    del index_update

    index_update = df[df['eventId'] == 832103].index
    df.loc[index_update, 'hm_t_shot'] = 8
    del index_update

    index_update = df[df['eventId'] == 832345].index
    df.loc[index_update, 'hm_t_shot'] = 13
    del index_update

    index_update = df[df['eventId'] == 832074].index
    df.loc[index_update, 'aw_t_shot'] = 6
    del index_update

    index_update = df[df['eventId'] == 832077].index
    df.loc[index_update, 'aw_t_shot'] = 10
    del index_update

    index_update = df[df['eventId'] == 832105].index
    df.loc[index_update, 'aw_t_shot'] = 6
    del index_update

    index_update = df[df['eventId'] == 832005].index
    df.loc[index_update, 'aw_t_shot'] = 7
    del index_update

    index_update = df[df['eventId'] == 832073].index
    df.loc[index_update, 'aw_t_shot'] = 6
    del index_update

    index_update = df[df['eventId'] == 832078].index
    df.loc[index_update, 'aw_t_shot'] = 6
    del index_update

    index_update = df[df['eventId'] == 832080].index
    df.loc[index_update, 'aw_t_shot'] = 9
    del index_update

    index_update = df[df['eventId'] == 832103].index
    df.loc[index_update, 'aw_t_shot'] = 10
    del index_update

    index_update = df[df['eventId'] == 832345].index
    df.loc[index_update, 'aw_t_shot'] = 3
    del index_update

    index_update = df[df['eventId'] == 832074].index
    df.loc[index_update, 'hm_t_shot_gol'] = 3
    del index_update

    index_update = df[df['eventId'] == 832077].index
    df.loc[index_update, 'hm_t_shot_gol'] = 4
    del index_update

    index_update = df[df['eventId'] == 832105].index
    df.loc[index_update, 'hm_t_shot_gol'] = 2
    del index_update

    index_update = df[df['eventId'] == 832005].index
    df.loc[index_update, 'hm_t_shot_gol'] = 8
    del index_update

    index_update = df[df['eventId'] == 832073].index
    df.loc[index_update, 'hm_t_shot_gol'] = 3
    del index_update

    index_update = df[df['eventId'] == 832078].index
    df.loc[index_update, 'hm_t_shot_gol'] = 2
    del index_update

    index_update = df[df['eventId'] == 832080].index
    df.loc[index_update, 'hm_t_shot_gol'] = 4
    del index_update

    index_update = df[df['eventId'] == 832103].index
    df.loc[index_update, 'hm_t_shot_gol'] = 5
    del index_update

    index_update = df[df['eventId'] == 832345].index
    df.loc[index_update, 'hm_t_shot_gol'] = 6
    del index_update

    index_update = df[df['eventId'] == 832074].index
    df.loc[index_update, 'aw_t_shot_gol'] = 4
    del index_update

    index_update = df[df['eventId'] == 832077].index
    df.loc[index_update, 'aw_t_shot_gol'] = 3
    del index_update

    index_update = df[df['eventId'] == 832105].index
    df.loc[index_update, 'aw_t_shot_gol'] = 3
    del index_update

    index_update = df[df['eventId'] == 832005].index
    df.loc[index_update, 'aw_t_shot_gol'] = 1
    del index_update

    index_update = df[df['eventId'] == 832073].index
    df.loc[index_update, 'aw_t_shot_gol'] = 3
    del index_update

    index_update = df[df['eventId'] == 832078].index
    df.loc[index_update, 'aw_t_shot_gol'] = 3
    del index_update

    index_update = df[df['eventId'] == 832080].index
    df.loc[index_update, 'aw_t_shot_gol'] = 3
    del index_update

    index_update = df[df['eventId'] == 832103].index
    df.loc[index_update, 'aw_t_shot_gol'] = 3
    del index_update

    index_update = df[df['eventId'] == 832345].index
    df.loc[index_update, 'aw_t_shot_gol'] = 2
    del index_update

    index_update = df[df['eventId'] == 832074].index
    df.loc[index_update, 'hm_t_xtg_gol'] = 0.429
    del index_update

    index_update = df[df['eventId'] == 832077].index
    df.loc[index_update, 'hm_t_xtg_gol'] = 0.444
    del index_update

    index_update = df[df['eventId'] == 832105].index
    df.loc[index_update, 'hm_t_xtg_gol'] = 0.167
    del index_update

    index_update = df[df['eventId'] == 832005].index
    df.loc[index_update, 'hm_t_xtg_gol'] = 0.471
    del index_update

    index_update = df[df['eventId'] == 832073].index
    df.loc[index_update, 'hm_t_xtg_gol'] = 0.333
    del index_update

    index_update = df[df['eventId'] == 832078].index
    df.loc[index_update, 'hm_t_xtg_gol'] = 0.333
    del index_update

    index_update = df[df['eventId'] == 832080].index
    df.loc[index_update, 'hm_t_xtg_gol'] = 0.444
    del index_update

    index_update = df[df['eventId'] == 832103].index
    df.loc[index_update, 'hm_t_xtg_gol'] = 0.625
    del index_update

    index_update = df[df['eventId'] == 832345].index
    df.loc[index_update, 'hm_t_xtg_gol'] = 0.461
    del index_update

    index_update = df[df['eventId'] == 832074].index
    df.loc[index_update, 'aw_t_xtg_gol'] = 0.667
    del index_update

    index_update = df[df['eventId'] == 832077].index
    df.loc[index_update, 'aw_t_xtg_gol'] = 0.3
    del index_update

    index_update = df[df['eventId'] == 832105].index
    df.loc[index_update, 'aw_t_xtg_gol'] = 0.5
    del index_update

    index_update = df[df['eventId'] == 832005].index
    df.loc[index_update, 'aw_t_xtg_gol'] = 0.143
    del index_update

    index_update = df[df['eventId'] == 832073].index
    df.loc[index_update, 'aw_t_xtg_gol'] = 0.5
    del index_update

    index_update = df[df['eventId'] == 832078].index
    df.loc[index_update, 'aw_t_xtg_gol'] = 0.5
    del index_update

    index_update = df[df['eventId'] == 832080].index
    df.loc[index_update, 'aw_t_xtg_gol'] = 0.333
    del index_update

    index_update = df[df['eventId'] == 832103].index
    df.loc[index_update, 'aw_t_xtg_gol'] = 0.3
    del index_update

    index_update = df[df['eventId'] == 832345].index
    df.loc[index_update, 'aw_t_xtg_gol'] = 0.667
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'hm_t_assis'] = 1
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'hm_t_assis'] = 3
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'hm_t_assis'] = 0
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'hm_t_assis'] = 0
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'hm_t_assis'] = 1
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'hm_t_assis'] = 0
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'hm_t_assis'] = 1
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'hm_t_assis'] = 0
    del index_update

    index_update = df[df['eventId'] == 831959].index
    df.loc[index_update, 'aw_t_assis'] = 2
    del index_update

    index_update = df[df['eventId'] == 831960].index
    df.loc[index_update, 'aw_t_assis'] = 0
    del index_update

    index_update = df[df['eventId'] == 831962].index
    df.loc[index_update, 'aw_t_assis'] = 0
    del index_update

    index_update = df[df['eventId'] == 831989].index
    df.loc[index_update, 'aw_t_assis'] = 0
    del index_update

    index_update = df[df['eventId'] == 831990].index
    df.loc[index_update, 'aw_t_assis'] = 0
    del index_update

    index_update = df[df['eventId'] == 831992].index
    df.loc[index_update, 'aw_t_assis'] = 0
    del index_update

    index_update = df[df['eventId'] == 831993].index
    df.loc[index_update, 'aw_t_assis'] = 0
    del index_update

    index_update = df[df['eventId'] == 832552].index
    df.loc[index_update, 'aw_t_assis'] = 0
    del index_update

    return (df)

def delete_duplicates(df):
    df[['season', 'eventId', 'hm_t_id', 'aw_t_id']].groupby(['season'])
    df.merge(df[(df.season == 2011)][['hm_t_id', 'aw_t_id', 'eventId']])
    d2011 = df[(df.season == 2011)]
    d2011_r = df[(df.season == 2011)][['hm_t_id', 'aw_t_id', 'eventId']]  # dataframe reducido en columnas
    dups = d2011.merge(d2011_r, how='inner', on=['hm_t_id', 'aw_t_id'])
    dups = dups[dups.eventId_x != dups.eventId_y].sort_values(by='hm_t_id')
    dups2 = dups[['eventId_x', 'eventId_y', 'hm_t_id', 'aw_t_id', 'hm_t_n', 'aw_t_n', 'week_0', 'week_1']].sort_values(
        by=['hm_t_id', 'aw_t_id', 'eventId_x'])
    # Eliminamos los duplicados de la jornada 1
    list_of_values = dups2.eventId_x
    drop_index = df[df.eventId.isin(list_of_values) & (df.week_1 == 1)].index
    df = df.drop(drop_index)
    del drop_index
    for index, row in dups2[dups2['week_1'] == 20][['eventId_x', 'eventId_y']].iterrows():
        # print(row['eventId_x'], row['eventId_y'])
        #print("dups2.index =", index)
        update_index = df[df.eventId == row['eventId_x']].eventId.index.values
        #print("row['eventId_x'] = ", row['eventId_x'], "update_index =", update_index)
        #print("row['eventId_y'] = ", row['eventId_y'])
        df.loc[update_index, 'eventId'] = row['eventId_y']
        #print("update hecho", row['eventId_x'], "->", row['eventId_y'])
        del update_index
    drop_index = df[df.eventId == 1226429].index
    df = df.drop(drop_index)
    del drop_index

    return (df)

def alineate_players(df):
    df["hm_t_plyr15_Id"] = df["hm_t_plyr10_Id"]
    df["hm_t_plyr15_n"] = df["hm_t_plyr10_n"]
    df["hm_t_plyr15_posId"] = df["hm_t_plyr10_posId"]
    df["hm_t_plyr15_started"] = df["hm_t_plyr10_started"]
    df["hm_t_plyr15_minutes"] = df["hm_t_plyr10_minutes"]
    df["hm_t_plyr15_gol"] = df["hm_t_plyr10_gol"]
    df["hm_t_plyr15_shots"] = df["hm_t_plyr10_shots"]
    df["hm_t_plyr15_shGoal"] = df["hm_t_plyr10_shGoal"]
    df["hm_t_plyr15_fouls_do"] = df["hm_t_plyr10_fouls_do"]
    df["hm_t_plyr15_yellow_do"] = df["hm_t_plyr10_yellow_do"]

    df["aw_t_plyr15_Id"] = df["aw_t_plyr10_Id"]
    df["aw_t_plyr15_n"] = df["aw_t_plyr10_n"]
    df["aw_t_plyr15_posId"] = df["aw_t_plyr10_posId"]
    df["aw_t_plyr15_started"] = df["aw_t_plyr10_started"]
    df["aw_t_plyr15_minutes"] = df["aw_t_plyr10_minutes"]
    df["aw_t_plyr15_gol"] = df["aw_t_plyr10_gol"]
    df["aw_t_plyr15_shots"] = df["aw_t_plyr10_shots"]
    df["aw_t_plyr15_shGoal"] = df["aw_t_plyr10_shGoal"]
    df["aw_t_plyr15_fouls_do"] = df["aw_t_plyr10_fouls_do"]
    df["aw_t_plyr15_yellow_do"] = df["aw_t_plyr10_yellow_do"]

    return (df)

def alineation_check(df):
    # seguidamente un condicional con cada columna comparando siempre la variable _started para ver si salido de inicio:
    index_hm_t_plyr11 = df.iloc[np.where(df.hm_t_plyr11_started == True)]
    df.loc[index_hm_t_plyr11.index, "hm_t_plyr10_Id"] = df.loc[index_hm_t_plyr11.index]["hm_t_plyr11_Id"]
    df.loc[index_hm_t_plyr11.index, "hm_t_plyr10_Id"] = df.loc[index_hm_t_plyr11.index]["hm_t_plyr11_Id"]
    df.loc[index_hm_t_plyr11.index, "hm_t_plyr10_n"] = df.loc[index_hm_t_plyr11.index]["hm_t_plyr11_n"]
    df.loc[index_hm_t_plyr11.index, "hm_t_plyr10_posId"] = df.loc[index_hm_t_plyr11.index]["hm_t_plyr11_posId"]
    df.loc[index_hm_t_plyr11.index, "hm_t_plyr10_started"] = df.loc[index_hm_t_plyr11.index]["hm_t_plyr11_started"]
    df.loc[index_hm_t_plyr11.index, "hm_t_plyr10_minutes"] = df.loc[index_hm_t_plyr11.index]["hm_t_plyr11_minutes"]
    df.loc[index_hm_t_plyr11.index, "hm_t_plyr10_gol"] = df.loc[index_hm_t_plyr11.index]["hm_t_plyr11_gol"]
    df.loc[index_hm_t_plyr11.index, "hm_t_plyr10_shots"] = df.loc[index_hm_t_plyr11.index]["hm_t_plyr11_shots"]
    df.loc[index_hm_t_plyr11.index, "hm_t_plyr10_shGoal"] = df.loc[index_hm_t_plyr11.index]["hm_t_plyr11_shGoal"]
    df.loc[index_hm_t_plyr11.index, "hm_t_plyr10_fouls_do"] = df.loc[index_hm_t_plyr11.index]["hm_t_plyr11_fouls_do"]
    df.loc[index_hm_t_plyr11.index, "hm_t_plyr10_yellow_do"] = df.loc[index_hm_t_plyr11.index]["hm_t_plyr11_yellow_do"]
    index_hm_t_plyr12 = df.iloc[np.where(df.hm_t_plyr12_started == True)]
    df.loc[index_hm_t_plyr12.index, "hm_t_plyr10_Id"] = df.loc[index_hm_t_plyr12.index]["hm_t_plyr12_Id"]
    df.loc[index_hm_t_plyr12.index, "hm_t_plyr10_n"] = df.loc[index_hm_t_plyr12.index]["hm_t_plyr12_n"]
    df.loc[index_hm_t_plyr12.index, "hm_t_plyr10_posId"] = df.loc[index_hm_t_plyr12.index]["hm_t_plyr12_posId"]
    df.loc[index_hm_t_plyr12.index, "hm_t_plyr10_started"] = df.loc[index_hm_t_plyr12.index]["hm_t_plyr12_started"]
    df.loc[index_hm_t_plyr12.index, "hm_t_plyr10_minutes"] = df.loc[index_hm_t_plyr12.index]["hm_t_plyr12_minutes"]
    df.loc[index_hm_t_plyr12.index, "hm_t_plyr10_gol"] = df.loc[index_hm_t_plyr12.index]["hm_t_plyr12_gol"]
    df.loc[index_hm_t_plyr12.index, "hm_t_plyr10_shots"] = df.loc[index_hm_t_plyr12.index]["hm_t_plyr12_shots"]
    df.loc[index_hm_t_plyr12.index, "hm_t_plyr10_shGoal"] = df.loc[index_hm_t_plyr12.index]["hm_t_plyr12_shGoal"]
    df.loc[index_hm_t_plyr12.index, "hm_t_plyr10_fouls_do"] = df.loc[index_hm_t_plyr12.index]["hm_t_plyr12_fouls_do"]
    df.loc[index_hm_t_plyr12.index, "hm_t_plyr10_yellow_do"] = df.loc[index_hm_t_plyr12.index]["hm_t_plyr12_yellow_do"]
    index_hm_t_plyr13 = df.iloc[np.where(df.hm_t_plyr13_started == True)]
    df.loc[index_hm_t_plyr13.index, "hm_t_plyr10_Id"] = df.loc[index_hm_t_plyr13.index]["hm_t_plyr13_Id"]
    df.loc[index_hm_t_plyr13.index, "hm_t_plyr10_n"] = df.loc[index_hm_t_plyr13.index]["hm_t_plyr13_n"]
    df.loc[index_hm_t_plyr13.index, "hm_t_plyr10_posId"] = df.loc[index_hm_t_plyr13.index]["hm_t_plyr13_posId"]
    df.loc[index_hm_t_plyr13.index, "hm_t_plyr10_started"] = df.loc[index_hm_t_plyr13.index]["hm_t_plyr13_started"]
    df.loc[index_hm_t_plyr13.index, "hm_t_plyr10_minutes"] = df.loc[index_hm_t_plyr13.index]["hm_t_plyr13_minutes"]
    df.loc[index_hm_t_plyr13.index, "hm_t_plyr10_gol"] = df.loc[index_hm_t_plyr13.index]["hm_t_plyr13_gol"]
    df.loc[index_hm_t_plyr13.index, "hm_t_plyr10_shots"] = df.loc[index_hm_t_plyr13.index]["hm_t_plyr13_shots"]
    df.loc[index_hm_t_plyr13.index, "hm_t_plyr10_shGoal"] = df.loc[index_hm_t_plyr13.index]["hm_t_plyr13_shGoal"]
    df.loc[index_hm_t_plyr13.index, "hm_t_plyr10_fouls_do"] = df.loc[index_hm_t_plyr13.index]["hm_t_plyr13_fouls_do"]
    df.loc[index_hm_t_plyr13.index, "hm_t_plyr10_yellow_do"] = df.loc[index_hm_t_plyr13.index]["hm_t_plyr13_yellow_do"]
    index_hm_t_plyr14 = df.iloc[np.where(df.hm_t_plyr14_started == True)]
    df.loc[index_hm_t_plyr14.index, "hm_t_plyr10_Id"] = df.loc[index_hm_t_plyr14.index]["hm_t_plyr14_Id"]
    df.loc[index_hm_t_plyr14.index, "hm_t_plyr10_n"] = df.loc[index_hm_t_plyr14.index]["hm_t_plyr14_n"]
    df.loc[index_hm_t_plyr14.index, "hm_t_plyr10_posId"] = df.loc[index_hm_t_plyr14.index]["hm_t_plyr14_posId"]
    df.loc[index_hm_t_plyr14.index, "hm_t_plyr10_started"] = df.loc[index_hm_t_plyr14.index]["hm_t_plyr14_started"]
    df.loc[index_hm_t_plyr14.index, "hm_t_plyr10_minutes"] = df.loc[index_hm_t_plyr14.index]["hm_t_plyr14_minutes"]
    df.loc[index_hm_t_plyr14.index, "hm_t_plyr10_gol"] = df.loc[index_hm_t_plyr14.index]["hm_t_plyr14_gol"]
    df.loc[index_hm_t_plyr14.index, "hm_t_plyr10_shots"] = df.loc[index_hm_t_plyr14.index]["hm_t_plyr14_shots"]
    df.loc[index_hm_t_plyr14.index, "hm_t_plyr10_shGoal"] = df.loc[index_hm_t_plyr14.index]["hm_t_plyr14_shGoal"]
    df.loc[index_hm_t_plyr14.index, "hm_t_plyr10_fouls_do"] = df.loc[index_hm_t_plyr14.index]["hm_t_plyr14_fouls_do"]
    df.loc[index_hm_t_plyr14.index, "hm_t_plyr10_yellow_do"] = df.loc[index_hm_t_plyr14.index]["hm_t_plyr14_yellow_do"]

    ###    AWAY TEAM    ###

    index_aw_t_plyr11 = df.iloc[np.where(df.aw_t_plyr11_started == True)]
    df.loc[index_aw_t_plyr11.index, "aw_t_plyr10_Id"] = df.loc[index_aw_t_plyr11.index]["aw_t_plyr11_Id"]
    df.loc[index_aw_t_plyr11.index, "aw_t_plyr10_Id"] = df.loc[index_aw_t_plyr11.index]["aw_t_plyr11_Id"]
    df.loc[index_aw_t_plyr11.index, "aw_t_plyr10_n"] = df.loc[index_aw_t_plyr11.index]["aw_t_plyr11_n"]
    df.loc[index_aw_t_plyr11.index, "aw_t_plyr10_posId"] = df.loc[index_aw_t_plyr11.index]["aw_t_plyr11_posId"]
    df.loc[index_aw_t_plyr11.index, "aw_t_plyr10_started"] = df.loc[index_aw_t_plyr11.index]["aw_t_plyr11_started"]
    df.loc[index_aw_t_plyr11.index, "aw_t_plyr10_minutes"] = df.loc[index_aw_t_plyr11.index]["aw_t_plyr11_minutes"]
    df.loc[index_aw_t_plyr11.index, "aw_t_plyr10_gol"] = df.loc[index_aw_t_plyr11.index]["aw_t_plyr11_gol"]
    df.loc[index_aw_t_plyr11.index, "aw_t_plyr10_shots"] = df.loc[index_aw_t_plyr11.index]["aw_t_plyr11_shots"]
    df.loc[index_aw_t_plyr11.index, "aw_t_plyr10_shGoal"] = df.loc[index_aw_t_plyr11.index]["aw_t_plyr11_shGoal"]
    df.loc[index_aw_t_plyr11.index, "aw_t_plyr10_fouls_do"] = df.loc[index_aw_t_plyr11.index]["aw_t_plyr11_fouls_do"]
    df.loc[index_aw_t_plyr11.index, "aw_t_plyr10_yellow_do"] = df.loc[index_aw_t_plyr11.index]["aw_t_plyr11_yellow_do"]
    index_aw_t_plyr12 = df.iloc[np.where(df.aw_t_plyr12_started == True)]
    df.loc[index_aw_t_plyr12.index, "aw_t_plyr10_Id"] = df.loc[index_aw_t_plyr12.index]["aw_t_plyr12_Id"]
    df.loc[index_aw_t_plyr12.index, "aw_t_plyr10_n"] = df.loc[index_aw_t_plyr12.index]["aw_t_plyr12_n"]
    df.loc[index_aw_t_plyr12.index, "aw_t_plyr10_posId"] = df.loc[index_aw_t_plyr12.index]["aw_t_plyr12_posId"]
    df.loc[index_aw_t_plyr12.index, "aw_t_plyr10_started"] = df.loc[index_aw_t_plyr12.index]["aw_t_plyr12_started"]
    df.loc[index_aw_t_plyr12.index, "aw_t_plyr10_minutes"] = df.loc[index_aw_t_plyr12.index]["aw_t_plyr12_minutes"]
    df.loc[index_aw_t_plyr12.index, "aw_t_plyr10_gol"] = df.loc[index_aw_t_plyr12.index]["aw_t_plyr12_gol"]
    df.loc[index_aw_t_plyr12.index, "aw_t_plyr10_shots"] = df.loc[index_aw_t_plyr12.index]["aw_t_plyr12_shots"]
    df.loc[index_aw_t_plyr12.index, "aw_t_plyr10_shGoal"] = df.loc[index_aw_t_plyr12.index]["aw_t_plyr12_shGoal"]
    df.loc[index_aw_t_plyr12.index, "aw_t_plyr10_fouls_do"] = df.loc[index_aw_t_plyr12.index]["aw_t_plyr12_fouls_do"]
    df.loc[index_aw_t_plyr12.index, "aw_t_plyr10_yellow_do"] = df.loc[index_aw_t_plyr12.index]["aw_t_plyr12_yellow_do"]
    index_aw_t_plyr13 = df.iloc[np.where(df.aw_t_plyr13_started == True)]
    df.loc[index_aw_t_plyr13.index, "aw_t_plyr10_Id"] = df.loc[index_aw_t_plyr13.index]["aw_t_plyr13_Id"]
    df.loc[index_aw_t_plyr13.index, "aw_t_plyr10_n"] = df.loc[index_aw_t_plyr13.index]["aw_t_plyr13_n"]
    df.loc[index_aw_t_plyr13.index, "aw_t_plyr10_posId"] = df.loc[index_aw_t_plyr13.index]["aw_t_plyr13_posId"]
    df.loc[index_aw_t_plyr13.index, "aw_t_plyr10_started"] = df.loc[index_aw_t_plyr13.index]["aw_t_plyr13_started"]
    df.loc[index_aw_t_plyr13.index, "aw_t_plyr10_minutes"] = df.loc[index_aw_t_plyr13.index]["aw_t_plyr13_minutes"]
    df.loc[index_aw_t_plyr13.index, "aw_t_plyr10_gol"] = df.loc[index_aw_t_plyr13.index]["aw_t_plyr13_gol"]
    df.loc[index_aw_t_plyr13.index, "aw_t_plyr10_shots"] = df.loc[index_aw_t_plyr13.index]["aw_t_plyr13_shots"]
    df.loc[index_aw_t_plyr13.index, "aw_t_plyr10_shGoal"] = df.loc[index_aw_t_plyr13.index]["aw_t_plyr13_shGoal"]
    df.loc[index_aw_t_plyr13.index, "aw_t_plyr10_fouls_do"] = df.loc[index_aw_t_plyr13.index]["aw_t_plyr13_fouls_do"]
    df.loc[index_aw_t_plyr13.index, "aw_t_plyr10_yellow_do"] = df.loc[index_aw_t_plyr13.index]["aw_t_plyr13_yellow_do"]
    index_aw_t_plyr14 = df.iloc[np.where(df.aw_t_plyr14_started == True)]
    df.loc[index_aw_t_plyr14.index, "aw_t_plyr10_Id"] = df.loc[index_aw_t_plyr14.index]["aw_t_plyr14_Id"]
    df.loc[index_aw_t_plyr14.index, "aw_t_plyr10_n"] = df.loc[index_aw_t_plyr14.index]["aw_t_plyr14_n"]
    df.loc[index_aw_t_plyr14.index, "aw_t_plyr10_posId"] = df.loc[index_aw_t_plyr14.index]["aw_t_plyr14_posId"]
    df.loc[index_aw_t_plyr14.index, "aw_t_plyr10_started"] = df.loc[index_aw_t_plyr14.index]["aw_t_plyr14_started"]
    df.loc[index_aw_t_plyr14.index, "aw_t_plyr10_minutes"] = df.loc[index_aw_t_plyr14.index]["aw_t_plyr14_minutes"]
    df.loc[index_aw_t_plyr14.index, "aw_t_plyr10_gol"] = df.loc[index_aw_t_plyr14.index]["aw_t_plyr14_gol"]
    df.loc[index_aw_t_plyr14.index, "aw_t_plyr10_shots"] = df.loc[index_aw_t_plyr14.index]["aw_t_plyr14_shots"]
    df.loc[index_aw_t_plyr14.index, "aw_t_plyr10_shGoal"] = df.loc[index_aw_t_plyr14.index]["aw_t_plyr14_shGoal"]
    df.loc[index_aw_t_plyr14.index, "aw_t_plyr10_fouls_do"] = df.loc[index_aw_t_plyr14.index]["aw_t_plyr14_fouls_do"]
    df.loc[index_aw_t_plyr14.index, "aw_t_plyr10_yellow_do"] = df.loc[index_aw_t_plyr14.index]["aw_t_plyr14_yellow_do"]

    df.drop(["hm_t_plyr11_Id", "hm_t_plyr11_n", "hm_t_plyr11_posId", "hm_t_plyr11_started", "hm_t_plyr11_minutes",
            "hm_t_plyr11_gol", "hm_t_plyr11_shots",
            "hm_t_plyr11_shGoal", "hm_t_plyr11_fouls_do", "hm_t_plyr11_yellow_do", "hm_t_plyr12_Id", "hm_t_plyr12_n",
            "hm_t_plyr12_posId",
            "hm_t_plyr12_started", "hm_t_plyr12_minutes", "hm_t_plyr12_gol", "hm_t_plyr12_shots", "hm_t_plyr12_shGoal",
            "hm_t_plyr12_fouls_do", "hm_t_plyr12_yellow_do", "aw_t_plyr11_shots", "aw_t_plyr11_shGoal",
            "aw_t_plyr11_fouls_do",
            "aw_t_plyr11_yellow_do", "aw_t_plyr12_Id", "aw_t_plyr12_n", "aw_t_plyr12_posId", "aw_t_plyr12_started",
            "aw_t_plyr12_minutes",
            "aw_t_plyr12_gol", "aw_t_plyr12_shots", "aw_t_plyr12_shGoal", "aw_t_plyr12_fouls_do",
            "aw_t_plyr12_yellow_do", "aw_t_plyr13_Id",
            "aw_t_plyr13_n", "aw_t_plyr13_posId", "aw_t_plyr13_started", "aw_t_plyr13_minutes", "aw_t_plyr13_gol",
            "aw_t_plyr13_shots",
            "aw_t_plyr13_shGoal", "aw_t_plyr13_fouls_do", "aw_t_plyr13_yellow_do", "hm_t_plyr13_Id", "hm_t_plyr13_n",
            "hm_t_plyr13_posId",
            "hm_t_plyr13_started", "hm_t_plyr13_minutes", "hm_t_plyr13_gol", "hm_t_plyr13_shots", "hm_t_plyr13_shGoal",
            "hm_t_plyr13_fouls_do",
            "hm_t_plyr13_yellow_do", "aw_t_plyr14_Id", "aw_t_plyr14_n", "aw_t_plyr14_posId", "aw_t_plyr14_started",
            "aw_t_plyr14_minutes",
            "aw_t_plyr14_gol", "aw_t_plyr14_shots", "aw_t_plyr14_shGoal", "aw_t_plyr14_fouls_do",
            "aw_t_plyr14_yellow_do", "hm_t_plyr14_Id",
            "hm_t_plyr14_n", "hm_t_plyr14_posId", "hm_t_plyr14_started", "hm_t_plyr14_minutes", "hm_t_plyr14_gol",
            "hm_t_plyr14_shots", "hm_t_plyr14_shGoal", "hm_t_plyr14_fouls_do", "hm_t_plyr14_yellow_do"
            ], inplace=True, axis=1)

    fouls_do = df[df.aw_t_plyr0_fouls_do.isna() == True][
        ['eventId', 'season', 'hm_t_plyr0_Id', 'hm_t_plyr0_fouls_do', 'hm_t_plyr1_Id',
         'hm_t_plyr1_fouls_do', 'hm_t_plyr2_Id', 'hm_t_plyr2_fouls_do', 'hm_t_plyr3_Id',
         'hm_t_plyr3_fouls_do', 'hm_t_plyr4_Id', 'hm_t_plyr4_fouls_do', 'hm_t_plyr5_Id',
         'hm_t_plyr5_fouls_do', 'hm_t_plyr6_Id', 'hm_t_plyr6_fouls_do', 'hm_t_plyr7_Id',
         'hm_t_plyr7_fouls_do', 'hm_t_plyr8_Id', 'hm_t_plyr8_fouls_do', 'hm_t_plyr9_Id',
         'hm_t_plyr9_fouls_do', 'hm_t_plyr10_Id', 'hm_t_plyr10_fouls_do', 'aw_t_plyr0_Id',
         'aw_t_plyr0_fouls_do', 'aw_t_plyr1_Id', 'aw_t_plyr1_fouls_do', 'aw_t_plyr2_Id',
         'aw_t_plyr2_fouls_do', 'aw_t_plyr3_Id', 'aw_t_plyr3_fouls_do', 'aw_t_plyr4_Id',
         'aw_t_plyr4_fouls_do', 'aw_t_plyr5_Id', 'aw_t_plyr5_fouls_do', 'aw_t_plyr6_Id',
         'aw_t_plyr6_fouls_do', 'aw_t_plyr7_Id', 'aw_t_plyr7_fouls_do', 'aw_t_plyr8_Id',
         'aw_t_plyr8_fouls_do', 'aw_t_plyr9_Id', 'aw_t_plyr9_fouls_do', 'aw_t_plyr10_Id',
         'aw_t_plyr10_fouls_do']]
    fouls_do[['season']].drop_duplicates()
    return (df, fouls_do)

def web_scrap_fouls_do(df, fouls_do):
    hm_var = pd.DataFrame(
        {'id': ['hm_t_plyr0_Id', 'hm_t_plyr1_Id', 'hm_t_plyr2_Id', 'hm_t_plyr3_Id', 'hm_t_plyr4_Id', 'hm_t_plyr5_Id',
                'hm_t_plyr6_Id', 'hm_t_plyr7_Id', 'hm_t_plyr8_Id', 'hm_t_plyr9_Id', 'hm_t_plyr10_Id'],
         'pname': ['hm_t_plyr0_n', 'hm_t_plyr1_n', 'hm_t_plyr2_n', 'hm_t_plyr3_n', 'hm_t_plyr4_n', 'hm_t_plyr5_n',
                   'hm_t_plyr6_n', 'hm_t_plyr7_n', 'hm_t_plyr8_n', 'hm_t_plyr9_n', 'hm_t_plyr10_n'],
         'fouls_do': ['hm_t_plyr0_fouls_do', 'hm_t_plyr1_fouls_do', 'hm_t_plyr2_fouls_do', 'hm_t_plyr3_fouls_do',
                      'hm_t_plyr4_fouls_do', 'hm_t_plyr5_fouls_do', 'hm_t_plyr6_fouls_do', 'hm_t_plyr7_fouls_do',
                      'hm_t_plyr8_fouls_do', 'hm_t_plyr9_fouls_do', 'hm_t_plyr10_fouls_do']})
    aw_var = pd.DataFrame(
        {'id': ['aw_t_plyr0_Id', 'aw_t_plyr1_Id', 'aw_t_plyr2_Id', 'aw_t_plyr3_Id', 'aw_t_plyr4_Id', 'aw_t_plyr5_Id',
                'aw_t_plyr6_Id', 'aw_t_plyr7_Id', 'aw_t_plyr8_Id', 'aw_t_plyr9_Id', 'aw_t_plyr10_Id'],
         'pname': ['aw_t_plyr0_n', 'aw_t_plyr1_n', 'aw_t_plyr2_n', 'aw_t_plyr3_n', 'aw_t_plyr4_n', 'aw_t_plyr5_n',
                   'aw_t_plyr6_n', 'aw_t_plyr7_n', 'aw_t_plyr8_n', 'aw_t_plyr9_n', 'aw_t_plyr10_n'],
         'fouls_do': ['aw_t_plyr0_fouls_do', 'aw_t_plyr1_fouls_do', 'aw_t_plyr2_fouls_do', 'aw_t_plyr3_fouls_do',
                      'aw_t_plyr4_fouls_do', 'aw_t_plyr5_fouls_do', 'aw_t_plyr6_fouls_do', 'aw_t_plyr7_fouls_do',
                      'aw_t_plyr8_fouls_do', 'aw_t_plyr9_fouls_do', 'aw_t_plyr10_fouls_do']})

    player_mean_acum = 0
    for index, row in hm_var.iterrows():
        # print("'",row.id,"'",sep='')
        vector = df[df[row.id] == 348490][row.fouls_do].values
        #     print("vector",vector)
        player_mean = np.nan_to_num(np.nan_to_num(vector).mean())
        #     print("player_mean",player_mean)
        player_mean_acum = player_mean_acum + player_mean
    #     print("player_mean_acum",player_mean_acum)
    #     print()

    # Modificamos los partidos con fouls_do nulos para los jugadores locales
    for index, row in fouls_do.iterrows():

        update_index = df[df.eventId == row['eventId']].eventId.index.values
        # print("update_index",update_index)
        # print()

        for indexH, rowH in hm_var.iterrows():
            #         print("player_id",row[rowH.id])
            #         print("player_name",c[c[rowH.id]==row[rowH.id]][[rowH.pname]].drop_duplicates().values)
            player_fouls_do_acum = 0
            player_mean_acum = 0
            num_matches = 0
            for indexV, rowV in hm_var.iterrows():
                vector = df[(df[rowV.id] == row[rowH.id])][rowV.fouls_do].values
                # print("vector",vector)
                if vector.size > 0:
                    num_matches = num_matches + vector.size
                    player_fouls_do = np.nan_to_num(vector).sum()
                    # print("player_clears",player_clears)
                    player_fouls_do_acum = player_fouls_do_acum + player_fouls_do

            if (num_matches > 0):
                player_mean_acum = player_fouls_do_acum / num_matches
            else:
                player_mean_acum = 0

            #         print("update_index",update_index)
            #         print("player_mean_acum",player_mean_acum)
            #         print("rowH.fouls_do",rowH.fouls_do)
            #         print()

            df.loc[update_index, rowH.fouls_do] = round(player_mean_acum)

        # d.loc[update_index,'hm_t_cross'] = hmcm[hmcm.hm_t_id==row['hm_t_id']]['mean'].values
        # d.loc[update_index,'aw_t_cross'] = awcm[awcm.aw_t_id==row['aw_t_id']]['mean'].values
        # print("hm_mean:",hmcm[hmcm.hm_t_id==row['hm_t_id']]['mean'].values)
        # print("aw_mean:",awcm[awcm.aw_t_id==row['aw_t_id']]['mean'].values)
        del update_index

        return (df)
## SALTA ERROR EN ROLLING WINDOWS -> ValueError: Length of values (16121) does not match length of index (16122)
def create_rolling_windows(df):
    df["hm_hm_t_roll3_win"] = df.groupby("hm_t_id")["hm_t_win"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_los"] = df.groupby("hm_t_id")["hm_t_los"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_tie"] = df.groupby("hm_t_id")["hm_t_tie"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_gol"] = df.groupby("hm_t_id")["hm_t_gol"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_autogol"] = df.groupby("hm_t_id")["hm_t_autogol"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_assis"] = df.groupby("hm_t_id")["hm_t_assis"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_shot"] = df.groupby("hm_t_id")["hm_t_shot"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_shot_gol"] = df.groupby("hm_t_id")["hm_t_shot_gol"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_save"] = df.groupby("hm_t_id")["hm_t_save"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_cross"] = df.groupby("hm_t_id")["hm_t_cross"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_pty"] = df.groupby("hm_t_id")["hm_t_pty"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_fouls_do"] = df.groupby("hm_t_id")["hm_t_fouls_do"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_fouls_re"] = df.groupby("hm_t_id")["hm_t_fouls_re"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_yel_card"] = df.groupby("hm_t_id")["hm_t_yel_card"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_red_card"] = df.groupby("hm_t_id")["hm_t_red_card"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_offsid"] = df.groupby("hm_t_id")["hm_t_offsid"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_corner"] = df.groupby("hm_t_id")["hm_t_corner"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_catch"] = df.groupby("hm_t_id")["hm_t_catch"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_punch"] = df.groupby("hm_t_id")["hm_t_punch"].rolling(3, closed="left").mean().values
    df["hm_hm_t_roll3_xtg_poss"] = df.groupby("hm_t_id")["hm_t_xtg_poss"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_win"] = df.groupby("hm_t_id")["aw_t_win"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_los"] = df.groupby("hm_t_id")["aw_t_los"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_tie"] = df.groupby("hm_t_id")["aw_t_tie"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_gol"] = df.groupby("hm_t_id")["aw_t_gol"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_autogol"] = df.groupby("hm_t_id")["aw_t_autogol"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_assis"] = df.groupby("hm_t_id")["aw_t_assis"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_shot"] = df.groupby("hm_t_id")["aw_t_shot"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_shot_gol"] = df.groupby("hm_t_id")["aw_t_shot_gol"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_save"] = df.groupby("hm_t_id")["aw_t_save"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_cross"] = df.groupby("hm_t_id")["aw_t_cross"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_pty"] = df.groupby("hm_t_id")["aw_t_pty"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_fouls_do"] = df.groupby("hm_t_id")["aw_t_fouls_do"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_fouls_re"] = df.groupby("hm_t_id")["aw_t_fouls_re"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_yel_card"] = df.groupby("hm_t_id")["aw_t_yel_card"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_red_card"] = df.groupby("hm_t_id")["aw_t_red_card"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_offsid"] = df.groupby("hm_t_id")["aw_t_offsid"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_corner"] = df.groupby("hm_t_id")["aw_t_corner"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_catch"] = df.groupby("hm_t_id")["aw_t_catch"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_punch"] = df.groupby("hm_t_id")["aw_t_punch"].rolling(3, closed="left").mean().values
    df["hm_aw_t_roll3_xtg_poss"] = df.groupby("hm_t_id")["aw_t_xtg_poss"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_win"] = df.groupby("aw_t_id")["aw_t_win"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_los"] = df.groupby("aw_t_id")["aw_t_los"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_tie"] = df.groupby("aw_t_id")["aw_t_tie"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_gol"] = df.groupby("aw_t_id")["aw_t_gol"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_autogol"] = df.groupby("aw_t_id")["aw_t_autogol"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_assis"] = df.groupby("aw_t_id")["aw_t_assis"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_shot"] = df.groupby("aw_t_id")["aw_t_shot"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_shot_gol"] = df.groupby("aw_t_id")["aw_t_shot_gol"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_save"] = df.groupby("aw_t_id")["aw_t_save"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_cross"] = df.groupby("aw_t_id")["aw_t_cross"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_pty"] = df.groupby("aw_t_id")["aw_t_pty"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_fouls_do"] = df.groupby("aw_t_id")["aw_t_fouls_do"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_fouls_re"] = df.groupby("aw_t_id")["aw_t_fouls_re"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_yel_card"] = df.groupby("aw_t_id")["aw_t_yel_card"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_red_card"] = df.groupby("aw_t_id")["aw_t_red_card"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_offsid"] = df.groupby("aw_t_id")["aw_t_offsid"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_corner"] = df.groupby("aw_t_id")["aw_t_corner"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_catch"] = df.groupby("aw_t_id")["aw_t_catch"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_punch"] = df.groupby("aw_t_id")["aw_t_punch"].rolling(3, closed="left").mean().values
    df["aw_aw_t_roll3_xtg_poss"] = df.groupby("aw_t_id")["aw_t_xtg_poss"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_win"] = df.groupby("aw_t_id")["hm_t_win"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_los"] = df.groupby("aw_t_id")["hm_t_los"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_tie"] = df.groupby("aw_t_id")["hm_t_tie"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_gol"] = df.groupby("aw_t_id")["hm_t_gol"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_autogol"] = df.groupby("aw_t_id")["hm_t_autogol"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_assis"] = df.groupby("aw_t_id")["hm_t_assis"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_shot"] = df.groupby("aw_t_id")["hm_t_shot"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_shot_gol"] = df.groupby("aw_t_id")["hm_t_shot_gol"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_save"] = df.groupby("aw_t_id")["hm_t_save"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_cross"] = df.groupby("aw_t_id")["hm_t_cross"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_pty"] = df.groupby("aw_t_id")["hm_t_pty"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_fouls_do"] = df.groupby("aw_t_id")["hm_t_fouls_do"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_fouls_re"] = df.groupby("aw_t_id")["hm_t_fouls_re"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_yel_card"] = df.groupby("aw_t_id")["hm_t_yel_card"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_red_card"] = df.groupby("aw_t_id")["hm_t_red_card"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_offsid"] = df.groupby("aw_t_id")["hm_t_offsid"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_corner"] = df.groupby("aw_t_id")["hm_t_corner"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_catch"] = df.groupby("aw_t_id")["hm_t_catch"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_punch"] = df.groupby("aw_t_id")["hm_t_punch"].rolling(3, closed="left").mean().values
    df["aw_hm_t_roll3_xtg_poss"] = df.groupby("aw_t_id")["hm_t_xtg_poss"].rolling(3, closed="left").mean().values

    attributes = ['roll3_win', 'roll3_los', 'roll3_tie', 'roll3_gol', 'roll3_autogol', 'roll3_assis', 'roll3_shot',
                  'roll3_shot_gol', 'roll3_save', 'roll3_cross',
                  'roll3_pty', 'roll3_fouls_do', 'roll3_fouls_re', 'roll3_yel_card', 'roll3_red_card', 'roll3_offsid',
                  'roll3_corner', 'roll3_catch', 'roll3_punch', ]
    for attribute in attributes:
        x = df['hm_hm_t_' + attribute].mean()
        df['hm_hm_t_' + attribute] = df['hm_hm_t_' + attribute].fillna(x)
        y = df['aw_hm_t_' + attribute].mean()
        df['aw_hm_t_' + attribute] = df['aw_hm_t_' + attribute].fillna(y)
        z = df['hm_aw_t_' + attribute].mean()
        df['hm_aw_t_' + attribute] = df['hm_aw_t_' + attribute].fillna(z)
        t = df['aw_aw_t_' + attribute].mean()
        df['aw_aw_t_' + attribute] = df['aw_aw_t_' + attribute].fillna(t)

    return (df)

def fill_last_nas(df):
    attributes = ['catch', 'punch']

    for attribute in attributes:
        df['hm_t_' + attribute] = df['hm_t_' + attribute].fillna(0)
        df['aw_t_' + attribute] = df['aw_t_' + attribute].fillna(0)

    return (df)

def web_scrapping_results(df):
    # merge_pos = read_csv('/Users/lmjov/Documents/MASTER BIG DATA/Proyecto/Luis/5. Merge Posesion.csv')
    merge_pos = pd.read_csv('/Users/paues/Desktop/MASTER/TFM/dades/TEST/a/web scraping_5._Merge_Posesion.csv')

    for index, row in merge_pos.iterrows():
        update_index = df[df.eventId == row.eventId].index
        df.loc[update_index, 'hm_t_xtg_poss'] = row.hm_t_xtg_poss
        df.loc[update_index, 'aw_t_xtg_poss'] = row.aw_t_xtg_poss
        del update_index

    return (df)