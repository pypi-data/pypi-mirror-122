import numpy as np
import logging
from tqdm import tqdm

class Perceptron:
  def __init__(self, eta, epochs):
    self.weights = np.random.randn(3)*10e-4 #Sample eights
    logging.info(f"Initial weights are being trained : \n{self.weights}")
    self.eta = eta #learning rate
    self.epochs = epochs #number of iterations

  def activationfunction(self, inputs, weights):
    z = np.dot(inputs, weights) #z gives dot product of X*W
    return np.where(z>0,1,0) #condition if true retirn 1 else 0
  
  def fit(self, X, y):
    self.X = X
    self.y = y
    X_with_bais = np.c_[self.X,-np.ones((len(self.X), 1))] #Concatinating bais with inputs
    logging.info(f"Input after bais : \n{X_with_bais}")
    for epoch in tqdm(range(self.epochs), total=self.epochs, desc="training the model"):
      logging.info("**"*10)
      logging.info(f"for epoch : {epoch+1}")
      logging.info("**"*10)
      y_hat = self.activationfunction(X_with_bais, self.weights) #forward propagation
      logging.info(f"Predicted value after forward pass : \n{y_hat}")
      self.error = self.y-y_hat
      logging.info(f"Error is : \n{self.error}")
      self.weights = self.weights + self.eta*np.dot(X_with_bais.T,self.error) #backward propagation
      logging.info(f"Updated weights after : \n{epoch}/{self.epochs} \n{self.weights}")
      logging.info("##"*10)
  
  def predict(self, X):
    X_with_bais = np.c_ [X,-np.ones((len(X), 1))]
    return self.activationfunction(X_with_bais, self.weights)
  
  def total_loss(self):
    total_loss = np.sum(self.error)
    logging.info(f"Total Loss : \n{total_loss}")
    return total_loss