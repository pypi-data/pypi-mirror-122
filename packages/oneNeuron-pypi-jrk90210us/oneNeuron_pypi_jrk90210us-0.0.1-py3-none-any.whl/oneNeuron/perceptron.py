import numpy as np
import logging
from tqdm import tqdm

class Perceptron:
  def __init__(self, learning_rate, epochs):
    self.learning_rate = learning_rate
    self.epochs = epochs
    # initiliaze random weights
    self.weights = np.random.randn(3) * 1e-4 
    logging.info(f"Initial weights before training: \n{self.weights}")
  
  def activationFunction(self, X, weights):
    z = np.dot(X, weights)
    return np.where(z>0, 1, 0)
  
  def fit(self, X, y):
    self.X = X
    self.y = y

    # prepare X with Bias term
    X_with_bias = np.c_[X, -np.ones((len(self.X), 1))]
    logging.info(f"X with bias: \n{X_with_bias}")

    for epoch in tqdm(range(self.epochs), total=self.epochs, desc="Training model"):
      logging.info("----"*10)
      logging.info(f"Epoch: {epoch}/{self.epochs}")
      logging.info("----"*10)
      # Forward pass
      y_hat = self.activationFunction(X_with_bias, self.weights)
      logging.info(f"Predicted values: \n{y_hat}")
      self.error = self.y - y_hat
      logging.info(f"Errors: \n{self.error}")
      # Backpropogation
      self.weights = self.weights + self.learning_rate * np.dot(X_with_bias.T, self.error)
      logging.info(f"Updated weights after epoch {epoch}/{self.epochs}: \n{self.weights}")
      logging.info("======"*10)
  
  def predict(self, X):
    X_with_bias = np.c_[X, -np.ones((len(X), 1))]
    #logging.info(f"Predict: X with bias: \n{X_with_bias}")
    return self.activationFunction(X_with_bias, self.weights)
  
  def total_loss(self):
    total_loss = np.sum(self.error)
    logging.info(f"Total loss: {total_loss}")
    return total_loss