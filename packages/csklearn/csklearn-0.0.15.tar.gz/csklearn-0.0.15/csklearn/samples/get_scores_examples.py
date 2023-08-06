# %% Import needed modules -----------------------------------------------------
from sklearn import datasets, linear_model
from sklearn.metrics import *
from sklearn.model_selection import cross_validate

# UDFs
from ..metrics.get_scores import *


# %% Load Data and Estimator ---------------------------------------------------
diabetes = datasets.load_diabetes()
X = diabetes.data[:150]
y = diabetes.target[:150]
lasso = linear_model.Lasso()


# %% Define d_scorer -----------------------------------------------------------
d_scorer = {
            'rmse':make_scorer(mean_squared_error),
            'mae':make_scorer(mean_absolute_error),
            'r2':make_scorer(r2_score)
            }


# %% Make CrossValidation ------------------------------------------------------
d_cv_results = get_cv(lasso, X, y, d_scorer)
d_cv_results


# %% CrossValidation scores from d_cv_results ----------------------------------
d_cv_scores = get_cv_scores_from_cv_results(d_cv_results, only_mean=True)
d_cv_scores


# %% Test Scores with d_cv_results estimators ----------------------------------
get_test_scores_from_cv_results(d_cv_results, X_test = X, y_test = y, 
                                d_scorer = d_scorer, prefix='valid', 
                                only_mean=True)

# %%
{k:v for k,v in d_cv_results.items() if ('fitted_estimator' in k)}
# %%
