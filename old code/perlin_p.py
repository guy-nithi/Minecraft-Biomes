

# from perlin_noise import PerlinNoise
from perlin_noise_module import PerlinNoise

class Perlin:
    def __init__(self):

        self.octaves = 3
        self.seed = 123
        self.freq = 64
        self.amp = 12
        self.pNoise = PerlinNoise(  octaves=self.octaves,
                                    seed=self.seed)

    def getHeight(self, x, z):
        y = self.pNoise([x/self.freq, z/self.freq]) * self.amp
        return y