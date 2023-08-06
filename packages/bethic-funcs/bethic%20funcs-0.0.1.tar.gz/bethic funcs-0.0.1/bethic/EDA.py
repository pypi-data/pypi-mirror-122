import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def plot_var_distr(df):
    attributes = ["assis", "autogol", "catch", "corner", "cross", "fouls_do", "fouls_re", "gol", "offsid", "pty",
                  "pty_gol", "punch", "red_card", "save", "shot", "shot_gol", "yel_card"]

    for attribute in attributes:
        plt.figure()
        plt.title('hm_t_' + attribute)
        df['hm_t_' + attribute].hist(bins=20)
        plt.figure()
        plt.title('aw_t_' + attribute)
        df['aw_t_' + attribute].hist(bins=20)


def tidy_corr_matrix(corr_mat):
    '''
    Función para convertir una matrix de correlación de pandas en formato tidy
    '''
    corr_mat = corr_mat.stack().reset_index()
    corr_mat.columns = ['variable_1', 'variable_2', 'r']
    corr_mat = corr_mat.loc[corr_mat['variable_1'] != corr_mat['variable_2'], :]
    corr_mat['abs_r'] = np.abs(corr_mat['r'])
    corr_mat = corr_mat.sort_values('abs_r', ascending=False)

    return (corr_mat)

def corr_matrix(df):
    corr_matrix = df.select_dtypes(include=['float64', 'int']).corr(method='pearson')
    tidy_corr_matrix(corr_matrix).head(10)
    return (corr_matrix)

def plot_corr_matrix(corr_matrix):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(300, 300))

    sns.heatmap(
        corr_matrix,
        annot=True,
        cbar=False,
        annot_kws={"size": 6},
        vmin=-1,
        vmax=1,
        center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True,
        ax=ax
    )
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right',
    )

    ax.tick_params(labelsize=8)

def plot_violin_plot(df):
    data = df[['result', 'month']]
    sns.violinplot(x='result', y='month', data=data, color='white')
