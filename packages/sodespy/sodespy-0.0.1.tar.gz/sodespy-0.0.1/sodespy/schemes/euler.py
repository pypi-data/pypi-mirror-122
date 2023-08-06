import tensorflow as tf
from sodespy.schemes.scheme_base import SchemeBase

class EulerScheme(SchemeBase):
    def __init__(self, drift, diffusion, initial_condition, time_step):
        super().__init__(drift, diffusion, initial_condition, time_step)

    def perform_step(self, x, p):
        t = p[0]
        z = p[1]

        dt = self.time_step

        mu = self.drift(x, t)
        sigma = self.diffusion(x, t)

        xt = x + mu * dt + sigma * z * tf.math.sqrt(dt)

        return xt
