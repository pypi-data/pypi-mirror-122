import numpy as np
import logging
from tqdm import tqdm

class Perceptron:
  def __init__(self, eta, epochs):
    self.weights = np.random.randn(3) * 1e-4 # small weight INIT
    logging.info(f"initial weights before training: \n{self.weights}")
    self.eta = eta # Learning rate
    self.epochs = epochs


  def activationFunction(self, inputs, weights):
    z = np.dot(inputs, weights) # z = W * X
    return np.where(z>0, 1, 0)

  def fit(self, X, y):
    """training the perceptron

    Args:
        X (pd.DataFrame): Independent features DataFrame
        y (pd.DataFrame): Dependent feature DataFrame
    """
    self.X = X
    self.y = y

    X_with_bias = np.c_[self.X, -np.ones((len(self.X), 1))] # Concatenation
    logging.info(f"X with bias: \n{X_with_bias}")

    for epoch in tqdm(range(1,self.epochs+1), total=self.epochs, desc="training the model"):
      logging.info("--" * 10)
      logging.info(f"for epoch: {epoch}")

      y_hat = self.activationFunction(X_with_bias, self.weights) # forward propogation
      logging.info(f"predicted value after forward pass: {y_hat}")
      self.error = self.y - y_hat
      logging.info(f"error: \n{self.error}")
      self.weights = self.weights + self.eta * np.dot(X_with_bias.T, self.error) # backward propagation
      logging.info(f"updated weights after epoch: {epoch}/{self.epochs} \n{self.weights}")
      logging.info("#####"*10)



  def predict(self, X):
    """For generating predictions for unknown data

    Args:
        X (np.array): array of inputs

    Returns:
        np.array: array of predictions
    """
    X_with_bias = np.c_[X, -np.ones((len(X), 1))]
    return self.activationFunction(X_with_bias, self.weights)
  
  def total_loss(self):
    """total training error

    Returns:
        float: sum of errors of trained model
    """
    total_loss = np.sum(self.error)
    logging.info(f"total_loss: {total_loss}")
    return total_loss