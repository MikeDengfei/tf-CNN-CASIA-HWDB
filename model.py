#!/usr/bin/env python
# -*- coding:utf-8 -*-
###################################################
#      Filename: model.py
#        Author: lzw.whu@gmail.com
#       Created: 2017-11-16 11:58:28
# Last Modified: 2017-11-21 23:02:12
###################################################
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import tensorflow as tf


def weights_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def biases_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(name, x, W, b, strides=1):
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x, name=name)


def maxpool2d(name, x, k=2):
    return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1], padding='SAME', name=name)


def norm(name, l_input, lsize=4):
    return tf.nn.lrn(l_input, lsize, bias=1.0, alpha=0.001 / 90, beta=0.75, name=name)


# Works perfect on 140 mostly used characters
def CNN(x, n_classes, keep_prob):
    with tf.name_scope('reshape'):
        x = tf.reshape(x, [-1, 64, 64, 1])

    with tf.name_scope('conv1'):
        W_c1 = weights_variable([3, 3, 1, 32])
        b_c1 = biases_variable([32])
        c1 = conv2d('c1', x, W_c1, b_c1)

    with tf.name_scope('norm1'):
        c1 = norm('norm1', c1)

    with tf.name_scope('pool1'):
        p1 = maxpool2d('p1', c1)

    with tf.name_scope('conv2'):
        W_c2 = weights_variable([3, 3, 32, 64])
        b_c2 = biases_variable([64])
        c2 = conv2d('c2', p1, W_c2, b_c2)

    with tf.name_scope('norm2'):
        c2 = norm('norm2', c2)

    with tf.name_scope('pool2'):
        p2 = maxpool2d('p2', c2)

    with tf.name_scope('conv3'):
        W_c3 = weights_variable([3, 3, 64, 64])
        b_c3 = biases_variable([64])
        c3 = conv2d('c3', p2, W_c3, b_c3)

    with tf.name_scope('pool3'):
        p3 = maxpool2d('p3', c3)

    with tf.name_scope('fc1'):
        W_fc1 = weights_variable([8 * 8 * 64, 1024])
        b_fc1 = biases_variable([1024])
        flat = tf.reshape(p3, [-1, 8 * 8 * 64])
        fc1 = tf.nn.relu(tf.matmul(flat, W_fc1) + b_fc1)

    with tf.name_scope('dropout'):
        fc1 = tf.nn.dropout(fc1, keep_prob)

    with tf.name_scope('fc2'):
        W_fc2 = weights_variable([1024, n_classes])
        b_fc2 = biases_variable([n_classes])
        y = tf.matmul(fc1, W_fc2) + b_fc2
    return y


# For 3755-character GB2312 charset
def cnn_for_medium_charset(x, n_classes, keep_prob):
    with tf.name_scope('reshape'):
        x = tf.reshape(x, [-1, 64, 64, 1])

    with tf.name_scope('conv1'):
        W_c1 = weights_variable([3, 3, 1, 32])
        b_c1 = biases_variable([32])
        c1 = conv2d('c1', x, W_c1, b_c1)

    with tf.name_scope('pool1'):
        p1 = maxpool2d('p1', c1)

    with tf.name_scope('conv2'):
        W_c2 = weights_variable([3, 3, 32, 64])
        b_c2 = biases_variable([64])
        c2 = conv2d('c2', p1, W_c2, b_c2)

    with tf.name_scope('pool2'):
        p2 = maxpool2d('p2', c2)

    with tf.name_scope('conv3'):
        W_c3 = weights_variable([3, 3, 64, 64])
        b_c3 = biases_variable([64])
        c3 = conv2d('c3', p2, W_c3, b_c3)

    with tf.name_scope('pool3'):
        p3 = maxpool2d('p3', c3)

    with tf.name_scope('fc1'):
        W_fc1 = weights_variable([8 * 8 * 64, 1024])
        b_fc1 = biases_variable([1024])
        flat = tf.reshape(p3, [-1, 8 * 8 * 64])
        fc1 = tf.nn.relu(tf.matmul(flat, W_fc1) + b_fc1)

    with tf.name_scope('dropout'):
        fc1 = tf.nn.dropout(fc1, keep_prob)

    with tf.name_scope('fc2'):
        W_fc2 = weights_variable([1024, n_classes])
        b_fc2 = biases_variable([n_classes])
        y = tf.matmul(fc1, W_fc2) + b_fc2
    return y
