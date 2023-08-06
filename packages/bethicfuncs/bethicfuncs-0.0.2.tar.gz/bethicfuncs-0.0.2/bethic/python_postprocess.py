import pandas as pd
import numpy as np

def join_with_coach(df1, df2):
    df1 = pd.merge(df1, df2,  how='left', left_on=['week_0','hm_t_id','season'],
                right_on = ['jornada','Team_id','Temporada'])
    df1 = df1.rename(columns={'Apodo y Nombre': 'hm_t_coach_n', 'CODIGO_ENTREN': 'hm_t_coach_id'})

    df1 = pd.merge(df1, df2,  how='left', left_on=['week_0','aw_t_id','season'],
                  right_on = ['jornada','Team_id','Temporada'])
    df1 = df1.rename(columns={'Apodo y Nombre': 'aw_t_coach_n', 'CODIGO_ENTREN': 'aw_t_coach_id'})

    df = df1.drop(['jornada_y', 'Team_id_y', 'Temporada_y', 'Name Team_y', 'jornada_x', 'Team_id_x', 'Temporada_x', 'Name Team_x'],
           inplace=True, axis=1)
    return (df)

def generate_result_variable(df):
    df['Match result'] = np.where(
        df['hm_t_win'] == 1, 3, np.where(
        df['aw_t_win'] == 1, 0, 1))
    df['Match result'] = df['Match result'].astype(object)
    return (df)