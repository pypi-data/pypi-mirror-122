from sodespy.schemes.scheme_base import SchemeBase
import tensorflow as tf


class SRI1W1Scheme(SchemeBase):
    def __init__(self, drift, diffusion, initial_condition, time_step):
        super().__init__(drift, diffusion, initial_condition, time_step)

    def perform_step(self, x, p):
        t = p[0]
        w = p[1]
        z = p[2]

        dt = self.time_step

        drift_term = self.drift(x, t)
        diffusion_term = self.diffusion(x, t)

        # TODO: check if w and z are flipped
        # TODO: check diffusion term and sqrt(dt) like terms
        I_10 = dt ** (3 / 2) / 2 * (w + z / tf.math.sqrt(3.))
        I_1 = tf.math.sqrt(dt) * w
        I_11 = dt / 2 * (w ** 2 - 1)
        I_111 = 1 / 2 * dt ** (3 / 2) * (1 / 3 * w ** 2 - 1) * w

        drift_term_1 = self.drift(x + 3 / 4 * drift_term + 3 / 2 * diffusion_term * I_10 / dt, t + 3 / 4 * dt) * dt

        diffusion_term_1 = self.diffusion(x + drift_term / 4 + tf.math.sqrt(dt) * diffusion_term / 2, t + dt / 4)

        diffusion_term_2 = self.diffusion(x + drift_term - tf.math.sqrt(dt) * diffusion_term, t + dt)

        diffusion_term_3 = self.diffusion(x + drift_term / 4 + tf.math.sqrt(dt) * (- 5 * diffusion_term +
                                                                               3 * diffusion_term_1 +
                                                                               diffusion_term_2 / 2), t + dt / 4)

        xt = x + drift_term / 3 + 2 / 3 * drift_term_1 + diffusion_term + I_1 * (
                - diffusion_term + 4 / 3 * diffusion_term_1 + 2 / 3 * diffusion_term_2) + I_10 * (
                     2 * diffusion_term - 4 / 3 * diffusion_term_1 - 2 / 3 * diffusion_term_2) + I_11 * (
                     - diffusion_term + 4 / 3 * diffusion_term_1 - diffusion_term_2 / 3) + \
             I_111 * (- 2 * diffusion_term + 5 / 3 * diffusion_term_1 - 2 / 3 * diffusion_term_2 + diffusion_term_3)

        return xt
