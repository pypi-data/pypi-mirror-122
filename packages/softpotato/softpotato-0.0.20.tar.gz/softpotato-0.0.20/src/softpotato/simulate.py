import numpy as np
from scipy.linalg import solve_banded

F = 96485 # C/mol, Faraday constant    
R = 8.315 # J/mol K, Gas constant


class Macro:
	
    def __init__(self, wf):
        self.E = wf.E
        self.t = wf.t
        self.dt = self.t[1]
        self.nT = np.size(self.t)
        self.dT = 1/self.nT
        self.lamb = 0.45
        self.Xmax = 6*np.sqrt(self.nT*self.lamb)
        self.dX = np.sqrt(self.dT/self.lamb) # distance increment
        self.nX = int(self.Xmax/self.dX) # number of distance elements
        self.X = np.linspace(0,self.Xmax,self.nX) # Discretisation of distance

    def Emech(self, E0=0, n=1, DO=1e-5, DR=1e-5, cRb=1e-6, ks=1e8, alpha=0.5, 
              BV='QR', Ageo=1, T=298):
        
        self.E0 = E0
        self.n = n
        self.DO = DO
        self.DR = DR
        self.cRb = cRb
        self.ks = ks
        self.alpha = alpha
        self.BV = BV
        self.Ageo = Ageo
        self.T = T
        self.FRT = F/(R*self.T)

        self.delta = np.sqrt(self.DR*self.t[-1]) # cm, diffusion layer thickness
        self.K0 = self.ks*self.delta/self.DR # Normalised standard rate constant
        self.DOR = self.DO/self.DR
        
        ## Discretisation of variables and initialisation
        self.CR = np.ones([self.nT,self.nX])
        self.CO = np.zeros([self.nT,self.nX])            
        

    def bc(self, CR1kb, CO1kb, eps):
        if self.BV == 'RO': # R -> O
            CR = CR1kb/(1 + self.dX*self.K0*np.exp((1-self.alpha)*eps))
            CO = CO1kb + (CR1kb - CR)/self.DOR
        else: # O <-> R
            CR = (CR1kb + self.dX*self.K0*np.exp(-self.alpha*eps)*(CO1kb + 
                  CR1kb/self.DOR))/(1 + self.dX*self.K0*(np.exp((1-
                  self.alpha)*eps) + np.exp(-self.alpha*eps)/self.DOR))
            CO = CO1kb + (CR1kb - CR)/self.DOR
        return CR, CO

    def sim(self):
        self.eps = (self.E-self.E0)*self.n*self.FRT # adimensional potential waveform

        for k in range(1,self.nT):

            # Boundary condition, Butler-Volmer:
            self.CR[k,0], self.CO[k,0] = self.bc(self.CR[k-1,1], 
                                         self.CO[k-1,1], self.eps[k])

            # Solving finite differences:
            for j in range(1,self.nX-1):
                self.CR[k,j] = self.CR[k-1,j] + self.lamb*(self.CR[k-1,j+1] - 
                               2*self.CR[k-1,j] + self.CR[k-1,j-1])
                self.CO[k,j] = self.CO[k-1,j] + self.DOR*self.lamb*(self.CO[k-1,j+1] - 
                               2*self.CO[k-1,j] + self.CO[k-1,j-1])
        
        I = -self.CR[:,2] + 4*self.CR[:,1] - 3*self.CR[:,0]
        self.cR = self.CR*self.cRb
        self.cO = (1-self.CR)*self.cRb
        self.i = self.n*F*self.Ageo*self.DR*self.cRb*I/(2*self.dX*self.delta)
        self.x = self.X*self.delta
