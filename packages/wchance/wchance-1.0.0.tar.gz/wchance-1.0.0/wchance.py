import random

class chance:
	def __init__(self, chance: int, *args, **kwargs):
		if isinstance(chance, str):
			raise ValueError("Supported type is int or float")
		self.chance = chance
		if isinstance(chance, float):
			self.chance = round(chance*100)
		if chance > 100:
			raise ValueError("Maximum chance is 100")
		if chance < 0:
			raise ValueError("Chance can not be zero or less than zero")

	def generate(self, *args, **kwargs) -> bool:
		if random.randint(1, 100) <= self.chance:
			return True
		return False
