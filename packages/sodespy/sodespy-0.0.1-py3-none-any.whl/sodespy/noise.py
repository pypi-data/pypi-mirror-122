from numpy.linalg import LinAlgError
import tensorflow as tf


class Noise:
    def __init__(self, random_generator, noise_type, seed, correlations, num_noises):
        self.random_generator = random_generator
        self.noise_type = noise_type

        self.seed = seed

        self.rho = correlations

        self.num_noises = num_noises

        self.rng = tf.random.Generator.from_seed(self.seed)

    # TODO : use svd as default when non square noise is present
    def sample(self, num_paths, num_steps):
        if self.rho is not None:
            
            if self.noise_type == "Scalar" and self.num_noises > 1:

                x = self.rng.normal(shape=(num_steps, 1, num_paths))
                normal_samples = tf.repeat(x, self.num_noises, axis=1)

                return normal_samples
            else:

                x = self.rng.normal(shape=(num_steps, self.num_noises, num_paths))
                c = tf.linalg.cholesky(self.rho, lower=True)
                normal_samples = c @ x

                return normal_samples

        else:
            normal_samples = self.rng.normal(shape=(num_steps, self.num_noises, num_paths), dtype=tf.float32)

            return normal_samples

