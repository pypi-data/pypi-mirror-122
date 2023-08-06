import pandas as pd
from sklearn.base import *

class VariableSelection(BaseEstimator, TransformerMixin):
    """
    Transformer which keep necessary columns to run the model.
    """
    def __init__(self, columns = None):
        """Columns to keep in this class. If not is initialized, then uses
        columns defined by X in fit

        Args:
            columns (array, optional): column names to keep. If None, then uses
                all columns from X. Defaults to None.
        """
        self.columns = columns


    def fit(self, X, y=None):
        """Get columns from X, and keep useful variables and drop useless.
        This transformer is useful when you are not sure if your new datasets
        have new columns that you don't need. In that case, automatically new
        variables will be droped and passthrought error

        Args:
            X (pd.DataFrame): X matrix with column names.
            y (array, optional): y matrix (only for sklearn, not needed). 
                Defaults to None.
        Returns:
            [pd.DataFrame]: X with columns filtered
        """
       
        if self.columns is None:
            self.columns = X.columns.tolist()
        return self
        

    def transform(self, X, y=None):
        """Returns X with columns needed to fit the model

        Args:
            X (pd.DataFrame): X matrix with column names.
            y (array, optional): y matrix (only for sklearn, not needed). 
                Defaults to None.

        Returns:
            [pd.DataFrame]: X with columns filtered
        """
        needed_cols = [x for x in self.columns if x not in X.columns]
        if len(needed_cols) > 0:
            raise Exception('{} cols are needed in matrix!'.\
                                format(needed_cols))
        return X[self.columns]
