import numpy as np
import numpy.random as rand
from scipy.linalg import toeplitz

def Simulate(Rho=0, Beta = 0, D_N = np.eye(100), D_T = np.eye(150), Sigma_E = 1, idx = 1):
    N_Assets = 100
    T_Observations = 150
    Factor1 = rand.normal(loc=1.2, scale=3.0, size=T_Observations)
    Factor2 = rand.normal(loc=0.1, scale=1.0, size=T_Observations)
    Factor3 = rand.normal(loc=0.4, scale=0.4, size=T_Observations)
    F_Matrix = np.array([Factor1, Factor2, Factor3]).T

    Loading2 = rand.rand(N_Assets)
    Loading1 = np.ones_like(Loading2)
    Loading3 = rand.rand(N_Assets)
    Lambda_Matrix = np.stack([Loading1, Loading2, Loading3]).T/np.sqrt(N_Assets)
    Part1 = F_Matrix.dot(Lambda_Matrix.T)

    Epsilon = rand.randn(T_Observations, N_Assets)
    A_T_Column1 = [Rho ** (i) for i in range(T_Observations)]
    A_T = toeplitz(c=A_T_Column1, r=[1]+[0]*(T_Observations-1))
    A_N = toeplitz(c=[1]+[0]*(N_Assets-1),r=[1,Beta,Beta,Beta, Beta**2]+[0]*(N_Assets-5))
    Residuals = Sigma_E * (((D_T.dot(A_T)).dot(Epsilon)).dot(A_N).dot(D_N))
    Result = Part1 + Residuals

    np.savetxt(fname='Simulation_Dataset_{}.csv'.format(idx), X=Result, delimiter=',')
    np.savetxt(fname='Simulation_Factor_{}.csv'.format(idx), X=F_Matrix, delimiter=',')
    np.savetxt(fname='Simulation_Loading_{}.csv'.format(idx), X=Lambda_Matrix, delimiter=',')

def main():
    Simulate(Rho=0, Beta=0, D_N=np.eye(100), D_T=np.eye(150), Sigma_E=1, idx=1)
    Simulate(Rho=0, Beta=0, D_N=np.eye(100), D_T=np.eye(150), Sigma_E=25, idx=2)

    D_N3 = np.diag(rand.normal(loc=1,scale=np.sqrt(0.2),size=100))
    D_T3 = np.diag(rand.normal(loc=1,scale=np.sqrt(0.2),size=150))
    Simulate(Rho=0.1, Beta=0.7, D_N=D_N3, D_T=D_T3, Sigma_E=10, idx=3)

if __name__ == '__main__':
    main()