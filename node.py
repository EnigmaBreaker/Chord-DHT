from hashlib import sha1
from codecs import encode
import hmac
from helper import *

class Node:
	def __init__(self, m):
		self.m = m
		self.n = 2**m
		self.dic = {}

	def printFingerTable(self):
		# print("Info: {}, {}".format(self.key, self.successor.key))
		for i, item in enumerate(self.finger):
			print(i, item[0], item[1].key)

	def printNode(self):
		print("||| --- Printing for node: {} --- |||".format(self.key))
		print("[@] Successor: {}".format(self.successor.key))
		print("[@] Predecessor: {}".format(self.predecessor.key))
		print()
		print("[@] Fingertable")
		self.printFingerTable()
		print("||| --- --- --- --- --- --- --- --- --- |||")
		print()
		print()

	def connectToInternet(self, internet):
		self.internet = internet
		self.x, self.y = self.internet.getIp(self)

	def create(self):
		self.successor = self
		self.predecessor = self
		self.finger = [[((2**i + self.key) % self.n), self] for i in range(self.m)]

	def findSuccessor(self, key, hops):
		# print(key, self.key, self.successor.key, self.n)
		if(self.key == key):
			return self
		if(self.successor.key == key):
			return self.successor
		if(inRange(key, self.key, self.successor.key, self.n)):
			# print(key, self.key, self.successor.key, self.n)
			return self.successor
		else:
			for i in range(self.m - 1, -1, -1):
				# print(self.finger[i][1].key, self.key, key, self.n)
				if(inRange(self.finger[i][1].key, self.key, key, self.n)):
					hops.append(self.finger[i][1].key)
					return self.finger[i][1].findSuccessor(key, hops)
			return self

	def initFingerTable(self, node):
		self.finger = [[((2**i + self.key) % self.n), None] for i in range(self.m)]
		self.finger[0][1] = node.findSuccessor(self.key, [])
		self.successor = self.finger[0][1]
		self.predecessor = self.successor.predecessor
		self.predecessor.successor = self
		self.successor.predecessor = self

		for i in range(1, self.m):	
			if self.finger[i][0] == self.successor.key:
				self.finger[i][1] = self.successor
			elif(inRange(self.finger[i][0], self.key, self.successor.key, self.n)):
				self.finger[i][1] = self.successor
			else:
				self.finger[i][1] = node.findSuccessor(self.finger[i][0], [])

	def updateOthers(self):
		for i in range(self.m):
			pred = self.findSuccessor((self.key - 2**i) % self.n, [])

			if(pred.key != (self.key - 2**i) % self.n):
				pred = pred.predecessor

			# print("Updating Others. {} {} {}".format(self.key, (self.key - 2**i) % self.n, pred.key))
			pred.updateFingerTable(self, i)


	def updateFingerTable(self, n, i):
		# print("Printing Finger table: {}, {}, {}".format(n.key, self.key, self.finger[i][1].key))
		# if(self.finger[i][1].key == n.key):
		# 	self.finger[i][1] = n
		# 	if(self.predecessor.key != self.key):
		# 		self.predecessor.updateFingerTable(n, i)

		if(inRange(n.key, self.key, self.finger[i][1].key, self.n)):
			self.finger[i][1] = n
			self.predecessor.updateFingerTable(n, i)

	def join(self, node):
		self.initFingerTable(node)
		self.updateOthers()

	def joinChord(self):
		self.key = hextoint(hmac.new(encode("my-secret"), msg=encode("{}, {}".format(self.x, self.y)), digestmod=sha1).hexdigest()[:self.m//4])

		# print(self.key)

		nearesetNode = self.internet.getNearestNode(self.x, self.y)
		if(nearesetNode == None):
			self.create()
		else:
			self.join(nearesetNode)

	def routeMsg(self, key, value):
		hops = []
		nextone = self.findSuccessor(key, hops)
		if key in nextone.dic:
			return None
		nextone.dic[key] = value
		return hops

	def lookup(self, key):
		hops = []
		nextone = self.findSuccessor(key, hops)
		if key in nextone.dic:
			return nextone.dic[key], hops
		return None

	def deleteNode(self):
		self.predecessor.successor = self.successor
		self.successor.predecessor = self.predecessor
		for key in self.dic:
			self.successor.dic[key] = self.dic[key]

	def reUpdateFingerTable(self):
		for x in self.finger:
			x[1] = self.findSuccessor(x[0], [])

	