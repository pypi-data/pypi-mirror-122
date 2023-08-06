# https://buhrmann.github.io/sklearn-pipelines.html


from sklearn.base import *
from sklearn.pipeline import *
import numpy as np

class ModelTransformer(TransformerMixin):
    ''' Use model predictions as transformed data. '''
    def __init__(self, model, probs=True):
        self.model = model
        self.probs = probs

    def get_params(self, deep=True):
        return dict(model=self.model, probs=self.probs)

    def fit(self, *args, **kwargs):
        self.model.fit(*args, **kwargs)
        return self

    def transform(self, X, **transform_params):
        if self.probs:
            Xtrf = self.model.predict_proba(X)[:, 1]
        else:
            Xtrf = self.model.predict(X)
        return np.asarray(Xtrf).reshape((len(X), 1))


def build_ensemble(model_list, estimator=None, probs=True):
    ''' Build an ensemble as a FeatureUnion of ModelTransformers and a 
        final estimator using their predictions as input. '''

    models = []
    for i, model in enumerate(model_list):
        models.append(('model_transform'+str(i), ModelTransformer(model, 
                                                                probs=probs)))

    if not estimator:
        return FeatureUnion(models)
    else:
        return Pipeline([
            ('features', FeatureUnion(models)),
            ('estimator', estimator)
            ])