import numpy as np
import pandas as pd


# calculate weight covariance
def preprocess_returns(returns):

    returns_array = returns.values
    mean_return = np.mean(returns_array, axis=0)
    normalized_returns = returns_array - mean_return
    return normalized_returns, mean_return


def exp_weighted_cov(returns, lambda_=0.97):
    
    normalized_returns, mean_return = preprocess_returns(returns)
    n = len(returns)
    weighted_cov = np.cov(normalized_returns.T)
    for t in range(1, n):
        current_return = normalized_returns[t]
        weighted_cov = lambda_ * weighted_cov + (1 - lambda_) * np.outer(current_return, current_return)
    return weighted_cov

# calculate weighted matrxi

def exp_weighted_matrix(returns, lambda_=0.97):

    returns = returns.values
    n_w_m = returns.shape[0]
    weights = np.zeros(n_w_m)
    
    for t in range(n_w_m):
        weights[n_w_m-1-t]  = (1-lambda_)*lambda_**t

    weights_matrix = np.diag(weights/sum(weights))

    return weights_matrix

# cholesky decomposition
def chol_psd(matrix):
    le = len(matrix)
    ze = -1e-8
    root = np.array([[0.0] * le for _ in range(le)])
    for j in range(le):
        s = root[j,:j]@root[j,:j].T
        temp = matrix[j,j] - s
        if 0 >= temp >= ze:
            temp = 0.0
        elif temp < ze:
            raise ValueError("non-PSD")
        root[j,j] = np.sqrt(temp)
        if root[j,j] == 0:
            continue
        for i in range(j+1,le):
            s = root[i,:j]@root[j,:j]
            root[i,j] =(matrix[i,j] - s)*1.0/root[j,j]
    return root


# Rebonato and Jackel
def near_psd(matrix, epsilon=0.0):

    invSD = None

    n = matrix.shape[0]
    out = matrix.copy()
    if np.count_nonzero(np.diag(out) == 1.0) != n:
        invSD = np.diag(1 / np.sqrt(np.diag(out)))
        out = np.matmul(np.matmul(invSD, out), invSD)

    vals, vecs = np.linalg.eigh(out)
    vals = np.maximum(vals, epsilon)
    T = np.reciprocal(np.matmul(np.square(vecs), vals))
    T = np.diag(np.sqrt(T))
    l = np.diag(np.sqrt(vals))
    B = np.matmul(np.matmul(T, vecs), l)
    out = np.matmul(B, np.transpose(B))

    if invSD is not None:
        invSD = np.diag(1 / np.diag(invSD))
        out = np.matmul(np.matmul(invSD, out), invSD)

    return out

# Higham
def proj_u(matrix):
    cor = matrix.copy()
    np.fill_diagonal(cor,1)
    return cor

def Frobenius_norm(matrix):
    return np.linalg.norm(matrix, 'fro')**2

def proj_s(matrix):
    eig_val, eig_vec = np.linalg.eigh(matrix)
    eig_val[eig_val<0] = 0
    p = eig_vec@ np.diagflat(eig_val)@eig_vec.T
    return p


def Higham_near_psd(matrix):
    dS = 0
    Y = matrix
    last_gamma = float("inf")
    iteration = 100000
    tol = 1e-10

    for i in range(iteration):
        R = Y - dS                      
        X = proj_s(R)                   
        dS = X - R                       
        Y = proj_u(X)                   
        gamma = Frobenius_norm(Y - matrix)   
        if abs(gamma-last_gamma)< tol:  
            break
        last_gamma = gamma
    return Y