from sodespy.schemes.scheme_base import SchemeBase
import tensorflow as tf

class SRA1Scheme(SchemeBase):
    def __init__(self, drift, diffusion, initial_condition, time_step):
        super().__init__(drift, diffusion, initial_condition, time_step)

    def perform_step(self, x, p):
        t = p[0]
        w = p[1]
        z = p[2]

        # TODO: call function called update_dt
        dt = self.time_step

        # TODO: check diffusion term and sqrt(dt) like terms
        drift = self.drift(x, t) * dt
        diffusion = self.diffusion(x, t)
        I_10 = dt ** (3 / 2) / 2 * (w + z / tf.math.sqrt(3.))

        diffusion_1 = self.diffusion(x, t + dt)
        drift_1 = self.drift(x + 3 / 4 * drift + 1 / 2 * diffusion_1 * I_10 / dt, t + 3 / 4 * dt) * dt

        xt = x + 1 / 3 * (drift + 2 * drift_1) + tf.math.sqrt(dt) * diffusion * w

        return xt
