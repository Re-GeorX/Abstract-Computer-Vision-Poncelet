# -*- coding: utf-8 -*-
"""ellipse-detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FgIEBIu8PMvooHy3hzycCAeRWEGwijco
"""

import tensorflow as tf
import numpy as np

RES= 512
BATCH_SIZE = 64
EPOCHS = 100

class RadialDense1D(tf.keras.layers.Layer):
    def __init__(self,units):
        super(RadialDense1D, self).__init__()
        self.units=units

    def build(self,input_shape):
        print(input_shape)
        self.centers=self.add_weight(
            name='centers',
            shape=[self.units,1,int(input_shape[-1])],
            initializer="random_normal",
            trainable=True
        )
        self.weight=self.add_weight(
            name='weight',
            shape=2*[self.units],
            initializer="random_normal",
            trainable=True
        )
        self.lambd=self.add_weight(
             name='lambda',
            shape=[1],
            initializer="random_normal",
            trainable=True           
        )
    def call(self,inputs):
        res=self.centers-inputs
        pre=tf.transpose(tf.exp(-abs(self.lambd)*tf.norm(res,axis=-1)**2))
        return tf.matmul(pre,self.weight)

(x_train, y_train), (x_test, y_test) =  poncelet_gen.data()
x_train = x_train.reshape( (-1, RES,RES,1) ).astype("float32")/255.0
x_test = x_test.reshape( (-1, RES,RES,1) ).astype("float32")/255.0

#### OPTION 1### CONVNETS

i = tf.keras.layers.Input((RES,RES,1))
x = tf.keras.layers.Conv2D(32, (3,3) )(i)
x = tf.keras.layers.MaxPool2D()(x)
x = tf.keras.layers.Dense(32, activation='relu')(x)
o = tf.keras.layers.Dense(1, activation='softmax')(x)

ellipse_detetction_model = tf.keras.Model(i,o)

#### OPTION 2### RADIAL_NETWORKS

i = tf.keras.layers.Input((RES,RES,1))
x = rn.RadialDense2D(32)(i)
x = tf.keras.layers.Dense(32, activation='relu')(x)
o = tf.keras.layers.Dense(1, activation='softmax')(x)

ellipse_detetction_model = tf.keras.Model(i,o)

ellipse_detection_model.compile(optimizer=tf.keras.optimizers.RMSprop(0.003), loss = tf.keras.losses.binary_crossentropy, metrics=['accuracy']  )

ellipse_detection_model.summary()

tf.keras.backend.clear_session()
ellipse_detection_model.fit( x_train, y_train, batch_size = BATCH_SIZE, epochs = EPOCHS)
ellipse_detection_model.evaluate(x_test, y_test, batch_size = BATCH_size)