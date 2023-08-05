from .lib import *

def backend_test(func, **kwargs):
    X, y, X_test = func(backend='numpy', **kwargs).get_data()
    assert X.dtype == y.dtype == X_test.dtype == np.float64
    X, y, X_test = func(backend='torch', **kwargs).get_data()
    assert X.dtype == y.dtype == X_test.dtype == torch.float64
    X, y, X_test = func(backend='tf', **kwargs).get_data()
    assert X.dtype == y.dtype == X_test.dtype == tf.float64

def plotting_test(func, **kwargs):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    func(backend='numpy', **kwargs).plot(ax=ax)
    fig.savefig('figures/'+func.__name__+'.pdf')

def non_syntetic_test(func, **kwargs):
    """
    Non-synthetic data should not have noise by default.
    """
    import pandas as pd
    obj = func(return_test=False, scale_X=False, scale_y=False, mean_normalize_y=False, backend='numpy')
    X, y = obj.get_data(squeeze_y=False)
    end_data = np.concatenate([X, y], axis=1)
    start_data = pd.read_csv('archive/'+obj.file_name).values
    assert np.allclose(end_data, start_data)