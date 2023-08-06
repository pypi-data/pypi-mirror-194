# -*- coding: utf-8 -*-

import numpy as np
from ._optimizer import Optimizer, CandidateState 
from scipy.special import gamma


class FlyingSquirrel(CandidateState):
    """SSA agent class.
    
    Returns
    -------
    FS : FlyingSquirrel
        FlyingSquirrel instance.        
    """
    
    def __init__(self, optimizer: Optimizer):
        CandidateState.__init__(self, optimizer)


class SSA(Optimizer):
    """Squirrel Search Algorithm method class.
    
    Reference: Jain, M., Singh, V., & Rani, A. (2019). A novel nature-inspired algorithm 
    for optimization: Squirrel search algorithm. Swarm and evolutionary computation, 
    44, 148-175.
    
    Parameters
    ----------
    variant : str
        Name of the SSA variant. Default: ``Vanilla``.
    params : dict
        A dictionary of SSA parameters.
    """

    def __init__(self):        
        Optimizer.__init__(self)

        self.variant = 'Vanilla'
        self.params = {}

    def _check_params(self):
        """Private method which prepares the parameters to be validated by Optimizer._check_params.

        Returns
        -------
        None
            Nothing
        """
        
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []
        
        if 'swarm_size' in self.params:
            self.params['swarm_size'] = int(self.params['swarm_size'])

        if self.variant == 'Vanilla':
            mandatory_params = 'swarm_size acorn_tree_attraction'.split()
            # the following params are better left at default
            mandatory_params += 'predator_presence_probability gliding_constant \
                                gliding_distance_limits'.split() 
            if 'swarm_size' not in self.params:
                self.params['swarm_size'] = self.dimensions
                defined_params += 'swarm_size'.split()
            if 'acorn_tree_attraction' not in self.params:
                self.params['acorn_tree_attraction'] = 0.5
                defined_params += 'acorn_tree_attraction'.split()
            # the following params are better left at default
            if 'predator_presence_probability' not in self.params:
                self.params['predator_presence_probability'] = 0.1
                defined_params += 'predator_presence_probability'.split()
            if 'gliding_constant' not in self.params:
                self.params['gliding_constant'] = 1.9
                defined_params += 'gliding_constant'.split()
            if 'gliding_distance_limits' not in self.params:
                self.params['gliding_distance_limits'] = [0.5, 1.11]
                defined_params += 'gliding_distance_limits'.split()
            optional_params = ''.split()
        else:
            assert False, f'Unknown variant! {self.variant}'
            
        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)
        
    def _init_method(self):
        """Private method for initializing the SSA optimizer instance.
        Initializes and evaluates the swarm.

        Returns
        -------
        None
            Nothing
        """
        
        err_msg = None

        # Generate a swarm of FS
        self.cS = np.array([FlyingSquirrel(self) for c in range(self.params['swarm_size'])], \
                            dtype=FlyingSquirrel)
        
        # Generate initial positions
        n0 = 0 if self._cs0 is None else self._cs0.size
        for p in range(self.params['swarm_size']):            
            # Random position
            self.cS[p].X = np.random.uniform(self.lb, self.ub)           
            # Using specified particles initial positions
            if p < n0:
                self.cS[p] = self._cs0[p].copy()
        
        # Evaluate
        if n0 < self.params['swarm_size']:
            err_msg = self.collective_evaluation(self.cS[n0:])

        # if all candidates are NaNs       
        if np.isnan([cP.f for cP in self.cS]).all():
            err_msg = 'ALL CANDIDATES FAILED TO EVALUATE.'
        if err_msg:
            return err_msg
        
        self._finalize_iteration()
        
    def _run(self):
        """Main loop of SSA method.

        Returns
        -------
        optimum: FlyingSquirrel
            Best solution found during the PSO optimization.
        """
        
        self._check_params()
        
        err_msg = self._init_method()
        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'
      
        # Load params
        if 'acorn_tree_attraction' in self.params:
            # part of FSnt moving to FSat
            # ATA=0 (all move to FSht) - emphasize local search
            # ATA=1 (all move to FSat's) - emphasize global search
            ATA = self.params['acorn_tree_attraction']
        if 'predator_presence_probability' in self.params:
            Pdp = self.params['predator_presence_probability']
        if 'gliding_constant' in self.params:
            Gc = self.params['gliding_constant']
        if 'gliding_distance_limits' in self.params:
            dg_lim = self.params['gliding_distance_limits']
            
        def Levy():
            ra, rb = np.random.normal(0, 1), np.random.normal(0, 1)
            beta = 1.5
            sigma = ((gamma(1 + beta) * np.sin(np.pi * beta / 2)) / \
                     gamma((1 + beta) / 2) * beta * 2**((beta - 1)/2)) **(1 / beta)
            return 0.01 * (ra * sigma) / (np.abs(rb)**(1 / beta))

        while True:
            
            # Categorizing FS's
            FSht = np.sort(self.cS)[0] # best FS (hickory nut trees)
            FSat = np.sort(self.cS)[1:4] # good FS (acorn trees)
            FSnt = np.sort(self.cS)[5:] # bad FS (normal trees)
            
            """
            # Moving FSnt - cascading strategy
            # move principally to FSat; 
            # with probability = (1-Pdp)*Pdp = 0.09 move to Fsht
            for fs in FSnt:
                if np.random.rand() >= Pdp: # move towards FSat
                    dg = np.random.uniform(dg_lim[0], dg_lim[1])
                    fs.X = fs.X + dg * Gc * \
                            (np.random.choice(FSat).X - fs.X)
                elif np.random.rand() >= Pdp: # move towards FSht
                    dg = np.random.uniform(dg_lim[0], dg_lim[1])
                    fs.X = fs.X + dg * Gc * (FSht.X - fs.X)
                else: # not moving, i.e. respawning randomly
                    fs.X = np.random.uniform(self.lb, self.ub)
            """
            
            # Moving FSnt
            Nnt2at = int(np.size(FSnt) * ATA) # attracted to acorn trees
            np.random.shuffle(FSnt)
            for fs in FSnt[:Nnt2at]:
                if np.random.rand() >= Pdp: # move towards FSat
                    dg = np.random.uniform(dg_lim[0], dg_lim[1])
                    fs.X = fs.X + dg * Gc * \
                            (np.random.choice(FSat).X - fs.X)
                else: # not moving, i.e. respawning randomly
                    fs.X = np.random.uniform(self.lb, self.ub)
            for fs in FSnt[Nnt2at:]:
                if np.random.rand() >= Pdp: # move towards FSht
                    dg = np.random.uniform(dg_lim[0], dg_lim[1])
                    fs.X = fs.X + dg * Gc * (FSht.X - fs.X)
                else: # not moving, i.e. respawning randomly
                    fs.X = np.random.uniform(self.lb, self.ub)
            
            # Moving FSat
            for fs in FSat:
                if np.random.rand() >= Pdp: # move towards FSht
                    dg = np.random.uniform(dg_lim[0], dg_lim[1])
                    fs.X = fs.X + dg * Gc * (FSht.X - fs.X)
                else: # not moving, i.e. respawning randomly
                    fs.X = np.random.uniform(self.lb, self.ub)
            
            # Seasonal constants (for FSat)
            Sc = np.empty(3)
            for i, fs in enumerate(FSat):
                Sc[i] = np.sqrt(np.sum((fs.X - FSht.X)**2))
                
            # Minimum value of seasonal constant
            Scmin = 1e-6 / (365**(self._progress_factor() * 2.5)) # this is some black magic shit
            
            # Random-Levy relocation at the end of winter season
            if (Sc < Scmin).all():
                for fs in FSnt:
                    fs.X = self.lb + Levy() * (self.ub - self.lb)
            
            # Correct position to the bounds
            for cP in self.cS:               
                cP.clip()       
                
            # Evaluate swarm
            err_msg = self.collective_evaluation(self.cS)
            if err_msg:
                break
             
            if self._finalize_iteration():
                break
            
        assert not err_msg, \
            f'Error: {err_msg} OPTIMIZATION ABORTED'
        
        return self.best