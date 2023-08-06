import numpy as np


def TimeSeriesSplit_TrainBlock(len_df, n_splits=5, test_size=33, 
                                train_block_size=100):
    '''
    Función para generar split ordenados y acumulados.
    
    - len_df: longitud del dataframe a hacer splits
    - n_splits: número de splits
    - test_size: tamaño del conjunto test sobre el bloque de datos
    - min_block_size: tamaño mínimo del bloque sobre el que se quiere 
                empezar a hacer splits
    '''
    train_size = len_df - test_size
    if train_size <= 0:
        raise Exception('train_size <= 0.')

    idxs_acumulative = []
    idxs_offset = [x for x in range(train_block_size)]
    idxs_group = []
    len_block = int(np.floor((len_df-train_block_size)/n_splits))

    for i in range(n_splits):        
        idxs_block = list(range(i*len_block+train_block_size, 
                                min((i+1)*len_block+train_block_size, len_df)))
        idxs_block_aux = idxs_offset+idxs_acumulative+idxs_block
        idxs_train = idxs_block_aux[:len(idxs_block_aux)-test_size]
        idxs_test = idxs_block_aux[len(idxs_block_aux)-test_size:]
        
        # Acumulado
        idxs_acumulative.extend(idxs_block)
        idxs_acumulative = np.unique(idxs_acumulative).tolist()
        
        # Split indexes
        idxs_group.append([idxs_train, idxs_test])

    return np.array(idxs_group)