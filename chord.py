from node import Node
from internet import Internet
from helper import *
from collections import Counter



class Chord:
	def __init__(self, n):
		self.internet = Internet(n)
		self.n = n
		for i in range(n):
			node = Node(8)
			node.connectToInternet(self.internet)
			node.joinChord()

	def print_chord(self):
		minkey = None

		for x in self.internet.ip_data:
			if(minkey == None):
				minkey = self.internet.ip_data[x]
			curr = self.internet.ip_data[x]
			print(curr)
			if(hextoint(curr.key) < hextoint(minkey.key)):
				minkey = curr

		for i in range(self.n):
			print(minkey.key, minkey.successor.key)
			minkey = minkey.successor




