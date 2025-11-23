import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
from scipy.stats import multivariate_normal

class GaussianClusterModel:
    def __init__(self, clusters=3, iterations=100, threshold=1e-4, seed=42):
        self.clusters = clusters
        self.iterations = iterations
        self.threshold = threshold
        self.seed = seed
        
        self.mix_ratio = None
        self.centroids = None
        self.cov_matrices = None
        
    def _setup(self, matrix):
        np.random.seed(self.seed)
        samples, feats = matrix.shape
        
        chosen = np.random.choice(samples, self.clusters, replace=False)
        self.centroids = matrix[chosen]
        
        self.mix_ratio = np.ones(self.clusters) / self.clusters
        
        self.cov_matrices = [np.cov(matrix.T) for _ in range(self.clusters)]
    
    def _log_prob(self, matrix, centroids, covs, weights):
        rows, _ = matrix.shape
        log_p = np.zeros((rows, self.clusters))
        
        for c in range(self.clusters):
            dist = multivariate_normal(
                mean=centroids[c], 
                cov=covs[c], 
                allow_singular=True
            )
            log_p[:, c] = np.log(weights[c] + 1e-10) + dist.logpdf(matrix)
        
        return log_p
    
    def train(self, matrix):
        matrix = np.atleast_2d(matrix)
        if matrix.shape[1] == 1:
            matrix = matrix.reshape(-1, 1)
        
        self._setup(matrix)
        
        for _ in range(self.iterations):
            logp = self._log_prob(matrix, self.centroids, self.cov_matrices, self.mix_ratio)
            combined = np.logaddexp.reduce(logp, axis=1)
            
            resp_log = logp - combined[:, np.newaxis]
            resp = np.exp(resp_log)
            
            nk = resp.sum(axis=0)
            upd_weights = nk / nk.sum()
            
            upd_means = resp.T @ matrix / nk[:, np.newaxis]
            
            upd_covs = []
            for c in range(self.clusters):
                diff = matrix - upd_means[c]
                cov = (resp[:, c][:, np.newaxis] * diff).T @ diff / nk[c]
                cov += np.eye(cov.shape[0]) * 1e-6
                upd_covs.append(cov)
            
            w_change = np.abs(upd_weights - self.mix_ratio).max()
            m_change = np.abs(upd_means - self.centroids).max()
            
            self.mix_ratio = upd_weights
            self.centroids = upd_means
            self.cov_matrices = upd_covs
            
            if w_change < self.threshold and m_change < self.threshold:
                break
        
        return self
    
    def assign(self, matrix):
        logp = self._log_prob(matrix, self.centroids, self.cov_matrices, self.mix_ratio)
        return np.argmax(logp, axis=1)


def fetch_data(symbol, start, end):
    frame = yf.download(symbol, start=start, end=end)
    frame = frame[['Adj Close']]
    frame['Ret'] = frame['Adj Close'].pct_change()
    frame = frame.dropna()
    return frame


def visualize_states(frame, model, symbol, ret_array):
    plt.figure(figsize=(15, 10))
    
    states = model.assign(ret_array)
    
    for s in range(model.clusters):
        idx = states == s
        plt.plot(
            frame.index[idx],
            frame['Adj Close'][idx],
            '.',
            label=f'Cluster {s}'
        )
    
    plt.title(f'{symbol} Regimes')
    plt.xlabel('Date')
    plt.ylabel('Adjusted Close')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return states


def inspect_states(assignments, model, ret_array, frame):
    print("\nCluster-Wise Market Summary:")
    for s in range(model.clusters):
        mask = assignments == s
        cluster_ret = ret_array[mask]
        cluster_prices = frame['Adj Close'][mask]


def run():
    STOCK = "AAPL"
    DATE_START = "2010-01-01"
    DATE_END = datetime.today().strftime('%Y-%m-%d')
    CLUSTERS = 3

    frame = fetch_data(STOCK, DATE_START, DATE_END)
    ret_arr = frame['Ret'].values.reshape(-1, 1)

    model = GaussianClusterModel(clusters=CLUSTERS)
    model.train(ret_arr)

    state_tags = visualize_states(frame, model, STOCK, ret_arr)
    inspect_states(state_tags, model, ret_arr, frame)


if __name__ == "__main__":
    run()
