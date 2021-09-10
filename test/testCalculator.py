# sample script to unit test a hoc function

import unittest
import neuron

class TestNeuron(unittest.TestCase):
	def setUp(self):
		self.h = neuron.h
		self.h('load_file("./sim/calculator.hoc")')

	def testAdd(self):
		self.h('addResult = add(3,5)')
		addResult = self.h.addResult
		self.assertEqual(addResult,8)
