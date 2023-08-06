# import numpy as np
# import copy as cp
# import numpy as np

# sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '..') ))
import unittest

from pybendt.interaction import *

class TestAtom(unittest.TestCase):
	def setUp(self):
		pass
		# self.initial_position = [2.0, 3.0, 4.0]
		# self.atom1 = Atom(position = [2.0, 3.0, 4.0], friction = 1.0, label = "TST")
	def test_harmonic_energy_minimum(self):
		distance = 100.0
		equilibrium_distance = 100.0
		for force_constant in [-48732.0, 1/12.0, 0.0, 12.0, 48732.0]:
			energy = harmonic_energy(distance = distance, force_constant = force_constant, equilibrium_distance = equilibrium_distance)
			self.assertEqual(0.0, energy)
	def test_harmonic_force_minimum(self):
		distance = 100.0
		pointer = distance*np.array([1, 0, 0])
		equilibrium_distance = 100.0
		for force_constant in [-48732.0, 1/12.0, 0.0, 12.0, 48732.0]:
			force = harmonic_force(distance = distance, pointer = pointer, force_constant = force_constant, equilibrium_distance = equilibrium_distance)
			self.assertSequenceEqual([0.0, 0.0, 0.0], list(force))


if __name__ == '__main__':	
	unittest.main()
