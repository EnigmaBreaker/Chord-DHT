from node import Node
from internet import Internet
from helper import *
from collections import Counter
import random


class Chord:
	def __init__(self, n):
		self.internet = Internet()
		self.n = n
		self.m = 32
		for i in range(n):
			self.addNode()

	def print_chord(self):
		minkey = None

		for x in self.internet.ip_data:
			self.internet.ip_data[x].printNode()


	def addNode(self):
		node = Node(self.m)
		node.connectToInternet(self.internet)
		node.joinChord()


	def addMsg(self, value):
		key = random.randint(0, (2**self.m)-1)
		random_key = random.choice(list(self.internet.ip_data.keys()))
		random_node = self.internet.ip_data[random_key]
		output = random_node.routeMsg(key, value)
		if(output):
			return key, output
		return None

	def lookup(self, key):
		random_key = random.choice(list(self.internet.ip_data.keys()))
		random_node = self.internet.ip_data[random_key]
		return random_node.lookup(key)

	def deleteNode(self, key):
		for ip in self.internet.ip_data:
			if(self.internet.ip_data[ip].key == key):
				ip_ind = ip 
				break
		else:
			return False

		self.internet.ip_data[ip_ind].deleteNode()
		self.reUpdateFingerTables()

	def deleteRandomNode(self, n):
		for i in range(n):
			print("Deleting Node: {}".format(i))
			random_key = random.choice(list(self.internet.ip_data.keys()))
			self.internet.ip_data[random_key].deleteNode()
			del self.internet.ip_data[random_key]
			self.reUpdateFingerTables()

	def reUpdateFingerTables(self):
		for key in self.internet.ip_data.keys():
			self.internet.ip_data[key].reUpdateFingerTable()	


