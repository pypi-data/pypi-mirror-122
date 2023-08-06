import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.feature_extraction.text import _VectorizerMixin
from sklearn.feature_selection._base import SelectorMixin
from sklearn.decomposition import PCA


def get_feature_out(estimator, feature_in):
    if hasattr(estimator,'get_feature_names'):
        if isinstance(estimator, _VectorizerMixin):
            # handling all vectorizers
            return [f'vec_{f}' for f in estimator.get_feature_names()]
        else:
            try:
                return estimator.get_feature_names(feature_in)
            except TypeError:
                return estimator.get_feature_names()
    elif isinstance(estimator, SelectorMixin):
        return np.array(feature_in)[estimator.get_support()]
    elif isinstance(estimator, PCA):
        n_components = estimator.__dict__['n_components']
        if n_components is None:
            return [f'pca{i}' for i in len(feature_in)]
        else:
            return [f'pca{i}' for i in range(n_components)]
    else:
        return feature_in


def get_preprocessor_feature_names(preprocessor):
    # handles all estimators, pipelines inside ColumnTransfomer
    # doesn't work when remainder =='passthrough'
    # which requires the input column names.
    output_features = []
    
    for name, estimator, features in preprocessor.transformers_:
        if name!='remainder':
            if isinstance(estimator, Pipeline):
                current_features = features
                for step in estimator:
                    current_features = get_feature_out(step, current_features)
                features_out = current_features
            else:
                features_out = get_feature_out(estimator, features)
            output_features.extend(features_out)
        elif estimator=='passthrough':
            output_features.extend(preprocessor._feature_names_in[features])
    return output_features  



def get_pipe_feature_names(pipe):
    # handles all estimators, pipelines inside ColumnTransfomer
    # doesn't work when remainder =='passthrough'
    # which requires the input column names.
    output_features = []

    if isinstance(pipe, pd.DataFrame):
        return pipe.columns.tolist()

    if isinstance(pipe, Pipeline):
        for obj in pipe:
            # Caso en que sea column transformer
            if isinstance(obj, ColumnTransformer):
                output_features.extend(get_preprocessor_feature_names(obj))
    
    if isinstance(pipe, ColumnTransformer):
        output_features.extend(get_preprocessor_feature_names(pipe))

    return output_features  



