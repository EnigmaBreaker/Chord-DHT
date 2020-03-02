from hashlib import sha1
from codecs import encode
import hmac
from helper import *

class Finger:
	def __init__(self, n, i, m, node):
		self.start = hex((n + 2**(i-1)) % (2**m))[2:]
		self.end = hex((n + 2**i - 1) % (2**m))[2:]
		self.node = node

class Node:
	def __init__(self, m):
		self.m = m
		self.n = hex(2**m)[2:]

	def connectToInternet(self, internet):	
		self.internet = internet
		self.x, self.y = self.internet.getIp(self)

	def printFingerTable(self):
		# print("Info: {}, {}".format(self.key, self.successor.key))
		for i, item in enumerate(self.finger):
			print(i, hextoint(item.start), hextoint(item.end), hextoint(item.node.key))

	def printNode(self):
		print("||| --- Printing for node: {} --- |||".format(hextoint(self.key)))
		print("[@] Successor: {}".format(hextoint(self.successor.key)))
		print("[@] Predecessor: {}".format(hextoint(self.predecessor.key)))
		print()
		print("[@] Fingertable")
		self.printFingerTable()
		print("||| --- --- --- --- --- --- --- --- --- |||")
		print()
		print()


	def findSuccesor(self, key):
		new_node = self.findPredecessor(key)
		return new_node.successor

	def findPredecessor(self, key):
		new_node = self

		for i in range(self.m - 1, -1, -1):
			if(inRange(self.finger[i].node.key, self.key, key, self.n)):
				new_node = self.finger[i].node
				return new_node.findPredecessor(key)
		return self

		# while(inRange(key, new_node.key, new_node.successor.key, self.n)):
		# 	new_node = new_node.closestPrecedingFinger(key)
		# 	# print("Looping here")
		# return new_node

	def closestPrecedingFinger(self, key):
		for i in range(self.m-1, -1, -1):
			# print(hextoint(self.finger[i].node.key), hextoint(self.key), hextoint(key))
			if(inRange(self.finger[i].node.key, self.key, key, self.n)):
				# print("Going Inside")
				return finger[i].key
		return self

	def create(self):
		self.successor = self
		self.predecessor = self
		self.finger = [Finger(int(self.key, 16), i+1, self.m, self) for i in range(self.m)]

	def initFingerTable(self, node):
		self.finger = [Finger(int(self.key, 16), i+1, self.m, None) for i in range(self.m)]
		# for i in range(self.m):
		# 	print(i, int(self.finger[i].start, 16))

		# print(self.finger[0].start)
		self.finger[0].node = node.findSuccesor(self.finger[0].start)
		self.successor = self.finger[0].node
		self.predecessor = self.successor.predecessor
		self.successor.predecessor = self
		self.predecessor.successor = self
		# print(self.predecessor.key, self.successor.key)
		# print(self.successor.successor.key, self.successor.predecessor.key)
		# print(self.predecessor.successor.key, self.predecessor.predecessor.key)
		# print(0, self.finger[0].start)

		for i in range(self.m-1):
			if inRange(self.finger[i+1].start, self.key, self.finger[i].node.key, self.n):
				# print("Inrange")
				self.finger[i+1].node = self.finger[i].node
			else:
				self.finger[i+1].node = node.findSuccesor(self.finger[i+1].start)
				if(inRange(self.key, self.finger[i+1].start, self.finger[i+1].node.key, self.n)):
					self.finger[i+1].node = self




	def updateOthers(self):
		for i in range(self.m):
			print(hex(hextoint(self.key) - 2**(i+1)))
			pred = self.findPredecessor(hex((hextoint(self.key) - 2**(i+1))%(2**self.m))[2:])
			# print("Updating Finger table")
			pred.updateFingerTable(self, i)

	def updateFingerTable(self, n, i):
		if inRange(n.key, self.key, self.finger[i].node.key, self.n):
			self.finger[i].node = n 
			p = self.predecessor
			p.updateFingerTable(n, i)

	def join(self, node):
		self.initFingerTable(node)
		# print("Initialized")
		# self.printFingerTable()
		# self.successor.printFingerTable()
		self.updateOthers()
		# self.printNode()
		# self.successor.printNode()
		# self.predecessor.printNode()

	def joinChord(self):
		self.key = hmac.new(encode("my-secret"), msg=encode("{}, {}".format(self.x, self.y)), digestmod=sha1).hexdigest()[:self.m//4]

		# print(hextoint(self.key))
		nearesetNode = self.internet.getNearestNode(self.x, self.y)
		if(nearesetNode == None):
			self.create()
		else:
			self.join(nearesetNode)
