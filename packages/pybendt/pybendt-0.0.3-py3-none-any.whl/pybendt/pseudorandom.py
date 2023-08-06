import numpy as np

class Pseudorandom():
	def __init__(self, seed = None):
		if seed is None: self.seed = np.random.randint(2**32-1)
		else: self.seed = seed
		self.generator = np.random.RandomState(self.seed)
		self.draw_count = 0
	def draw(self):
		self.draw_count += 3
		return self.generator.standard_normal(3)