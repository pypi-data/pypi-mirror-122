import pandas as pd
from scripts.lib.csklearn.utils.get_pipe_feature_names import *


def get_preprocessed_matrix(preprocessor, X, y=None, featsel = None, fit=False, 
                                                            verbose=False):
    """Esta función nos ayuda a hacer el preprocesamiento previo al algoritmo
    y obtener el nombre de la matriz resultante (si es posible con la
    función get_pipe_feature_names)

    Args:
        preprocessor (Pipeline): el preprocesamiento que se desee realizar.
        X ([type]): matriz de entrada
        y ([type], optional): target. Defaults to None.
        featsel ([type], optional): En caso de que haya una selección de
            variables, hay que especificarlo para poder seleccionarlas. 
            Defaults to None.
        fit (bool, optional): si la Pipeline no ha sido entrenada, este
            argumento debería ser True. Defaults to False.
        verbose (bool, optional): para imprimir variables que se van a
            utilizar. Defaults to False.

    Returns:
        [type]: la matriz X transformada con los nombres de las columnas

    Examples:
        X_train_ = get_preprocessed_matrix(pipe[:2], X_train, y_train, fit=True)

    """
    
    if fit:
        X_ = preprocessor.fit_transform(X, y) 
    else:
        X_ = preprocessor.transform(X) 
    ls_var_names = get_pipe_feature_names(preprocessor)
    X_ = pd.DataFrame(X_, columns = ls_var_names)
    
    if featsel:
        # Variables seleccionadas por featsel. NOTA: Importante key para q no cambie orden
        ls_var_ranking = sorted(zip(featsel.ranking_, ls_var_names), 
                                                            key=lambda x: x[0])
        ls_var_selected = [x[1] for x in ls_var_ranking[:featsel.n_features_]]
        X_ = X_[ls_var_selected]
        
        if verbose:
            print('Feature selection Ranking:')
            for i,var in ls_var_ranking:
                print('- {}: {}'.format(i,var))
        
    if verbose:
        print('\n\nFinal model features:')
        for var in X_.columns:
            print('- {}'.format(var))
            
    return X_