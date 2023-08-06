# -*- coding: utf-8 -*-
"""ARTIFICIAL BEE COLONY ALGORITHM"""



import numpy as np
from ._optimizer import Optimizer, CandidateState 
import random as rnd


class Bee(CandidateState):
    
    def __init__(self, optimizer: Optimizer):
        CandidateState.__init__(self, optimizer)
        #self.trials = 0#np.zeros([optimizer.dimensions], dtype=np.int32) #* np.nan


class ABC(Optimizer):
    """Artificial Bee Colony Algorithm class"""

    def __init__(self):
        """Initialization"""
        Optimizer.__init__(self)

        self.variant = 'Vanilla'
        self.params = {}


    def _check_params(self):
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.variant == 'Vanilla':
            mandatory_params += 'bees trial_limit'.split()
            
            if 'bees' in self.params:
                self.params['bees'] = int(self.params['bees'])
            else:
                self.params['bees'] = self.dimensions
            defined_params += 'bees'.split()
            
            if 'trial_limit' in self.params:
                self.params['trial_limit'] = int(self.params['trial_limit'])            
            else:
                self.params['trial_limit'] = int((self.params['bees']*self.dimensions)/2) # Karaboga and Gorkemli 2014 - "A quick artificial bee colony (qabc) algorithm and its performance on optimization problems"
                defined_params += 'trial_limit'.split()
        
        else:
            assert False, f'Unknown variant! {self.variant}'

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)


    def _init_method(self):

        self._evaluate_initial_candidates()
        err_msg = None

        # Generate a swarm
        self.cS = np.array([Bee(self) for c in range(self.params['bees'])], dtype=Bee)
        self.cS_k = np.array([Bee(self) for c in range(self.params['bees'])], dtype=Bee)

        # Generate initial trial and probability vectors

        self.trials = np.zeros([self.params['bees']],dtype=np.int32)
        self.probability = np.zeros([self.params['bees']])

        n0 = 0 if self._cs0 is None else self._cs0.size
        for p in range(self.params['bees']):
            
            # Random position
            self.cS[p].X =  np.random.uniform(self.lb, self.ub)

            # Using specified particles initial positions
            if p < n0:
                self.cS[p] = self._cs0[p].copy()
            
        # Evaluate
        if n0 < self.params['bees']:
            err_msg = self.collective_evaluation(self.cS[n0:])
        # err_msg = self.collective_evaluation(self.cS)
        # err_msg = self.collective_evaluation(self.cS_k)
        #self.cS_k = np.copy(self.cS)

        # if all candidates are NaNs       
        if np.isnan([cP.f for cP in self.cS]).all():
            err_msg = 'ALL CANDIDATES FAILED TO EVALUATE.'
        
        if err_msg:
            return err_msg
        
        self.cB = np.array([cP.copy() for cP in self.cS])

        self._finalize_iteration()
        
    
    def _employed_bees_phase(self):
        
        err_msg = None
        
        for p, cP in enumerate(self.cS_k):
        
            k = np.random.randint(0,self.params['bees'])
            while k == p:
                k = np.random.randint(0,self.params['bees'])
     
            d = np.random.randint(0,self.dimensions)
            phi = np.random.uniform(-1,1)
            
            for i in range(self.dimensions):
                if i != d: self.cS_k[p].X[i] = self.cS[p].X[i]
     
            self.cS_k[p].X[d] = self.cS[p].X[d] + phi*(self.cS[p].X[d] - self.cS[k].X[d])
            
            cP.clip()
                
        for cP in self.cS:
            cP.clip()

        err_msg = self.collective_evaluation(self.cS_k)
        
        for p, cP in enumerate(self.cS_k):
            if self.cS_k[p] < self.cS[p]:
                self.cS[p] = self.cS_k[p].copy()
                self.trials[p] = 0
            else:
                self.trials[p] = self.trials[p] + 1
    
        if err_msg:
            return err_msg
    
    
    def _fitness_calc(self):
        temp_fitness = np.array([])
            
        for p, cP in enumerate(self.cS):
            temp_fitness = np.append(temp_fitness, self.cS[p].f)
        
        return temp_fitness
        
        
    def _run(self):
        self._check_params()
        
        err_msg = self._init_method()
        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'

        if 'trial_limit' in self.params:
            trial_limit = self.params['trial_limit']

        while True:
            
            """employed bees phase"""
            err_msg = self._employed_bees_phase()
        
            
            """probability update"""
            for p, cP in enumerate(self.cS):
                # self.probability[p] = 0.1 + 0.9 * (self.cS[p].f/np.max(temp_fitness))
                self.probability[p] = self.cS[p].f / np.sum(self._fitness_calc())
                
            """onlooker bee phase"""
            i = 0
            t = 0
            while t < self.params['bees']:
                
                if np.random.uniform(0,1) < self.probability[i]:
                    
                    t = t + 1
                    err_msg = self._employed_bees_phase()
   
                i = (i + 1)%(self.params['bees'] - 1)

            
            """scout bee phase"""
            for p, cP in enumerate(self.cS):
                if self.trials[p] > trial_limit:
                    self.cS[p].X = np.random.uniform(self.lb, self.ub)
                    self.trials[p] = 0
            
            if err_msg:
                break

            if self._finalize_iteration():
                break

        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'
        
        return self.best

