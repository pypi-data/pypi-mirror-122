import numpy as np
import logging

class Perceptron:
  def __init__(self,eta,epochs):
    self.weights = np.random.randn(3) * 1e-4  # Randomly Initialize weights
    logging.info(f'Initial weights before training: {self.weights}')
    self.eta = eta
    self.epochs = epochs

  def activationFunction(self,input,weights):
    z = np.dot(input, weights)
    return(np.where(z > 0, 1, 0))

  def fit(self,X,y):
    self.X = X
    self.y = y

    X_with_bias =  np.c_[self.X, -np.ones((len(self.X),1))]

    for epoch in range(1,self.epochs + 1):
      logging.info('--'*10)
      logging.info(f'For epoch: {epoch}')
      logging.info('--'*10)
      y_hat = self.activationFunction(X_with_bias, self.weights) # Forward Propagation
      logging.info(f'Predicted value after forward pass: {y_hat}')
      self.error = self.y - y_hat
      logging.info(f'Error: \n{self.error}')
      self.weights = self.weights + self.eta * np.dot(X_with_bias.T, self.error) # Backward Propagation
      logging.info(f'Update weights after epoch: {epoch}/{self.epochs} : {self.weights}')
      self.total_loss()
      logging.info('####'*10)

  def predict(self,X):
    X_with_bias =  np.c_[X, -np.ones((len(X),1))]
    return(self.activationFunction(X_with_bias, self.weights))

  def total_loss(self):
    total_loss = np.sum(self.error) 
    logging.info(f'Total Loss: {total_loss}')
    return(total_loss)