import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal, wishart

class GMM_Clustering:
  def __init__(self, K):
    self.K = K

  def _initialization(self, X):
    p = X.shape[1]
    self.p = np.random.dirichlet([1]*self.K)
    self.mean =  np.random.permutation(X)[:self.K]
    self.cov = np.zeros((self.K, p, p))
    for k in range(self.K):
      self.cov[k] = wishart.rvs(df=p, scale=[0.1]*p)
      #self.cov[k] = np.identity(p)


  def fit(self, X, max_iter=1000):
    #self.likelihood_history = []
    self._initialization(X)
    for i in range(max_iter):
      P = self.expectation(X)
      self.maximization(X, P)
      #self.likelihood_history.append(self.log_likelihood(X))

  def maximization(self, X, P):
    n = len(X)
    d = X.shape[1]
    nk = P.sum(axis=0)
    self.p = nk / n
    self.mean = (P.T @ X) / nk[None].T
    for k in range(self.K):
      p = P[:, k]
      X_ = X - self.mean[k]
      self.cov[k] = ((X_ * p[None].T).T @ X_) / p.sum()

  def expectation(self, X):
    n = len(X)
    fk = np.zeros((self.K, n))
    for k in range(self.K):
      fk[k, :] = multivariate_normal.pdf(X, self.mean[k], self.cov[k]) 
    
    f = fk.T @ self.p
    P = ((fk.T * self.p).T / f).T
    return P

  def predict(self, X):
    n = len(X)
    fk = np.zeros((self.K, n))
    for k in range(self.K):
      fk[k, :] = multivariate_normal.pdf(X, self.mean[k], self.cov[k])
    
    P = fk.T * self.p
    y_hat = P.argmax(axis=1) + 1
    return y_hat

  def log_likelihood(self, X):
    n = len(X)
    fk = np.zeros((self.K, n))
    for k in range(self.K):
      fk[k, :] = multivariate_normal.pdf(X, self.mean[k], self.cov[k])
    
    f = fk.T @ self.p
    return np.log(f).sum()

  def log_likelihood_completed(self, X):
    n = len(X)
    fk = np.zeros((self.K, n))
    for k in range(self.K):
      fk[k, :] = multivariate_normal.logpdf(X, self.mean[k], self.cov[k])
    
    P = fk.T + np.log(self.p)
    Z = P.argmax(axis=1)
    mask = Z[:, None] == np.array([np.arange(self.K)])
    return P[mask].sum()

  def BIC(self, X):
    p = X.shape[1]
    log_likelihood = self.log_likelihood(X)
    n = len(X)
    v = self.K - 1 + (self.K * p) + (self.K * p * (p+1)/2)
    return 2 * log_likelihood - v * np.log(n)

  def ICL(self, X):
    p = X.shape[1]
    log_likelihood_completed = self.log_likelihood_completed(X)
    v = self.K - 1 + (self.K * p) + (self.K * p * (p+1)/2)
    return log_likelihood_completed - v * np.log(np.pi*2) / 2
