from node1 import Node
from internet import Internet
from helper import *
from collections import Counter



class Chord:
	def __init__(self, n):
		self.internet = Internet(n)
		self.n = n
		for i in range(n):
			self.addNode()

	def print_chord(self):
		minkey = None

		# for x in self.internet.ip_data:
		# 	if(minkey == None):
		# 		minkey = self.internet.ip_data[x]
		# 	curr = self.internet.ip_data[x]
		# 	print(curr)
		# 	if(curr.key < minkey.key):
		# 		minkey = curr
		# print("Printing")
		# for i in range(self.n):
		# 	# print(minkey.key, minkey.successor.key)
		# 	minkey.printNode()
		# 	minkey = minkey.successor

		for x in self.internet.ip_data:
			self.internet.ip_data[x].printNode()


	def addNode(self):
		node = Node(8)
		node.connectToInternet(self.internet)
		node.joinChord()

	def addMsg(self, key, value):
		random_key = random.choice(list(self.internet.ip_data.keys()))
		random_node = self.internet.ip_data[random_key]
		random_node.routeMsg(key, value)

	def lookup(self, key):
		random_key = random.choice(list(self.internet.ip_data.keys()))
		random_node = self.internet.ip_data[random_key]
		return random_node.lookup(key)

