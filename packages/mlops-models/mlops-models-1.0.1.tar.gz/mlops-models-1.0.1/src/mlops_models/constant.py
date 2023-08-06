# Very basic model


class ConstantPredictionModel:

	def __init__(self, c=0):
		self.c = c

	def predict(self, X):
		return self.c