

from abc import ABC, abstractmethod

class SchemeBase(ABC):
    def __init__(self, drift, diffusion, initial_condition, time_step):

        self.drift = drift
        self.diffusion = diffusion

        self.initial_condition = initial_condition
        self.time_step = time_step

    @abstractmethod
    def perform_step(self, x, p):
        raise NotImplementedError
