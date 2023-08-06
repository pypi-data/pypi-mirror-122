from sklearn.model_selection import cross_validate
import numpy as np
import re


def get_score(y_test, y_pred, scorer):
    """Get score from an element of d_scorer

    Args:
        y_test (array): test data
        y_pred (array): predicted data
        scorer (float): sklearn scorer

    Returns:
        [float]: score
    """
    metric = scorer.__dict__['_score_func']
    kwargs = scorer.__dict__['_kwargs']
    return metric(y_test, y_pred, **kwargs)


def get_pipe_score(pipe, X_test, y_test, scorer):
    y_pred = pipe.predict(X_test)
    return get_score(y_test, y_pred, scorer)


def get_scores(y_test, y_pred, d_scorer, prefix:str=None):
    if prefix:
        return {prefix+'_'+k:get_score(y_test, y_pred, v) 
                                                    for k,v in d_scorer.items()}
    return {k:get_score(y_test, y_pred, v) for k,v in d_scorer.items()}



def get_pipe_scores(pipe, X_test, y_test, d_scorer, prefix=None):
    y_pred = pipe.predict(X_test)
    return get_scores(y_test, y_pred, d_scorer, prefix)


def get_cv(pipe, X, y, d_scorer, cv=3, prefix='cv', dec_round = 4, 
                                                    return_times = True, 
                                                    return_estimators = True,
                                                    **kwargs):

    # To get useful info
    regex_filter = 'test'
    if return_times:
        regex_filter = '(test|fit_time)'

    # Crossvalidate with sklearn function
    cv_output = cross_validate(pipe, X, y, cv=cv, scoring=d_scorer, 
                                            return_estimator=return_estimators,
                                            **kwargs)

    # Results
    d_cv_results = {k.replace('test', prefix).replace('fit', prefix):v 
                                        for k,v in cv_output.items() 
                                        if re.compile(regex_filter).match(k)}
    d_cv_results = {k+'_'+str(i):v for k in d_cv_results.keys() 
                                    for i,v in enumerate(d_cv_results[k])}

    # Mean
    d_cv_results_mean = {prefix+'_mean_'+k:np.mean(
                            [v2 for k2,v2 in d_cv_results.items() if k in k2]) 
                                    for k in d_scorer.keys()}

    # Std
    d_cv_results_std = {prefix+'_std_'+k:np.std(
                            [v2 for k2,v2 in d_cv_results.items() if k in k2]) 
                                    for k in d_scorer.keys()}

    # Mean+Std
    d_cv_results_std = {prefix+'_meanstd_'+k:np.std(
                            [v2 for k2,v2 in d_cv_results.items() if k in k2]) 
                                    for k in d_scorer.keys()}
    d_cv_results.update(d_cv_results_std)

    # Time
    if return_times:
        d_cv_results_times = {prefix+'_mean_time':np.mean(
                            [v2 for k2,v2 in d_cv_results.items() if 'time' in k2])}
        d_cv_results_mean.update(d_cv_results_times)
        d_cv_results_std.update({prefix+'_std_time':np.std(
                        [v2 for k2,v2 in d_cv_results.items() if 'time' in k2])})

    # Update all
    d_cv_results.update(d_cv_results_mean)
    d_cv_results.update(d_cv_results_std)
    d_cv_results = {k:round(v, dec_round) for k,v in d_cv_results.items() 
                                                    if 'meanstd' not in k}

    # Mean+Std
    d_ms = {k.replace('mean','meanstd'):'{:}+-{:}'.format(round(v1,dec_round),
                                                            round(v2,dec_round)) 
                                for k,v1,v2 in zip(d_cv_results_mean.keys(), 
                                                    d_cv_results_mean.values(), 
                                                    d_cv_results_std.values())}
    d_cv_results.update(d_ms)
    

    # Add Estimators
    if return_estimators:
        cv_estimators = {'fitted_estimator_'+str(i):v for i,v in 
                                            enumerate(cv_output['estimator'])}
        d_cv_results.update(cv_estimators)

    return d_cv_results


def get_cv_scores_from_cv_results(d_cv_results, only_mean=False, prefix='cv'):
    """Función muy particular para obtener predicción en otro conjunto de cada
    fold. Coge el d_cv_results de la función get_scores_cv filtrando.

    """
    if only_mean:
        return {k:v for k,v in d_cv_results.items() if 
                                ((prefix+'_mean' in k) & ('meanstd' not in k))}
    return {k:v for k,v in d_cv_results.items() if 
                                        ((prefix in k) & ('meanstd' not in k))}


def get_test_scores_from_cv_results(d_cv_results, X_test, y_test, d_scorer, 
                                                            prefix='test',
                                                            only_mean=False):
    """Función muy particular para obtener predicción en otro conjunto de cada
    fold. Coge el d_cv_results de la función get_scores_cv, filtra y calcula.

    Args:
        d_cv_results ([type]): [description]
        X_test ([type]): [description]
        y_test ([type]): [description]
        d_scorer ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Score in Test
    d_res_test = {k:get_pipe_scores(est, X_test, y_test, d_scorer, prefix) 
                                        for k, est in  d_cv_results.items() 
                                            if ('fitted_estimator' in k)}


    d_res_test = {k.replace('fitted_','')+'_'+k2:v2 
                    for k,v in d_res_test.items() for k2,v2 in v.items()}
    d_res_test = {'_'.join([k.split('_')[2],
                            k.split('_')[0],
                            k.split('_')[1],
                            k.split('_')[3]]):v for k,v in d_res_test.items()}
    d_res_test.update({prefix+'_mean_'+k:
                    np.mean([v2 for k2,v2 in d_res_test.items() if '_'+k in k2]) 
                    for k in d_scorer.keys()})
    d_res_test.update({prefix+'_std_'+k:
                    np.std([v2 for k2,v2 in d_res_test.items() if '_'+k in k2]) 
                    for k in d_scorer.keys()})
    if only_mean:
        return {k:v for k,v in d_res_test.items() if 
                                ((prefix+'_mean_' in k) |
                                  (prefix+'_std_' in k))}
    return d_res_test