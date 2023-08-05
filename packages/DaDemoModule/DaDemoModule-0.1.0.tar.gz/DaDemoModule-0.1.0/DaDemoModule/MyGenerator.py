import numpy as np

class MyGenerator:
    def __init__(self, seed):
        self._generator = np.random
        self._generator.seed(seed)
    
    def next(self):
        return self._generator.rand()