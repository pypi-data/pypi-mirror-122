import pandas as pd
from statsmodels.multivariate.pca import PCA
from statsmodels.multivariate.factor_rotation import rotate_factors
import pca_lib
## ERROR NA o INF, SEGURO QUE ES NA
def PCA_analysis(df):
    n = df.select_dtypes(include=['float', 'int'])
    pca = PCA(n, standardize=True)
    pca.eigenvals /= n.shape[0]

    print("Eigenvalues: ")
    print(pca.eigenvals)
    print("Eigenvectors: ")
    print(pca.eigenvecs)

    # # PCA Graph - Scree plot
    scree_plot(pca)

    # # PCA Graph - Correlation of variables with the Principal Components
    var_correlation_plot(pca, n, plot_pc=(0, 1), act=())

    # # PCA Graph - Individuals map

    # Cambiar numeros en plot_pc para cambiar dimensione
    pca_indv_plot(pca, plot_pc=(0,1), color=d['Match result'], data = df)