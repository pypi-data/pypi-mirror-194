import unittest

import mlops_models as mlops


class TestConstantPredictionModel(unittest.TestCase):

	def test_constant_matches_initilized_value(self):

		model = mlops.ConstantPredictionModel(0)
		self.assertEqual(model.predict(None), 0)

		# Test diferent data types
		self.assertEqual(model.predict(1), 0)
		self.assertEqual(model.predict(-1), 0)
		self.assertEqual(model.predict("a"), 0)
		self.assertEqual(model.predict(["a"]), 0)


		model = mlops.ConstantPredictionModel(1)
		self.assertEqual(model.predict(None), 1)


	def test_default_init_value(self):

		model = mlops.ConstantPredictionModel()
		self.assertEqual(model.predict(None), 0)

		model = mlops.ConstantPredictionModel()
		self.assertNotEqual(model.predict(None), 1)
