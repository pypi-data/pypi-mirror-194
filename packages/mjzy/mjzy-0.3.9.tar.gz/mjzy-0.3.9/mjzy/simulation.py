import numpy as np
from . import covarience_matrix

def multivariate_normal_simulation(covariance_matri, n_samples, explained_variance=1.0,mean=0, method="Direct"):
    if method == "PCA":

        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matri)

        mask = eigenvalues > np.finfo(np.float32).eps
        eigenvalues = eigenvalues[mask][::-1]
        eigenvectors = eigenvectors[:, mask][:, ::-1]

        if explained_variance == 1.0:
            explained_variance = 1.0
        elif explained_variance <= 0.0:
            raise ValueError("explained_variance must be a positive number")
        else:
            explained_variance = min(1.0, explained_variance)

        cum_var = np.cumsum(eigenvalues) / np.sum(eigenvalues)
        n_components = np.searchsorted(
        cum_var, explained_variance, side='right')
        z = np.random.normal(size=(n_components, n_samples))
        B = eigenvectors[:, :n_components] * \
          np.sqrt(eigenvectors[:n_components])
        x = np.dot(B, z).T

        return x
    elif method == "Direct":
        ma = covarience_matrix.chol_psd(covariance_matri)
        n=np.random.normal(size=(covariance_matri.shape[0], n_samples))
        x=np.transpose(np.dot(ma, n) + mean)
        return x


