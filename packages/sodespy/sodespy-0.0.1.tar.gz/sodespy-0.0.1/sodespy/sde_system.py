from .schemes import *
from .noise import Noise
import tensorflow as tf

# TODO: Add save_at param!!!
class SDESystem:
    def __init__(self, drift, diffusion, noise_type, scheme, x0, tspan, dt, paths, random_generator=None, seed=1234, correlations=None):

        self.drift = drift
        self.diffusion = diffusion

        # Before building noise check concordance between drift, diffusion and dW or noise_type
        self._check_consistency(drift, diffusion, noise_type, x0)

        # TODO: add seed to noise to track results
        self.noise = self._build_noise(diffusion, noise_type, random_generator, seed, correlations)
        self.extra_noise = self._build_extra_noise(diffusion, scheme, noise_type, random_generator, seed, correlations)

        self.tspan = tspan
        self.dt = dt

        self.num_time_steps = self._build_num_time_steps()
        self.time_grid = self._build_time_grid()
        self.num_paths = paths
        self.num_processes = 1 if type(x0) == tf.float32 else len(x0)

        self.x0 = tf.reshape(tf.repeat(x0, self.num_paths), (self.num_processes, self.num_paths))

        self.scheme = self._build_scheme(scheme)

        # Useful handler
        self.solution = None

    def _check_consistency(self, drift, diffusion, noise, x0):
        if type(x0) == float:
            pass
        elif isinstance(x0, list):
            pass
        else:
            raise Exception("x0 type not correct, x0 should be a float or a list")

        if type(drift) == float:
            pass
        elif isinstance(drift, list):
            pass
        else:
            raise Exception("drift type not correct, drift should be a float or a list")

        if type(diffusion) == float:
            pass
        elif isinstance(diffusion, list):
            pass
        else:
            raise Exception("diffusion type not correct, diffusion should be a float or a list")

    def _build_extra_noise(self, diffusion, scheme, noise_type, random_generator, seed, correlations):
        if scheme in ["SRA1", "SRI1W1", "PlatenWagner"]:
            return self._build_noise(noise_type, random_generator, seed, correlations)
        else:
            return None

    def _build_noise(self, diffusion, noise_type, random_generator, seed, correlations):
        if noise_type == "Scalar":
            num_noises = len(diffusion) if type(diffusion) == list else 1
            return Noise(random_generator, noise_type, seed, correlations=None, num_noises=num_noises)

        elif noise_type == "Diagonal":
            num_noises = len(diffusion) if type(diffusion) == list else 1
            return Noise(random_generator, noise_type, seed, correlations, num_noises)
  
        else:
            raise Exception("Noise type is not correct")

    def _build_scheme(self, scheme):
        if scheme == "Euler":
            e = [EulerScheme(self.drift[i], self.diffusion[i], self.x0, self.dt) for i in range(self.num_processes)]

            return e

        elif scheme == "SRA1":
            sra1 = [SRA1Scheme(self.drift[i], self.diffusion[i], self.x0[i], self.dt) for i in range(self.num_processes)]

            return sra1

        elif scheme == "SRI1W1":
            sri1w1 = [SRI1W1Scheme(self.drift[i], self.diffusion[i], self.x0[i], self.dt) for i in range(self.num_processes)]

            return sri1w1

        else:
            raise Exception("Provided scheme is not correct.")

    def _build_num_time_steps(self):
        t1 = self.tspan[-1]
        dt = self.dt

        return int(tf.math.ceil(t1 / dt))

    def _build_time_grid(self):
        t0 = self.tspan[0] + self.dt
        t1 = self.tspan[-1]

        grid = tf.linspace(t0, t1, self.num_time_steps)

        return grid

    @tf.function
    def simulate(self):
        if not self.extra_noise:
            # Assume that the number of noise sources is equal to the number of processes.
            w = self.noise.sample(self.num_paths, self.num_time_steps)

            sol = []
            # TODO: add initial condition to solution
            for i in range(self.num_processes):
                sol.append(tf.scan(self.scheme[i].perform_step, [self.time_grid, w[:, i, :]], self.x0)[:, 0, :])

        else:
            w = self.noise.sample(self.num_paths, self.num_time_steps)
            z = self.extra_noise.sample(self.num_paths, self.num_time_steps)

            sol = []
            for i in range(self.num_processes):
                sol.append(tf.scan(self.scheme[i].perform_step, [self.time_grid, w[:, i, :], z[:, i, :]], self.x0)[:, 0, :])

        return sol


