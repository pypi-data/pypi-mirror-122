import copy

# UDFs
from ..utils.get_pipe_feature_names import *


def get_featsel_vars(pipe):
    """Get feature selection names after preprocessing a SKLearn Pipeline.

    Args:
        pipe (Pipeline): SKLearn Pipeline

    Returns:
        dict: dictionary with ranking selection and variable name.
    """

    featsel = pipe['featsel']
    preprocessing = copy.deepcopy(pipe)
    preprocessing.steps.pop(-1)
    ls_var_names = get_pipe_feature_names(preprocessing)

    # Variables seleccionadas por featsel. NOTA: Importante key para q no 
    # cambie orden
    ls_var_ranking = sorted(zip(featsel.ranking_, ls_var_names), 
                                                        key=lambda x: x[0])
    return {v:k for k,v in ls_var_ranking}
