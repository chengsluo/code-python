'''
Train a simple deep CNN on the CIFAR10 small images dataset.
在CIFAR10这个小的数据集上，训练一个简单的深度卷积神经网络
GPU run command with Theano backend (with TensorFlow, the GPU is automatically used):
    THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python cifar10_cnn.py
将GPU模式设为Theano后端模式
It gets down to 0.65 test logloss in 25 epochs, and down to 0.55 after 50 epochs.
训练的时候一般采用stochastic gradient descent（SGD），一次迭代选取一个batch进行update。一个epoch的意思就是迭代次数*batch的数目 和训练数据的个数一样。
(it's still underfitting at that point, though).
还能继续拟合
'''

from __future__ import print_function

from keras.callbacks import CSVLogger
from keras.datasets import cifar10    #keras库是用于学习DL的库，所以包含常用数据集
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.utils.visualize_util import plot


batch_size = 20     #利用随机梯度下降分割的batch包含的图片数量
nb_classes = 10     #目标类别数
nb_epoch =10         #进行全数据规模训练的次数
data_augmentation = True #添加数据训练模式

# input image dimensions
img_rows, img_cols = 32, 32
# The CIFAR10 images are RGB.
img_channels = 3

# The data, shuffled and split between train and test sets:
(X_train, y_train), (X_test, y_test) = cifar10.load_data()
print (X_train.shape)
print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# Convert class vectors to binary class matrices.
#将目标数据转化成对应的二进制矩阵，对应位为1.
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

# Sequential是一系列网络层按顺序构成的栈模型
model = Sequential()

#构建网络
model.add(Convolution2D(32, 3, 3, border_mode='same',#卷积核的数目,行数，列数
                         input_shape=(3,32,32)))#对二维输入进行滑动窗卷积
print ("层编号1:,类型:二维卷积层(32,3,3),输出规模:"+str(model.output_shape))
model.add(Activation('relu'))#添加一个激活层,对一个层的输出施加激活函数relu(The Rectified Linear Unit):f(x)=max(0,x);d
print ("嵌入relu激活层")
model.add(Convolution2D(32, 3, 3))
print ("层编号2:,类型:二维卷积层(32,3,3),输出规模:"+str(model.output_shape))
model.add(Activation('relu'))
print ("嵌入relu激活层")
model.add(MaxPooling2D(pool_size=(2, 2))) #为空域信号施加最大值池化，将使图片在两个维度上均变为原长的一半
print ("层编号3:,类型:二维汇集层(2,2),输出规模:"+str(model.output_shape))
model.add(Dropout(0.25))
#为输入数据施加Dropout,将在训练过程中每次更新参数时以25%的随机断开的输入神经元连接，Dropout层用于防止过拟合

model.add(Convolution2D(64, 3, 3, border_mode='same'))
print ("层编号4:,类型:二维卷积层(64,3,3),输出规模:"+str(model.output_shape))
model.add(Activation('relu'))
print ("嵌入relu激活层")
model.add(Convolution2D(64, 3, 3))
print ("层编号5:,类型:二维汇集层(64,3,3),输出规模:"+str(model.output_shape))
model.add(Activation('relu'))
print ("嵌入relu激活层")
model.add(MaxPooling2D(pool_size=(2, 2)))
print ("层编号6:,类型:二维汇集层(2,2),输出规模:"+str(model.output_shape))
model.add(Dropout(0.25))

model.add(Flatten())  #Flatten层用来将输入“压平”，即把多维的输入一维化，常用在从卷积层到全连接层的过渡。
print ("层编号7:,类型:过渡层,多维输入>>一维输入,输出规模:"+str(model.output_shape))
model.add(Dense(512)) #添加一个512输出的全连接层,输入数自动判断
print ("层编号8:,类型:全连接层(512),输出规模:"+str(model.output_shape))
model.add(Activation('relu'))
print ("嵌入relu激活层")
model.add(Dropout(0.5))

model.add(Dense(nb_classes))#添加一个10输出的全连接层,输入数自动判断
print ("层编号:9,类型:全连接层(10),输出规模:"+str(model.output_shape))
model.add(Activation('softmax'))
print ("嵌入softmax激活层")

#编译模型
# Let's train the model using RMSprop
model.compile(loss='categorical_crossentropy',#损失函数
              optimizer='rmsprop',#优化器
              metrics=['accuracy']) #最终的性能评价函数
            #对多分类问题,计算在所有预测值上的平均正确率

#绘制模型
plot(model, to_file='model.png',show_shapes=True)

#将数据归一到[0-1]
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

#在训练数据上按batch进行一定次数的迭代训练
if not data_augmentation:
    print('Not using data augmentation.')
    csv_logger = CSVLogger('training.log')
    model.fit(X_train, Y_train,callbacks=[csv_logger],
              batch_size=batch_size,
              nb_epoch=nb_epoch,
              validation_data=(X_test, Y_test),
              shuffle=True)
else:
    print('Using real-time data augmentation.')
    # This will do preprocessing and realtime data augmentation:
    datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=0,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images

    # Compute quantities required for featurewise normalization
    # (std, mean, and principal components if ZCA whitening is applied).
    datagen.fit(X_train)

    # Fit the model on the batches generated by datagen.flow().
    model.fit_generator(datagen.flow(X_train, Y_train,
                                     batch_size=batch_size),
                        samples_per_epoch=X_train.shape[0],
                        nb_epoch=nb_epoch,
                        validation_data=(X_test, Y_test))
