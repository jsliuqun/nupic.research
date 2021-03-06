#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2016, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import csv
import os
import numpy as np


"""
Data pre-processing from: 
https://github.com/guillaume-chevalier/LSTM-Human-Activity-Recognition
"""


def load_X(X_signals_paths):
  """
  Load X (inputs)

  :param X_signals_paths: (list of strings) path to input files 
  return headers: (list) columns headers
  :return: (np.Array) formatted input data.
  
  Fixed-width sliding windows of 2.56 sec and 50% overlap (128 
  readings/window).
  """
  X_signals = []
  headers = []
  for signal_type_path in X_signals_paths:
    header = '_'.join(signal_type_path.split('/')[-1].split('_')[:-1])
    headers.append(header)
    with open(signal_type_path, 'rb') as f:
      X_signals.append([np.array(r, dtype=np.float32)
                        for r in [row.replace('  ', ' ').strip().split(' ')
                                  for row in f]])
  return headers, np.transpose(np.array(X_signals), (1, 2, 0))



def load_y(y_path):
  """
  Load y (targets)

  :param y_path: (string) path to targets file. 
  :return: (np.Array) formatted targets
  """
  with open(y_path, 'rb') as f:
    y_ = np.array([elem for elem in [row.replace('  ', ' ').strip().split(' ')
                                     for row in f]], dtype=np.int32)
    return y_ - 1  # 0-based indexing



def generate_data(X_train_signals_paths,
                  X_test_signals_paths,
                  y_train_path,
                  y_test_path):
  """
  Generate train and test data.
  
  :param X_train_signals_paths: (list of str) paths to train data (inputs)
  :param X_test_signals_paths: (list of str) paths to test data (inputs) 
  :param y_train_path: (str) path to train data (targets)
  :param y_test_path: (str) path to test data (targets)
  """
  headers_train, X_train = load_X(X_train_signals_paths)
  headers_test, X_test = load_X(X_test_signals_paths)
  y_train = load_y(y_train_path)
  y_test = load_y(y_test_path)

  assert headers_test == headers_train
  headers_train.append('label')
  train_csv = 'inertial_signals_train.csv'

  with open(train_csv, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers_train)
    for i in range(len(X_train)):
      for x in X_train[i]:
        row = list(x)
        row.append(y_train[i][0])
        writer.writerow(row)

  test_csv = 'inertial_signals_test.csv'
  with open(test_csv, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers_test)
    for i in range(len(X_test)):
      for x in X_test[i]:
        row = list(x)
        row.append(y_test[i][0])
        writer.writerow(row)



if __name__ == '__main__':
  INPUT_SIGNAL_TYPES = [
    'body_acc_x_',
    'body_acc_y_',
    'body_acc_z_',
    'body_gyro_x_',
    'body_gyro_y_',
    'body_gyro_z_',
    'total_acc_x_',
    'total_acc_y_',
    'total_acc_z_'
  ]

  LABELS = [
    'WALKING',
    'WALKING_UPSTAIRS',
    'WALKING_DOWNSTAIRS',
    'SITTING',
    'STANDING',
    'LAYING'
  ]

  DATASET_PATH = 'UCI HAR Dataset'
  TRAIN = 'train'
  TEST = 'test'

  X_train_signals_paths = [os.path.join(DATASET_PATH,
                                        TRAIN,
                                        'Inertial Signals',
                                        signal + 'train.txt')
                           for signal in INPUT_SIGNAL_TYPES]

  X_test_signals_paths = [os.path.join(DATASET_PATH,
                                       TEST,
                                       'Inertial Signals',
                                       signal + 'test.txt')
                          for signal in INPUT_SIGNAL_TYPES]

  y_train_path = os.path.join(DATASET_PATH, TRAIN, 'y_train.txt')
  y_test_path = os.path.join(DATASET_PATH, TEST, 'y_test.txt')

  generate_data(X_train_signals_paths,
                X_test_signals_paths,
                y_train_path,
                y_test_path)
