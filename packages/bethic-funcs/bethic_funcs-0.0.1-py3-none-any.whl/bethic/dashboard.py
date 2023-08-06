import pandas as pd
import numpy as np
import altair as alt

def plot_all(df):
    def plot_win_los_tie_teams(df):
        d2_1 = df[['season', 'hm_t_n', 'hm_t_win', 'hm_t_los', 'hm_t_tie']]
        d2_2 = df[['season', 'aw_t_n', 'aw_t_win', 'aw_t_los', 'aw_t_tie']]
        d2_1 = d2_1.sort_values(by=['hm_t_n'])
        d2_2 = d2_2.sort_values(by=['aw_t_n'])
        d2_1 = d2_1.groupby(['season', 'hm_t_n'], as_index=False).max()
        d2_2 = d2_2.groupby(['season', 'aw_t_n'], as_index=False).max()
        d2_1 = d2_1.groupby('hm_t_n', as_index=False).sum()
        d2_2 = d2_2.groupby('aw_t_n', as_index=False).sum()
        d2 = pd.concat([d2_1, d2_2], axis=1)
        d2 = d2.drop(['aw_t_n', 'season'], axis=1)
        d2 = d2.rename(columns={'hm_t_n': 'Teams'})
        d2_3 = d2.melt('Teams', var_name='team', value_name='amount')
        plot = alt.Chart(d2_3).mark_bar().encode(
            x='team:O',
            y='amount:Q',
            color='team:N',
            column='Teams:N'
        )
        return (plot)

    def plot_goals(df):
        d5_1 = df[['season', 'hm_t_n', 'hm_t_gol']]
        d5_2 = df[['season', 'aw_t_n', 'aw_t_gol']]
        d5_1 = d5_1.sort_values(by=['hm_t_n'])
        d5_2 = d5_2.sort_values(by=['aw_t_n'])
        d5_1 = d5_1.groupby('hm_t_n', as_index=False).sum()
        d5_2 = d5_2.groupby('aw_t_n', as_index=False).sum()
        d2 = pd.concat([d5_1, d5_2], axis=1)
        d2 = d2.drop(['aw_t_n', 'season'], axis=1)
        d2 = d2.rename(columns={'hm_t_n': 'Teams'})
        d5_3 = d2.melt('Teams', var_name='team', value_name='amount')
        plot = alt.Chart(d5_3).mark_bar().encode(
            x='team:O',
            y='amount:Q',
            color='team:N',
            column='Teams:N'
        )
        return (plot)

    def plot_autogols(df):
        d6_1 = df[['season', 'hm_t_n', 'hm_t_autogol']]
        d6_2 = df[['season', 'aw_t_n', 'aw_t_autogol']]
        d6_1 = d6_1.sort_values(by=['hm_t_n'])
        d6_2 = d6_2.sort_values(by=['aw_t_n'])
        d6_1 = d6_1.groupby('hm_t_n', as_index=False).sum()
        d6_2 = d6_2.groupby('aw_t_n', as_index=False).sum()
        d2 = pd.concat([d6_1, d6_2], axis=1)
        d2 = d2.drop(['aw_t_n', 'season'], axis=1)
        d2 = d2.rename(columns={'hm_t_n': 'Teams'})
        d6_3 = d2.melt('Teams', var_name='team', value_name='amount')
        plot = alt.Chart(d6_3).mark_bar().encode(
            x='team:O',
            y='amount:Q',
            color='team:N',
            column='Teams:N'
        )
        return (plot)

    def plot_shots_shotsongol(df):
        d7_1 = df[['season', 'hm_t_n', 'hm_t_shot', 'hm_t_shot_gol']]
        d7_2 = df[['season', 'aw_t_n', 'aw_t_shot', 'aw_t_shot_gol']]
        d7_1 = d7_1.sort_values(by=['hm_t_n'])
        d7_2 = d7_2.sort_values(by=['aw_t_n'])
        d7_1 = d7_1.groupby('hm_t_n', as_index=False).sum()
        d7_2 = d7_2.groupby('aw_t_n', as_index=False).sum()
        d2 = pd.concat([d7_1, d7_2], axis=1)
        d2 = d2.drop(['aw_t_n', 'season'], axis=1)
        d2 = d2.rename(columns={'hm_t_n': 'Teams'})
        d7_3 = d2.melt('Teams', var_name='team', value_name='amount')
        plot = alt.Chart(d7_3).mark_bar().encode(
            x='team:O',
            y='amount:Q',
            color='team:N',
            column='Teams:N'
        )
        return (plot)

    def plot_yel_red_cards(df):
        d8_1 = df[['season', 'hm_t_n', 'hm_t_yel_card', 'hm_t_red_card']]
        d8_2 = df[['season', 'aw_t_n', 'aw_t_yel_card', 'aw_t_red_card']]
        d8_1 = d8_1.sort_values(by=['hm_t_n'])
        d8_2 = d8_2.sort_values(by=['aw_t_n'])
        d8_1 = d8_1.groupby('hm_t_n', as_index=False).sum()
        d8_2 = d8_2.groupby('aw_t_n', as_index=False).sum()
        d2 = pd.concat([d8_1, d8_2], axis=1)
        d2 = d2.drop(['aw_t_n', 'season'], axis=1)
        d2 = d2.rename(columns={'hm_t_n': 'Teams'})
        d8_3 = d2.melt('Teams', var_name='team', value_name='amount')
        plot = alt.Chart(d8_3).mark_bar().encode(
            x='team:O',
            y='amount:Q',
            color='team:N',
            column='Teams:N'
        )
        return (plot)

    def plot_punch_fouls(df):
        d9_1 = df[['season', 'hm_t_n', 'hm_t_fouls_do', 'hm_t_fouls_re', 'hm_t_punch']]
        d9_2 = df[['season', 'aw_t_n', 'aw_t_fouls_do', 'aw_t_fouls_re', 'aw_t_punch']]
        d9_1 = d9_1.sort_values(by=['hm_t_n'])
        d9_2 = d9_2.sort_values(by=['aw_t_n'])
        d9_1 = d9_1.groupby('hm_t_n', as_index=False).sum()
        d9_2 = d9_2.groupby('aw_t_n', as_index=False).sum()
        d2 = pd.concat([d9_1, d9_2], axis=1)
        d2 = d2.drop(['aw_t_n', 'season'], axis=1)
        d2 = d2.rename(columns={'hm_t_n': 'Teams'})
        d9_3 = d2.melt('Teams', var_name='team', value_name='amount')
        plot = alt.Chart(d9_3).mark_bar().encode(
            x='team:O',
            y='amount:Q',
            color='team:N',
            column='Teams:N'
        )
        return (plot)

    def plot_offside_corners(df):
        d10_1 = df[['season', 'hm_t_n', 'hm_t_pty', 'hm_t_offsid', 'hm_t_corner']]
        d10_2 = df[['season', 'aw_t_n', 'aw_t_pty', 'aw_t_offsid', 'aw_t_corner']]
        d10_1 = d10_1.sort_values(by=['hm_t_n'])
        d10_2 = d10_2.sort_values(by=['aw_t_n'])
        d10_1 = d10_1.groupby('hm_t_n', as_index=False).sum()
        d10_2 = d10_2.groupby('aw_t_n', as_index=False).sum()
        d2 = pd.concat([d10_1, d10_2], axis=1)
        d2 = d2.drop(['aw_t_n', 'season'], axis=1)
        d2 = d2.rename(columns={'hm_t_n': 'Teams'})
        d10_3 = d2.melt('Teams', var_name='team', value_name='amount')
        plot = alt.Chart(d10_3).mark_bar().encode(
            x='team:O',
            y='amount:Q',
            color='team:N',
            column='Teams:N'
        )
        return (plot)

    def plot_arbit_stats(df):
        d11 = df[['season', 'arbitr_n', 'hm_t_pty', 'aw_t_pty', 'hm_t_yel_card', 'aw_t_yel_card', 'hm_t_red_card','aw_t_red_card']]
        d11['penal/match'] = d11['hm_t_pty'] + d11['aw_t_pty']
        d11['yel_card/match'] = d11['hm_t_yel_card'] + d11['aw_t_yel_card']
        d11['red_card/match'] = d11['hm_t_red_card'] + d11['aw_t_red_card']
        d11_2 = d11['arbitr_n'].value_counts()
        d11_2 = d11_2.to_frame()
        d11_2.reset_index(level=0, inplace=True)
        d11 = d11.groupby('arbitr_n', as_index=False).sum()
        d11_3 = pd.merge(d11, d11_2, how='left', left_on='arbitr_n', right_on='index')
        d11_3 = d11_3.drop(['hm_t_pty', 'season', 'aw_t_pty', 'hm_t_yel_card', 'aw_t_yel_card', 'hm_t_red_card',
                            'aw_t_red_card', 'index'], axis=1)
        d11_3 = d11_3.rename(columns={'arbitr_n_y': 'total games'})
        d11_3 = d11_3.rename(columns={'arbitr_n_x': 'arbitr_n'})
        d11_3 = d11_3.drop(d11.index[[0]])
        d11_3['penal/match'] = d11_3['penal/match'] / d11_3['total games']
        d11_3['yel_card/match'] = d11_3['yel_card/match'] / d11_3['total games']
        d11_3['red_card/match'] = d11_3['red_card/match'] / d11_3['total games']
        d11_3 = d11_3.drop(['total games'], axis=1)
        d11_4 = d11_3.melt('arbitr_n', var_name='Var', value_name='amount')
        plot = alt.Chart(d11_4).mark_bar().encode(
            x='Var:O',
            y='amount:Q',
            color='Var:N',
            column='arbitr_n:N'
        )
        return (plot)

    def plot_stadi_win_loss(df):
        d12 = df[['season', 'stadi', 'hm_t_isw', 'aw_t_isw']]
        d12['hm_t_isw'] = d12['hm_t_isw'].astype(int)
        d12['aw_t_isw'] = d12['aw_t_isw'].astype(int)
        d12 = d12.groupby('stadi', as_index=False).sum()
        d12 = d12.drop('season', axis=1)
        d12_2 = d12.melt('stadi', var_name='Var', value_name='amount')
        plot = alt.Chart(d12_2).mark_bar().encode(
            x='Var:O',
            y='amount:Q',
            color='Var:N',
            column='stadi:N'
        )
        return (plot)

    def stadi_win_attend(df):
        d13 = df[['season', 'stadi', 'hm_t_isw', 'Attend']]
        d13['hm_t_isw'] = d13['hm_t_isw'].astype(int)
        d13['Attend'] = d13['Attend'].astype(float)
        x = d13['Attend'].describe()[1]
        y = d13['Attend'].describe()[4]
        t = d13['Attend'].describe()[5]
        z = d13['Attend'].describe()[6]
        d13['Mean Attendance'] = np.where(
            d13['Attend'] == x, 1, np.where(
                d13['Attend'] > x, 1, 0))
        d13['25 Attendance'] = np.where(
            d13['Attend'] == y, 1, np.where(
                d13['Attend'] > y, 1, 0))
        d13['50 Attendance'] = np.where(
            d13['Attend'] == t, 1, np.where(
                d13['Attend'] > t, 1, 0))
        d13['75 Attendance'] = np.where(
            d13['Attend'] == z, 1, np.where(
                d13['Attend'] > z, 1, 0))
        d13 = d13.drop(['season', 'Attend'], axis=1)
        d13 = d13.groupby('stadi', as_index=False).sum()
        d13_2 = d13.melt('stadi', var_name='Var', value_name='amount')
        plot = alt.Chart(d13_2).mark_bar().encode(
            x='Var:O',
            y='amount:Q',
            color='Var:N',
            column='stadi:N'
        )
        return (plot)

    def pos_win(df):
        d14_1 = df[['season', 'hm_t_n', 'hm_t_isw', 'hm_t_xtg_poss']]
        d14_2 = df[['season', 'aw_t_n', 'aw_t_isw', 'aw_t_xtg_poss']]
        d14_1['hm_t_xtg_poss'] = d14_1['hm_t_xtg_poss'].astype(float)
        d14_2['aw_t_xtg_poss'] = d14_2['aw_t_xtg_poss'].astype(float)
        d14_1['hm_t_isw'] = d14_1['hm_t_isw'].astype(int)
        d14_2['aw_t_isw'] = d14_2['aw_t_isw'].astype(int)
        d14_1['hm_t_xtg_poss'] = np.where(
            d14_1['hm_t_xtg_poss'] == 50, 1, np.where(
                d14_1['hm_t_xtg_poss'] > 50, 1, 0))
        d14_2['aw_t_xtg_poss'] = np.where(
            d14_2['aw_t_xtg_poss'] == 50, 1, np.where(
                d14_2['aw_t_xtg_poss'] > 50, 1, 0))
        d14_1 = d14_1.fillna(0)
        d14_2 = d14_2.fillna(0)
        d14_1 = d14_1.drop(['season', 'hm_t_xtg_poss'], axis=1)
        d14_2 = d14_2.drop(['season', 'aw_t_xtg_poss'], axis=1)
        d14_1 = d14_1.groupby('hm_t_n', as_index=False).sum()
        d14_2 = d14_2.groupby('aw_t_n', as_index=False).sum()
        d14 = pd.concat([d14_1, d14_2], axis=1)
        d14 = d14.drop(['aw_t_n'], axis=1)
        d14 = d14.rename(columns={'hm_t_n': 'Teams'})
        d14_3 = d14.melt('Teams', var_name='team', value_name='amount')
        plot = alt.Chart(d14_3).mark_bar().encode(
            x='team:O',
            y='amount:Q',
            color='team:N',
            column='Teams:N'
        )
        return (plot)