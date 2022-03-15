import numpy as np


def augment(A,b): 
  return np.column_stack((A,b))


def first_column_zeros(A):
  B=np.copy(A)
  for i in range(1, len(A)):
    coeff = B[i,0]/B[0,0]
    B[i] = B[i]-coeff*B[0]
  return B

def row_echelon(C):
    for i in range(len(C) - 1):
        C[i:,i:] = first_column_zeros(C[i:,i:])
    return C


def LU_decomposition(A):
  U=np.copy(A)
  L=np.identity(len(A))
  m,n = np.shape(A)
  for j in range(n):
    for i in range(j+1, m):
      L[i,j] = (U[i,j]/U[j,j])
      U[i,:] = U[i,:] - L[i,j]*U[j,:]
  return L,U


def forward_substitution(L,b): # Accepts a lower triangular square matrix L and a vector b, solves Ly=b for y.
  n = len(b)
  y = np.zeros(n)
  for i in range(n):
    y[i] = (b[i] - np.dot(y, L[i,:]))/L[i,i]
  return y


def back_substitution(U,y):    # Accepts an upper triangular square matrix U and a vector b, solves Ux=b for x.
  n = len(y)
  x = np.zeros(n)
  for i in range(n-1, -1, -1):
    x[i] = (y[i] - np.dot(x, U[i,:]))/U[i,i]
  return x


def LU_solver(A,b): 
  L,U = LU_decomposition(A)
  y = forward_substitution(L,b)
  x = back_substitution(U, y)
  return x
