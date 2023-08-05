import numpy as np
import logging
from tqdm import tqdm

class Perceptron:
  def __init__(self,eta,epochs):        #eta is learning rate
    self.weights = np.random.randn(3) * 1e-4   #making small weight init
    logging.info(f"initial weights before training :\n {self.weights}")
    self.eta = eta
    self.epochs = epochs

  def activationfunction(self,inputs,weights):
    z = np.dot(inputs,weights)  # z = w * x  a matrix
    logging.info("#"*10)
    #logging.info(f"activation  z vale :\n{z}")
    #logging.info("#"*10)
    return np.where(z > 0,1,0)

  def fit(self,x,y):
     self.x = x
     self.y = y
     x_with_bias = np.c_[self.x,-np.ones((len(self.x),1))] #concatenation of x and bias to give matrix
     logging.info(f"x with bais : \n{x_with_bias}")

     #for epoch in range(self.epochs):
     for epoch in tqdm(range(self.epochs),total=self.epochs,desc="training the model"): 
       logging.info("#"*10)
       logging.info(f"for epoch :{epoch}")
       logging.info("#"*10)

       y_hat = self.activationfunction(x_with_bias,self.weights)  # z value 0 or 1  #forward propogation
       logging.info(f"predicted value after forward pass :\n{y_hat}")
       logging.info(f"expected value after forward pass :\n{y}")
       self.error = self.y - y_hat  #error = y - y_hat
       logging.info(f"error :\n{self.error}")
       self.weights = self.weights + self.eta * np.dot(x_with_bias.T,self.error) # new weight = old weight + n(y_hat) #backward propogation
       logging.info(f"update weights after epoch :\n{epoch}/{self.epochs} : {self.weights}")
       logging.info("#"*10)

  def predict(self,x):
     x_with_bias = np.c_[x,-np.ones((len(x),1))]
     return self.activationfunction(x_with_bias,self.weights)  # x with updated weights

  def total_loss(self):
      total_loss = np.sum(self.error)   
      logging.info(f"total loss :{total_loss}")
      return total_loss