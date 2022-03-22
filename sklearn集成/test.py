import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component
from kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model, InputPath
import kfp.components as comp

@component(output_component_file='load_digits_component.yaml', packages_to_install=['utils', 'os', 'os.path', 'joblib', 'urllib.request', 'gzip', 'hashlib', 'numpy', 'utils.deprecation', 'importlib', 'collections', 'preprocessing', 'shutil', 'pathlib', 'csv'])
def load_digits(load_digits_output:Output[Dataset], *, n_class=10, return_X_y=False, as_frame=False):
    from collections import namedtuple
    import shutil

    from os.path import expanduser, isdir, join, splitext
    import gzip

    import hashlib

    from os import environ, listdir, makedirs
    from urllib.request import urlretrieve
    from pathlib import Path
    import csv
    from importlib import resources
    import numpy as np
    import shutil
    from os.path import expanduser, isdir, join, splitext
    from importlib import resources
    from urllib.request import urlretrieve
    from os import environ, listdir, makedirs

    import hashlib
    import gzip
    import csv
    from pathlib import Path
    from collections import namedtuple
    import os
    import numpy as np
    import joblib

    def _convert_data_dataframe(caller_name, data, target, feature_names, target_names, sparse_data=False):
        pd = check_pandas_support('{} with as_frame=True'.format(caller_name))
        if (not sparse_data):
            data_df = pd.DataFrame(data, columns=feature_names)
        else:
            data_df = pd.DataFrame.sparse.from_spmatrix(data, columns=feature_names)
        target_df = pd.DataFrame(target, columns=target_names)
        combined_df = pd.concat([data_df, target_df], axis=1)
        X = combined_df[feature_names]
        y = combined_df[target_names]
        if (y.shape[1] == 1):
            y = y.iloc[(:, 0)]
        return (combined_df, X, y)

    def load_gzip_compressed_csv_data(data_file_name, *, data_module=DATA_MODULE, descr_file_name=None, descr_module=DESCR_MODULE, encoding='utf-8', **kwargs):
        'Loads gzip-compressed `data_file_name` from `data_module` with `importlib.resources`.\n\n    1) Open resource file with `importlib.resources.open_binary`\n    2) Decompress file obj with `gzip.open`\n    3) Load decompressed data with `np.loadtxt`\n\n    Parameters\n    ----------\n    data_file_name : str\n        Name of gzip-compressed csv file  (`\'*.csv.gz\'`) to be loaded from\n        `data_module/data_file_name`. For example `\'diabetes_data.csv.gz\'`.\n\n    data_module : str or module, default=\'sklearn.datasets.data\'\n        Module where data lives. The default is `\'sklearn.datasets.data\'`.\n\n    descr_file_name : str, default=None\n        Name of rst file to be loaded from `descr_module/descr_file_name`.\n        For example `\'wine_data.rst\'`. See also :func:`load_descr`.\n        If not None, also returns the corresponding description of\n        the dataset.\n\n    descr_module : str or module, default=\'sklearn.datasets.descr\'\n        Module where `descr_file_name` lives. See also :func:`load_descr`.\n        The default  is `\'sklearn.datasets.descr\'`.\n\n    encoding : str, default="utf-8"\n        Name of the encoding that the gzip-decompressed file will be\n        decoded with. The default is \'utf-8\'.\n\n    **kwargs : dict, optional\n        Keyword arguments to be passed to `np.loadtxt`;\n        e.g. delimiter=\',\'.\n\n    Returns\n    -------\n    data : ndarray of shape (n_samples, n_features)\n        A 2D array with each row representing one sample and each column\n        representing the features and/or target of a given sample.\n\n    descr : str, optional\n        Description of the dataset (the content of `descr_file_name`).\n        Only returned if `descr_file_name` is not None.\n    '
        with resources.open_binary(data_module, data_file_name) as compressed_file:
            compressed_file = gzip.open(compressed_file, mode='rt', encoding=encoding)
            data = np.loadtxt(compressed_file, **kwargs)
        if (descr_file_name is None):
            return data
        else:
            assert (descr_module is not None)
            descr = load_descr(descr_module=descr_module, descr_file_name=descr_file_name)
            return (data, descr)
    'Load and return the digits dataset (classification).\n\n    Each datapoint is a 8x8 image of a digit.\n\n    =================   ==============\n    Classes                         10\n    Samples per class             ~180\n    Samples total                 1797\n    Dimensionality                  64\n    Features             integers 0-16\n    =================   ==============\n\n    This is a copy of the test set of the UCI ML hand-written digits datasets\n    https://archive.ics.uci.edu/ml/datasets/Optical+Recognition+of+Handwritten+Digits\n\n    Read more in the :ref:`User Guide <digits_dataset>`.\n\n    Parameters\n    ----------\n    n_class : int, default=10\n        The number of classes to return. Between 0 and 10.\n\n    return_X_y : bool, default=False\n        If True, returns ``(data, target)`` instead of a Bunch object.\n        See below for more information about the `data` and `target` object.\n\n        .. versionadded:: 0.18\n\n    as_frame : bool, default=False\n        If True, the data is a pandas DataFrame including columns with\n        appropriate dtypes (numeric). The target is\n        a pandas DataFrame or Series depending on the number of target columns.\n        If `return_X_y` is True, then (`data`, `target`) will be pandas\n        DataFrames or Series as described below.\n\n        .. versionadded:: 0.23\n\n    Returns\n    -------\n    data : :class:`~sklearn.utils.Bunch`\n        Dictionary-like object, with the following attributes.\n\n        data : {ndarray, dataframe} of shape (1797, 64)\n            The flattened data matrix. If `as_frame=True`, `data` will be\n            a pandas DataFrame.\n        target: {ndarray, Series} of shape (1797,)\n            The classification target. If `as_frame=True`, `target` will be\n            a pandas Series.\n        feature_names: list\n            The names of the dataset columns.\n        target_names: list\n            The names of target classes.\n\n            .. versionadded:: 0.20\n\n        frame: DataFrame of shape (1797, 65)\n            Only present when `as_frame=True`. DataFrame with `data` and\n            `target`.\n\n            .. versionadded:: 0.23\n        images: {ndarray} of shape (1797, 8, 8)\n            The raw image data.\n        DESCR: str\n            The full description of the dataset.\n\n    (data, target) : tuple if ``return_X_y`` is True\n        A tuple of two ndarrays by default. The first contains a 2D ndarray of\n        shape (1797, 64) with each row representing one sample and each column\n        representing the features. The second ndarray of shape (1797) contains\n        the target samples.  If `as_frame=True`, both arrays are pandas objects,\n        i.e. `X` a dataframe and `y` a series.\n\n        .. versionadded:: 0.18\n\n    Examples\n    --------\n    To load the data and visualize the images::\n\n        >>> from sklearn.datasets import load_digits\n        >>> digits = load_digits()\n        >>> print(digits.data.shape)\n        (1797, 64)\n        >>> import matplotlib.pyplot as plt\n        >>> plt.gray()\n        >>> plt.matshow(digits.images[0])\n        <...>\n        >>> plt.show()\n    '
    (data, fdescr) = load_gzip_compressed_csv_data(data_file_name='digits.csv.gz', descr_file_name='digits.rst', delimiter=',')
    target = data[(:, (- 1))].astype(int, copy=False)
    flat_data = data[(:, :(- 1))]
    images = flat_data.view()
    images.shape = ((- 1), 8, 8)
    if (n_class < 10):
        idx = (target < n_class)
        (flat_data, target) = (flat_data[idx], target[idx])
        images = images[idx]
    feature_names = ['pixel_{}_{}'.format(row_idx, col_idx) for row_idx in range(8) for col_idx in range(8)]
    frame = None
    target_columns = ['target']
    if as_frame:
        (frame, flat_data, target) = _convert_data_dataframe('load_digits', flat_data, target, feature_names, target_columns)
    if return_X_y:
        return joblib.dump({'flat_data': flat_data, ' target': target}, load_digits_output.path)
    return joblib.dump({'Bunchdataflat_data': Bunchdataflat_data, ' targettarget': targettarget, ' frameframe': frameframe, ' feature_namesfeature_names': feature_namesfeature_names, ' target_namesnp.arange10': target_namesnp.arange10, ' imagesimages': imagesimages, ' DESCRfdescr': DESCRfdescr}, load_digits_output.path)
