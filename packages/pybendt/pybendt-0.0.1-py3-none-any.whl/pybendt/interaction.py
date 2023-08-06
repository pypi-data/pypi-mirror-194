import itertools
import numpy as np

class Interaction():
	id_iter = itertools.count()
	def __init__(self, atom1, atom2, force_function, energy_function, parameters):
		self.id = next(Interaction.id_iter)+1
		self.atom1 = atom1
		self.atom2 = atom2
		self.force_function = force_function
		self.energy_function = energy_function
		self.parameters = parameters
	def compute_force(self, distance, pointer):
		F = self.force_function(distance, pointer, **self.parameters)
		self.atom1.force += F
		self.atom2.force -= F
	def compute_energy(self, distance):
		self.energy = self.energy_function(distance, **self.parameters)
	def remove(self):
		self.atom1.interactions = [ i for i in self.atom1.interactions if i.id != self.id ]
		self.atom2.interactions = [ i for i in self.atom2.interactions if i.id != self.id ]
		del self
	def __str__(self):
		return '#{} {}-{} | force: {}, energy: {}, auxiliary parameters: {}'.format(self.id, self.atom1.id, self.atom2.id, self.force_function.__name__, self.energy_function.__name__, self.parameters)
	def __repr__(self):
		return self.__str__()

def null_energy(distance):
	return 0.0

def null_force(distance, pointer):
	return np.zeros(3)