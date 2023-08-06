import numpy as np
# import copy as cp
# import numpy as np

# sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '..') ))
import unittest

from pybendt.atom import *
from pybendt.interaction import kB_in_kcal_per_mole_per_kelvin

class TestAtom(unittest.TestCase):
	def setUp(self):
		self.initial_position = [2.0, 3.0, 4.0]
		self.atom1 = Atom(position = [2.0, 3.0, 4.0], friction = 1.0, label = "TST")
	def test_if_move_atom_by_zero_makes_no_change(self):
		translation_vector = np.zeros(3)
		self.atom1.move(translation_vector)
		self.assertSequenceEqual(self.initial_position, list(self.atom1.position))
	def test_friction_conversion(self):
		gamma = friction_from_hydrodynamic_radius_and_viscosity(hydradius = 51.0, viscosity = 1.0)
		self.assertAlmostEqual(0.00420953, kB_in_kcal_per_mole_per_kelvin*293/gamma, places = 7)

if __name__ == '__main__':	
	unittest.main()
