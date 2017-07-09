from __future__ import absolute_import
from .cifar import load_batch
from ..utils.data_utils import get_file
from .. import backend as K
import numpy as np
import os


def load_data():
    """Loads CIFAR10 dataset.

    # Returns
        Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.
    """
    dirname = 'cifar-10-batches-py'
    origin = 'http://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'
    path = get_file(dirname, origin=origin, untar=True)
    nb_train_samples = 50000

    #生成4阶张量50000*3*32*32
    x_train = np.zeros((nb_train_samples, 3, 32, 32), dtype='uint8')
    #生成1阶张量50000*1
    y_train = np.zeros((nb_train_samples,), dtype='uint8')
    #导入训练数据
    for i in range(1, 6):
        fpath = os.path.join(path, 'data_batch_' + str(i))
        data, labels = load_batch(fpath)
        x_train[(i - 1) * 10000: i * 10000, :, :, :] = data
        y_train[(i - 1) * 10000: i * 10000] = labels

    #导入测试数据
    fpath = os.path.join(path, 'test_batch')
    x_test, y_test = load_batch(fpath)
    #将目标变换成50000*3*32*32维列向量
    y_train = np.reshape(y_train, (len(y_train), 1))
    y_test = np.reshape(y_test, (len(y_test), 1))

    #如果后端为tensorflow,需要进一步转换,theano使用的要求是(数据量，色度，行数，列数)
    #tensorflow使用的要求是(数据量，行数，列数，色度)
    if K.image_dim_ordering() == 'tf':
        x_train = x_train.transpose(0, 2, 3, 1)
        x_test = x_test.transpose(0, 2, 3, 1)

    return (x_train, y_train), (x_test, y_test)
