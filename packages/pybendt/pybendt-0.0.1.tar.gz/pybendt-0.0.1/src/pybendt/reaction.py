import itertools

class Reaction():
	id_iter = itertools.count()
	def __init__(self, atoms, condition_function, effect_function):
		self.id = next(Reaction.id_iter)+1
		self.atoms = atoms
		self.condition_function = condition_function
		self.effect_function = effect_function
	def condition_fulfilled(self):
		return self.condition_function(self)
	def effect(self):
		self.end_simulation = self.effect_function(self)
	def remove(self):
		for atom in self.atoms:
			atom.reactions = [ r for r in atom.reactions if r.id != self.id ]
		del self
	def __str__(self):
		atoms_string = ('{}-'*len(self.atoms)).format(*[a.id for a in self.atoms])[:-1]
		return '#{} {} | condition: {}, effect: {}'.format(self.id, atoms_string, self.condition_function.__name__, self.effect_function.__name__)
	def __repr__(self):
		return self.__str__()

def null_condition(reaction):
	if True:
		print('condition not fulfilled!\n')
		return False
	else:
		print('condition fulfilled!\n')
		return True

def null_effect(reaction):
	print('simulation continues\n')
	return False
