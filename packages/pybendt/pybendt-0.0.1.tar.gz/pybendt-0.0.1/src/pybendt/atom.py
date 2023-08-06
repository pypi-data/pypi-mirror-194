import itertools
import numpy as np
from scipy.constants import Boltzmann

from interaction import Interaction
from reaction import Reaction

class Atom():
	id_iter = itertools.count()
	def __init__(self, position, friction, label = ""):
		self.id = next(Atom.id_iter)+1
		self.label = label
		self.position = np.array(position)
		self.interactions = []
		self.reactions = []
		self.force = np.zeros(3)
		self.mobility = 1/friction
	def __str__(self):
		return '{}#{} {} {} {}'.format(self.label, self.id, *self.position)
	def __repr__(self):
		return self.__str__()
	def add_interaction(self, atom2, force_function, energy_function, parameters):
		interaction = Interaction(self, atom2, force_function, energy_function, parameters)
		self.interactions.append(interaction)
		atom2.interactions.append(interaction)
	def add_reaction(self, atoms, condition_function, effect_function):
		reaction = Reaction([self] + atoms, condition_function, effect_function)
		self.reactions.append(reaction)
		for atom in atoms:
			atom.reactions.append(reaction)
	def move(self, vector):
		self.position += vector
	def deterministic_move(self, timestep):
		self.move(self.mobility * self.force)
	def brownian_move(self, timestep, temperature, random_vector):
		self.move(np.sqrt(2*Boltzmann*temperature*self.mobility) * random_vector)
	def remove_interactions_by_id(self, ids):
		for i in self.interactions:
			if i.id in ids: i.remove()
	def remove_reactions_by_id(self, ids):
		for r in self.reactions:
			if r.id in ids: r.remove()
	def reset_force(self):
		self.force = np.zeros(3)