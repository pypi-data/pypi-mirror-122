import numpy as np
import logging
from tqdm import tqdm

class Perceptron:
  def __init__(self, eta, epochs):
    self.weights = np.random.randn(3) * 1e-5   # Small weight
    logging.info(f"initial weights before training: \n{self.weights}")
    self.eta = eta   # learning rate
    self.epochs = epochs  # number of epochs

  def activationFunction(self, inputs, weights):
      z = np.dot(inputs, weights)   # z = W * X
      return np.where(z > 0, 1, 0)  # Condition If True, False

  def fit(self, X, Y):
      self.X = X
      self.Y = Y
      X_with_bias = np.c_[self.X, -np.ones((len(self.X), 1))]  # concatenation
      logging.info(f"X with bias is: \n{X_with_bias}")

      for epoch in tqdm(range(self.epochs), total=self.epochs, desc='training the model'):
        logging.info("--"*10)
        logging.info(f"for epoch: {epoch}")
        logging.info("--"*10) # 

        y_hat = self.activationFunction(X_with_bias, self.weights) # forward propagation
        logging.info(f"predicted value after forward pass is: {y_hat}")
        self.error = self.Y - y_hat
        logging.info(f"error is: \n{self.error}")
        self.weights = self.weights + self.eta * np.dot(X_with_bias.T, self.error) # backward propagation
        logging.info(f"updated weights after epoch: \n{epoch}/{self.epochs}: \n {self.weights}")
        logging.info("######"*10)

  def predict(self, X):
      X_with_bias = np.c_[X, -np.ones((len(X), 1))]
      return self.activationFunction(X_with_bias, self.weights)

  def total_loss(self):
      total_loss = np.sum(self.error)
      logging.info(f"total loss is: {total_loss}")
      return total_loss