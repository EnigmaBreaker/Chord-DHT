from hashlib import sha1
from codecs import encode
import hmac
from helper import *

class Finger:
	def __init__(self, n, i, m):
		self.start = hex((n + 2**(i-1)) % (2**m))[2:]
		self.end = hex((n + 2**i - 1) % (2**m))[2:]
		self.node = None

class Node:
	def __init__(self, m):
		self.m = m
		self.n = hex(2**m)[2:]

	def connectToInternet(self, internet):	
		self.internet = internet
		self.x, self.y = self.internet.getIp(self)


	def findSuccesor(self, key):
		new_node = self.findPredecessor(key)
		return new_node.successor

	def findPredecessor(self, key):
		new_node = self
		while(inRange(key, new_node.key, new_node.successor, self.n)):
			new_node = new_node.closestPrecedingFinger(key)
		return new_node

	def closestPrecedingFinger(self, key):
		for i in range(m-1, -1, -1):
			if(inRange(self.finger[i].node.key, self.key, key, self.n)):
				return finger[i].key
		return self

	def create(self):
		self.successor = self
		self.predecessor = self
		self.finger = [Finger(int(self.key, 16), i+1) for i in range(self.m)]

	def initFingerTable(self, node):
		self.finger[0].node = node.findSuccesor(self.finger[0].start)
		self.successor = self.finger[0].node
		self.predecessor = self.successor.predecessor
		self.successor.predecessor = self
		self.predecessor.successor = self

		for i in range(m-1):
			if inRange(self.finger[i+1].start, self.key, self.finger[i].node.key, self.n):
				self.finger[i+1].node = self.finger[i].node
			else:
				finger[i+1].node = node.findSuccesor(finger[i+1].start)


	def updateOthers(self):
		for i in range(m):
			pred = findPredecessor(int(self.n - 2**(i+1)))
			pred.updateFingerTable(self, i)

	def updateFingerTable(self, n, i):
		if inRange(n.key, self.key, self.finger[i].node.key, self.n):
			self.finger[i].node = n 
			p = self.predecessor
			p.updateFingerTable(n, i)

	def join(self, node):
		self.initFingerTable(node)
		self.updateOthers()

	def joinChord(self):
		self.key = hmac.new(encode("my-secret"), msg=encode("{}, {}".format(self.x, self.y)), digestmod=sha1).hexdigest()[:self.m//4]
		nearesetNode = self.internet.getNearestNode(self.x, self.y)
		if(nearesetNode == None):
			self.create()
		else:
			self.join(nearesetNode)
