# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

"""pca_lib.py contains all the functions relevant for the PCA analysis that is
not already present in the current libraries."""

__author__ = "Alberto Gutiérrez Torre"


def postprocess_pca(pca, nrow, data = None):
    """
    postprocess pca to have the same results as factominer's pca.

    Modifies the pca object to a pca object so taht the eigenvalues are
    corrected and the individuals projected in the non-normalized principal
    components. Also adds active variables mean and std for further projections.

    :param pca [statsmodel pca]: statsmodels pca model object
    :param nrow [integer]: number of rows of the original dataset
    :param data [pandas dataframe]: Dataset of active variables and individuals
        used to calculate the pca.
    """
    # divide the eigenvalue by the number of rows so that eigenvalues sum up to
    # the number of columns
    pca.eigenvals /= nrow

    std = pca.factors.std()
    sqrt_eig = pca.eigenvals**(1/2)
    sqrt_eig.index = std.index
    pca.factors *= sqrt_eig / std
    
    # Add mean and std to
    if data is not None:
        pca.mean = data.mean()
        pca.std = data.std()
    else:
        pca.mean = None
        pca.std = None
        print("""Warning: If the pca is normalized and you want to project
              supplementary individuals, provide the data used to calculate 
              the PCA in the data variable to this function.""")
        
        
def project_individuals(pca, indv):
    """
    Projects the individuals given in indv to the projection defined in pca.
    
    :param pca [statsmodel pca]: statsmodel pca model object
    :param indv [pandas dataframe]: individuals to project
    """
    proj_ind_pd = None
    if pca.mean is None:
        print("""Error: Please provide the data used to calculate the pca to
             postprocess_pca function.""")
    else:
        norm_indv = (indv-pca.mean)/pca.std
        proj_ind = norm_indv.values.dot(pca.eigenvecs.values)
        proj_ind_pd = pd.DataFrame(data=proj_ind, index=indv.index, columns=pca.factors.columns)
    return(proj_ind_pd)

                    
def calculate_pc_variance(pca):
    """
    Calculates the variance and accumulated variance percentage of the
    components using the eigenvalues.

    :param pca [statsmodel pca]: StatsModels PCA model object

    :returns: tuple of arrays containing the percentage of variance and the
    accumulated percentage of variance.
    """
    total = pca.eigenvals.sum()
    var = [(v/total)*100 for v in pca.eigenvals]
    cumvar = var.copy()
    for i in range(1, len(cumvar)):
        cumvar[i] += cumvar[i-1]
    return(var, cumvar)


def eigen_var(pca):
    """
    Returns a dataframe with the eigenvalues, the variance and the cummulate
    variance.

    :param pca [statsmodel pca]: StatsModels PCA model object

    :returns: Pandas DataFrame.
    """
    var, cvar = calculate_pc_variance(pca)
    pca.eigenvals

    data = {
        'Eigenvalue': pca.eigenvals,
        'Perc. of Variance': var,
        'Cummulative Perc. of Variance': cvar
    }
    return(pd.DataFrame(data))


def corr_pc_vars(pca, data, nd=None, as_df=False):
    """
    Calculate the correlation between the principal components and the original
    variables.

    :param pca [statsmodel pca]: StatsModels PCA model object
    :param data [Pandas dataframe]: Original dataset used for PCA
    :param nd [int]: Number of principal components to show
    :param as_df [bool]: Return the result as a pandas dataframe
    """
    if nd is None:
        nd = len(pca.eigenvals)  # If no limit, use all
    cor = np.array(
        [
            [
                data[col].corr(pca.factors.iloc[:, comp])
                for comp in range(0, nd)
            ]
            for col in data.columns
        ]
    )
    if as_df:
        cor = pd.DataFrame(cor)
        cor.index = data.columns
    return(cor)


def varimax_to_df(cor, columns=None):
    """
    Transforms the VARIMAX rotated correlation matrix obtained from statsmodel
    to a pandas dataframe.

    :param cor [Matrix]: Matrix of correlations from VARIMAX
    :param columns [Pandas index]: Names of the variables from
    original_data.columns
    """
    cc = pd.DataFrame(cor)
    if columns is not None:
        #  cc.insert(0, 'var_name', columns)
        cc.index = columns
    return(cc)


def simplify_corr(cor, threshold=0.15, n_dig=3):
    """
    Removes values that are lower than the threshold and rounds everything to
    the number of digits n_dig.

    :param cor [Pandas DF]: Matrix of correlations as pandas Dataframe
    :param threshold [Float]: Threshold used to remove elements that are lower
    than it
    :param n_dig [Int]: Number of decimals to show
    """
    cor = cor.copy()
    cor = np.round(cor, n_dig)
    cor[abs(cor) < threshold] = " "

    return(cor)


def rotate_quanti_sup(data, pca, transf, quanti_sup):
    """
    Rotate quantitative supplementary using the transformation matrix transf

    :param data [Pandas DF]: Original dat
    :param pca [Statsmodel PCA]: PCA model to use for correlation calculation
    :param transf [array of Float]: Transformation matrix to apply (VARIMAX)
    :param quanti_sup [tuple of strings]: Columns to use as supplementary
    """
    nd = transf.shape[0]
    d_quanti = data[quanti_sup]
    cor_sup = corr_pc_vars(pca, d_quanti, nd=nd)
    return(np.matmul(cor_sup, transf))


def scree_plot(pca, nd=None):
    """
    Prints a screeplot of the selected components

    :param pca [statsmodel pca]: StatsModels PCA model object
    :param nd [int]: Number of principal components to show
    """
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylabel('Eigenvalues')
    ax.set_xlabel('Dimensions')
    if nd is None:
        nd = pca.coeff.shape[0]  # We get all the PC
    x = range(0, nd)
    y = pca.eigenvals[0:nd]
    plt.scatter(x, y)
    plt.plot(x, y)
    plt.show()


def var_correlation_plot(pca, data, plot_pc=(0, 1), act=(), quanti_sup=(),
                         quali_sup=()):
    """
    Prints a variable correlation plot of the selected components

    :param pca [statsmodel pca]: StatsModels PCA model object
    :param data [pandas dataframe]: Dataset used for PCA projection
    :param plot_pc [tuple of int]: Components to be used for axis x and y
    :param act [tuple of string]: Variables to be used as active (Default: all
    minus supplementaries)
    :param quanti_sup [tuple of string]: Quantitative variables to be used as
    supplementaries
    :param quali_sup [tuple of string]: Qualitative variables to be used as
    supplementaries
    """
    var, _ = calculate_pc_variance(pca)
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid()

    # ax.set_aspect(aspect=1)
    plt.title('PCA Graph of variables')
    ax.set_xlabel('Dim ' + str(plot_pc[0]) +
                  '(' + str(round(var[plot_pc[0]], 2)) + '%)')
    ax.set_ylabel('Dim ' + str(plot_pc[1]) +
                  '(' + str(round(var[plot_pc[1]], 2)) + '%)')
    # Set x-axis range
    plt.xlim((-1.1, 1.1))
    # Set y-axis range
    plt.ylim((-1.1, 1.1))
    ax.set_xticks(np.linspace(-1, 1, 9))
    ax.set_yticks(np.linspace(-1, 1, 9))

    # Draw lines to split quadrants
    #  [X1,X2], [Y1,Y2]
    # Axis
    plt.plot([0, 0], [-1, 1], linewidth=1, color='black',  linestyle='dashed')
    plt.plot([-1, 1], [0, 0], linewidth=1, color='black',  linestyle='dashed')
    # Circle
    circle = plt.Circle((0, 0), 1, color='black', fill=False)
    ax.add_patch(circle)

    # act-sup preprocess
    if len(quanti_sup) != 0 and type(quanti_sup) is str:
        # If it's a string (only one value), transform to tuple
        quanti_sup = (quanti_sup, )
    if len(quali_sup) != 0 and type(quali_sup) is str:
        # If it's a string (only one value), transform to tuple
        quali_sup = (quali_sup, )
    if len(act) == 0:
        # If active is empty, use all except sup
        act = set(data.columns.to_list()).difference(quanti_sup)\
                .difference(quali_sup)
    elif type(act) is str:
        # If it's a string (only one value), transform to tuple
        act = (act,)

    # Plot columns(y for y in items if y > 10)
    for col in (
                col for col in data.columns
                if (col in act or col in quanti_sup) and col not in quali_sup):
        if col in act:
            color = "black"
        else:  # Supplementary
            color = "blue"
        c1 = data[col].corr(pca.factors.iloc[:, plot_pc[0]])
        c2 = data[col].corr(pca.factors.iloc[:, plot_pc[1]])
        ax.arrow(0, 0, c1, c2, head_width=0.02, head_length=0.03, fc=color,
                 ec=color)
        plt.annotate(col, xy=(c1+0.005, c2+0.03), color=color)
    plt.show()


def varimax_var_correlation_plot(cor_var, plot_pc=(0, 1), sup_rotated=None):
    """
    Prints a variable correlation plot of the selected components

    :param cor_var [Pandas dataframe]: Correlation matrix in pandas format
    :param plot_pc [tuple of int]: Components to be used for axis x and y
    :param sup_rotated [Pandas dataframe]: Correlation matrix in pandas format
    of the supplementary variables
    """
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid()

    # ax.set_aspect(aspect=1)
    plt.title('PCA Graph of variables VARIMAX')
    ax.set_xlabel('Dim ' + str(plot_pc[0]))
    ax.set_ylabel('Dim ' + str(plot_pc[1]))
    # Set x-axis range
    plt.xlim((-1.1, 1.1))
    # Set y-axis range
    plt.ylim((-1.1, 1.1))
    ax.set_xticks(np.linspace(-1, 1, 9))
    ax.set_yticks(np.linspace(-1, 1, 9))

    # Draw lines to split quadrants
    #  [X1,X2], [Y1,Y2]
    # Axis
    plt.plot([0, 0], [-1, 1], linewidth=1, color='black',  linestyle='dashed')
    plt.plot([-1, 1], [0, 0], linewidth=1, color='black',  linestyle='dashed')
    # Circle
    circle = plt.Circle((0, 0), 1, color='black', fill=False)
    ax.add_patch(circle)

    # act-sup preprocess
    # if len(sup) != 0 and type(sup) is str:
    #     # If it's a string (only one value), transform to tuple
    #     sup = (sup, )
    # if len(act) == 0:
    #     # If active is empty, use all except sup
    #     act = set(data.columns.to_list()).difference(sup)
    # elif type(act) is str:
    #     # If it's a string (only one value), transform to tuple
    #     act = (act,)

    # Plot columns(y for y in items if y > 10)
    color = "black"
    for index, row in cor_var.iterrows():
        # if index in act:
        # else:
        #   color = "blue
        c1 = row[plot_pc[0]]
        c2 = row[plot_pc[1]]
        ax.arrow(0, 0, c1, c2, head_width=0.02, head_length=0.03, fc=color,
                 ec=color)
        plt.annotate(index, xy=(c1+0.005, c2+0.03), color=color)

    if sup_rotated is not None:
        color = "blue"
        for index, row in sup_rotated.iterrows():
            # if index in act:
            # else:
            #   color = "blue
            c1 = row[plot_pc[0]]
            c2 = row[plot_pc[1]]
            ax.arrow(0, 0, c1, c2, head_width=0.02, head_length=0.03, fc=color,
                     ec=color)
            plt.annotate(index, xy=(c1+0.005, c2+0.03), color=color)

    plt.show()


def pca_indv_plot(pca, plot_pc=(0, 1), color=None, data=None, quali_sup=(),
                  indv_sup=None, use_index_names=False):
    """
    Prints a scatterplot of the individuals in the PCA projected space

    :param pca [statsmodel pca]: StatsModels PCA model object
    :param plot_pc [tuple of int]: Components to be used for axis x and y
    :param color [array of string]: Group variable that defines the color of
    each point
    :param data [Pandas DF]: Original dataframe used in pca including
    supplementaries
    :param quali_sup [tuple of string]: Supplementary columns to show
    :param indv_sup [Pandas DF]: Supplementary individuals to plot
    :param use_index_names [bool]: whether to print the index names along
    the point or not.
    """
    var, _ = calculate_pc_variance(pca)
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid()

    # ax.set_aspect(aspect=1)
    plt.title('PCA Graph of individuals')
    ax.set_xlabel(
            'Dim ' + str(plot_pc[0]) +
            '(' + str(round(var[plot_pc[0]], 2)) + '%)'
    )
    ax.set_ylabel(
            'Dim ' + str(plot_pc[1]) +
            '(' + str(round(var[plot_pc[1]], 2)) + '%)'
    )
    sc = sns.scatterplot(x=pca.factors.iloc[:, plot_pc[0]],
                         y=pca.factors.iloc[:, plot_pc[1]], hue=color, ax = ax)
    
    if use_index_names:
        for line in range(0, pca.factors.shape[0]):
            sc.text(pca.factors.iloc[line, plot_pc[0]], pca.factors.iloc[line, plot_pc[1]],
                    pca.factors.index[line], horizontalalignment='left', size='medium',
                    color='black')
            
    # Plot supplementary individuals
    if indv_sup is not None:
        sc = sns.scatterplot(x=indv_sup.iloc[:, plot_pc[0]],
                             y=indv_sup.iloc[:, plot_pc[1]], ax = ax)
        if use_index_names:
            for line in range(0, len(indv_sup)):
                sc.text(indv_sup.iloc[line, plot_pc[0]], indv_sup.iloc[line, plot_pc[1]],
                        indv_sup.index[line], horizontalalignment='left', size='medium',
                        color='black')
 
    # Supplementary variables
    if data is not None:
        if len(quali_sup) != 0:
            if len(quali_sup) != 0 and type(quali_sup) is str:
                # If it's a string (only one value), transform to tuple
                quali_sup = (quali_sup, )
            for var in quali_sup:
                # Calculate group means
                df_avg = pca.factors.groupby(by=data[var]).mean()
                # Print annotations
                for row in df_avg.iterrows():
                    x_grp = row[1][plot_pc[0]]
                    y_grp = row[1][plot_pc[1]]
                    grp = var + '_' + str(row[0])  # Build variable name
                    sc.text(x_grp, y_grp, grp,
                            horizontalalignment='left', size='medium',
                            color='black', weight='semibold')


