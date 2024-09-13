import numpy as np


def one_hot_encode(labels: np.ndarray, num_classes: int) -> np.ndarray:
    """Converts a 1D array of labels to a 2D one-hot encoded array.
    """
    return np.eye(num_classes)[labels]


def normalize(X: np.ndarray, axis: int = 0) -> np.ndarray:
    """Normalizes a 2D array along a specified axis.
    The normalize function normalizes a 2D array along a specified axis by subtracting the mean and dividing by the standard deviation."""
    return (X - np.mean(X, axis=axis, keepdims=True)) / np.std(X, axis=axis, keepdims=True)


def sigmoid(X: np.ndarray) -> np.ndarray:
    """Applies the sigmoid function element-wise to a 2D array.
    The sigmoid function applies the sigmoid function element-wise to a 2D array.
"""
    return 1 / (1 + np.exp(-X))


def relu(X: np.ndarray) -> np.ndarray:
    """Applies the ReLU function element-wise to a 2D array.
    """
    return np.maximum(0, X)


def softmax(X: np.ndarray) -> np.ndarray:
    """Applies the softmax function to a 2D array.
    """
    exp_X = np.exp(X - np.max(X, axis=1, keepdims=True))
    return exp_X / np.sum(exp_X, axis=1, keepdims=True)


def binary_crossentropy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Computes the binary cross-entropy loss between two 2D arrays.

"""
    return -np.mean(y_true * np.log(y_pred + 1e-9) + (1 - y_true) * np.log(1 - y_pred + 1e-9))


def categorical_crossentropy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Computes the categorical cross-entropy loss between two 2D arrays.

"""
    return -np.mean(y_true * np.log(y_pred + 1e-9))


def accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Computes the classification accuracy between two 2D arrays.
    """
    return np.mean(np.argmax(y_true, axis=1) == np.argmax(y_pred, axis=1))
